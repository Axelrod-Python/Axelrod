"""Tests DBS strategy."""

import unittest

import axelrod as axl
from axelrod.strategies import dbs

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestNode(unittest.TestCase):
    """Test for the base Node class."""

    node = dbs.Node()

    def test_get_siblings(self):
        with self.assertRaises(NotImplementedError):
            self.node.get_siblings()

    def test_is_stochastic(self):
        with self.assertRaises(NotImplementedError):
            self.node.is_stochastic()


class TestTreeSearch(unittest.TestCase):
    """
    A set of tests for the tree-search functions. We test the answers of both
    minimax_tree_search and move_gen functions, against a set of classic
    policies (the answer being the best move to play for the next turn,
    considering an incoming position (C, C), (C, D), (D, C) or (D, D)).
    For each policy, we test the answer for all incoming position.
    """

    def setUp(self):
        """Initialization for tests."""
        # For each test, we check the answer against each possible
        # inputs, that are in self.input_pos.
        self.input_pos = [(C, C), (C, D), (D, C), (D, D)]
        # We define the policies against which we are going to test.
        self.cooperator_policy = dbs.create_policy(1, 1, 1, 1)
        self.defector_policy = dbs.create_policy(0, 0, 0, 0)
        self.titForTat_policy = dbs.create_policy(1, 1, 0, 0)
        self.alternator_policy = dbs.create_policy(0, 1, 0, 1)
        self.grudger_policy = dbs.create_policy(1, 0, 0, 0)
        self.random_policy = dbs.create_policy(0.5, 0.5, 0.5, 0.5)

    def test_minimaxTreeSearch_cooperator(self):
        """
        Tests the minimax_tree_search function when playing against a
        Cooperator player. Output == 0 means Cooperate, 1 means Defect.
        The best (hence expected) answer to Cooperator is to defect
        whatever the input position is.
        """
        expected_output = [1, 1, 1, 1]
        for inp, out in zip(self.input_pos, expected_output):
            begin_node = dbs.DeterministicNode(inp[0], inp[1], depth=0)
            values = dbs.minimax_tree_search(
                begin_node, self.cooperator_policy, max_depth=5
            )
            self.assertEqual(values.index(max(values)), out)

    def test_move_gen_cooperator(self):
        """
        Tests the move_gen function when playing against a Cooperator player.
        """
        expected_output = [D, D, D, D]
        for inp, out in zip(self.input_pos, expected_output):
            out_move = dbs.move_gen(
                inp, self.cooperator_policy, depth_search_tree=5
            )
            self.assertEqual(out_move, out)

    def test_minimaxTreeSearch_defector(self):
        """
        Tests the minimax_tree_search function when playing against a
        Defector player. The best answer to Defector is to always defect
        """
        expected_output = [1, 1, 1, 1]
        for inp, out in zip(self.input_pos, expected_output):
            begin_node = dbs.DeterministicNode(inp[0], inp[1], depth=0)
            values = dbs.minimax_tree_search(
                begin_node, self.defector_policy, max_depth=5
            )
            self.assertEqual(values.index(max(values)), out)

    def test_move_gen_defector(self):
        """
        Tests the move_gen function when playing against a Defector player.
        """
        expected_output = [D, D, D, D]
        for inp, out in zip(self.input_pos, expected_output):
            out_move = dbs.move_gen(
                inp, self.defector_policy, depth_search_tree=5
            )
            self.assertEqual(out_move, out)

    def test_minimaxTreeSearch_titForTat(self):
        """
        Tests the minimax_tree_search function when playing against a
        TitForTat player. The best (hence expected) answer to TitFOrTat is to
        cooperate whatever the input position is.
        """
        expected_output = [0, 0, 0, 0]
        for inp, out in zip(self.input_pos, expected_output):
            begin_node = dbs.DeterministicNode(inp[0], inp[1], depth=0)
            values = dbs.minimax_tree_search(
                begin_node, self.titForTat_policy, max_depth=5
            )
            self.assertEqual(values.index(max(values)), out)

    def test_last_node_titForTat(self):
        """
        Test that against TitForTat, for the last move, i.e. if tree depth is 1,
        the algorithms defects for all input.
        """
        expected_output = [1, 1, 1, 1]
        for inp, out in zip(self.input_pos, expected_output):
            begin_node = dbs.DeterministicNode(inp[0], inp[1], depth=0)
            values = dbs.minimax_tree_search(
                begin_node, self.titForTat_policy, max_depth=1
            )
            self.assertEqual(values.index(max(values)), out)

    def test_move_gen_titForTat(self):
        """
        Tests the move_gen function when playing against a TitForTat player.
        """
        expected_output = [C, C, C, C]
        for inp, out in zip(self.input_pos, expected_output):
            out_move = dbs.move_gen(
                inp, self.titForTat_policy, depth_search_tree=5
            )
            self.assertEqual(out_move, out)

    def test_minimaxTreeSearch_alternator(self):
        """
        Tests the minimax_tree_search function when playing against an
        Alternator player. The best answer to Alternator is to always defect.
        """
        expected_output = [1, 1, 1, 1]
        for inp, out in zip(self.input_pos, expected_output):
            begin_node = dbs.DeterministicNode(inp[0], inp[1], depth=0)
            values = dbs.minimax_tree_search(
                begin_node, self.alternator_policy, max_depth=5
            )
            self.assertEqual(values.index(max(values)), out)

    def test_move_gen_alternator(self):
        """
        Tests the move_gen function when playing against an Alternator player.
        """
        expected_output = [D, D, D, D]
        for inp, out in zip(self.input_pos, expected_output):
            out_move = dbs.move_gen(
                inp, self.random_policy, depth_search_tree=5
            )
            self.assertEqual(out_move, out)

    def test_minimaxTreeSearch_random(self):
        """
        Tests the minimax_tree_search function when playing against a Random
        player. The best answer to Random is to always defect.
        """
        expected_output = [1, 1, 1, 1]
        for inp, out in zip(self.input_pos, expected_output):
            begin_node = dbs.DeterministicNode(inp[0], inp[1], depth=0)
            values = dbs.minimax_tree_search(
                begin_node, self.random_policy, max_depth=5
            )
            self.assertEqual(values.index(max(values)), out)

    def test_move_gen_random(self):
        """
        Tests the move_gen function when playing against a Random player.
        """
        expected_output = [D, D, D, D]
        for inp, out in zip(self.input_pos, expected_output):
            out_move = dbs.move_gen(
                inp, self.random_policy, depth_search_tree=5
            )
            self.assertEqual(out_move, out)

    def test_minimaxTreeSearch_grudger(self):
        """
        Tests the minimax_tree_search function when playing against a
        Grudger player. The best answer to Grudger is to cooperate if both
        cooperated at last round, else it's to defect.
        """
        expected_output = [0, 1, 1, 1]
        for inp, out in zip(self.input_pos, expected_output):
            begin_node = dbs.DeterministicNode(inp[0], inp[1], depth=0)
            values = dbs.minimax_tree_search(
                begin_node, self.grudger_policy, max_depth=5
            )
            self.assertEqual(values.index(max(values)), out)

    def test_move_gen_grudger(self):
        """
        Tests the move_gen function when playing against a Grudger player.
        """
        expected_output = [C, D, D, D]
        for inp, out in zip(self.input_pos, expected_output):
            out_move = dbs.move_gen(
                inp, self.grudger_policy, depth_search_tree=5
            )
            self.assertEqual(out_move, out)


