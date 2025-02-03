import axelrod as axl
from axelrod import Action
from axelrod.strategies.momentum import Momentum
from axelrod.tests.strategies.test_player import TestPlayer

C, D = Action.C, Action.D


class TestMomentum(TestPlayer):
    name = "Momentum"
    player = Momentum
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_initialisation(self):
        player = self.player(alpha=0.9, threshold=0.8)
        self.assertEqual(player.alpha, 0.9)
        self.assertEqual(player.threshold, 0.8)
        self.assertEqual(player.momentum, 1.0)

    def test_repr(self):
        player = self.player(alpha=0.9, threshold=0.8)
        self.assertEqual(
            repr(player), "Momentum: 1.0, Alpha: 0.9, Threshold: 0.8"
        )

    def test_strategy(self):
        actions = [(C, C)]
        self.versus_test(
            axl.MockPlayer(actions=[C]),
            expected_actions=actions,
            init_kwargs={"alpha": 0.5, "threshold": 0.5},
            attrs={"momentum": 1.0},
        )

        actions = [(C, D), (C, D), (D, D)]
        self.versus_test(
            axl.MockPlayer(actions=[D]),
            expected_actions=actions,
            init_kwargs={"alpha": 0.5, "threshold": 0.5},
            attrs={"momentum": 0.25},
        )

    def test_vs_alternator(self):
        actions = [(C, C), (C, D), (C, C), (C, D), (D, C)]
        self.versus_test(
            axl.Alternator(),
            expected_actions=actions,
            init_kwargs={"alpha": 0.5, "threshold": 0.5},
        )

    def test_vs_cooperator(self):
        actions = [(C, C), (C, C), (C, C), (C, C), (C, C)]
        self.versus_test(
            axl.Cooperator(),
            expected_actions=actions,
            init_kwargs={"alpha": 0.5, "threshold": 0.5},
        )

    def test_vs_defector(self):
        actions = [(C, D), (C, D), (D, D), (D, D), (D, D)]
        self.versus_test(
            axl.Defector(),
            expected_actions=actions,
            init_kwargs={"alpha": 0.5, "threshold": 0.5},
        )

    def test_vs_random(self):
        actions = [(C, D), (C, C), (C, C), (C, D), (D, D)]
        self.versus_test(
            axl.Random(),
            expected_actions=actions,
            seed=17,
            init_kwargs={"alpha": 0.5, "threshold": 0.5},
        )

    def test_vs_random2(self):
        actions = [(C, C), (C, C), (C, C), (C, C)]
        self.versus_test(
            axl.Random(),
            expected_actions=actions,
            seed=3,
            init_kwargs={"alpha": 0.5, "threshold": 0.5},
        )
