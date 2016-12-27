# Source: https://gist.github.com/mojones/550b32c46a8169bb3cd89d917b73111a#file-ann-strategy-test-L60
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

    @init_args
    def __init__(
        self,
        input_to_hidden_layer_weights=[],
        hidden_to_output_layer_weights=[],
        bias_weights=[]
    ):

        Player.__init__(self)
        self.input_to_hidden_layer_weights = input_to_hidden_layer_weights
        self.hidden_to_output_layer_weights = hidden_to_output_layer_weights
        self.bias_weights = bias_weights

        self.input_values = len(input_to_hidden_layer_weights[0])
        self.hidden_layer_size = len(hidden_to_output_layer_weights)

    def strategy(self, opponent):
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
        # turns_remaining = self.match_attributes['length'] - len(self.history)
        total_opponent_c = opponent.history.count(C)
        total_opponent_d = opponent.history.count(D)
        total_self_c = self.history.count(C)
        total_self_d = self.history.count(D)

        output = self.activate([
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
        ])
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
        input_values = 17
        hidden_layer_size = 10

        weights = nn_weights['']

        (i2h, h2o, bias) = split_weights(
            weights,
            input_values,
            hidden_layer_size
        )
        ANN.__init__(self, i2h, h2o, bias)


class EvolvedANN2(ANN):
    """
    A strategy based on a pre-trained neural network.

    Names:

     - EvolvedANN2: : Original name by Marc Harper.
    """

    name = "EvolvedANN2"

    @init_args
    def __init__(self):
        input_values = 17
        hidden_layer_size = 10

        weights = nn_weights['2']

        (i2h, h2o, bias) = split_weights(
            weights,
            input_values,
            hidden_layer_size
        )
        ANN.__init__(self, i2h, h2o, bias)


class EvolvedANN05(ANN):
    """
    A strategy based on a pre-trained neural network, trained with noise=0.05.

    Names:

     - EvolvedANN05: Original name by Marc Harper.
    """

    name = "EvolvedANN05"

    @init_args
    def __init__(self):
        input_values = 17
        hidden_layer_size = 10

        weights = nn_weights['05']

        (i2h, h2o, bias) = split_weights(
            weights,
            input_values,
            hidden_layer_size
        )
        ANN.__init__(self, i2h, h2o, bias)


class EvolvedANNMoran(ANN):
    """
    A strategy based on a pre-trained neural network, optimized for the Moran
    process.

    Names:

     - EvolvedANNMoran: Original name by Marc Harper.
    """

    name = "EvolvedANNMoran"

    @init_args
    def __init__(self):
        input_values = 17
        hidden_layer_size = 10

        weights = nn_weights['moran']

        (i2h, h2o, bias) = split_weights(
            weights,
            input_values,
            hidden_layer_size
        )
        ANN.__init__(self, i2h, h2o, bias)
