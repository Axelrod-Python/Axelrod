import copy
from enum import IntEnum
from typing import Optional, Tuple

import torch
from torch import nn

from axelrod.action import Action
from axelrod.load_data_ import load_attention_model_weights
from axelrod.player import Player

C, D = Action.C, Action.D

MEMORY_LENGTH = 200

CLS_TOKEN = 0
PAD_TOKEN = 1

DEVICES = torch.device("cpu")


class GameState(IntEnum):
    CooperateDefect = 2
    DefectCooperate = 3
    CooperateCooperate = 4
    DefectDefect = 5


def actions_to_game_state(
    player_action: Action, opponent_action: Action
) -> GameState:
    action_mapping = {
        (C, D): GameState.CooperateDefect,
        (D, C): GameState.DefectCooperate,
        (C, C): GameState.CooperateCooperate,
        (D, D): GameState.DefectDefect,
    }
    return action_mapping[(player_action, opponent_action)]


def compute_features(
    player: Player, opponent: Player, right_pad: bool = False
) -> torch.IntTensor:
    # The first token is the CLS token
    player_history = player.history[-MEMORY_LENGTH:]
    player_history = player_history[::-1]
    opponent_history = opponent.history[-MEMORY_LENGTH:]
    opponent_history = opponent_history[::-1]

    feature_size = MEMORY_LENGTH + 1 if right_pad else len(player_history) + 1

    game_history = torch.full((feature_size,), PAD_TOKEN, dtype=torch.int)
    game_history[0] = CLS_TOKEN
    for index, (action_player, action_opponent) in enumerate(
        zip(player_history, opponent_history)
    ):
        game_state = actions_to_game_state(action_player, action_opponent)
        game_history[index + 1] = game_state
    return game_history


class GELUActivation(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, input):
        return nn.functional.gelu(input)


class PlayerConfig:
    def __init__(
        self,
        state_size=6,  # Number of possible game states, 4 possible game states and 2 specials token
        hidden_size=256,
        num_hidden_layers=24,
        num_attention_heads=8,
        intermediate_size=512,
        hidden_dropout_prob=0.3,
        attention_probs_dropout_prob=0.3,
        max_game_size=MEMORY_LENGTH + 1,  # Add 1 for the CLS token
        initializer_range=0.02,
        layer_norm_eps=1e-12,
    ):
        self.state_size = state_size
        self.hidden_size = hidden_size
        self.num_hidden_layers = num_hidden_layers
        self.num_attention_heads = num_attention_heads
        self.intermediate_size = intermediate_size
        self.hidden_dropout_prob = hidden_dropout_prob
        self.attention_probs_dropout_prob = attention_probs_dropout_prob
        self.max_game_size = max_game_size
        self.initializer_range = initializer_range
        self.layer_norm_eps = layer_norm_eps


