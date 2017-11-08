"""Tests for the random tit for tat strategy."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Action.C, axelrod.Action.D


class TestRandomTitForTat(TestPlayer):
    """Tests for random tit for tat strategy."""

    name = "Random Tit for Tat: 0.5"
    player = axelrod.RandomTitForTat
    expected_classifier = {
        'memory_depth': 1,  # Four-Vector = (1.,0.,1.,0.)
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """
        Test that strategy reacts to opponent, and controlled by
        probability every other iteration.  Also reacts randomly if no
        probability input.
        """
        actions = [(C, C), (C, C), (C, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions,
                         init_kwargs={"p": 1})

        actions = [(D, D), (D, D), (D, D)]
        self.versus_test(axelrod.Defector(), expected_actions=actions,
                         init_kwargs={"p": 0})

        actions = [(D, C), (C, C), (D, C), (C, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions,
                         init_kwargs={"p": 0})

        actions = [(C, D), (D, D), (C, D), (D, D)]
        self.versus_test(axelrod.Defector(), expected_actions=actions,
                         init_kwargs={"p": 1})

        actions = [(D, C), (C, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions,
                         seed=2)

    def test_deterministic_classification(self):
        """
        Test classification when probability input is 0 or 1.
        Should change stochastic to false, because actions are no
        longer random.

        """
        for p in [0, 1]:
            player = axelrod.RandomTitForTat(p=p)
            # import pdb; pdb.set_trace()
            self.assertFalse(player.classifier['stochastic'])
