"""Tests for the tit for tat strategies."""

import copy

from hypothesis import given, settings
from hypothesis.strategies import integers

import axelrod as axl
from axelrod.tests.property import strategy_lists

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestTitForTat(TestPlayer):
    """
    Note that this test is referred to in the documentation as an example on
    writing tests.  If you modify the tests here please also modify the
    documentation.
    """

    name = "Tit For Tat"
    player = axl.TitForTat
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": False,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_vs_alternator(self):
        actions = [(C, C), (C, D), (D, C), (C, D), (D, C)]
        self.versus_test(axl.Alternator(), expected_actions=actions)

        # This behaviour is independent of knowledge of the Match length
        actions = [(C, C), (C, D), (D, C), (C, D), (D, C)]
        self.versus_test(
            axl.Alternator(),
            expected_actions=actions,
            match_attributes={"length": float("inf")},
        )

    def test_vs_cooperator(self):
        actions = [(C, C), (C, C), (C, C), (C, C), (C, C)]
        self.versus_test(axl.Cooperator(), expected_actions=actions)

    def test_vs_defector(self):
        actions = [(C, D), (D, D), (D, D), (D, D), (D, D)]
        self.versus_test(axl.Defector(), expected_actions=actions)

    def test_vs_random(self):
        # We can also test against random strategies
        actions = [(C, D), (D, C), (C, C), (C, D), (D, D)]
        self.versus_test(axl.Random(), expected_actions=actions, seed=17)

    def test_vs_random2(self):
        actions = [(C, C), (C, C), (C, C), (C, C)]
        self.versus_test(axl.Random(), expected_actions=actions, seed=3)

    def test_vs_mock_players(self):
        #  If you would like to test against a sequence of moves you should use
        #  a MockPlayer
        opponent = axl.MockPlayer(actions=[C, D])
        actions = [(C, C), (C, D), (D, C), (C, D)]
        self.versus_test(opponent, expected_actions=actions)

        opponent = axl.MockPlayer(actions=[C, C, D, D, C, D])
        actions = [(C, C), (C, C), (C, D), (D, D), (D, C), (C, D)]
        self.versus_test(opponent, expected_actions=actions)


