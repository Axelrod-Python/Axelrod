"""Tests for Finite State Machine Strategies."""
import unittest

import axelrod
from .test_player import TestPlayer
from axelrod.strategies.finite_state_machines import SimpleFSM


C, D = axelrod.Actions.C, axelrod.Actions.D


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


class TestFsmTransitions(TestPlayer):
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

    def transitions_test(self, state_and_action):
        """
        takes a list of [(initial_state, first_opponent_action), (next_state, next_opponent_action), ...]
        and creates a list of opponent moves, and a list of expected_actions based on the FiniteStateMachine.
        Then creates a versus_test of those two lists.
        """
        fsm_player = self.player()
        transitions = fsm_player.fsm.state_transitions
        first_opponent_move = state_and_action[0][1]

        expected_actions = [(fsm_player.initial_action, first_opponent_move)]
        opponent_actions = [first_opponent_move]

        for index in range(1, len(state_and_action)):
            current_state_and_last_opponent_move = state_and_action[index - 1]
            fsm_move = transitions[current_state_and_last_opponent_move][1]

            current_opponent_move = state_and_action[index][1]

            expected_actions.append((fsm_move, current_opponent_move))
            opponent_actions.append(current_opponent_move)

        self.versus_test(axelrod.MockPlayer(opponent_actions), expected_actions=expected_actions)

    def test_transitions_with_default_fsm(self):
        if self.player is axelrod.FSMPlayer:
            state_action = [(1, C), (1, D)]
            self.transitions_test(state_action)


class TestFortress3(TestFsmTransitions):

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
    """
    transitions = [
            (1, C, 1, D),
            (1, D, 2, D),
            (2, C, 1, D),
            (2, D, 3, C),
            (3, C, 3, C),
            (3, D, 1, D)
        ]
    """

    def test_strategy(self):
        self.first_play_test(D)

        state_and_actions = [(1, C), (1, D), (2, C), (1, C)]
        self.transitions_test(state_and_actions)

        state_and_actions = [(1, D), (2, D), (3, C), (3, C), (3, C), (3, D), (1, C)] * 2
        self.transitions_test(state_and_actions)

    @unittest.expectedFailure
    def test_incorrect_transitions(self):
        state_and_actions = [(1, C), (1, C), (2, D), (3, C)]
        self.transitions_test(state_and_actions)


class TestFortress4(TestFsmTransitions):

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
    """
    transitions = [
            (1, C, 1, D),
            (1, D, 2, D),
            (2, C, 1, D),
            (2, D, 3, D),
            (3, C, 1, D),
            (3, D, 4, C),
            (4, C, 4, C),
            (4, D, 1, D)
        ]
    """

    def test_strategy(self):
        self.first_play_test(D)

        state_and_actions = [(1, C), (1, D), (2, C)] * 3
        self.transitions_test(state_and_actions)

        state_and_actions = [(1, D), (2, D), (3, C), (1, C)] * 3
        self.transitions_test(state_and_actions)

        state_and_actions = [(1, D), (2, D), (3, D), (4, C), (4, C), (4, C), (4, C), (4, D)] * 3
        self.transitions_test(state_and_actions)


class TestPredator(TestFsmTransitions):

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
    """
    transitions = [
            (0, C, 0, D),
            (0, D, 1, D),
            (1, C, 2, D),
            (1, D, 3, D),
            (2, C, 4, C),
            (2, D, 3, D),
            (3, C, 5, D),
            (3, D, 4, C),
            (4, C, 2, C),
            (4, D, 6, D),
            (5, C, 7, D),
            (5, D, 3, D),
            (6, C, 7, C),
            (6, D, 7, D),
            (7, C, 8, D),
            (7, D, 7, D),
            (8, C, 8, D),
            (8, D, 6, D)
        ]
    """

    def test_strategy(self):
        self.first_play_test(C)

        # TODO CHECK POSSIBLE ISSUE - STATE: 0 CAN NEVER BE REACHED
        state_and_actions = ([(1, C), (2, C), (4, C), (2, D), (3, D), (4, D), (6, C)] +
                             [(7, D), (7, C), (8, C), (8, D), (6, D)] * 3)
        self.transitions_test(state_and_actions)

        state_and_actions = [(1, C), (2, D), (3, C), (5, D), (3, C), (5, C)] + [(7, C), (8, D), (6, C)] * 5
        self.transitions_test(state_and_actions)

        state_and_actions = [(1, D), (3, D), (4, D), (6, D)] + [(7, D)] * 10
        self.transitions_test(state_and_actions)


class TestPun1(TestFsmTransitions):

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

    """
    transitions = [
            (1, C, 2, C),
            (1, D, 2, C),
            (2, C, 1, C),
            (2, D, 1, D)
        ]
    """

    def test_strategy(self):
        self.first_play_test(D)

        


