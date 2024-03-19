"""Tests for Prober strategies."""

import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestCollectiveStrategy(TestPlayer):

    name = "CollectiveStrategy"
    player = axl.CollectiveStrategy
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # If handshake (C, D) is used cooperate until a defection occurs and
        # then defect throughout
        opponent = axl.MockPlayer([C, D] + [C] * 10)
        actions = [(C, C), (D, D)] + [(C, C)] * 11 + [(C, D)] + [(D, C)] * 10
        self.versus_test(opponent=opponent, expected_actions=actions)

        # If handshake is not used: defect
        actions = [(C, C), (D, C)] + [(D, C)] * 15
        self.versus_test(opponent=axl.Cooperator(), expected_actions=actions)

        actions = [(C, D), (D, D)] + [(D, D)] * 15
        self.versus_test(opponent=axl.Defector(), expected_actions=actions)


class TestDetective(TestPlayer):

    name = "Detective"
    player = axl.Detective
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        self.versus_test(
            opponent=axl.TitForTat(),
            expected_actions=[(C, C), (D, C), (C, D)] + [(C, C)] * 15,
        )

        self.versus_test(
            opponent=axl.Cooperator(),
            expected_actions=[(C, C), (D, C), (C, C), (C, C)] + [(D, C)] * 15,
        )

        self.versus_test(
            opponent=axl.Defector(),
            expected_actions=[(C, D), (D, D), (C, D), (C, D)] + [(D, D)] * 15,
        )

    def test_other_initial_actions(self):
        self.versus_test(
            opponent=axl.TitForTat(),
            expected_actions=[(C, C), (C, C), (D, C)] + [(D, D)] * 15,
            init_kwargs={"initial_actions": [C, C]},
        )

        # Extreme case: no memory at all, it's simply a defector
        self.versus_test(
            opponent=axl.TitForTat(),
            expected_actions=[(D, C)] + [(D, D)] * 15,
            init_kwargs={"initial_actions": []},
        )


class TestProber(TestPlayer):

    name = "Prober"
    player = axl.Prober
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # Starts by playing DCC.
        # Defects forever if opponent cooperated in moves 2 and 3
        actions = [(D, C), (C, C), (C, C)] + [(D, C)] * 3
        self.versus_test(opponent=axl.Cooperator(), expected_actions=actions)

        opponent = axl.MockPlayer([D, C, C])
        actions = [(D, D), (C, C), (C, C)] + [(D, D), (D, C), (D, C)]
        self.versus_test(opponent=opponent, expected_actions=actions)

        # Otherwise it plays like TFT
        actions = [(D, C), (C, D), (C, C), (C, D), (D, C)]
        self.versus_test(opponent=axl.Alternator(), expected_actions=actions)

        actions = [(D, D), (C, D), (C, D), (D, D), (D, D)]
        self.versus_test(opponent=axl.Defector(), expected_actions=actions)


class TestProber2(TestPlayer):

    name = "Prober 2"
    player = axl.Prober2
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # Starts by playing DCC.
        # Cooperates forever if opponent played D, C in moves 2 and 3
        actions = [(D, C), (C, D), (C, C)] + [(C, D), (C, C), (C, D)]
        self.versus_test(opponent=axl.Alternator(), expected_actions=actions)

        opponent = axl.MockPlayer([D, D, C])
        actions = [(D, D), (C, D), (C, C)] + [(C, D), (C, D), (C, C)]
        self.versus_test(opponent=opponent, expected_actions=actions)

        # Otherwise it plays like TFT
        actions = [(D, C), (C, C), (C, C), (C, C), (C, C)]
        self.versus_test(opponent=axl.Cooperator(), expected_actions=actions)

        actions = [(D, D), (C, D), (C, D), (D, D), (D, D)]
        self.versus_test(opponent=axl.Defector(), expected_actions=actions)

        opponent = axl.MockPlayer([D, C])
        actions = [(D, D), (C, C), (C, D)] + [(D, C), (C, D), (D, C)]
        self.versus_test(opponent=opponent, expected_actions=actions)


class TestProber3(TestPlayer):

    name = "Prober 3"
    player = axl.Prober3
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # Starts by playing DC.
        # Defects forever if opponent played C in move 2.
        actions = [(D, C), (C, C)] + [(D, C), (D, C), (D, C)]
        self.versus_test(opponent=axl.Cooperator(), expected_actions=actions)

        opponent = axl.MockPlayer([D, C])
        actions = [(D, D), (C, C)] + [(D, D), (D, C), (D, D)]
        self.versus_test(opponent=opponent, expected_actions=actions)

        # Otherwise it plays like TFT
        actions = [(D, C), (C, D), (D, C), (C, D), (D, C)]
        self.versus_test(opponent=axl.Alternator(), expected_actions=actions)

        actions = [(D, D), (C, D), (D, D), (D, D), (D, D)]
        self.versus_test(opponent=axl.Defector(), expected_actions=actions)