class TestTitFor2Tats(TestPlayer):
    name = "Tit For 2 Tats"
    player = axl.TitFor2Tats
    expected_classifier = {
        "memory_depth": 2,
        "stochastic": False,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # Will punish sequence of 2 defections but will forgive one
        opponent = axl.MockPlayer(actions=[D, D, D, C, C])
        actions = [(C, D), (C, D), (D, D), (D, C), (C, C), (C, D)]
        self.versus_test(opponent, expected_actions=actions)
        opponent = axl.MockPlayer(actions=[C, C, D, D, C, D, D, C, C, D, D])
        actions = [
            (C, C),
            (C, C),
            (C, D),
            (C, D),
            (D, C),
            (C, D),
            (C, D),
            (D, C),
            (C, C),
            (C, D),
            (C, D),
        ]
        self.versus_test(opponent, expected_actions=actions)


class TestTwoTitsForTat(TestPlayer):
    name = "Two Tits For Tat"
    player = axl.TwoTitsForTat
    expected_classifier = {
        "memory_depth": 2,
        "stochastic": False,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # Will defect twice when last turn of opponent was defection.
        opponent = axl.MockPlayer(actions=[D, C, C, D, C])
        actions = [(C, D), (D, C), (D, C), (C, D), (D, C)]
        self.versus_test(opponent, expected_actions=actions)

        actions = [(C, C), (C, C)]
        self.versus_test(opponent=axl.Cooperator(), expected_actions=actions)

        actions = [(C, D), (D, D), (D, D)]
        self.versus_test(opponent=axl.Defector(), expected_actions=actions)


class TestDynamicTwoTitsForTat(TestPlayer):
    name = "Dynamic Two Tits For Tat"
    player = axl.DynamicTwoTitsForTat
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # Test that it is stochastic
        opponent = axl.MockPlayer(actions=[D, C, D, D, C])
        actions = [(C, D), (D, C), (C, D), (D, D), (D, C)]
        self.versus_test(opponent, expected_actions=actions, seed=1)
        # Should respond differently with a different seed
        actions = [(C, D), (D, C), (D, D), (D, D), (D, C)]
        self.versus_test(opponent, expected_actions=actions, seed=2)

        # Will cooperate if opponent cooperates.
        actions = [(C, C), (C, C), (C, C), (C, C), (C, C)]
        self.versus_test(axl.Cooperator(), expected_actions=actions)
        # Test against defector
        actions = [(C, D), (D, D), (D, D), (D, D), (D, D)]
        self.versus_test(axl.Defector(), expected_actions=actions)


class TestBully(TestPlayer):
    name = "Bully"
    player = axl.Bully
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": False,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # Will do opposite of what opponent does.
        actions = [(D, C), (D, D), (C, C), (D, D), (C, C)]
        self.versus_test(axl.Alternator(), expected_actions=actions)

        actions = [(D, C), (D, C), (D, C), (D, C), (D, C)]
        self.versus_test(axl.Cooperator(), expected_actions=actions)

        actions = [(D, D), (C, D), (C, D), (C, D), (C, D)]
        self.versus_test(axl.Defector(), expected_actions=actions)


class TestSneakyTitForTat(TestPlayer):
    name = "Sneaky Tit For Tat"
    player = axl.SneakyTitForTat
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        opponent = axl.MockPlayer(actions=[C, C, C, D, C, C])
        actions = [(C, C), (C, C), (D, C), (D, D), (C, C), (C, C)]
        self.versus_test(opponent, expected_actions=actions)

        # Repents if punished for a defection
        actions = [(C, C), (C, D), (D, C), (C, D), (C, C)]
        self.versus_test(axl.Alternator(), expected_actions=actions)


class TestSuspiciousTitForTat(TestPlayer):
    name = "Suspicious Tit For Tat"
    player = axl.SuspiciousTitForTat
    expected_classifier = {
        "memory_depth": 1,  # Four-Vector = (1.,0.,1.,0.)
        "stochastic": False,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # Plays like TFT after the first move, repeating the opponents last
        # move.
        actions = [(D, C), (C, D)] * 8
        self.versus_test(axl.TitForTat(), expected_actions=actions)

        actions = [(D, C), (C, C), (C, C)]
        self.versus_test(axl.Cooperator(), expected_actions=actions)

        actions = [(D, D), (D, D), (D, D)]
        self.versus_test(axl.Defector(), expected_actions=actions)


class TestAntiTitForTat(TestPlayer):
    name = "Anti Tit For Tat"
    player = axl.AntiTitForTat
    expected_classifier = {
        "memory_depth": 1,  # Four-Vector = (1.,0.,1.,0.)
        "stochastic": False,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (D, C), (D, D), (C, D)] * 4
        self.versus_test(axl.TitForTat(), expected_actions=actions)


class TestHardTitForTat(TestPlayer):
    name = "Hard Tit For Tat"
    player = axl.HardTitForTat
    expected_classifier = {
        "memory_depth": 3,
        "stochastic": False,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        opponent = axl.MockPlayer(actions=[D, C, C, C, D, C])
        actions = [(C, D), (D, C), (D, C), (D, C), (C, D), (D, C)]
        self.versus_test(opponent, expected_actions=actions)

        actions = [(C, C), (C, C), (C, C)]
        self.versus_test(axl.Cooperator(), expected_actions=actions)

        actions = [(C, D), (D, D), (D, D)]
        self.versus_test(axl.Defector(), expected_actions=actions)


class TestHardTitFor2Tats(TestPlayer):
    name = "Hard Tit For 2 Tats"
    player = axl.HardTitFor2Tats
    expected_classifier = {
        "memory_depth": 3,
        "stochastic": False,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # Uses memory 3 to punish 2 consecutive defections
        opponent = axl.MockPlayer(actions=[D, C, C, D, D, D, C])
        actions = [(C, D), (C, C), (C, C), (C, D), (C, D), (D, D), (D, C)]
        self.versus_test(opponent, expected_actions=actions)


class TestOmegaTFT(TestPlayer):
    name = "Omega TFT: 3, 8"
    player = axl.OmegaTFT

    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        player_history = [C, D, C, D, C, C, C, C, C]
        opp_history = [D, C, D, C, D, C, C, C, C]
        actions = list(zip(player_history, opp_history))
        self.versus_test(axl.SuspiciousTitForTat(), expected_actions=actions)

        player_history = [C, C, D, C, D, C, C, C, D, D, D, D, D, D]
        opp_history = [C, D] * 7
        actions = list(zip(player_history, opp_history))
        self.versus_test(axl.Alternator(), expected_actions=actions)


class TestGradual(TestPlayer):
    name = "Gradual"
    player = axl.Gradual
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # Punishes defection with a growing number of defections and calms
        # the opponent with two cooperations in a row.
        opponent = axl.MockPlayer(actions=[C])
        actions = [(C, C)]
        self.versus_test(
            opponent,
            expected_actions=actions,
            attrs={
                "calm_count": 0,
                "punish_count": 0,
            },
        )

        opponent = axl.MockPlayer(actions=[D])
        actions = [(C, D)]
        self.versus_test(
            opponent,
            expected_actions=actions,
            attrs={
                "calm_count": 0,
                "punish_count": 0,
            },
        )

        opponent = axl.MockPlayer(actions=[D, C])
        actions = [(C, D), (D, C)]
        self.versus_test(
            opponent,
            expected_actions=actions,
            attrs={
                "calm_count": 2,
                "punish_count": 0,
            },
        )

        opponent = axl.MockPlayer(actions=[D, C, C])
        actions = [(C, D), (D, C), (C, C)]
        self.versus_test(
            opponent,
            expected_actions=actions,
            attrs={
                "calm_count": 1,
                "punish_count": 0,
            },
        )

        opponent = axl.MockPlayer(actions=[D, C, D, C])
        actions = [(C, D), (D, C), (C, D), (C, C)]
        self.versus_test(
            opponent,
            expected_actions=actions,
            attrs={
                "calm_count": 0,
                "punish_count": 0,
            },
        )

        opponent = axl.MockPlayer(actions=[D, C, D, C, C])
        actions = [(C, D), (D, C), (C, D), (C, C), (C, C)]
        self.versus_test(
            opponent,
            expected_actions=actions,
            attrs={
                "calm_count": 0,
                "punish_count": 0,
            },
        )

        opponent = axl.MockPlayer(actions=[D, C, D, C, C, C])
        actions = [(C, D), (D, C), (C, D), (C, C), (C, C), (C, C)]
        self.versus_test(
            opponent,
            expected_actions=actions,
            attrs={
                "calm_count": 0,
                "punish_count": 0,
            },
        )

        opponent = axl.MockPlayer(actions=[D, C, D, C, C, C, D, C])
        actions = [
            (C, D),
            (D, C),
            (C, D),
            (C, C),
            (C, C),
            (C, C),
            (C, D),
            (D, C),
        ]
        self.versus_test(
            opponent,
            expected_actions=actions,
            attrs={
                "calm_count": 2,
                "punish_count": 2,
            },
        )

        opponent = axl.MockPlayer(actions=[D, C, D, C, C, D, D, D])
        actions = [
            (C, D),
            (D, C),
            (C, D),
            (C, C),
            (C, C),
            (C, D),
            (D, D),
            (D, D),
        ]
        self.versus_test(
            opponent,
            expected_actions=actions,
            attrs={
                "calm_count": 2,
                "punish_count": 1,
            },
        )

        opponent = axl.Defector()
        actions = [
            (C, D),
            (D, D),  # 1 defection as a response to the 1 defection by opponent
            (C, D),
            (C, D),
            (D, D),
            # starts defecting after a total of 4 defections by the opponent
            (D, D),
            (D, D),
            (D, D),  # 4 defections
            (C, D),
            (C, D),
            (D, D),
            # Start defecting after a total of 10 defections by the opponent
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, D),  # 10 defections
            (C, D),
            (C, D),
            (D, D),  # starts defecting after 22 defections by the opponent
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, D),  # 22 defections
            (C, D),
            (C, D),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
        ]
        self.versus_test(
            opponent,
            expected_actions=actions,
            attrs={
                "calm_count": 2,
                "punish_count": 42,
            },
        )

    def test_specific_set_of_results(self):
        """
        This tests specific reported results as discussed in
        https://github.com/Axelrod-Python/Axelrod/issues/1294

        The results there used a version of mistrust with a bug that corresponds
        to a memory one player that start by defecting and only cooperates if
        both players cooperated in the previous round.
        """
        mistrust_with_bug = axl.MemoryOnePlayer(
            initial=D,
            four_vector=(1, 0, 0, 0),
        )
        players = [
            self.player(),
            axl.TitForTat(),
            axl.GoByMajority(),
            axl.Grudger(),
            axl.WinStayLoseShift(),
            axl.Prober(),
            axl.Defector(),
            mistrust_with_bug,
            axl.Cooperator(),
            axl.CyclerCCD(),
            axl.CyclerDDC(),
        ]
        tournament = axl.Tournament(players, turns=1000, repetitions=1, seed=1)
        results = tournament.play(progress_bar=False)
        scores = [
            round(average_score_per_turn * 1000, 1)
            for average_score_per_turn in results.payoff_matrix[0]
        ]
        expected_scores = [
            3000.0,
            3000.0,
            3000.0,
            3000.0,
            3000.0,
            2999.0,
            983.0,
            983.0,
            3000.0,
            3596.0,
            2302.0,
        ]
        self.assertEqual(scores, expected_scores)


class TestOriginalGradual(TestPlayer):
    name = "Original Gradual"
    player = axl.OriginalGradual
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # Punishes defection with a growing number of defections and calms
        # the opponent with two cooperations in a row.
        opponent = axl.MockPlayer(actions=[C])
        actions = [(C, C)]
        self.versus_test(
            opponent,
            expected_actions=actions,
            attrs={
                "calming": False,
                "punishing": False,
                "punishment_count": 0,
                "punishment_limit": 0,
            },
        )

        opponent = axl.MockPlayer(actions=[D])
        actions = [(C, D)]
        self.versus_test(
            opponent,
            expected_actions=actions,
            attrs={
                "calming": False,
                "punishing": False,
                "punishment_count": 0,
                "punishment_limit": 0,
            },
        )

        opponent = axl.MockPlayer(actions=[D, C])
        actions = [(C, D), (D, C)]
        self.versus_test(
            opponent,
            expected_actions=actions,
            attrs={
                "calming": False,
                "punishing": True,
                "punishment_count": 1,
                "punishment_limit": 1,
            },
        )

        opponent = axl.MockPlayer(actions=[D, C, C])
        actions = [(C, D), (D, C), (C, C)]
        self.versus_test(
            opponent,
            expected_actions=actions,
            attrs={
                "calming": True,
                "punishing": False,
                "punishment_count": 0,
                "punishment_limit": 1,
            },
        )

        opponent = axl.MockPlayer(actions=[D, C, D, C])
        actions = [(C, D), (D, C), (C, D), (C, C)]
        self.versus_test(
            opponent,
            expected_actions=actions,
            attrs={
                "calming": False,
                "punishing": False,
                "punishment_count": 0,
                "punishment_limit": 1,
            },
        )

        opponent = axl.MockPlayer(actions=[D, C, D, C, C])
        actions = [(C, D), (D, C), (C, D), (C, C), (C, C)]
        self.versus_test(
            opponent,
            expected_actions=actions,
            attrs={
                "calming": False,
                "punishing": False,
                "punishment_count": 0,
                "punishment_limit": 1,
            },
        )

        opponent = axl.MockPlayer(actions=[D, C, D, C, C, C])
        actions = [(C, D), (D, C), (C, D), (C, C), (C, C), (C, C)]
        self.versus_test(
            opponent,
            expected_actions=actions,
            attrs={
                "calming": False,
                "punishing": False,
                "punishment_count": 0,
                "punishment_limit": 1,
            },
        )

        opponent = axl.MockPlayer(actions=[D, C, D, C, C, C, D, C])
        actions = [
            (C, D),
            (D, C),
            (C, D),
            (C, C),
            (C, C),
            (C, C),
            (C, D),
            (D, C),
        ]
        self.versus_test(
            opponent,
            expected_actions=actions,
            attrs={
                "calming": False,
                "punishing": True,
                "punishment_count": 1,
                "punishment_limit": 2,
            },
        )

        opponent = axl.MockPlayer(actions=[D, C, D, C, C, D, D, D])
        actions = [
            (C, D),
            (D, C),
            (C, D),
            (C, C),
            (C, C),
            (C, D),
            (D, D),
            (D, D),
        ]
        self.versus_test(
            opponent,
            expected_actions=actions,
            attrs={
                "calming": False,
                "punishing": True,
                "punishment_count": 2,
                "punishment_limit": 2,
            },
        )

    def test_output_from_literature(self):
        """
        This strategy is not fully described in the literature, however the
        scores for the strategy against a set of opponents is reported

        Bruno Beaufils, Jean-Paul Delahaye, Philippe Mathie
        "Our Meeting With Gradual: A Good Strategy For The Iterated Prisoner's
        Dilemma" Proc. Artif. Life 1996

        This test just ensures that the strategy is as was originally defined.

        See https://github.com/Axelrod-Python/Axelrod/issues/1294 for another
        discussion of this.
        """
        players = [
            axl.Cooperator(),
            axl.Defector(),
            axl.Random(),
            axl.TitForTat(),
            axl.Grudger(),
            axl.CyclerDDC(),
            axl.CyclerCCD(),
            axl.GoByMajority(),
            axl.SuspiciousTitForTat(),
            axl.Prober(),
            self.player(),
            axl.WinStayLoseShift(),
        ]

        turns = 1000
        tournament = axl.Tournament(
            players, turns=turns, repetitions=1, seed=75
        )
        results = tournament.play(progress_bar=False)
        scores = [
            round(average_score_per_turn * 1000, 1)
            for average_score_per_turn in results.payoff_matrix[-2]
        ]
        expected_scores = [
            3000.0,
            915.0,
            2763.0,
            3000.0,
            3000.0,
            2219.0,
            3472.0,
            3000.0,
            2996.0,
            2999.0,
            3000.0,
            3000.0,
        ]
        self.assertEqual(scores, expected_scores)


class TestContriteTitForTat(TestPlayer):
    name = "Contrite Tit For Tat"
    player = axl.ContriteTitForTat
    expected_classifier = {
        "memory_depth": 3,
        "stochastic": False,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    deterministic_strategies = [
        s for s in axl.strategies if not axl.Classifiers["stochastic"](s())
    ]

    def test_init(self):
        player = self.player()
        self.assertFalse(player.contrite, False)
        self.assertEqual(player._recorded_history, [])

    @given(
        strategies=strategy_lists(
            strategies=deterministic_strategies, max_size=1
        ),
        turns=integers(min_value=1, max_value=20),
    )
    @settings(deadline=None)
    def test_is_tit_for_tat_with_no_noise(self, strategies, turns):
        tft = axl.TitForTat()
        player = self.player()
        opponent = strategies[0]()
        m1 = axl.Match((tft, opponent), turns)
        m2 = axl.Match((player, opponent), turns)
        self.assertEqual(m1.play(), m2.play())

    def test_strategy_with_noise1(self):
        self.versus_test(
            axl.Defector(),
            [(C, D)],
            turns=1,
            seed=9,
            attrs={"_recorded_history": [C]},
        )

    def test_strategy_with_noise2(self):
        self.versus_test(
            axl.Defector(),
            [(D, C)],
            turns=1,
            noise=0.5,
            seed=11,
            attrs={"_recorded_history": [C]},
        )

    def test_strategy_with_noise3(self):
        # After noise: is contrite
        actions = list(zip([D, C], [C, D]))
        self.versus_test(
            axl.Defector(),
            actions,
            turns=2,
            noise=0.5,
            seed=49,
            attrs={"_recorded_history": [C, C], "contrite": True},
        )

    def test_strategy_with_noise4(self):
        # Cooperates and no longer contrite
        actions = list(zip([D, C, C], [C, D, D]))
        self.versus_test(
            axl.Defector(),
            actions,
            turns=3,
            noise=0.5,
            seed=49,
            attrs={"_recorded_history": [C, C, C], "contrite": False},
        )

    def test_strategy_with_noise5(self):
        # Defects and no longer contrite
        actions = list(zip([D, C, C, D], [C, D, D, D]))
        self.versus_test(
            axl.Defector(),
            actions,
            turns=4,
            noise=0.5,
            seed=158,
            attrs={"_recorded_history": [C, C, C, D], "contrite": False},
        )


class TestAdaptiveTitForTat(TestPlayer):
    name = "Adaptive Tit For Tat: 0.5"
    player = axl.AdaptiveTitForTat
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (C, D), (D, C), (C, D), (D, C)]
        self.versus_test(
            axl.Alternator(),
            expected_actions=actions,
            attrs={"world": 0.34375, "rate": 0.5},
        )


class TestSpitefulTitForTat(TestPlayer):
    name = "Spiteful Tit For Tat"
    player = axl.SpitefulTitForTat
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # Repeats last action of opponent history until 2 consecutive
        # defections, then always defects
        opponent = axl.MockPlayer(actions=[C, C, C, C])
        actions = [(C, C)] * 5
        self.versus_test(
            opponent, expected_actions=actions, attrs={"retaliating": False}
        )

        opponent = axl.MockPlayer(actions=[C, C, C, C, D, C])
        actions = [(C, C)] * 4 + [(C, D), (D, C), (C, C)]
        self.versus_test(
            opponent, expected_actions=actions, attrs={"retaliating": False}
        )

        opponent = axl.MockPlayer(actions=[C, C, D, D, C])
        actions = [(C, C), (C, C), (C, D), (D, D), (D, C)]
        self.versus_test(
            opponent, expected_actions=actions, attrs={"retaliating": True}
        )


class TestSlowTitForTwoTats2(TestPlayer):
    name = "Slow Tit For Two Tats 2"
    player = axl.SlowTitForTwoTats2
    expected_classifier = {
        "memory_depth": 2,
        "stochastic": False,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # If opponent plays the same move twice, repeats last action of
        # opponent history, otherwise repeats previous move.
        opponent = axl.MockPlayer(actions=[C, C, D, D, C, D, D, C, C, D, D])
        actions = [
            (C, C),
            (C, C),
            (C, D),
            (C, D),
            (D, C),
            (D, D),
            (D, D),
            (D, C),
            (D, C),
            (C, D),
            (C, D),
        ]
        self.versus_test(opponent, expected_actions=actions)


class TestAlexei(TestPlayer):
    """
    Tests for the Alexei strategy
    """

    name = "Alexei: (D,)"
    player = axl.Alexei
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": {"length"},
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (C, C), (C, C), (C, C), (D, C)]
        self.versus_test(axl.Cooperator(), expected_actions=actions)

        actions = [(C, D), (D, D), (D, D), (D, D), (D, D)]
        self.versus_test(axl.Defector(), expected_actions=actions)

        actions = [(C, C), (C, D), (D, C), (C, D), (D, C), (C, D)]
        self.versus_test(
            axl.Alternator(),
            expected_actions=actions,
            match_attributes={"length": float("inf")},
        )

        actions = [(C, C), (C, D), (D, C), (C, D), (D, C), (D, D)]
        self.versus_test(axl.Alternator(), expected_actions=actions)

        opponent = axl.MockPlayer(actions=[C, C, D, D, C, D])
        actions = [(C, C), (C, C), (C, D), (D, D), (D, C), (D, D)]
        self.versus_test(opponent, expected_actions=actions)


class TestEugineNier(TestPlayer):
    """
    Tests for the Eugine Nier strategy
    """

    name = "EugineNier: (D,)"
    player = axl.EugineNier
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": {"length"},
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (C, C), (C, C), (D, C)]
        self.versus_test(
            axl.Cooperator(),
            expected_actions=actions,
            attrs={"is_defector": False},
        )

        actions = [(C, C), (C, C), (C, C), (C, C)]
        self.versus_test(
            axl.Cooperator(),
            expected_actions=actions,
            attrs={"is_defector": False},
            match_attributes={"length": float("inf")},
        )

        # Plays TfT and defects in last round
        actions = [(C, C), (C, D), (D, C), (C, D), (D, C), (D, D)]
        self.versus_test(
            axl.Alternator(),
            expected_actions=actions,
            attrs={"is_defector": False},
        )

        actions = [(C, C), (C, D), (D, C), (C, D), (D, C), (C, D)]
        self.versus_test(
            axl.Alternator(),
            expected_actions=actions,
            attrs={"is_defector": False},
            match_attributes={"length": float("inf")},
        )

        # Becomes defector after 5 defections
        opponent = axl.MockPlayer(actions=[D, C, D, D, D, D, C, C])
        actions = [
            (C, D),
            (D, C),
            (C, D),
            (D, D),
            (D, D),
            (D, D),
            (D, C),
            (D, C),
        ]
        self.versus_test(opponent, expected_actions=actions)


class TestNTitsForMTats(TestPlayer):
    """
    Tests for the N Tit(s) For M Tat(s) strategy
    """

    name = "N Tit(s) For M Tat(s): 3, 2"
    player = axl.NTitsForMTats
    expected_classifier = {
        "memory_depth": 3,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    expected_class_classifier = copy.copy(expected_classifier)

    def test_strategy(self):
        # TitFor2Tats test_strategy
        init_kwargs = {"N": 1, "M": 2}
        opponent = axl.MockPlayer(actions=[D, D, D, C, C])
        actions = [(C, D), (C, D), (D, D), (D, C), (C, C), (C, D)]
        self.versus_test(
            opponent, expected_actions=actions, init_kwargs=init_kwargs
        )

        # TwoTitsForTat test_strategy
        init_kwargs = {"N": 2, "M": 1}
        opponent = axl.MockPlayer(actions=[D, C, C, D, C])
        actions = [(C, D), (D, C), (D, C), (C, D), (D, C)]
        self.versus_test(
            opponent, expected_actions=actions, init_kwargs=init_kwargs
        )
        actions = [(C, C), (C, C)]
        self.versus_test(
            opponent=axl.Cooperator(),
            expected_actions=actions,
            init_kwargs=init_kwargs,
        )
        actions = [(C, D), (D, D), (D, D)]
        self.versus_test(
            opponent=axl.Defector(),
            expected_actions=actions,
            init_kwargs=init_kwargs,
        )

        # Cooperator test_strategy
        actions = [(C, C)] + [(C, D), (C, C)] * 9
        self.versus_test(
            opponent=axl.Alternator(),
            expected_actions=actions,
            init_kwargs={"N": 0, "M": 1},
        )
        self.versus_test(
            opponent=axl.Alternator(),
            expected_actions=actions,
            init_kwargs={"N": 0, "M": 5},
        )
        self.versus_test(
            opponent=axl.Alternator(),
            expected_actions=actions,
            init_kwargs={"N": 0, "M": 0},
        )

        # Defector test_strategy
        actions = [(D, C)] + [(D, D), (D, C)] * 9
        self.versus_test(
            opponent=axl.Alternator(),
            expected_actions=actions,
            init_kwargs={"N": 1, "M": 0},
        )
        self.versus_test(
            opponent=axl.Alternator(),
            expected_actions=actions,
            init_kwargs={"N": 5, "M": 0},
        )

        # Default init args
        actions = [(C, C), (C, D), (C, D), (D, C), (D, C), (D, D), (C, C)]
        opponent = axl.MockPlayer(actions=[acts[1] for acts in actions])
        self.versus_test(opponent=opponent, expected_actions=actions)

    def test_varying_memory_depth(self):
        self.assertEqual(axl.Classifiers["memory_depth"](self.player(1, 1)), 1)
        self.assertEqual(axl.Classifiers["memory_depth"](self.player(0, 3)), 3)
        self.assertEqual(axl.Classifiers["memory_depth"](self.player(5, 3)), 5)


class Test1TitsFor1TatsIsTFT(TestTitForTat):
    """Tests that for N = 1 = M, all the TFT tests are passed."""

    name = "N Tit(s) For M Tat(s): 1, 1"
    player = lambda x: axl.NTitsForMTats(1, 1)
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }


class Test1TitsFor2TatsIsTF2T(TestTitFor2Tats):
    """Tests that for N = 1,  M = 2, all the TF2T tests are passed."""

    name = "N Tit(s) For M Tat(s): 1, 2"
    player = lambda x: axl.NTitsForMTats(1, 2)
    expected_classifier = {
        "memory_depth": 2,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }


class Test2TitsFor1TatsIs2TFT(TestTwoTitsForTat):
    """Tests that for N = 2,  M = 1, all the 2TFT tests are passed."""

    name = "N Tit(s) For M Tat(s): 2, 1"
    player = lambda x: axl.NTitsForMTats(2, 1)
    expected_classifier = {
        "memory_depth": 2,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestMichaelos(TestPlayer):
    """
    Tests for the Michaelos strategy
    """

    name = "Michaelos: (D,)"
    player = axl.Michaelos
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "makes_use_of": {"length"},
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (C, C), (C, C), (D, C)]
        self.versus_test(
            axl.Cooperator(),
            expected_actions=actions,
            attrs={"is_defector": False},
            seed=1,
        )

        actions = [(C, C), (C, C), (C, C), (C, C)]
        self.versus_test(
            axl.Cooperator(),
            expected_actions=actions,
            attrs={"is_defector": False},
            match_attributes={"length": float("inf")},
            seed=1,
        )

        actions = [(C, D), (D, D), (D, D), (D, D)]
        self.versus_test(
            axl.Defector(),
            expected_actions=actions,
            attrs={"is_defector": False},
            seed=1,
        )

        actions = [(C, D), (D, D), (D, D), (D, D)]
        self.versus_test(
            axl.Defector(),
            expected_actions=actions,
            attrs={"is_defector": False},
            match_attributes={"length": float("inf")},
            seed=1,
        )

        # Chance of becoming a defector is 50% after (D, C) occurs.
        actions = [(C, C), (C, D), (D, C), (C, D), (D, C)]
        self.versus_test(
            axl.Alternator(),
            expected_actions=actions,
            attrs={"is_defector": False},
            seed=1,
        )

        actions = [(C, C), (C, D), (D, C), (D, D), (D, C), (D, D), (D, C)]
        self.versus_test(
            axl.Alternator(),
            expected_actions=actions,
            attrs={"is_defector": True},
            seed=2,
        )

        actions = [(C, C), (C, D), (D, C), (C, D), (D, C), (D, D), (D, C)]
        self.versus_test(
            axl.Alternator(),
            expected_actions=actions,
            attrs={"is_defector": True},
            match_attributes={"length": float("inf")},
            seed=1,
        )


class TestRandomTitForTat(TestPlayer):
    """Tests for random tit for tat strategy."""

    name = "Random Tit for Tat: 0.5"
    player = axl.RandomTitForTat
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
        """
        Test that strategy reacts to opponent, and controlled by
        probability every other iteration.  Also reacts randomly if no
        probability input.
        """
        actions = [(C, C), (C, C), (C, C)]
        self.versus_test(
            axl.Cooperator(), expected_actions=actions, init_kwargs={"p": 1}
        )

        actions = [(C, D), (D, D), (D, D)]
        self.versus_test(
            axl.Defector(), expected_actions=actions, init_kwargs={"p": 0}
        )

        actions = [(C, C), (C, C), (D, C), (C, C)]
        self.versus_test(
            axl.Cooperator(), expected_actions=actions, init_kwargs={"p": 0}
        )

        actions = [(C, D), (D, D), (C, D), (D, D)]
        self.versus_test(
            axl.Defector(), expected_actions=actions, init_kwargs={"p": 1}
        )

        actions = [(C, C), (C, C), (D, C), (C, C), (C, C), (C, C)]
        self.versus_test(axl.Cooperator(), expected_actions=actions, seed=2)

        actions = [(C, D), (D, D), (C, D), (D, D), (D, D), (D, D)]
        self.versus_test(axl.Defector(), expected_actions=actions, seed=1)

    def test_deterministic_classification(self):
        """
        Test classification when probability input is 0 or 1.
        Should change stochastic to false, because actions are no
        longer random.

        """
        for p in [0, 1]:
            player = axl.RandomTitForTat(p=p)
            self.assertFalse(axl.Classifiers["stochastic"](player))


class TestBurnBothEnds(TestPlayer):
    name = "Burn Both Ends"
    player = axl.BurnBothEnds
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": True,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_vs_cooperator(self):
        actions = [(C, C), (C, C), (C, C), (D, C), (C, C)]
        self.versus_test(axl.Cooperator(), expected_actions=actions, seed=1)

    def test_vs_cooperator2(self):
        actions = [(C, C), (C, C), (C, C), (C, C), (C, C)]
        self.versus_test(axl.Cooperator(), expected_actions=actions, seed=2)

    def test_vs_defector(self):
        actions = [(C, D), (D, D), (D, D), (D, D), (D, D)]
        self.versus_test(axl.Defector(), expected_actions=actions)
