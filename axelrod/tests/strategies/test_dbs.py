"""Tests DBS strategy."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestDBS(TestPlayer):
    name = "DBS: 0.75, 3, 4, 3, 5"
    player = axelrod.DBS

    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # start by cooperating
        print('\n')
        print("############################")
        print('\n')
        self.first_play_test(C)

        print('\n')
        print("############################")
        print('\n')

        default_init_kwargs = {'discount_factor':.75, 'promotion_threshold':3, 'violation_threshold':4, 'reject_threshold':4,'tree_depth':5}

        actions = [(C, C)] * 7
        self.versus_test(opponent=axelrod.Cooperator(), expected_actions=actions)
                         #attrs={"opponent_class": "Cooperative"})


        print('\n')
        print("############################")
        print('\n')


        actions = [(C,C),(C,D)]*3 + [(D,C),(C,D)]*3 
        self.versus_test(opponent=axelrod.Alternator(), expected_actions=actions,init_kwargs = default_init_kwargs)
                         #attrs={"opponent_class": "Cooperative"})


        print('\n')
        print("############################")
        print('\n')

        # check that algorithms take into account a change in 
        # opponent's strategy

        mock_actions = [C,C,C,D,D,D,D,D,D,D]
        exp_actions = [(C,C)]*3 + [(C,D)]*4 + [(D,D)]*3 
        self.versus_test(opponent=axelrod.MockPlayer(actions=mock_actions),
                                 expected_actions=exp_actions, seed=None,init_kwargs = default_init_kwargs)


        # check that adaptation is faster if diminishing promotion_threshold
        init_kwargs_2 = {'discount_factor':.75, 'promotion_threshold':2, 'violation_threshold':4, 'reject_threshold':4,'tree_depth':5}
        mock_actions = [C,C,C,D,D,D,D,D,D,D]
        exp_actions = [(C,C)]*3 + [(C,D)]*3 + [(D,D)]*4 
        self.versus_test(opponent=axelrod.MockPlayer(actions=mock_actions),
                                 expected_actions=exp_actions, seed=None,init_kwargs = init_kwargs_2)


#        opponent = axelrod.MockPlayer(actions=[C] * 6 + [D])
#        actions = [(C, C)] * 6 + [(C, D), (D, C)]
#        self.versus_test(opponent, expected_actions=actions,
#                         attrs={"opponent_class": "Cooperative"})
#
#        actions = [(C, D)] + [(D, D)] * 6
#        self.versus_test(axelrod.Defector(), expected_actions=actions,
#                         attrs={"opponent_class": "ALLD"})
#
#        opponent = axelrod.MockPlayer(actions=[D, C, D, C, D, C])
#        actions = [(C, D), (D, C), (C, D), (D, C),
#                   (C, D), (D, C), (C, D), (C, C),
#                   (C, D), (D, C)]
#        self.versus_test(opponent, expected_actions=actions,
#                         attrs={"opponent_class": "STFT"})
#
#        opponent = axelrod.MockPlayer(actions=[D, D, C, D, D, C])
#        actions = [(C, D), (D, D), (D, C), (C, D), (D, D), (D, C), (D, D)]
#        self.versus_test(opponent, expected_actions=actions,
#                         attrs={"opponent_class": "PavlovD"})
#
#        opponent = axelrod.MockPlayer(actions=[D, D, C, D, D, C, D])
#        actions = [(C, D), (D, D), (D, C), (C, D),
#                   (D, D), (D, C), (D, D), (C, D)]
#        self.versus_test(opponent, expected_actions=actions,
#                         attrs={"opponent_class": "PavlovD"})
#
#        opponent = axelrod.MockPlayer(actions=[C, C, C, D, D, D])
#        actions = [(C, C), (C, C), (C, C), (C, D), (D, D), (D, D), (D, C)]
#        self.versus_test(opponent, expected_actions=actions,
#                         attrs={"opponent_class": "Random"})
#
#        opponent = axelrod.MockPlayer(actions=[D, D, D, C, C, C])
#        actions = [(C, D), (D, D), (D, D), (D, C), (C, C), (C, C), (D, D)]
#        self.versus_test(opponent, expected_actions=actions,
#                         attrs={"opponent_class": "Random"})
#
#
#class TestAPavlov2011(TestPlayer):
#    name = "Adaptive Pavlov 2011"
#    player = axelrod.APavlov2011
#
#    expected_classifier = {
#        'memory_depth': float('inf'),
#        'stochastic': False,
#        'makes_use_of': set(),
#        'long_run_time': False,
#        'inspects_source': False,
#        'manipulates_source': False,
#        'manipulates_state': False
#    }
#
#    def test_strategy(self):
#        self.first_play_test(C)
#
#        actions = [(C, C)] * 8
#        self.versus_test(axelrod.Cooperator(), expected_actions=actions,
#                         attrs={"opponent_class": "Cooperative"})
#
#        actions = [(C, D)] + [(D, D)] * 9
#        self.versus_test(axelrod.Defector(), expected_actions=actions,
#                         attrs={"opponent_class": "ALLD"})
#
#        opponent = axelrod.MockPlayer(actions=[C, D, D, D, D, D, D])
#        actions = [(C, C), (C, D)] + [(D, D)] * 5 + [(D, C)]
#        self.versus_test(opponent, expected_actions=actions,
#                         attrs={"opponent_class": "ALLD"})
#
#        opponent = axelrod.MockPlayer(actions=[C, C, D, D, D, D, D])
#        actions = [(C, C), (C, C), (C, D)] + [(D, D)] * 4 + [(D, C)]
#        self.versus_test(opponent, expected_actions=actions,
#                         attrs={"opponent_class": "ALLD"})
#
#        opponent = axelrod.MockPlayer(actions=[C, D, D, C, D, D, D])
#        actions = [(C, C), (C, D), (D, D), (D, C),
#                   (C, D), (D, D), (D, D), (D, C)]
#        self.versus_test(opponent, expected_actions=actions,
#                         attrs={"opponent_class": "ALLD"})
#
#        opponent = axelrod.MockPlayer(actions=[C, D, D, C, C, D, D])
#        actions = [(C, C), (C, D), (D, D), (D, C),
#                   (C, C), (C, D), (C, D), (D, C)]
#        self.versus_test(opponent, expected_actions=actions,
#                         attrs={"opponent_class": "STFT"})
#
#        opponent = axelrod.MockPlayer(actions=[C, D, C, D, C, D, D])
#        actions = [(C, C), (C, D), (D, C), (C, D),
#                   (D, C), (C, D), (C, D), (D, C)]
#        self.versus_test(opponent, expected_actions=actions,
#                         attrs={"opponent_class": "STFT"})
#
#        opponent = axelrod.MockPlayer(actions=[D, D, D, C, C, C, C])
#        actions = [(C, D), (D, D), (D, D), (D, C),
#                   (C, C), (C, C), (C, C), (C, D)]
#        self.versus_test(opponent, expected_actions=actions,
#                         attrs={"opponent_class": "STFT"})
#
#        opponent = axelrod.MockPlayer(actions=[C, C, C, C, D, D])
#        actions = [(C, C), (C, C), (C, C), (C, C),
#                   (C, D), (D, D), (D, C), (D, C)]
#        self.versus_test(opponent, expected_actions=actions,
#                         attrs={"opponent_class": "Random"})
#
#        opponent = axelrod.MockPlayer(actions=[D, D, C, C, C, C])
#        actions = [(C, D), (D, D), (D, C), (C, C),
#                   (C, C), (C, C), (D, D), (D, D)]
#        self.versus_test(opponent, expected_actions=actions,
#                         attrs={"opponent_class": "Random"})