class PlayerEmbeddings(nn.Module):
    """Construct the embeddings from game state and position embeddings."""

    def __init__(self, config: PlayerConfig):
        super().__init__()
        self.game_state_embeddings = nn.Embedding(
            config.state_size, config.hidden_size
        )
        self.position_embeddings = nn.Embedding(
            config.max_game_size, config.hidden_size
        )
        self.LayerNorm = nn.LayerNorm(
            config.hidden_size, eps=config.layer_norm_eps
        )
        self.dropout = nn.Dropout(config.hidden_dropout_prob)
        self.register_buffer(
            "position_ids",
            torch.arange(config.max_game_size).expand((1, -1)),
            persistent=False,
        )

    def forward(
        self,
        input_ids: torch.LongTensor,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        input_shape = input_ids.size()
        seq_length = input_shape[1]
        position_ids = self.position_ids[:, 0:seq_length]
        embeddings = self.game_state_embeddings(input_ids)
        position_embeddings = self.position_embeddings(position_ids)
        embeddings += position_embeddings
        embeddings = self.LayerNorm(embeddings)
        embeddings = self.dropout(embeddings)

        attention_mask = (input_ids != PAD_TOKEN).long()

        return embeddings, attention_mask


class PlayerSelfAttention(nn.Module):
    def __init__(self, config: PlayerConfig):
        super().__init__()
        self.num_attention_heads = config.num_attention_heads
        self.attention_head_size = int(
            config.hidden_size / config.num_attention_heads
        )
        self.all_head_size = self.num_attention_heads * self.attention_head_size

        self.query = nn.Linear(config.hidden_size, self.all_head_size)
        self.key = nn.Linear(config.hidden_size, self.all_head_size)
        self.value = nn.Linear(config.hidden_size, self.all_head_size)

        self.dropout_prob = config.attention_probs_dropout_prob

    def _transpose_for_scores(self, x: torch.Tensor) -> torch.Tensor:
        new_x_shape = x.size()[:-1] + (
            self.num_attention_heads,
            self.attention_head_size,
        )
        x = x.view(new_x_shape)
        return x.permute(0, 2, 1, 3)

    @staticmethod
    def _expand_mask(mask: torch.Tensor, dtype: torch.dtype) -> torch.Tensor:
        """
        Expands attention_mask from `[bsz, seq_len]` to `[bsz, 1, tgt_seq_len, src_seq_len]`.
        """
        bsz, src_len = mask.size()
        tgt_len = src_len

        expanded_mask = (
            mask[:, None, None, :].expand(bsz, 1, tgt_len, src_len).to(dtype)
        )

        inverted_mask = 1.0 - expanded_mask

        return inverted_mask.masked_fill(
            inverted_mask.to(torch.bool), torch.finfo(dtype).min
        )

    def forward(
        self, hidden_states: torch.Tensor, attention_mask: torch.Tensor
    ) -> torch.Tensor:
        bsz, tgt_len, _ = hidden_states.size()
        query_layer = self._transpose_for_scores(self.query(hidden_states))
        key_layer = self._transpose_for_scores(self.key(hidden_states))
        value_layer = self._transpose_for_scores(self.value(hidden_states))

        attn_mask = self._expand_mask(attention_mask, query_layer.dtype)

        attn_output = torch.nn.functional.scaled_dot_product_attention(
            query_layer,
            key_layer,
            value_layer,
            dropout_p=self.dropout_prob if self.training else 0.0,
            attn_mask=attn_mask,
        )

        attn_output = attn_output.transpose(1, 2)
        attn_output = attn_output.reshape(bsz, tgt_len, self.all_head_size)
        return attn_output


class PlayerSelfOutput(nn.Module):
    def __init__(self, config: PlayerConfig):
        super().__init__()
        self.dense = nn.Linear(config.hidden_size, config.hidden_size)
        self.LayerNorm = nn.LayerNorm(
            config.hidden_size, eps=config.layer_norm_eps
        )
        self.dropout = nn.Dropout(config.hidden_dropout_prob)

    def forward(
        self, hidden_states: torch.Tensor, input_tensor: torch.Tensor
    ) -> torch.Tensor:
        hidden_states = self.dense(hidden_states)
        hidden_states = self.dropout(hidden_states)
        hidden_states = self.LayerNorm(hidden_states + input_tensor)
        return hidden_states


class PlayerAttention(nn.Module):
    def __init__(self, config: PlayerConfig):
        super().__init__()
        self.self = PlayerSelfAttention(config)
        self.output = PlayerSelfOutput(config)

    def forward(
        self, hidden_states: torch.Tensor, attention_mask: torch.Tensor
    ) -> torch.Tensor:
        self_outputs = self.self(hidden_states, attention_mask)
        attention_output = self.output(self_outputs, hidden_states)
        return attention_output


class PlayerIntermediate(nn.Module):
    def __init__(self, config: PlayerConfig):
        super().__init__()
        self.dense = nn.Linear(config.hidden_size, config.intermediate_size)
        self.intermediate_act_fn = GELUActivation()

    def forward(self, hidden_states: torch.Tensor) -> torch.Tensor:
        hidden_states = self.dense(hidden_states)
        hidden_states = self.intermediate_act_fn(hidden_states)
        return hidden_states


class PlayerOutput(nn.Module):
    def __init__(self, config: PlayerConfig):
        super().__init__()
        self.dense = nn.Linear(config.intermediate_size, config.hidden_size)
        self.LayerNorm = nn.LayerNorm(
            config.hidden_size, eps=config.layer_norm_eps
        )
        self.dropout = nn.Dropout(config.hidden_dropout_prob)

    def forward(
        self, hidden_states: torch.Tensor, input_tensor: torch.Tensor
    ) -> torch.Tensor:
        hidden_states = self.dense(hidden_states)
        hidden_states = self.dropout(hidden_states)
        hidden_states = self.LayerNorm(hidden_states + input_tensor)
        return hidden_states


class PlayerLayer(nn.Module):
    def __init__(self, config: PlayerConfig):
        super().__init__()
        self.seq_len_dim = 1
        self.attention = PlayerAttention(config)
        self.intermediate = PlayerIntermediate(config)
        self.output = PlayerOutput(config)

    def forward(
        self,
        hidden_states: torch.Tensor,
        attention_mask: torch.Tensor,
    ) -> torch.Tensor:

        attention_output = self.attention(hidden_states, attention_mask)
        intermediate_output = self.intermediate(attention_output)
        layer_output = self.output(intermediate_output, attention_output)
        return layer_output


class PlayerEncoder(nn.Module):
    def __init__(self, config: PlayerConfig):
        super().__init__()
        self.layer = nn.ModuleList(
            [PlayerLayer(config) for _ in range(config.num_hidden_layers)]
        )

    def forward(
        self,
        hidden_states: torch.Tensor,
        attention_mask: torch.Tensor,
    ) -> torch.Tensor:

        for layer_module in self.layer:
            hidden_states = layer_module(hidden_states, attention_mask)
        return hidden_states


class PlayerPooler(nn.Module):
    def __init__(self, config: PlayerConfig):
        super().__init__()
        self.dense = nn.Linear(config.hidden_size, config.hidden_size)
        self.activation = nn.Tanh()

    def forward(self, hidden_states: torch.Tensor) -> torch.Tensor:
        first_token_tensor = hidden_states[:, 0]
        pooled_output = self.dense(first_token_tensor)
        pooled_output = self.activation(pooled_output)
        return pooled_output


class PlayerModel(nn.Module):
    _no_split_modules = ["PlayerEmbeddings"]

    def __init__(self, config: PlayerConfig):
        super().__init__()
        self.config = config
        self.embeddings = PlayerEmbeddings(config)
        self.encoder = PlayerEncoder(config)
        self.pooler = PlayerPooler(config)

        self.action = nn.Linear(config.hidden_size, 1)

    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        embedding_output, attention_mask = self.embeddings(input_ids=input_ids)
        sequence_output = self.encoder(embedding_output, attention_mask)
        pooled_output = self.pooler(sequence_output)
        return self.action(pooled_output)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, PlayerModel)


class EvolvedAttention(Player):
    """A player who uses an attention mechanism to analyse the game. Trained with self-play.

    Names:
    - EvolvedAttention: EvolvedAttention by Marc-Olivier Derouin
    """

    name = "EvolvedAttention"
    classifier = {
        "memory_depth": MEMORY_LENGTH,
        "stochastic": False,
        "long_run_time": True,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(
        self,
    ) -> None:
        super().__init__()
        self.model: Optional[PlayerModel] = None

    def load_model(self) -> None:
        """Load the model weights."""
        if self.model is None:
            self.model = PlayerModel(PlayerConfig())
            self.model.load_state_dict(load_attention_model_weights())
            self.model.to(DEVICES)
            self.model.eval()

    def strategy(self, opponent: Player) -> Action:
        """Actual strategy definition that determines player's action."""
        # Load the model if not already loaded
        self.load_model()
        assert self.model is not None, "Model must be loaded before playing."

        # Compute features
        features = compute_features(self, opponent).unsqueeze(0).to(DEVICES)

        # Get action from the model
        logits = self.model(features)

        # Apply sigmoid
        logits = torch.sigmoid(logits)

        return C if logits.item() < 0.5 else D
