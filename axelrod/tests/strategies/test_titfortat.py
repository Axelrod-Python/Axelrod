"""Tests for the tit for tat strategies."""

import random

import copy
from hypothesis import given
from hypothesis.strategies import integers
import axelrod
from axelrod.tests.property import strategy_lists
from .test_player import TestMatch, TestPlayer


C, D = axelrod.Action.C, axelrod.Action.D


class TestTitForTat(TestPlayer):
    """
    Note that this test is referred to in the documentation as an example on
    writing tests.  If you modify the tests here please also modify the
    documentation.
    """

    name = "Tit For Tat"
    player = axelrod.TitForTat
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Play against opponents
        actions = [(C, C), (C, D), (D, C), (C, D), (D, C)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions)

        actions = [(C, C), (C, C), (C, C), (C, C), (C, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        actions = [(C, D), (D, D), (D, D), (D, D), (D, D)]
        self.versus_test(axelrod.Defector(), expected_actions=actions)

        # This behaviour is independent of knowledge of the Match length
        actions = [(C, C), (C, D), (D, C), (C, D), (D, C)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions,
                         match_attributes={"length": -1})

        # We can also test against random strategies
        actions = [(C, D), (D, D), (D, C), (C, C), (C, D)]
        self.versus_test(axelrod.Random(), expected_actions=actions,
                         seed=0)

        actions = [(C, C), (C, D), (D, D), (D, C)]
        self.versus_test(axelrod.Random(), expected_actions=actions,
                         seed=1)

        #  If you would like to test against a sequence of moves you should use
        #  a MockPlayer
        opponent = axelrod.MockPlayer(actions=[C, D])
        actions = [(C, C), (C, D), (D, C), (C, D)]
        self.versus_test(opponent, expected_actions=actions)

        opponent = axelrod.MockPlayer(actions=[C, C, D, D, C, D])
        actions = [(C, C), (C, C), (C, D), (D, D), (D, C), (C, D)]
        self.versus_test(opponent, expected_actions=actions)


class TestTitFor2Tats(TestPlayer):

    name = 'Tit For 2 Tats'
    player = axelrod.TitFor2Tats
    expected_classifier = {
        'memory_depth': 2,
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Will punish sequence of 2 defections but will forgive
        opponent = axelrod.MockPlayer(actions=[D, D, D, C, C])
        actions = [(C, D), (C, D), (D, D), (D, C), (C, C), (C, D)]
        self.versus_test(opponent, expected_actions=actions)


class TestTwoTitsForTat(TestPlayer):

    name = 'Two Tits For Tat'
    player = axelrod.TwoTitsForTat
    expected_classifier = {
        'memory_depth': 2,
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Will defect twice when last turn of opponent was defection.
        opponent = axelrod.MockPlayer(actions=[D, C, C, D, C])
        actions = [(C, D), (D, C), (D, C), (C, D), (D, C)]
        self.versus_test(opponent, expected_actions=actions)

        actions = [(C, C), (C, C)]
        self.versus_test(opponent=axelrod.Cooperator(),
                         expected_actions=actions)

        actions = [(C, D), (D, D), (D, D)]
        self.versus_test(opponent=axelrod.Defector(),
                         expected_actions=actions)


class TestDynamicTwoTitsForTat(TestPlayer):

    name = 'Dynamic Two Tits For Tat'
    player = axelrod.DynamicTwoTitsForTat
    expected_classifier = {
        'memory_depth': 2,
        'stochastic': True,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Test that it is stochastic
        opponent = axelrod.MockPlayer(actions=[D, C, D, D, C])
        actions = [(C, D), (D, C), (C, D), (D, D), (D, C)]
        self.versus_test(opponent, expected_actions=actions, seed=1)
        # Should respond differently with a different seed
        actions = [(C, D), (D, C), (D, D), (D, D), (C, C)]
        self.versus_test(opponent, expected_actions=actions, seed=2)

        # Will cooperate if opponent cooperates.
        actions = [(C, C), (C, C), (C, C), (C, C), (C, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)
        # Test against defector
        actions = [(C, D), (D, D), (D, D), (D, D), (D, D)]
        self.versus_test(axelrod.Defector(), expected_actions=actions)

class TestBully(TestPlayer):

    name = "Bully"
    player = axelrod.Bully
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Will do opposite of what opponent does.
        actions = [(D, C), (D, D), (C, C), (D, D), (C, C)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions)

        actions = [(D, C), (D, C), (D, C), (D, C), (D, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        actions = [(D, D), (C, D), (C, D), (C, D), (C, D)]
        self.versus_test(axelrod.Defector(), expected_actions=actions)


class TestSneakyTitForTat(TestPlayer):

    name = "Sneaky Tit For Tat"
    player = axelrod.SneakyTitForTat
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        opponent = axelrod.MockPlayer(actions=[C, C, C, D, C, C])
        actions = [(C, C), (C, C), (D, C), (D, D), (C, C), (C, C)]
        self.versus_test(opponent, expected_actions=actions)

        # Repents if punished for a defection
        actions = [(C, C), (C, D), (D, C), (C, D), (C, C)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions)


class TestSuspiciousTitForTat(TestPlayer):

    name = 'Suspicious Tit For Tat'
    player = axelrod.SuspiciousTitForTat
    expected_classifier = {
        'memory_depth': 1,  # Four-Vector = (1.,0.,1.,0.)
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Plays like TFT after the first move, repeating the opponents last
        # move.
        actions = [(D, C), (C, D)] * 8
        self.versus_test(axelrod.TitForTat(), expected_actions=actions)

        actions = [(D, C), (C, C), (C, C)]
        self.versus_test(axelrod.Cooperator(),
                         expected_actions=actions)

        actions = [(D, D), (D, D), (D, D)]
        self.versus_test(axelrod.Defector(), expected_actions=actions)


class TestAntiTitForTat(TestPlayer):

    name = 'Anti Tit For Tat'
    player = axelrod.AntiTitForTat
    expected_classifier = {
        'memory_depth': 1,  # Four-Vector = (1.,0.,1.,0.)
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        actions = [(C, C), (D, C), (D, D), (C, D)] * 4
        self.versus_test(axelrod.TitForTat(), expected_actions=actions)


class TestHardTitForTat(TestPlayer):

    name = "Hard Tit For Tat"
    player = axelrod.HardTitForTat
    expected_classifier = {
        'memory_depth': 3,
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        opponent = axelrod.MockPlayer(actions=[D, C, C, C, D, C])
        actions = [(C, D), (D, C), (D, C), (D, C), (C, D), (D, C)]
        self.versus_test(opponent, expected_actions=actions)

        actions = [(C, C), (C, C), (C, C)]
        self.versus_test(axelrod.Cooperator(),
                         expected_actions=actions)

        actions = [(C, D), (D, D), (D, D)]
        self.versus_test(axelrod.Defector(), expected_actions=actions)


class TestHardTitFor2Tats(TestPlayer):

    name = "Hard Tit For 2 Tats"
    player = axelrod.HardTitFor2Tats
    expected_classifier = {
        'memory_depth': 3,
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Uses memory 3 to punish 2 consecutive defections
        opponent = axelrod.MockPlayer(actions=[D, C, C, D, D, D, C])
        actions = [(C, D), (C, C), (C, C), (C, D), (C, D), (D, D), (D, C)]
        self.versus_test(opponent, expected_actions=actions)


class TestOmegaTFT(TestPlayer):

    name = "Omega TFT: 3, 8"
    player = axelrod.OmegaTFT

    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        player_history =  [C, D, C, D, C, C, C, C, C]
        opp_history = [D, C, D, C, D, C, C, C, C]
        actions = list(zip(player_history, opp_history))
        self.versus_test(axelrod.SuspiciousTitForTat(),
                         expected_actions=actions)

        player_history = [C, C, D, C, D, C, C, C, D, D, D, D, D, D]
        opp_history = [C, D] * 7
        actions = list(zip(player_history, opp_history))
        self.versus_test(axelrod.Alternator(), expected_actions=actions)


class TestGradual(TestPlayer):

    name = 'Gradual'
    player = axelrod.Gradual
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Punishes defection with a growing number of defections and calms
        # the opponent with two cooperations in a row.
        opponent = axelrod.MockPlayer(actions=[C])
        actions = [(C, C)]
        self.versus_test(opponent, expected_actions=actions,
                         attrs={"calming": False, "punishing": False,
                                "punishment_count": 0, "punishment_limit": 0})

        opponent = axelrod.MockPlayer(actions=[D])
        actions = [(C, D)]
        self.versus_test(opponent, expected_actions=actions,
                         attrs={"calming": False, "punishing": False,
                                "punishment_count": 0, "punishment_limit": 0})

        opponent = axelrod.MockPlayer(actions=[D, C])
        actions = [(C, D), (D, C)]
        self.versus_test(opponent, expected_actions=actions,
                         attrs={"calming": False, "punishing": True,
                                "punishment_count": 1, "punishment_limit": 1})

        opponent = axelrod.MockPlayer(actions=[D, C, C])
        actions = [(C, D), (D, C), (C, C)]
        self.versus_test(opponent, expected_actions=actions,
                         attrs={"calming": True, "punishing": False,
                                "punishment_count": 0, "punishment_limit": 1})

        opponent = axelrod.MockPlayer(actions=[D, C, D, C])
        actions = [(C, D), (D, C), (C, D), (C, C)]
        self.versus_test(opponent, expected_actions=actions,
                         attrs={"calming": False, "punishing": False,
                                "punishment_count": 0, "punishment_limit": 1})

        opponent = axelrod.MockPlayer(actions=[D, C, D, C, C])
        actions = [(C, D), (D, C), (C, D), (C, C), (C, C)]
        self.versus_test(opponent, expected_actions=actions,
                         attrs={"calming": False, "punishing": False,
                                "punishment_count": 0, "punishment_limit": 1})

        opponent = axelrod.MockPlayer(actions=[D, C, D, C, C, C])
        actions = [(C, D), (D, C), (C, D), (C, C), (C, C), (C, C)]
        self.versus_test(opponent, expected_actions=actions,
                         attrs={"calming": False, "punishing": False,
                                "punishment_count": 0, "punishment_limit": 1})

        opponent = axelrod.MockPlayer(actions=[D, C, D, C, C, C, D, C])
        actions = [(C, D), (D, C), (C, D), (C, C),
                    (C, C), (C, C), (C, D), (D, C)]
        self.versus_test(opponent, expected_actions=actions,
                         attrs={"calming": False, "punishing": True,
                                "punishment_count": 1, "punishment_limit": 2})

        opponent = axelrod.MockPlayer(actions=[D, C, D, C, C, D, D, D])
        actions = [(C, D), (D, C), (C, D), (C, C),
                    (C, C), (C, D), (D, D), (D, D)]
        self.versus_test(opponent, expected_actions=actions,
                         attrs={"calming": False, "punishing": True,
                                "punishment_count": 2, "punishment_limit": 2})


    def test_output_from_literature(self):
        """
        This strategy is not fully described in the literature, however the
        following two results are reported in:

        Bruno Beaufils, Jean-Paul Delahaye, Philippe Mathie
        "Our Meeting With Gradual: A Good Strategy For The Iterated Prisoner's
        Dilemma" Proc. Artif. Life 1996

        This test just ensures that the strategy is as was originally defined.
        """
        player = self.player()

        opp1 = axelrod.Defector()
        match = axelrod.Match((player, opp1), 1000)
        match.play()
        self.assertEqual(match.final_score(), (915, 1340))

        opp2 = axelrod.CyclerCCD()
        match = axelrod.Match((player, opp2), 1000)
        match.play()
        self.assertEqual(match.final_score(), (3472, 767))


class TestContriteTitForTat(TestPlayer):

    name = "Contrite Tit For Tat"
    player = axelrod.ContriteTitForTat
    expected_classifier = {
        'memory_depth': 3,
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    deterministic_strategies = [s for s in axelrod.strategies
                                if not s().classifier['stochastic']]

    def test_init(self):
        ctft = self.player()
        self.assertFalse(ctft.contrite, False)
        self.assertEqual(ctft._recorded_history, [])

    @given(strategies=strategy_lists(strategies=deterministic_strategies,
                                     max_size=1),
           turns=integers(min_value=1, max_value=20))
    def test_is_tit_for_tat_with_no_noise(self, strategies, turns):
        tft = axelrod.TitForTat()
        ctft = self.player()
        opponent = strategies[0]()
        m1 = axelrod.Match((tft, opponent), turns)
        m2 = axelrod.Match((ctft, opponent), turns)
        self.assertEqual(m1.play(), m2.play())

    def test_strategy_with_noise(self):
        ctft = self.player()
        opponent = axelrod.Defector()
        self.assertEqual(ctft.strategy(opponent), C)
        self.assertEqual(ctft._recorded_history, [C])
        ctft.reset()  # Clear the recorded history
        self.assertEqual(ctft._recorded_history, [])

        random.seed(0)
        ctft.play(opponent, noise=.9)
        self.assertEqual(ctft.history, [D])
        self.assertEqual(ctft._recorded_history, [C])
        self.assertEqual(opponent.history, [C])

        # After noise: is contrite
        ctft.play(opponent)
        self.assertEqual(ctft.history, [D, C])
        self.assertEqual(ctft._recorded_history, [C, C])
        self.assertEqual(opponent.history, [C, D])
        self.assertTrue(ctft.contrite)

        # Cooperates and no longer contrite
        ctft.play(opponent)
        self.assertEqual(ctft.history, [D, C, C])
        self.assertEqual(ctft._recorded_history, [C, C, C])
        self.assertEqual(opponent.history, [C, D, D])
        self.assertFalse(ctft.contrite)

        # Goes back to playing tft
        ctft.play(opponent)
        self.assertEqual(ctft.history, [D, C, C, D])
        self.assertEqual(ctft._recorded_history, [C, C, C, D])
        self.assertEqual(opponent.history, [C, D, D, D])
        self.assertFalse(ctft.contrite)


class TestSlowTitForTwoTats(TestPlayer):

    name = "Slow Tit For Two Tats"
    player = axelrod.SlowTitForTwoTats
    expected_classifier = {
        'memory_depth': 2,
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # If opponent plays the same move twice, repeats last action of
        # opponent history.
        opponent = axelrod.MockPlayer(actions=[C, C, D, D, C, D, D, C, C, D, D])
        actions = [(C, C), (C, C), (C, D), (C, D), (D, C), (C, D), (C, D),
                    (D, C), (C, C), (C, D), (C, D)]
        self.versus_test(opponent, expected_actions=actions)


class TestAdaptiveTitForTat(TestPlayer):

    name = "Adaptive Tit For Tat: 0.5"
    player = axelrod.AdaptiveTitForTat
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        actions = [(C, C), (C, D), (D, C), (C, D), (D, C)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions,
                         attrs={"world":0.34375, "rate":0.5})


class TestSpitefulTitForTat(TestPlayer):
    name = "Spiteful Tit For Tat"
    player = axelrod.SpitefulTitForTat
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Repeats last action of opponent history until 2 consecutive
        # defections, then always defects
        opponent = axelrod.MockPlayer(actions=[C, C, C, C])
        actions = [(C, C)] * 5
        self.versus_test(opponent, expected_actions=actions,
                         attrs={"retaliating": False})

        opponent = axelrod.MockPlayer(actions=[C, C, C, C, D, C])
        actions = [(C, C)] * 4 + [(C, D), (D, C), (C, C)]
        self.versus_test(opponent, expected_actions=actions,
                         attrs={"retaliating": False})

        opponent = axelrod.MockPlayer(actions=[C, C, D, D, C])
        actions = [(C, C), (C, C), (C, D), (D, D), (D, C)]
        self.versus_test(opponent, expected_actions=actions,
                         attrs={"retaliating": True})


class TestSlowTitForTwoTats2(TestPlayer):

    name = "Slow Tit For Two Tats 2"
    player = axelrod.SlowTitForTwoTats2
    expected_classifier = {
        'memory_depth': 2,
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # If opponent plays the same move twice, repeats last action of
        # opponent history, otherwise repeats previous move.
        opponent = axelrod.MockPlayer(actions=[C, C, D, D, C, D, D, C, C, D, D])
        actions = [(C, C), (C, C), (C, D), (C, D), (D, C), (D, D), (D, D),
                    (D, C), (D, C), (C, D), (C, D)]
        self.versus_test(opponent, expected_actions=actions)

class TestAlexei(TestPlayer):
    """
    Tests for the Alexei strategy
    """

    name = "Alexei: (D,)"
    player = axelrod.Alexei
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': {'length'},
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        actions = [(C, C), (C, C), (C, C), (C, C), (D, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        actions = [(C, D), (D, D), (D, D), (D, D), (D, D)]
        self.versus_test(axelrod.Defector(), expected_actions=actions)

        actions = [(C, C), (C, D), (D, C), (C, D), (D, C), (C, D)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions,
                         match_attributes={"length": -1})

        actions = [(C, C), (C, D), (D, C), (C, D), (D, C), (D, D)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions)

        opponent = axelrod.MockPlayer(actions=[C, C, D, D, C, D])
        actions = [(C, C), (C, C), (C, D), (D, D), (D, C), (D, D)]
        self.versus_test(opponent, expected_actions=actions)

class TestEugineNier(TestPlayer):
    """
    Tests for the Eugine Nier strategy
    """

    name = "EugineNier: (D,)"
    player = axelrod.EugineNier
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': {'length'},
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        actions = [(C, C), (C, C), (C, C), (D, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions,
                         attrs={"is_defector": False})

        actions = [(C, C), (C, C), (C, C), (C, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions,
                         attrs={"is_defector": False},
                         match_attributes={"length": -1})


        # Plays TfT and defects in last round
        actions = [(C, C), (C, D), (D, C), (C, D), (D, C), (D, D)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions,
                         attrs={"is_defector": False})

        actions = [(C, C), (C, D), (D, C), (C, D), (D, C), (C, D)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions,
                         attrs={"is_defector": False},
                         match_attributes={"length": -1})

        # Becomes defector after 5 defections
        opponent = axelrod.MockPlayer(actions=[D, C, D, D, D, D, C, C])
        actions = [(C, D), (D, C), (C, D), (D, D),
                   (D, D), (D, D), (D, C), (D, C)]
        self.versus_test(opponent, expected_actions=actions)



class TestNTitsForMTats(TestPlayer):
    """
    Tests for the N Tit(s) For M Tat(s) strategy
    """

    name = 'N Tit(s) For M Tat(s): 1, 1'
    player = axelrod.NTitsForMTats
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    expected_class_classifier = copy.copy(expected_classifier)
    expected_class_classifier['memory_depth'] = float('inf')

    def test_strategy(self):
        TestTitForTat.test_strategy(self)

        # TitFor2Tats test_strategy
        opponent = axelrod.MockPlayer(actions=[D, D, D, C, C])
        actions = [(C, D), (C, D), (D, D), (D, C), (C, C), (C, D)]
        self.versus_test(opponent, expected_actions=actions, init_kwargs={'N': 1, 'M': 2})

        # TwoTitsForTat test_strategy
        opponent = axelrod.MockPlayer(actions=[D, C, C, D, C])
        actions = [(C, D), (D, C), (D, C), (C, D), (D, C)]
        self.versus_test(opponent, expected_actions=actions, init_kwargs={'N': 2, 'M': 1})
        actions = [(C, C), (C, C)]
        self.versus_test(opponent=axelrod.Cooperator(),
                         expected_actions=actions, init_kwargs={'N': 2, 'M': 1})
        actions = [(C, D), (D, D), (D, D)]
        self.versus_test(opponent=axelrod.Defector(),
                         expected_actions=actions, init_kwargs={'N': 2, 'M': 1})

        # Cooperator test_strategy
        actions = [(C, C)] + [(C, D), (C, C)] * 9
        self.versus_test(opponent=axelrod.Alternator(),
                         expected_actions=actions, init_kwargs={'N': 0, 'M': 1})
        self.versus_test(opponent=axelrod.Alternator(),
                         expected_actions=actions, init_kwargs={'N': 0, 'M': 5})
        self.versus_test(opponent=axelrod.Alternator(),
                         expected_actions=actions, init_kwargs={'N': 0, 'M': 0})

        # Defector test_strategy
        actions = [(D, C)] + [(D, D), (D, C)] * 9
        self.versus_test(opponent=axelrod.Alternator(),
                         expected_actions=actions, init_kwargs={'N': 1, 'M': 0})
        self.versus_test(opponent=axelrod.Alternator(),
                         expected_actions=actions, init_kwargs={'N': 5, 'M': 0})

        # Other init args
        actions = [(C, C), (C, D), (C, D), (D, C), (D, C), (D, D), (C, C)]
        opponent = axelrod.MockPlayer(actions=[acts[1] for acts in actions])
        self.versus_test(opponent=opponent,
                         expected_actions=actions, init_kwargs={'N': 3, 'M': 2})
