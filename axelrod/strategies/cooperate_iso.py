import numpy as np

import torch
from torch import optim

import axelrod as axl
from axelrod.action import Action
from axelrod.player import Player



C, D = Action.C, Action.D

class LongtermTfT(Player):
    """Noise-tolerant Tit-for-Tat.

    Cooperates by default and mirrors the opponent, but distinguishes
    noise-corrupted cooperation from genuine defection using a statistical
    test: it compares the opponent's observed defection count against the
    binomial null expected from the noise rate (via a z-statistic) and
    forgives defections that are consistent with noise. The number of
    forgiven defections grows like O(sqrt(N_C)), so the forgiven *rate*
    tends to zero — tolerating noise while staying unexploitable in the
    long run. Retaliates only when the defection rate is significantly
    above what noise alone would explain.

    Names:
    - Longterm TFT: [Hutter2023]_
    """
    name = "LongtermTfT"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "makes_use_of": {"noise"},
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self):
        super().__init__()
        self.n_tft_would_c = 0
        self.n_d_when_tft_would_c = 0
        self.z = 0.

    def receive_match_attributes(self):
        self.noise = self.match_attributes.get("noise", 0.0)

    def strategy(self, opponent: Player) -> Action:
        if not self.history:
            return C
        if len(self.history) == 1:
            return opponent.history[-1]
        if self.history[-2] == C:
            self.n_tft_would_c += 1
            if opponent.history[-1] == D:
                self.n_d_when_tft_would_c += 1
            n_expected_ds = self.n_tft_would_c * self.noise
            std_expected_ds = np.sqrt(self.noise * (1-self.noise) * self.n_tft_would_c)
            # This becomes n_d_when_tft_would_c for noise->0
            self.z = (self.n_d_when_tft_would_c - n_expected_ds) / max(1., std_expected_ds)
        if self.n_tft_would_c < 5 and self.n_d_when_tft_would_c < 3:
            # TfT
            return opponent.history[-1]
        elif self.z < 2:
            return C
        else:
            # TfT
            return opponent.history[-1]

def are_same_binomial(p1: float, n1: int, p2: float, n2: int, min_abs_z: float = 2.0) -> bool:
    """
    Tests if two binomial proportions are statistically indistinguishable 
    using a pooled two-proportion z-test.
    """
    p = (n1 * p1 + n2 * p2) / (n1 + n2)
    if p in (0., 1.):
        return p1 == p2
    z = (p1 - p2) / np.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    return abs(z) < min_abs_z

def has_greater_mean(ary1: np.ndarray, ary2: np.ndarray, min_z: float = 2.0) -> bool:
    """
    Tests if the mean of the first array is significantly greater than 
    the second array using a two-sample z-test.
    """
    se1 = np.std(ary1) / np.sqrt(len(ary1))
    se2 = np.std(ary2) / np.sqrt(len(ary2))
    if se1 == 0 and se2 == 0:
        return ary1.mean() > ary2.mean()
    return (ary1.mean() - ary2.mean()) / np.sqrt(se1**2 + se2**2) > min_z

def get_reward(
    my_strategy: torch.Tensor,
    opp_strategy: torch.Tensor,
    init_state: torch.Tensor,
    p_end: float,
    p_noise: float,
    RPST: tuple[float, float, float, float],
) -> float:
    """
    Calculates the expected average reward per step for a given policy 
    against a specific opponent strategy (including the effect of noise), 
    utilizing Markov transition matrices.
    """
    # Apply p_noise only to own strategy, not to opponent
    # (the opponen strategy already includes noise effects).
    own = my_strategy + p_noise * (1 - 2 * my_strategy)
    # Flip CD/DC for opponent
    opp = torch.Tensor(
        [opp_strategy[0], opp_strategy[2], opp_strategy[1], opp_strategy[3]])
    trans_mat = torch.stack([own * opp,
                             own * (1 - opp),
                             (1 - own) * opp,
                             (1 - own) * (1 - opp)])
    trans_mat = torch.transpose(trans_mat, 0, 1)
    R, P, S, T = RPST
    rewards = torch.tensor((R, S, T, P), dtype=torch.float)
    # Don't include init state in summed rewards.
    inv = torch.inverse(torch.eye(4) - (1 - p_end) * trans_mat)
    reward = torch.dot(init_state, torch.matmul(inv, rewards) - rewards)
    # Avg. reward per step
    return p_end * reward / (1 - p_end)

