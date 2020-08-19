from typing import List, Tuple

import numpy as np
from axelrod.action import Action
from axelrod.evolvable_player import (
    EvolvablePlayer,
    InsufficientParametersError,
    crossover_lists,
)
from axelrod.load_data_ import load_weights
from axelrod.player import Player

C, D = Action.C, Action.D
nn_weights = load_weights()

# Neural Network and Activation functions
relu = np.vectorize(lambda x: max(x, 0))


def num_weights(num_features, num_hidden):
    size = num_features * num_hidden + 2 * num_hidden
    return size


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
        my_previous_d = 1 if player.history[-1] == D else 0
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
        my_previous_d = 1 if player.history[-1] == D else 0
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
        len(player.history),
    ]


def activate(
    bias: List[float], hidden: List[float], output: List[float], inputs: List[int]
) -> float:
    """
    Compute the output of the neural network:
        output = relu(inputs * hidden_weights + bias) * output_weights
    """
    inputs = np.array(inputs)
    hidden_values = bias + np.dot(hidden, inputs)
    hidden_values = relu(hidden_values)
    output_value = np.dot(hidden_values, output)
    return output_value


def split_weights(
    weights: List[float], num_features: int, num_hidden: int
) -> Tuple[List[List[float]], List[float], List[float]]:
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
        input2hidden.append(weights[i : i + num_features])

    start = number_of_input_to_hidden_weights
    end = number_of_input_to_hidden_weights + number_of_hidden_to_output_weights

    hidden2output = weights[start:end]
    bias = weights[end:]
    return input2hidden, hidden2output, bias


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

    name = "ANN"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
        "long_run_time": False,
    }

    def __init__(
        self, num_features: int, num_hidden: int,
        weights: List[float] = None
    ) -> None:
        Player.__init__(self)
        self.num_features = num_features
        self.num_hidden = num_hidden
        self._process_weights(weights, num_features, num_hidden)

    def _process_weights(self, weights, num_features, num_hidden):
        self.weights = list(weights)
        (i2h, h2o, bias) = split_weights(weights, num_features, num_hidden)
        self.input_to_hidden_layer_weights = np.array(i2h)
        self.hidden_to_output_layer_weights = np.array(h2o)
        self.bias_weights = np.array(bias)

    def strategy(self, opponent: Player) -> Action:
        features = compute_features(self, opponent)
        output = activate(
            self.bias_weights,
            self.input_to_hidden_layer_weights,
            self.hidden_to_output_layer_weights,
            features,
        )
        if output > 0:
            return C
        else:
            return D


class EvolvableANN(ANN, EvolvablePlayer):
    """Evolvable version of ANN."""
    name = "EvolvableANN"

    def __init__(
        self, num_features: int, num_hidden: int,
        weights: List[float] = None,
        mutation_probability: float = None,
        mutation_distance: int = 5,
        seed: int = None
    ) -> None:
        EvolvablePlayer.__init__(self, seed=seed)
        num_features, num_hidden, weights, mutation_probability = self._normalize_parameters(
            num_features, num_hidden, weights, mutation_probability)
        ANN.__init__(self,
                     num_features=num_features,
                     num_hidden=num_hidden,
                     weights=weights)
        self.mutation_probability = mutation_probability
        self.mutation_distance = mutation_distance
        self.overwrite_init_kwargs(
            num_features=num_features,
            num_hidden=num_hidden,
            weights=weights,
            mutation_probability=mutation_probability)

    def _normalize_parameters(self, num_features=None, num_hidden=None, weights=None, mutation_probability=None):
        if not (num_features and num_hidden):
            raise InsufficientParametersError("Insufficient Parameters to instantiate EvolvableANN")
        size = num_weights(num_features, num_hidden)
        if not weights:
            weights = [self._random.uniform(-1, 1) for _ in range(size)]
        if mutation_probability is None:
            mutation_probability = 10. / size
        return num_features, num_hidden, weights, mutation_probability

    def mutate_weights(self, weights, num_features, num_hidden, mutation_probability,
                       mutation_distance):
        size = num_weights(num_features, num_hidden)
        randoms = self._random.random(size)
        for i, r in enumerate(randoms):
            if r < mutation_probability:
                p = 1 + self._random.uniform(-1, 1) * mutation_distance
                weights[i] *= p
        return weights

    def mutate(self):
        weights = self.mutate_weights(
            self.weights, self.num_features, self.num_hidden,
            self.mutation_probability, self.mutation_distance)
        return self.create_new(weights=weights)

    def crossover(self, other):
        if other.__class__ != self.__class__:
            raise TypeError("Crossover must be between the same player classes.")
        weights = crossover_lists(self.weights, other.weights, self._random)
        return self.create_new(weights=weights)


class EvolvedANN(ANN):
    """
    A strategy based on a pre-trained neural network with 17 features and a
    hidden layer of size 10.

    Trained using the `axelrod_dojo` version: 0.0.8
    Training data is archived at doi.org/10.5281/zenodo.1306926

    Names:

     - Evolved ANN: Original name by Martin Jones.
    """

    name = "Evolved ANN"

    def __init__(self) -> None:
        num_features, num_hidden, weights = nn_weights["Evolved ANN"]
        super().__init__(
            num_features=num_features,
            num_hidden=num_hidden,
            weights=weights)


class EvolvedANN5(ANN):
    """
    A strategy based on a pre-trained neural network with 17 features and a
    hidden layer of size 5.

    Trained using the `axelrod_dojo` version: 0.0.8
    Training data is archived at doi.org/10.5281/zenodo.1306931

    Names:

     - Evolved ANN 5: Original name by Marc Harper.
    """

    name = "Evolved ANN 5"

    def __init__(self) -> None:
        num_features, num_hidden, weights = nn_weights["Evolved ANN 5"]
        super().__init__(
            num_features=num_features,
            num_hidden=num_hidden,
            weights=weights)


class EvolvedANNNoise05(ANN):
    """
    A strategy based on a pre-trained neural network with a hidden layer of
    size 5, trained with noise=0.05.

    Trained using the `axelrod_dojo` version: 0.0.8
    Training data i archived at doi.org/10.5281/zenodo.1314247.

    Names:

     - Evolved ANN Noise 5: Original name by Marc Harper.
    """

    name = "Evolved ANN 5 Noise 05"

    def __init__(self) -> None:
        num_features, num_hidden, weights = nn_weights["Evolved ANN 5 Noise 05"]
        super().__init__(
            num_features=num_features,
            num_hidden=num_hidden,
            weights=weights)
