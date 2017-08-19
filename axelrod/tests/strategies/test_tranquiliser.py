import axelrod
from Axelrod.axelrod.tests.strategies.test_player import TestPlayer
import unittest

C, D = axelrod.Action.C, axelrod.Action.D


class TestTranquiliser(TestPlayer):
    """
 Note that this test is referred to in the documentation as an example on
 writing tests.  If you modify the tests here please also modify the
 documentation.
 """

    name = "Tranquiliser"
    player = axelrod.Tranquiliser
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': {"game"},
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }



    def test_strategy(self):

        player = axelrod.Tranquiliser()

        opponent = axelrod.Defector()
        actions = [(C, D)] + [(D, D)] * 20
        self.versus_test(opponent = opponent, expected_actions=actions)

        opponent = axelrod.Cooperator()
        actions = [(C, C)] * 5 + ([(C, C)]) * 20
        self.versus_test(opponent, expected_actions=actions)