class TestDBS(TestPlayer):
    name = "DBS: 0.75, 3, 4, 3, 5"
    player = axl.DBS

    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": True,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        default_init_kwargs = {
            "discount_factor": 0.75,
            "promotion_threshold": 3,
            "violation_threshold": 4,
            "reject_threshold": 4,
            "tree_depth": 5,
        }

        # Test that DBS always cooperate against Cooperator.
        actions = [(C, C)] * 7
        self.versus_test(
            opponent=axl.Cooperator(),
            expected_actions=actions,
            init_kwargs=default_init_kwargs,
        )

        # Test if it correctly learns Alternator strategy.
        actions = [(C, C), (C, D)] * 3 + [(D, C), (C, D)] * 3
        self.versus_test(
            opponent=axl.Alternator(),
            expected_actions=actions,
            init_kwargs=default_init_kwargs,
        )

        # Check that algorithms take into account a change in opponent's
        # strategy.
        mock_actions = [C, C, C, D, D, D, D, D, D, D]
        exp_actions = [(C, C)] * 3 + [(C, D)] * 4 + [(D, D)] * 3
        self.versus_test(
            opponent=axl.MockPlayer(actions=mock_actions),
            expected_actions=exp_actions,
            init_kwargs=default_init_kwargs,
        )

        # Check that adaptation is faster if diminishing promotion_threshold.
        init_kwargs_2 = {
            "discount_factor": 0.75,
            "promotion_threshold": 2,
            "violation_threshold": 4,
            "reject_threshold": 4,
            "tree_depth": 5,
        }
        mock_actions = [C, C, C, D, D, D, D, D, D, D]
        exp_actions = [(C, C)] * 3 + [(C, D)] * 3 + [(D, D)] * 4
        self.versus_test(
            opponent=axl.MockPlayer(actions=mock_actions),
            expected_actions=exp_actions,
            init_kwargs=init_kwargs_2,
        )

        # Check that ShouldDemote mechanism works.
        # We play against Alternator for 12 turns to make the
        # algorithm learn Alternator's strategy, then at turn 13 we
        # change opponent to Defector, hence triggering ShouldDemote
        # mechanism. For this test we use violation_threshold=3
        init_kwargs_3 = {
            "discount_factor": 0.75,
            "promotion_threshold": 3,
            "violation_threshold": 3,
            "reject_threshold": 3,
            "tree_depth": 5,
        }
        exp_actions = [(C, C), (C, D)] * 3 + [(D, C), (C, D)] * 3
        exp_actions += [(D, D), (C, D)] * 3 + [(D, D)]
        mock_actions = [C, D, C, D, C, D, C, D, C, D, C, D, D, D, D, D, D, D, D]
        self.versus_test(
            opponent=axl.MockPlayer(actions=mock_actions),
            expected_actions=exp_actions,
            init_kwargs=init_kwargs_3,
        )
