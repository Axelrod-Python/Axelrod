# Source: https://gist.github.com/mojones/550b32c46a8169bb3cd89d917b73111a#file-ann-strategy-test-L60
# Original Author: Martin Jones, @mojones

from axelrod import Actions, Player, init_args

C, D = Actions.C, Actions.D


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
        turns_remaining = self.match_attributes['length'] - len(self.history)
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
            turns_remaining
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
        self.classifier['makes_use_of'] = set(['length'])
        input_values = 17
        hidden_layer_size = 10

        weights = [0.19789658035994948, -5575.476236516673, 0.1028948855131803, 0.7421752484224489,
                       -16.286246197005298, 11708.007255945553, 0.01400184611448853, -33.39126355009626,
                       -12.755203414662356, -32.92388754142929, 197.3517717772447, 108262.87038790248,
                       -0.1084768512582505, 85.20738888799768, 723.9537664890132, -2.59453614458083,
                       0.5599936275978272, 7.89217571665664, -48014.821440080384, -1.364025168184463,
                       -1.062138244222801, 11153713.883580556, -59.58314524751318, 51278.916519524784,
                       3196.528224457722, -4635.771421694692, -129.93354968926164, -0.7927383528469051,
                       98.47779304649353, -81.19056440190543, 29.53082483602472, -48.16562780387682,
                       49.40755170297665, 288.3295763937912, -68.38780651250116, -167.64039570334904,
                       -0.1576073061122998, 160.6846658333963, 34.55451693336857, -0.08213997499783675,
                       -4.802560347075611, -1.4042000430302104, -0.9832145174590058, 0.008705149387813573,
                        14.041842191255089, 0.05395665905821821, -0.13856885306885558, 5.311455433711278,
                       -5.835498171845142, 0.00010294700612334848, 26.42528200366623, 33.690839945794785,
                       7.931017950666591, -0.00037662122944226125, 59.295075951374606, -0.15888507169191035,
                       3.670332254391659, 789.6230735057893, -0.7367125124436135, -198.44119280589902,
                       537.9939493545736, -287.54344903637207, 1759.5455359353778, -18.48997020629342,
                       -8426184.81603275, -82.36805426730088, 1144.1032034358543, 15635.402592538396,
                       3095.643889329041, 2332.107673930774, -0.5601648316602144, 101.98300711150003,
                       -7387.135294747112, -4241.004613717573, 3.06175607282536e-05, -35122.894421260884,
                       -38591.45572476855, -0.16081285130591272, -29608.73087879185, 122.47563639056185,
                       6.381946054740736, -0.8978628581801188, 17658.47647781355, -0.011719257684286711,
                       0.10734295104044986, -378.35448968529494, 225.06912279045062, -351.12326495980847,
                       -1.927322672845826, 0.0014584395475859544, -8.629826916169318, 22.43281153854352,
                       87.10895591188721, -0.22253937914423294, -233.06796470563208, -620.4917481128365,
                       -1.8253699204909606,-0.0030318160426064467, -77.25818476745101, -2057.311059352977,
                       3.764204074005541, -47.47629147374066, 233.16096124330778, -160721.96744375565,
                       -278292.9688140893, -2.093640525920404, -142886.66171202937, 53.64449245132945,
                       12.5162147724691, -207.75462390139955, 132167.659160016, 21.197418541051732,
                       83979.45623573882, -49.47558832987566, 0.05242625398046057, -842.1484416713075,
                       -0.1581049310461208, 2359.2124343564096, 1170.5147830681053, -847999.9145843558,
                       -0.8053911061885284, -5363.722820739466, 171.58433274294117, -724.7468082647013,
                       2500359.853524033, 1595.3955511798079, -4.254009123616706, -171.12968391407912,
                       -32.30624102753424, -558.412338112568, -234.29754199019308, -18768.34057250429,
                       8338.792126484348, -0.18593140210730602, -7.758804964874875, 0.39736677884665267,
                       547.0567585452197, 1.1969366369973133, 0.4861465741177498, -51.19319208716985,
                       12.775051406025534, -0.09185362260212569, 22.08417300332754, -5090.013231748707,
                       -0.814394991797045, 1.1534025840023847, 8.390439959276764, -0.02227253403481858,
                       0.14162040507921927, -0.011508263843203926, 0.22372493104861083, 0.7754713610627112,
                       0.1044033140236981, -4.377055307648915, -41.898221495326574, -18656.755601828827,
                       -134.56719406539244, -2405.8148785743474, 16864.049985157206, -0.5124682025216784,
                       14521.069005125159, -10.740782200739309, 18756.807715014013, -1723.9353962656946,
                       87029.99828299093, 5.7383786020894195e-05, 4762.960401619296, 0.7331769713238158,
                       -308.5673034493341, 85.29725765515369, 0.4268843538235295, -0.17788805472511407,
                       -1.1727033611646802, 7578.6822604990175, 0.5124673187864222, 0.1595627909684813,
                       -145.93742731401096, -2954.234440189563, 0.009672881359732015, 106.4646644917487,
                       -0.050606976105730346, 2.3904047264403596, -4.987645640997455, -43.22984692765006,
                       -36.177108409134966, -0.3812547430698569, -2959.4921368963633, -1.8635802741029985,
                       0.020513128847167047, -0.9179124323385958]

        (i2h, h2o, bias) = split_weights(
            weights,
            input_values,
            hidden_layer_size
        )
        ANN.__init__(self, i2h, h2o, bias)
