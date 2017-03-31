"""Tests for Finite State Machine Strategies."""
import unittest

import axelrod
from .test_player import TestMatch, TestPlayer
from axelrod.strategies.finite_state_machines import SimpleFSM


C, D = axelrod.Actions.C, axelrod.Actions.D


# def check_state_transitions(state_transitions):
#     """Checks that the supplied transitions for a finite state machine are
#     well-formed."""
#     keys = state_transitions.keys()
#     values = state_transitions.values()
#     # Check that the set of source states contains the set of sink states
#     sources = [k[0] for k in keys]
#     sinks = [v[0] for v in values]
#     if not set(sinks).issubset(set(sources)):
#         return False
#     # Check that there are two outgoing edges for every source state
#     for state in sources:
#         for action in [C, D]:
#             if not ((state, action) in keys):
#                 return False
#     return True


class TestSimpleFSM(unittest.TestCase):
    def setUp(self):
        self.two_state_transition = [(1, C, 0, C), (1, D, 0, D), (0, C, 1, D), (0, D, 1, C)]

        self.two_state = SimpleFSM(transitions=self.two_state_transition, initial_state=1)

    def test__eq__true(self):
        new_two_state = SimpleFSM(transitions=self.two_state_transition, initial_state=1)
        self.assertTrue(new_two_state.__eq__(self.two_state))
        new_two_state.move(C)
        self.two_state.move(D)
        self.assertTrue(new_two_state.__eq__(self.two_state))

    def test__eq__false_by_state(self):
        new_two_state = SimpleFSM(transitions=self.two_state_transition, initial_state=0)
        self.assertFalse(new_two_state.__eq__(self.two_state))

    def test__eq__false_by_transition(self):
        different_transitions = [(1, C, 0, D), (1, D, 0, D), (0, C, 1, D), (0, D, 1, C)]
        new_two_state = SimpleFSM(transitions=different_transitions, initial_state=1)

        self.assertFalse(new_two_state.__eq__(self.two_state))

    def test__eq__false_by_not_SimpleFSM(self):
        self.assertFalse(self.two_state.__eq__(3))

    def test__ne__(self):
        new_two_state = SimpleFSM(transitions=self.two_state_transition, initial_state=1)
        self.assertFalse(new_two_state.__ne__(self.two_state))
        new_two_state.move(C)
        self.assertTrue(new_two_state.__ne__(self.two_state))

    def test_move(self):
        self.assertEqual(self.two_state.move(C), C)
        self.assertEqual(self.two_state.state, 0)
        self.assertEqual(self.two_state.move(C), D)
        self.assertEqual(self.two_state.state, 1)

        self.assertEqual(self.two_state.move(D), D)
        self.assertEqual(self.two_state.state, 0)
        self.assertEqual(self.two_state.move(D), C)
        self.assertEqual(self.two_state.state, 1)

    def test_bad_transitions_raise_error(self):
        bad_transitions = [(1, C, 0, D), (1, D, 0, D), (0, C, 1, D)]
        self.assertRaises(ValueError, SimpleFSM, transitions=bad_transitions, initial_state=1)

    def test_bad_initial_state_raises_error(self):
        self.assertRaises(ValueError, SimpleFSM, transitions=self.two_state_transition, initial_state=5)

    def test_state_setter_raises_error_for_bad_input(self):
        with self.assertRaises(ValueError) as cm:
            self.two_state.state = 5
        error_msg = cm.exception.args[0]
        self.assertEqual(error_msg, 'state: 5 does not have values for both C and D')


class TestFSMPlayer(TestPlayer):
    """Test a few sample tables to make sure that the finite state machines are
    working as intended."""

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

    def test_cooperator(self):
        """Tests that the player defined by the table for Cooperator is in fact
        Cooperator."""
        cooperator_init_kwargs = {'transitions': [(1, C, 1, C), (1, D, 1, C)],
                                  'initial_state': 1,
                                  'initial_action': C}
        self.versus_test(axelrod.Alternator(), expected_actions=[(C, C), (C, D)] * 5,
                         init_kwargs=cooperator_init_kwargs)

    def test_defector(self):
        """Tests that the player defined by the table for Defector is in fact
        Defector."""
        defector_init_kwargs = {'transitions': [(1, C, 1, D), (1, D, 1, D)],
                                'initial_state': 1,
                                'initial_action': D}
        self.versus_test(axelrod.Alternator(), expected_actions=[(D, C), (D, D)] * 5, init_kwargs=defector_init_kwargs)

    def test_tft(self):
        """Tests that the player defined by the table for TFT is in fact
        TFT."""
        tft_init_kwargs = {'transitions': [(1, C, 1, C), (1, D, 1, D)],
                           'initial_state': 1,
                           'initial_action': C}
        self.versus_test(axelrod.Alternator(), expected_actions=[(C, C)] + [(C, D), (D, C)] * 5,
                         init_kwargs=tft_init_kwargs)

    def test_wsls(self):
        """Tests that the player defined by the table for TFT is in fact
        WSLS (also known as Pavlov."""
        wsls_init_kwargs = {'transitions': [(1, C, 1, C), (1, D, 2, D), (2, C, 2, D), (2, D, 1, C)],
                            'initial_state': 1,
                            'initial_action': C}
        expected = [(C, C), (C, D), (D, C), (D, D)] * 3
        self.versus_test(axelrod.Alternator(), expected_actions=expected, init_kwargs=wsls_init_kwargs)


class TestFortress3(TestPlayer):

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


class TestFortress4(TestPlayer):

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


class TestPredator(TestPlayer):

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


class TestPun1(TestPlayer):

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
        self.responses_test([C], [D, C], [C, C])
        self.responses_test([C], [D, C], [D, C])
        self.responses_test([C], [D, C, C], [C, C, C])
        self.responses_test([D], [D, C, C, C], [C, C, C, D])


class TestRaider(TestPlayer):

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


class TestRipoff(TestPlayer):

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


class TestSolutionB1(TestPlayer):

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


class TestSolutionB5(TestPlayer):

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


class TestThumper(TestPlayer):

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


class TestEvolvedFSM4(TestPlayer):

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


class TestEvolvedFSM16(TestPlayer):

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


class TestEvolvedFSM16Noise05(TestPlayer):

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


class TestFortress3vsFortress3(TestMatch):
    def test_rounds(self):
        self.versus_test(axelrod.Fortress3(), axelrod.Fortress3(),
                         [D, D, C, C, C], [D, D, C, C, C])


class TestFortress3vsTitForTat(TestMatch):
    def test_rounds(self):
        self.versus_test(axelrod.Fortress3(), axelrod.TitForTat(),
                         [D, D, D, C], [C, D, D, D])


class TestFortress3vsCooperator(TestMatch):
    def test_rounds(self):
        self.versus_test(axelrod.Fortress3(), axelrod.Cooperator(),
                         [D, D, D, D, D, D], [C] * 6)


class TestFortress4vsFortress4(TestMatch):
    def test_rounds(self):
        self.versus_test(axelrod.Fortress4(), axelrod.Fortress4(),
                         [D, D, D, C, C, C], [D, D, D, C, C, C])


class TestFortress4vsTitForTat(TestMatch):
    def test_rounds(self):
        self.versus_test(axelrod.Fortress4(), axelrod.TitForTat(),
                         [D, D, D, D, C, D], [C, D, D, D, D, C])


class TestFortress4vsCooperator(TestMatch):
    def test_rounds(self):
        self.versus_test(axelrod.Fortress4(), axelrod.Cooperator(),
                         [D, D, D, D, D, D], [C] * 6)
