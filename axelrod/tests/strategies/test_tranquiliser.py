import axelrod
from Axelrod.axelrod.tests.strategies.test_player import TestPlayer

C, D = axelrod.Action.C, axelrod.Action.D


class TestTranquiliser(TestPlayer):

    name = "Tranquiliser"
    player = axelrod.Tranquiliser
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(["game"]),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.assertEqual(2 + 2, 4)
