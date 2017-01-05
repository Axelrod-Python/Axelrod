"""Tests for Finite State Machine Strategies."""
import unittest

import axelrod
from .test_player import TestHeadsUp, TestPlayer


C, D = axelrod.Actions.C, axelrod.Actions.D


def check_state_transitions(state_transitions):
    """Checks that the supplied transitions for a finite state machine are
    well-formed."""
    keys = state_transitions.keys()
    values = state_transitions.values()
    # Check that the set of source states contains the set of sink states
    sources = [k[0] for k in keys]
    sinks = [v[0] for v in values]
    if not set(sinks).issubset(set(sources)):
        return False
    # Check that there are two outgoing edges for every source state
    for state in sources:
        for action in [C, D]:
            if not ((state, action) in keys):
                return False
    return True


class TestFSMPlayers(unittest.TestCase):
    """Test a few sample tables to make sure that the finite state machines are
    working as intended."""

    def test_cooperator(self):
        """Tests that the player defined by the table for Cooperator is in fact
        Cooperator."""
        transitions = [(1, C, 1, C), (1, D, 1, C)]
        player = axelrod.FSMPlayer(transitions, initial_state=1, initial_action=C)
        opponent = axelrod.Alternator()
        for i in range(6):
            player.play(opponent)
        self.assertEqual(opponent.history, [C, D] * 3)
        self.assertEqual(player.history, [C] * 6)

    def test_defector(self):
        """Tests that the player defined by the table for Defector is in fact
        Defector."""
        transitions = [(1, C, 1, D), (1, D, 1, D)]
        player = axelrod.FSMPlayer(transitions, initial_state=1, initial_action=D)
        opponent = axelrod.Alternator()
        for i in range(6):
            player.play(opponent)
        self.assertEqual(opponent.history, [C, D] * 3)
        self.assertEqual(player.history, [D] * 6)

    def test_tft(self):
        """Tests that the player defined by the table for TFT is in fact
        TFT."""
        transitions = [(1, C, 1, C), (1, D, 1, D)]
        player = axelrod.FSMPlayer(transitions, initial_state=1, initial_action=C)
        opponent = axelrod.Alternator()
        for i in range(6):
            player.play(opponent)
        self.assertEqual(opponent.history, [C, D] * 3)
        self.assertEqual(player.history, [C, C, D, C, D, C])

    def test_wsls(self):
        """Tests that the player defined by the table for TFT is in fact
        WSLS (also known as Pavlov."""
        transitions = [(1, C, 1, C), (1, D, 2, D), (2, C, 2, D), (2, D, 1, C)]
        player = axelrod.FSMPlayer(transitions, initial_state=1, initial_action=C)
        opponent = axelrod.Alternator()
        for i in range(6):
            player.play(opponent)
        self.assertEqual(opponent.history, [C, D] * 3)
        self.assertEqual(player.history, [C, C, D, D, C, C])

    def test_malformed_tables(self):
        # Test a malformed table
        transitions = ((1, D, 2, D),
                       (1, C, 1, D),
                       (2, C, 1, D),
                       (2, D, 3, C),
                       (3, C, 3, C))
        player = axelrod.FSMPlayer(transitions=transitions, initial_state=1,
                                initial_action=C)
        self.assertFalse(check_state_transitions(player.fsm.state_transitions))

        transitions = [(1, D, 2, D)]
        player = axelrod.FSMPlayer(transitions=transitions, initial_state=1,
                                initial_action=C)
        self.assertFalse(check_state_transitions(player.fsm.state_transitions))