class TestRaider(TestFsmTransitions):

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

    """
    transitions = [
            (0, C, 2, D),
            (0, D, 2, D),
            (1, C, 1, C),
            (1, D, 1, D),
            (2, C, 0, D),
            (2, D, 3, C),
            (3, C, 0, D),
            (3, D, 1, C)
        ]
    """

    def test_strategy(self):
        # Test initial play sequence
        self.first_play_test(D)


class TestRipoff(TestFsmTransitions):

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

    """
    transitions = [
            (1, C, 2, C),
            (1, D, 3, C),
            (2, C, 1, D),
            (2, D, 3, C),
            (3, C, 3, C),  # Note that it's TFT in state 3
            (3, D, 3, D)
        ]
    """

    def test_strategy(self):
        # Test initial play sequence
        self.first_play_test(D)


class TestSolutionB1(TestFsmTransitions):

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

    """
    transitions = [
            (1, C, 2, D),
            (1, D, 1, D),
            (2, C, 2, C),
            (2, D, 3, C),
            (3, C, 3, C),
            (3, D, 3, C)
        ]
    """

    def test_strategy(self):
        # Test initial play sequence
        self.first_play_test(D)


class TestSolutionB5(TestFsmTransitions):

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

    """
    transitions = [
            (1, C, 2, C),
            (1, D, 6, D),
            (2, C, 2, C),
            (2, D, 3, D),
            (3, C, 6, C),
            (3, D, 1, D),
            (4, C, 3, C),
            (4, D, 6, D),
            (5, C, 5, D),
            (5, D, 4, D),
            (6, C, 3, C),
            (6, D, 5, D)
        ]
    """

    def test_strategy(self):
        # Test initial play sequence
        self.first_play_test(D)


class TestThumper(TestFsmTransitions):

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

    """
    transitions = [
            (1, C, 1, C),
            (1, D, 2, D),
            (2, C, 1, D),
            (2, D, 1, D)
        ]
    """

    def test_strategy(self):
        # Test initial play sequence
        self.first_play_test(C)


class TestEvolvedFSM4(TestFsmTransitions):

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

    """
    transitions = [
            (0, C, 0, C),
            (0, D, 2, D),
            (1, C, 3, D),
            (1, D, 0, C),
            (2, C, 2, D),
            (2, D, 1, C),
            (3, C, 3, D),
            (3, D, 1, D)
        ]
    """

    def test_strategy(self):
        # Test initial play sequence
        self.first_play_test(C)


class TestEvolvedFSM16(TestFsmTransitions):

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

    """
    transitions = [
            (0, C, 0, C),
            (0, D, 12, D),
            (1, C, 3, D),
            (1, D, 6, C),
            (2, C, 2, D),
            (2, D, 14, D),
            (3, C, 3, D),
            (3, D, 3, D),
            (4, C, 11, D),
            (4, D, 7, D),
            (5, C, 12, D),
            (5, D, 10, D),
            (6, C, 5, C),
            (6, D, 12, D),
            (7, C, 3, D),
            (7, D, 1, C),
            (8, C, 5, C),
            (8, D, 5, C),
            (9, C, 10, D),
            (9, D, 13, D),
            (10, C, 11, D),
            (10, D, 8, C),
            (11, C, 15, D),
            (11, D, 5, D),
            (12, C, 8, C),
            (12, D, 11, D),
            (13, C, 13, D),
            (13, D, 7, D),
            (14, C, 13, D),
            (14, D, 13, D),
            (15, C, 15, D),
            (15, D, 2, C)
        ]
    """

    def test_strategy(self):
        # Test initial play sequence
        self.first_play_test(C)


class TestEvolvedFSM16Noise05(TestFsmTransitions):

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

    """
    transitions = [
            (0, C, 8, C),
            (0, D, 3, D),
            (1, C, 13, C),
            (1, D, 15, D),
            (2, C, 12, C),
            (2, D, 3, D),
            (3, C, 10, C),
            (3, D, 3, D),
            (4, C, 5, D),
            (4, D, 4, D),
            (5, C, 4, D),
            (5, D, 10, D),
            (6, C, 8, C),
            (6, D, 6, D),
            (7, C, 5, D),
            (7, D, 15, C),
            (8, C, 2, C),
            (8, D, 4, D),
            (9, C, 15, D),
            (9, D, 6, D),
            (10, C, 4, D),
            (10, D, 1, D),
            (11, C, 14, D),
            (11, D, 13, C),
            (12, C, 13, C),
            (12, D, 2, C),
            (13, C, 13, C),
            (13, D, 6, C),
            (14, C, 3, D),
            (14, D, 13, D),
            (15, C, 5, D),
            (15, D, 11, C)
        ]
    """

    def test_strategy(self):
        # Test initial play sequence
        self.first_play_test(C)
