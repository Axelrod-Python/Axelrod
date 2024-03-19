"""Tests for Compute FSM Memory."""

import unittest

import axelrod as axl
from axelrod.compute_finite_state_machine_memory import *

C, D = axl.Action.C, axl.Action.D


class TestOrderedMemitTuple(unittest.TestCase):
    def memits_completely_equal(self, x, y):
        """If the state and the actions are equal."""
        return x.state == y.state and x == y

    def memit_tuple_equal(self, x_tuple, y_tuple):
        """If the memits are the same in the same order."""
        return self.memits_completely_equal(
            x_tuple[0], y_tuple[0]
        ) and self.memits_completely_equal(x_tuple[1], y_tuple[1])

    def test_provided_ascending_order(self):
        memit_c1c = Memit(C, 1, C)
        memit_c2c = Memit(C, 2, C)

        actual_tuple = ordered_memit_tuple(memit_c1c, memit_c2c)
        expected_tuple = (memit_c1c, memit_c2c)

        return self.memit_tuple_equal(actual_tuple, expected_tuple)

    def test_provided_descending_order(self):
        memit_c1c = Memit(C, 1, C)
        memit_c2c = Memit(C, 2, C)

        actual_tuple = ordered_memit_tuple(memit_c2c, memit_c1c)
        expected_tuple = (memit_c1c, memit_c2c)

        return self.memit_tuple_equal(actual_tuple, expected_tuple)

    def test_order_on_actions(self):
        memit_c9c = Memit(C, 9, C)
        memit_c9d = Memit(C, 9, D)

        actual_tuple = ordered_memit_tuple(memit_c9d, memit_c9c)
        expected_tuple = (memit_c9c, memit_c9d)

        return self.memit_tuple_equal(actual_tuple, expected_tuple)