class TestProber4(TestPlayer):

    name = "Prober 4"
    player = axl.Prober4
    expected_classifier = {
        "stochastic": False,
        "memory_depth": float("inf"),
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }
    initial_sequence = [
        C,
        C,
        D,
        C,
        D,
        D,
        D,
        C,
        C,
        D,
        C,
        D,
        C,
        C,
        D,
        C,
        D,
        D,
        C,
        D,
    ]

    def test_strategy(self):
        # Starts by playing CCDCDDDCCDCDCCDCDDCD.
        # After playing the initial sequence defects forever
        # if the absolute difference in the number of retaliating
        # and provocative defections of the opponent is smaller or equal to 2
        provocative_histories = [
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, D, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, D, C, D, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, D, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, D, C, D, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [D, D, D, D, D, D, D, D, D, D, D, D, D, D, D, D, D, D, D, D],
        ]

        attrs = {"turned_defector": True}
        for history in provocative_histories:
            opponent = axl.MockPlayer(history + [C] * 5)
            actions = list(zip(self.initial_sequence, history)) + [(D, C)] * 5
            self.versus_test(
                opponent=opponent, expected_actions=actions, attrs=attrs
            )

        # Otherwise cooperates for 5 rounds and plays TfT afterwards
        unprovocative_histories = [
            [C, C, D, C, D, D, D, C, C, D, C, D, C, C, D, C, D, D, C, D],
            [D, D, C, D, C, C, C, D, D, C, D, C, D, D, C, D, C, C, D, C],
            [C, C, D, C, D, D, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, D, C, D, D, C, C, D, C, C, C, C, C, C, D, D, D, C, C],
            [C, C, C, C, D, D, C, C, D, C, C, D, D, C, D, C, D, C, C, C],
        ]

        attrs = {"turned_defector": False}
        for history in unprovocative_histories:
            opponent = axl.MockPlayer(history + [D] * 5 + [C, C])
            actions = list(zip(self.initial_sequence, history)) + [(C, D)] * 5
            actions += [(D, C), (C, C)]
            self.versus_test(
                opponent=opponent, expected_actions=actions, attrs=attrs
            )


class TestHardProber(TestPlayer):

    name = "Hard Prober"
    player = axl.HardProber
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # Starts by playing DDCC
        # Defects forever if opponent played C in moves 2 and 3
        actions = [(D, C), (D, C), (C, C), (C, C)] + [(D, C), (D, C), (D, C)]
        self.versus_test(opponent=axl.Cooperator(), expected_actions=actions)

        opponent = axl.MockPlayer([D, C, C, D])
        actions = [(D, D), (D, C), (C, C), (C, D)] + [(D, D), (D, C), (D, C)]
        self.versus_test(opponent=opponent, expected_actions=actions)

        # Otherwise it plays like TFT
        actions = [(D, C), (D, D), (C, C), (C, D)] + [(D, C), (C, D), (D, C)]
        self.versus_test(opponent=axl.Alternator(), expected_actions=actions)

        actions = [(D, D), (D, D), (C, D), (C, D)] + [(D, D), (D, D), (D, D)]
        self.versus_test(opponent=axl.Defector(), expected_actions=actions)


class TestNaiveProber(TestPlayer):

    name = "Naive Prober: 0.1"
    player = axl.NaiveProber
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # Always retaliate a defection
        opponent = axl.MockPlayer([C, D, D, D, D])
        actions = [(C, C), (C, D), (D, D), (D, D), (D, D)]
        self.versus_test(opponent=opponent, expected_actions=actions, seed=1)

    def test_random_defection(self):
        # Unprovoked defection with small probability
        actions = [(C, C), (D, C), (D, C), (C, C), (C, C)]
        self.versus_test(
            opponent=axl.Cooperator(), expected_actions=actions, seed=55
        )

    def test_random_defection2(self):
        actions = [(C, C), (C, C), (C, C), (C, C), (D, C)]
        self.versus_test(
            opponent=axl.Cooperator(), expected_actions=actions, seed=31
        )

    def test_random_defection3(self):
        # Always defect when p is 1
        actions = [(C, C), (D, C), (D, C), (D, C), (D, C)]
        self.versus_test(
            opponent=axl.Cooperator(),
            expected_actions=actions,
            init_kwargs={"p": 1},
        )

    def test_reduction_to_TFT(self):
        actions = [(C, C), (C, D), (D, C), (C, D), (D, C)]
        self.versus_test(
            opponent=axl.Alternator(),
            expected_actions=actions,
            init_kwargs={"p": 0},
        )


class TestRemorsefulProber(TestPlayer):

    name = "Remorseful Prober: 0.1"
    player = axl.RemorsefulProber
    expected_classifier = {
        "memory_depth": 2,
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # Always retaliate a defection
        actions = [(C, D)] + [(D, D)] * 10
        self.versus_test(
            opponent=axl.Defector(),
            expected_actions=actions,
            attrs={"probing": False},
        )

    def test_random_defection(self):
        # Unprovoked defection with small probability
        actions = [(C, C), (D, C), (D, C)]
        self.versus_test(
            opponent=axl.Cooperator(),
            expected_actions=actions,
            seed=55,
            attrs={"probing": True},
        )

    def test_random_defection2(self):
        actions = [(C, C), (C, C), (C, C), (C, C), (D, C)]
        self.versus_test(
            opponent=axl.Cooperator(),
            expected_actions=actions,
            seed=31,
            attrs={"probing": True},
        )

    def test_random_defection3(self):
        # Always defect when p is 1
        actions = [(C, C), (D, C), (D, C), (D, C), (D, C)]
        self.versus_test(
            opponent=axl.Cooperator(),
            expected_actions=actions,
            init_kwargs={"p": 1},
            attrs={"probing": True},
        )

    def test_remorse(self):
        """After probing, if opponent retaliates, will offer a C."""
        opponent = axl.MockPlayer([C, C, D, C])
        actions = [(C, C), (D, C), (D, D), (C, C)]
        self.versus_test(
            opponent=opponent,
            expected_actions=actions,
            seed=55,
            attrs={"probing": False},
        )

    def test_reduction_to_TFT(self):
        actions = [(C, C), (C, D), (D, C), (C, D), (D, C)]
        self.versus_test(
            opponent=axl.Alternator(),
            expected_actions=actions,
            init_kwargs={"p": 0},
            attrs={"probing": False},
        )