class TestFSMPlayer(TestPlayer):

    name = "FSM Player"
    player = axelrod.FSMPlayer

    expected_classifier = {
        'memory_depth': 1,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_transitions(self):
        # Test that the finite state machine is well-formed
        player = self.player()
        fsm = player.fsm
        self.assertTrue(check_state_transitions(fsm.state_transitions))

    def test_reset_initial_state(self):
        player = self.player()
        player.fsm.state = -1
        player.reset()
        self.assertFalse(player.fsm.state == -1)


class TestFortress3(TestFSMPlayer):

    name = "Fortress3"
    player = axelrod.Fortress3
    expected_classifier = {
        'memory_depth': 3,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Test initial play sequence
        self.first_play_test(D)


class TestFortress4(TestFSMPlayer):

    name = "Fortress4"
    player = axelrod.Fortress4
    expected_classifier = {
        'memory_depth': 4,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Test initial play sequence
        self.first_play_test(D)


class TestPredator(TestFSMPlayer):

    name = "Predator"
    player = axelrod.Predator
    expected_classifier = {
        'memory_depth': 9,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Test initial play sequence
        self.first_play_test(C)


class TestPun1(TestFSMPlayer):

    name = "Pun1"
    player = axelrod.Pun1
    expected_classifier = {
        'memory_depth': 2,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Test initial play sequence
        self.first_play_test(D)
        self.responses_test([D, C], [C, C], [C])
        self.responses_test([D, C], [D, C], [C])
        self.responses_test([D, C, C], [C, C, C], [C])
        self.responses_test([D, C, C, C], [C, C, C, D], [D])


class TestRaider(TestFSMPlayer):

    name = "Raider"
    player = axelrod.Raider
    expected_classifier = {
        'memory_depth': 3,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Test initial play sequence
        self.first_play_test(D)


class TestRipoff(TestFSMPlayer):

    name = "Ripoff"
    player = axelrod.Ripoff
    expected_classifier = {
        'memory_depth': 2,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Test initial play sequence
        self.first_play_test(D)


class TestSolutionB1(TestFSMPlayer):

    name = "SolutionB1"
    player = axelrod.SolutionB1
    expected_classifier = {
        'memory_depth': 3,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Test initial play sequence
        self.first_play_test(D)


class TestSolutionB5(TestFSMPlayer):

    name = "SolutionB5"
    player = axelrod.SolutionB5
    expected_classifier = {
        'memory_depth': 5,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Test initial play sequence
        self.first_play_test(D)


class TestThumper(TestFSMPlayer):

    name = "Thumper"
    player = axelrod.Thumper
    expected_classifier = {
        'memory_depth': 2,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Test initial play sequence
        self.first_play_test(C)


class TestEvolvedFSM4(TestFSMPlayer):

    name = "Evolved FSM 4"
    player = axelrod.EvolvedFSM4
    expected_classifier = {
        'memory_depth': 4,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Test initial play sequence
        self.first_play_test(C)


class TestEvolvedFSM16(TestFSMPlayer):

    name = "Evolved FSM 16"
    player = axelrod.EvolvedFSM16
    expected_classifier = {
        'memory_depth': 16,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Test initial play sequence
        self.first_play_test(C)


class TestEvolvedFSM16Noise05(TestFSMPlayer):

    name = "Evolved FSM 16 Noise 05"
    player = axelrod.EvolvedFSM16Noise05
    expected_classifier = {
        'memory_depth': 16,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Test initial play sequence
        self.first_play_test(C)


class TestFortress3vsFortress3(TestHeadsUp):
    def test_rounds(self):
        self.versus_test(axelrod.Fortress3(), axelrod.Fortress3(),
                         [D, D, C, C, C], [D, D, C, C, C])


class TestFortress3vsTitForTat(TestHeadsUp):
    def test_rounds(self):
        self.versus_test(axelrod.Fortress3(), axelrod.TitForTat(),
                         [D, D, D, C], [C, D, D, D])


class TestFortress3vsCooperator(TestHeadsUp):
    def test_rounds(self):
        self.versus_test(axelrod.Fortress3(), axelrod.Cooperator(),
                         [D, D, D, D, D, D], [C] * 6)


class TestFortress4vsFortress4(TestHeadsUp):
    def test_rounds(self):
        self.versus_test(axelrod.Fortress4(), axelrod.Fortress4(),
                         [D, D, D, C, C, C], [D, D, D, C, C, C])


class TestFortress4vsTitForTat(TestHeadsUp):
    def test_rounds(self):
        self.versus_test(axelrod.Fortress4(), axelrod.TitForTat(),
                         [D, D, D, D, C, D], [C, D, D, D, D, C])


class TestFortress4vsCooperator(TestHeadsUp):
    def test_rounds(self):
        self.versus_test(axelrod.Fortress4(), axelrod.Cooperator(),
                         [D, D, D, D, D, D], [C] * 6)