def optimize_against(
    opponent: np.ndarray,
    init_state_idx: int,
    p_end: float,
    p_noise: float,
    RPST: tuple[float, float, float, float],
    lr: float = 0.1,
    n_steps: float = 50,
) -> tuple[float, np.ndarray]:
    """
    Discovers the optimal response strategy (policy) against a fixed opponent 
    model by maximizing the expected reward from a given starting state 
    (init_state_idx in [0, 1, 2, 3]).
    """
    opp = torch.tensor(opponent, dtype=torch.float32)
    assert p_noise < 0.5
    opp.clamp_(min=p_noise, max=1.0 - p_noise)

    init_state = torch.zeros(4, dtype=torch.float32)
    init_state[init_state_idx] = 1.0

    params = torch.tensor([0.5, 0.5, 0.5, 0.5], requires_grad=True)
    opt = optim.Adam([params], lr=lr)

    min_loss = float("inf")
    best_params = None

    for _ in range(n_steps):
        loss = -get_reward(params, opp, init_state, p_end, p_noise, RPST)
        loss_val = loss.item()

        if loss_val < min_loss:
            min_loss = loss_val
            best_params = params.detach().numpy().copy()

        opt.zero_grad()
        loss.backward()
        opt.step()

        with torch.no_grad():
            params.clamp_(0.0, 1.0)

    return -min_loss, best_params

class ISO(Player):
    name = "ISO"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "makes_use_of": {"noise", "game"},
        "long_run_time": True,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self):
        super().__init__()
        self.discount_factor = 0.99

        # Track (numerator, denominator) for each state.
        self.ewma_CC = [1.0, 1.0]
        self.ewma_CD = [1.0, 1.0]
        self.ewma_DC = [0.0, 1.0]
        self.ewma_DD = [0.0, 1.0]

        # Initial cooperation probabilities (num / den)
        self.opp_model = [1.0, 0.0, 1.0, 0.0]
        self.my_policy = [1.0, 0.0, 1.0, 0.0]

    def receive_match_attributes(self):
        self.noise = self.match_attributes.get("noise", 0.0)
        game = self.match_attributes.get("game", axl.DefaultGame)
        self.RPST = game.RPST()

    def _update_single_ewma(self, state_ewma: list[float], action_val: float) -> float:
        """Updates the (numerator, denominator) pair in-place and returns the new average."""
        state_ewma[0] = self.discount_factor * state_ewma[0] + action_val
        state_ewma[1] = self.discount_factor * state_ewma[1] + 1.0
        return state_ewma[0] / state_ewma[1]

    def _update_opponent_model(self, opponent: Player):
        if len(self.history) < 2:
            return

        prev_state = (self.history[-2], opponent.history[-2])
        opp_act = 1.0 if opponent.history[-1] == C else 0.0

        if prev_state == (C, C):
            pr_c = self._update_single_ewma(self.ewma_CC, opp_act)
            self.opp_model[0] = pr_c
        elif prev_state == (C, D):
            pr_c = self._update_single_ewma(self.ewma_CD, opp_act)
            self.opp_model[2] = pr_c
        elif prev_state == (D, C):
            pr_c = self._update_single_ewma(self.ewma_DC, opp_act)
            self.opp_model[1] = pr_c
        elif prev_state == (D, D):
            pr_c = self._update_single_ewma(self.ewma_DD, opp_act)
            self.opp_model[3] = pr_c

    def _get_state_idx(self, opponent) -> int:
        if not self.history:
            # Pretend we started with CC
            return 0
        state = (self.history[-1], opponent.history[-1])
        if state == (C, C):
            return 0
        elif state == (C, D):
            return 1
        elif state == (D, C):
            return 2
        elif state == (D, D):
            return 3
        return -1

    def update(self, opponent: Player) -> float:
        """Updates the opponent model and our policy.

        Returns our expected reward per step."""
        self._update_opponent_model(opponent)
        state_idx = self._get_state_idx(opponent)
        expected, my_policy = optimize_against(self.opp_model,
                                               init_state_idx=state_idx,
                                               p_noise=self.noise,
                                               RPST=self.RPST,
                                               p_end=1e-2)
        self.my_policy = my_policy
        return expected

    def act(self, opponent: Player) -> Action:
        state_idx = self._get_state_idx(opponent)
        pr_c = self.my_policy[state_idx]
        return self._random.random_choice(pr_c)

    def strategy(self, opponent: Player) -> Action:
        _ = self.update(opponent)
        return self.act(opponent)
