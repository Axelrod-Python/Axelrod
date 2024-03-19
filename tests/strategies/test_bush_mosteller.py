import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestBushMostellar(TestPlayer):

    name = "Bush Mosteller: 0.5, 0.5, 3.0, 0.5"
    player = axl.BushMosteller
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "makes_use_of": {"game"},
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (D, C), (D, C)]
        self.versus_test(
            axl.Cooperator(),
            expected_actions=actions,
            attrs={"_stimulus": 1},
            seed=1,
        )

        # Making sure probabilities changes following payoffs
        actions = [(C, C), (D, D)]
        self.versus_test(
            axl.Alternator(),
            expected_actions=actions,
            attrs={"_stimulus": 0.4, "_c_prob": 0.6, "_d_prob": 0.5},
            seed=1,
        )

        actions = [(C, D), (D, D), (D, D)]
        self.versus_test(
            axl.Defector(),
            expected_actions=actions,
            attrs={
                "_stimulus": -0.20000000000000004,
                "_c_prob": 0.375,
                "_d_prob": 0.45,
            },
            seed=1,
        )

        # Testing that stimulus never goes under -1
        actions = [(C, C), (D, C), (D, C)]
        self.versus_test(
            axl.Cooperator(),
            expected_actions=actions,
            attrs={"_stimulus": -1},
            init_kwargs={"aspiration_level_divider": 0.1},
            seed=1,
        )

        # Ensures that the player will never play C or D if his probability is equal to 0
        actions = [(C, C)] * 100
        self.versus_test(
            axl.Cooperator(),
            expected_actions=actions,
            init_kwargs={"d_prob": 0.0},
            seed=1,
        )

        actions = [(D, C)] * 100
        self.versus_test(
            axl.Cooperator(),
            expected_actions=actions,
            init_kwargs={"c_prob": 0.0},
            seed=1,
        )
