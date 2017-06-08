import numpy as np

from axelrod.actions import Actions, Action
from axelrod.player import Player
from axelrod.load_data_ import load_weights

from typing import List, Tuple

C, D = Actions.C, Actions.D
nn_weights = load_weights()


# Neural Network and Activation functions
relu = np.vectorize(lambda x: max(x, 0))


def compute_features(player: Player, opponent: Player) -> List[int]:
    """
    Compute history features for Neural Network:
    * Opponent's first move is C
    * Opponent's first move is D
    * Opponent's second move is C
    * Opponent's second move is D
    * Player's previous move is C
    * Player's previous move is D
    * Player's second previous move is C
    * Player's second previous move is D
    * Opponent's previous move is C
    * Opponent's previous move is D
    * Opponent's second previous move is C
    * Opponent's second previous move is D
    * Total opponent cooperations
    * Total opponent defections
    * Total player cooperations
    * Total player defections
    * Round number
    """
    if len(opponent.history) == 0:
        opponent_first_c = 0
        opponent_first_d = 0
        opponent_second_c = 0
        opponent_second_d = 0
        my_previous_c = 0
        my_previous_d = 0
        my_previous2_c = 0
        my_previous2_d = 0
        opponent_previous_c = 0
        opponent_previous_d = 0
        opponent_previous2_c = 0
        opponent_previous2_d = 0

    elif len(opponent.history) == 1:
        opponent_first_c = 1 if opponent.history[0] == C else 0
        opponent_first_d = 1 if opponent.history[0] == D else 0
        opponent_second_c = 0
        opponent_second_d = 0
        my_previous_c = 1 if player.history[-1] == C else 0
        my_previous_d = 0 if player.history[-1] == D else 0
        my_previous2_c = 0
        my_previous2_d = 0
        opponent_previous_c = 1 if opponent.history[-1] == C else 0
        opponent_previous_d = 1 if opponent.history[-1] == D else 0
        opponent_previous2_c = 0
        opponent_previous2_d = 0

    else:
        opponent_first_c = 1 if opponent.history[0] == C else 0
        opponent_first_d = 1 if opponent.history[0] == D else 0
        opponent_second_c = 1 if opponent.history[1] == C else 0
        opponent_second_d = 1 if opponent.history[1] == D else 0
        my_previous_c = 1 if player.history[-1] == C else 0
        my_previous_d = 0 if player.history[-1] == D else 0
        my_previous2_c = 1 if player.history[-2] == C else 0
        my_previous2_d = 1 if player.history[-2] == D else 0
        opponent_previous_c = 1 if opponent.history[-1] == C else 0
        opponent_previous_d = 1 if opponent.history[-1] == D else 0
        opponent_previous2_c = 1 if opponent.history[-2] == C else 0
        opponent_previous2_d = 1 if opponent.history[-2] == D else 0

    # Remaining Features
    total_opponent_c = opponent.cooperations
    total_opponent_d = opponent.defections
    total_player_c = player.cooperations
    total_player_d = player.defections

    return [
        opponent_first_c,
        opponent_first_d,
        opponent_second_c,
        opponent_second_d,
        my_previous_c,
        my_previous_d,
        my_previous2_c,
        my_previous2_d,
        opponent_previous_c,
        opponent_previous_d,
        opponent_previous2_c,
        opponent_previous2_d,
        total_opponent_c,
        total_opponent_d,
        total_player_c,
        total_player_d,
        len(player.history)
    ]


def activate(bias: List[float], hidden: List[float], output: List[float], inputs: List[int]) -> float:
    """
    Compute the output of the neural network:
        output = relu(inputs * hidden_weights + bias) * output_weights
    """
    inputs = np.array(inputs)
    hidden_values = bias + np.dot(hidden, inputs)
    hidden_values = relu(hidden_values)
    output_value = np.dot(hidden_values, output)
    return output_value


def split_weights(weights: List[float], num_features: int, num_hidden: int) -> Tuple[List[List[float]], List[float], List[float]]:
    """Splits the input vector into the the NN bias weights and layer
    parameters."""
    # Check weights is the right length
    expected_length = num_hidden * 2 + num_features * num_hidden
    if expected_length != len(weights):
        raise ValueError("NN weights array has an incorrect size.")

    number_of_input_to_hidden_weights = num_features * num_hidden
    number_of_hidden_to_output_weights = num_hidden

    input2hidden = []
    for i in range(0, number_of_input_to_hidden_weights, num_features):
        input2hidden.append(weights[i:i + num_features])

    start = number_of_input_to_hidden_weights
    end = number_of_input_to_hidden_weights + number_of_hidden_to_output_weights

    hidden2output = weights[start: end]
    bias = weights[end:]
    return (input2hidden, hidden2output, bias)


class ANN(Player):
    """Artificial Neural Network based strategy.

    A single layer neural network based strategy, with the following
    features:
    * Opponent's first move is C
    * Opponent's first move is D
    * Opponent's second move is C
    * Opponent's second move is D
    * Player's previous move is C
    * Player's previous move is D
    * Player's second previous move is C
    * Player's second previous move is D
    * Opponent's previous move is C
    * Opponent's previous move is D
    * Opponent's second previous move is C
    * Opponent's second previous move is D
    * Total opponent cooperations
    * Total opponent defections
    * Total player cooperations
    * Total player defections
    * Round number

    Original Source: https://gist.github.com/mojones/550b32c46a8169bb3cd89d917b73111a#file-ann-strategy-test-L60


    Names

    - Artificial Neural Network based strategy: Original name by Martin Jones
    """
    name = 'ANN'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'inspects_source': False,
        'makes_use_of': set(),
        'manipulates_source': False,
        'manipulates_state': False,
        'long_run_time': False
    }

    def __init__(self, weights: List[float], num_features: int,
                 num_hidden: int) -> None:
        super().__init__()
        (i2h, h2o, bias) = split_weights(weights, num_features, num_hidden)
        self.input_to_hidden_layer_weights = np.matrix(i2h)
        self.hidden_to_output_layer_weights = np.array(h2o)
        self.bias_weights = np.array(bias)

    def strategy(self, opponent: Player) -> Action:
        features = compute_features(self, opponent)
        output = activate(self.bias_weights,
                          self.input_to_hidden_layer_weights,
                          self.hidden_to_output_layer_weights,
                          features)
        if output > 0:
            return C
        else:
            return D


class EvolvedANN(ANN):
    """
    A strategy based on a pre-trained neural network with 17 features and a
    hidden layer of size 10.

    Names:

     - Evolved ANN: Original name by Martin Jones.
    """

    name = "Evolved ANN"

    def __init__(self) -> None:
        num_features, num_hidden, weights = nn_weights["Evolved ANN"]
        super().__init__(weights, num_features, num_hidden)


class EvolvedANN5(ANN):
    """
    A strategy based on a pre-trained neural network with 17 features and a
    hidden layer of size 5.

    Names:

     - Evolved ANN 5: Original name by Marc Harper.
    """

    name = "Evolved ANN 5"

    def __init__(self) -> None:
        num_features, num_hidden, weights = nn_weights["Evolved ANN 5"]
        super().__init__(weights, num_features, num_hidden)


class EvolvedANNNoise05(ANN):
    """
    A strategy based on a pre-trained neural network with a hidden layer of
    size 10, trained with noise=0.05.

    Names:

     - Evolved ANN Noise 05: Original name by Marc Harper.
    """

    name = "Evolved ANN 5 Noise 05"

    def __init__(self) -> None:
        num_features, num_hidden, weights = nn_weights["Evolved ANN 5 Noise 05"]
        super().__init__(weights, num_features, num_hidden)