class TestGetMemoryFromTransitions(unittest.TestCase):
    def transitions_to_dict(self, transitions):
        return {
            (current_state, input_action): (next_state, output_action)
            for current_state, input_action, next_state, output_action in transitions
        }

    def test_cooperator(self):
        transitions = ((0, C, 0, C), (0, D, 0, C))

        trans_dict = self.transitions_to_dict(transitions)
        self.assertEqual(get_memory_from_transitions(trans_dict), 0)

    def test_tit_for_tat(self):
        transitions = ((0, C, 0, C), (0, D, 0, D))

        trans_dict = self.transitions_to_dict(transitions)
        self.assertEqual(get_memory_from_transitions(trans_dict), 1)

    def test_two_state_memory_two(self):
        """If all D lead to state 0 and all C lead to state 1.  We make it so
        that all paths out of state 0 plays Cooperator and state 1 plays
        Defector.
        In this case, we must know what state we're in to know how to respond to
        the opponent's previou action, but we cannot determine from our own
        previous action; we must look at opponent's action from two turns ago.
        """
        transitions = ((0, C, 0, C), (0, D, 1, C), (1, C, 0, D), (1, D, 1, D))

        trans_dict = self.transitions_to_dict(transitions)
        self.assertEqual(get_memory_from_transitions(trans_dict), 2)

    def test_two_state_tft(self):
        """Same case as above, but this time our own last action tells us which
        state we're in.  In fact, this strategy is exactly TFT.
        """
        transitions = ((0, C, 0, C), (0, D, 1, D), (1, C, 0, C), (1, D, 1, D))

        trans_dict = self.transitions_to_dict(transitions)
        self.assertEqual(get_memory_from_transitions(trans_dict), 1)

    def test_three_state_tft(self):
        """Tit-for-tat again, but using three states, and a complex web of
        transitions between them.
        """
        transitions = (
            (0, C, 1, C),
            (0, D, 1, D),
            (1, C, 2, C),
            (1, D, 0, D),
            (2, C, 0, C),
            (2, D, 2, D),
        )

        trans_dict = self.transitions_to_dict(transitions)
        self.assertEqual(get_memory_from_transitions(trans_dict), 1)

    def test_two_state_inf_memory(self):
        """A C will cause the FSM to stay in the same state, and D causes to
        change states.  Will always respond to a C with a C.   Will respond to a
        D with a C in state 0, but with a D in state 1.
        So we need to know the state to know how to respond to a D.  But since
        an arbitarily long sequence of C/C may occur, we need infinite memory.
        """
        transitions = ((0, C, 0, C), (0, D, 1, C), (1, C, 1, C), (1, D, 0, D))

        trans_dict = self.transitions_to_dict(transitions)
        self.assertEqual(get_memory_from_transitions(trans_dict), float("inf"))

    def test_four_state_memory_two(self):
        """Same as the two_state_memory_two test above, but we use two copies,
        stitched together.
        """
        transitions = (
            (0, C, 0, C),
            (0, D, 1, C),
            (1, C, 2, D),
            (1, D, 1, D),
            (2, C, 2, C),
            (2, D, 3, C),
            (3, C, 0, D),
            (3, D, 3, D),
        )

        trans_dict = self.transitions_to_dict(transitions)
        self.assertEqual(get_memory_from_transitions(trans_dict), 2)

    def test_tit_for_two_tat(self):
        """This strategy does the same thing until the opponent does the same
        action twice; then it responds in kind.  In the FSM implementation, we
        let states 1 and 2 be the cooperating states, with state 2 being the
        state after one opponent defection.  And states 3 and 4 are the
        defecting states, with state 4 after 1 opponent cooperation.
        The memory should be two, because if the last two moves don't match,
        then we can look to see what we did in the last move.  If the do match,
        then we can respond in kind.
        """
        transitions = (
            (1, C, 1, C),
            (1, D, 2, C),
            (2, C, 1, C),
            (2, D, 3, D),
            (3, C, 4, D),
            (3, D, 3, D),
            (4, C, 1, C),
            (4, D, 3, D),
        )

        trans_dict = self.transitions_to_dict(transitions)
        self.assertEqual(get_memory_from_transitions(trans_dict), 2)

    def test_tit_for_five_tat(self):
        """Analogous to tit for two tat above."""
        transitions = (
            (1, C, 1, C),
            (1, D, 2, C),
            (2, C, 1, C),
            (2, D, 3, C),
            (3, C, 1, C),
            (3, D, 4, C),
            (4, C, 1, C),
            (4, D, 5, C),
            (5, C, 1, C),
            (5, D, 6, D),
            (6, C, 6, D),
            (6, D, 7, D),
            (7, C, 6, D),
            (7, D, 8, D),
            (8, C, 6, D),
            (8, D, 9, D),
            (9, C, 6, D),
            (9, D, 10, D),
            (10, C, 6, D),
            (10, D, 1, C),
        )

        trans_dict = self.transitions_to_dict(transitions)
        self.assertEqual(get_memory_from_transitions(trans_dict), 5)

    def test_fortress_3(self):
        """Tests Fortress-3, which Defects unless the opponent D twice in a row.
        In that case C, and continue to C for as long as the opponent does.
        We know we're in state 3 if our own previous move was a C.  Otherwise, C
        if and only if the opponent's previous two moves were D.  [Unless we
        were in state 3 last turn, in which case we would have C'd two turns
        ago.]
        So the memory should be 2.
        """
        transitions = (
            (1, C, 1, D),
            (1, D, 2, D),
            (2, C, 1, D),
            (2, D, 3, C),
            (3, C, 3, C),
            (3, D, 1, D),
        )

        trans_dict = self.transitions_to_dict(transitions)
        self.assertEqual(get_memory_from_transitions(trans_dict), 2)

    def test_fortress_4(self):
        """Tests Fortress-4.  Should have memory=3 for same logic that
        Fortress-3 should have memory=2.
        """
        transitions = (
            (1, C, 1, D),
            (1, D, 2, D),
            (2, C, 1, D),
            (2, D, 3, D),
            (3, C, 1, D),
            (3, D, 4, C),
            (4, C, 3, C),
            (4, D, 1, D),
        )

        trans_dict = self.transitions_to_dict(transitions)
        self.assertEqual(get_memory_from_transitions(trans_dict), 3)

    def test_complex_cooperator(self):
        """Tests a cooperator with lots of states and transitions."""
        transitions = (
            (0, C, 0, C),
            (0, D, 1, C),
            (1, C, 2, C),
            (1, D, 3, C),
            (2, C, 4, C),
            (2, D, 3, C),
            (3, C, 5, C),
            (3, D, 4, C),
            (4, C, 2, C),
            (4, D, 6, C),
            (5, C, 7, C),
            (5, D, 3, C),
            (6, C, 7, C),
            (6, D, 7, C),
            (7, C, 8, C),
            (7, D, 7, C),
            (8, C, 8, C),
            (8, D, 6, C),
        )

        trans_dict = self.transitions_to_dict(transitions)
        self.assertEqual(get_memory_from_transitions(trans_dict), 0)

    def test_disconnected_graph(self):
        """Test two disjoint versions of Fortress3, with initial_state."""
        transitions = (
            (1, C, 1, D),
            (1, D, 2, D),
            (2, C, 1, D),
            (2, D, 3, C),
            (3, C, 3, C),
            (3, D, 1, D),
            (4, C, 4, D),
            (4, D, 5, D),
            (5, C, 4, D),
            (5, D, 6, C),
            (6, C, 6, C),
            (6, D, 4, D),
        )

        trans_dict = self.transitions_to_dict(transitions)
        self.assertEqual(
            get_memory_from_transitions(trans_dict, initial_state=1), 2
        )

    def test_transient_state(self):
        """Test a setup where we a transient state (no incoming transitions)
        goes into a Fortress3 (and D) if the opponent D, and goes into a
        Cooperator if the opponent C.
        The transient state is state 0.  Fortress3 starts at state 1.  And
        the Cooperator is state 4.
        """
        transitions = (
            (0, C, 4, C),
            (0, D, 1, D),
            (1, C, 1, D),
            (1, D, 2, D),
            (2, C, 1, D),
            (2, D, 3, C),
            (3, C, 3, C),
            (3, D, 1, D),
            (4, C, 4, C),
            (4, D, 4, C),
        )

        trans_dict = self.transitions_to_dict(transitions)
        # If starting in state 4, then treat like Cooperator
        self.assertEqual(
            get_memory_from_transitions(trans_dict, initial_state=4), 0
        )
        # Start in state 1, then a Fortress3.
        self.assertEqual(
            get_memory_from_transitions(trans_dict, initial_state=1), 2
        )

    def test_infinite_memory_transient_state(self):
        """A transient state at 0, which goes into either a Cooperator or a TFT.
        Because an arbitrarily-long chain of C/C may exist, we would need a
        infinite memory to determine which state we're in, so that we know how
        to respond to a D.
        """
        transitions = (
            (0, C, 1, C),
            (0, D, 2, D),
            (1, C, 1, C),
            (1, D, 1, C),
            (2, C, 2, C),
            (2, D, 2, D),
        )

        trans_dict = self.transitions_to_dict(transitions)
        self.assertEqual(
            get_memory_from_transitions(trans_dict, initial_state=0),
            float("inf"),
        )

        self.assertEqual(
            get_memory_from_transitions(trans_dict, initial_state=2), 1
        )

    def test_evolved_fsm_4(self):
        """This should be infinite memory because the C/D self-loop at state 2
        and state 3.
        """
        transitions = (
            (0, C, 0, C),
            (0, D, 2, D),
            (1, C, 3, D),
            (1, D, 0, C),
            (2, C, 2, D),
            (2, D, 1, C),
            (3, C, 3, D),
            (3, D, 1, D),
        )

        trans_dict = self.transitions_to_dict(transitions)
        self.assertEqual(get_memory_from_transitions(trans_dict), float("inf"))
