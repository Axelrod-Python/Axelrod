# Original Source: https://gist.github.com/mojones/550b32c46a8169bb3cd89d917b73111a#file-ann-strategy-test-L60
# Original Author: Martin Jones, @mojones

from axelrod import Actions, Player, init_args, load_weights

C, D = Actions.C, Actions.D
nn_weights = load_weights()


def split_weights(weights, input_values, hidden_layer_size):
    """Splits the input vector into the the NN bias weights and layer
    parameters."""
    number_of_input_to_hidden_weights = input_values * hidden_layer_size
    number_of_hidden_to_output_weights = hidden_layer_size

    input2hidden = []
    for i in range(0, number_of_input_to_hidden_weights, input_values):
        input2hidden.append(weights[i:i + input_values])

    start = number_of_input_to_hidden_weights
    end = number_of_input_to_hidden_weights + number_of_hidden_to_output_weights

    hidden2output = weights[start: end]
    bias = weights[end:]
    return (input2hidden, hidden2output, bias)


class ANN(Player):
    """A single layer neural network based strategy."""
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

    @init_args
    def __init__(self, weights, num_features, num_hidden):
        Player.__init__(self)
        (i2h, h2o, bias) = split_weights(weights, num_features, num_hidden)
        self.input_to_hidden_layer_weights = i2h
        self.hidden_to_output_layer_weights = h2o
        self.bias_weights = bias
        self.input_values = num_features
        self.hidden_layer_size = num_hidden

    def activate(self, inputs):
        """Compute the output of the neural network."""
        # Calculate values of hidden nodes
        hidden_values = []
        for i in range(self.hidden_layer_size):
            hidden_node_value = 0
            bias_weight = self.bias_weights[i]
            hidden_node_value += bias_weight
            for j in range(self.input_values):
                weight = self.input_to_hidden_layer_weights[i][j]
                hidden_node_value += inputs[j] * weight

            # ReLU activation function
            hidden_node_value = max(hidden_node_value, 0)

            hidden_values.append(hidden_node_value)

        # Calculate output value
        output_value = 0
        for i in range(self.hidden_layer_size):
            output_value += hidden_values[i] * \
                            self.hidden_to_output_layer_weights[i]

        return output_value

    def compute_features(self, opponent):
        # Compute features for Neural Network
        # These are True/False 0/1
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
            my_previous_c = 1 if self.history[-1] == C else 0
            my_previous_d = 0 if self.history[-1] == D else 0
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
            my_previous_c = 1 if self.history[-1] == C else 0
            my_previous_d = 0 if self.history[-1] == D else 0
            my_previous2_c = 1 if self.history[-2] == C else 0
            my_previous2_d = 1 if self.history[-2] == D else 0
            opponent_previous_c = 1 if opponent.history[-1] == C else 0
            opponent_previous_d = 1 if opponent.history[-1] == D else 0
            opponent_previous2_c = 1 if opponent.history[-2] == C else 0
            opponent_previous2_d = 1 if opponent.history[-2] == D else 0

        # Remaining Features
        total_opponent_c = opponent.cooperations
        total_opponent_d = opponent.defections
        total_self_c = self.cooperations
        total_self_d = self.defections

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
            total_self_c,
            total_self_d,
            len(self.history)
        ]

    def strategy(self, opponent):
        features = self.compute_features(opponent)
        output = self.activate(features)
        if output > 0:
            return C
        else:
            return D


class EvolvedANN(ANN):
    """
    A strategy based on a pre-trained neural network.

    Names:

     - EvolvedANN: : Original name by Martin Jones.
    """

    name = "EvolvedANN"

    @init_args
    def __init__(self):
        num_features, num_hidden, weights = nn_weights['1']
        ANN.__init__(self, weights, num_features, num_hidden)


class EvolvedANN5(ANN):
    """
    A strategy based on a pre-trained neural network.

    Names:

     - EvolvedANN2: : Original name by Marc Harper.
    """

    name = "EvolvedANN5"

    @init_args
    def __init__(self):
        num_features, num_hidden, weights = nn_weights['5']
        ANN.__init__(self, weights, num_features, num_hidden)


class EvolvedANNNoise05(ANN):
    """
    A strategy based on a pre-trained neural network, trained with noise=0.05.

    Names:

     - EvolvedANNNoise05: Original name by Marc Harper.
    """

    name = "EvolvedANNNoise05"

    @init_args
    def __init__(self):
        num_features, num_hidden, weights = nn_weights['05']
        ANN.__init__(self, weights, num_features, num_hidden)
