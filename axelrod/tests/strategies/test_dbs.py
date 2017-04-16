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
        self.first_play_test(C)

        default_init_kwargs = {'discount_factor':.75, 'promotion_threshold':3, 'violation_threshold':4, 'reject_threshold':4,'tree_depth':5}

        actions = [(C, C)] * 7
        self.versus_test(opponent=axelrod.Cooperator(), expected_actions=actions)

        # test if it correctly learns Alternator strategy
        actions = [(C,C),(C,D)]*3 + [(D,C),(C,D)]*3 
        self.versus_test(opponent=axelrod.Alternator(), expected_actions=actions,init_kwargs = default_init_kwargs)


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

