from collections import Counter
import itertools
import random
import unittest

from hypothesis import given, example, settings

import axelrod
from axelrod import MoranProcess, MoranProcessGraph
from axelrod.moran import fitness_proportionate_selection
from axelrod.tests.property import strategy_lists


class TestMoranProcess(unittest.TestCase):

    def test_fps(self):
        self.assertEqual(fitness_proportionate_selection([0, 0, 1]), 2)
        random.seed(1)
        self.assertEqual(fitness_proportionate_selection([1, 1, 1]), 0)
        self.assertEqual(fitness_proportionate_selection([1, 1, 1]), 2)

    def test_exit_condition(self):
        p1, p2 = axelrod.Cooperator(), axelrod.Cooperator()
        mp = MoranProcess((p1, p2))
        mp.play()
        self.assertEqual(len(mp), 1)

    def test_two_players(self):
        p1, p2 = axelrod.Cooperator(), axelrod.Defector()
        random.seed(5)
        mp = MoranProcess((p1, p2))
        populations = mp.play()
        self.assertEqual(len(mp), 5)
        self.assertEqual(len(populations), 5)
        self.assertEqual(populations, mp.populations)
        self.assertEqual(mp.winning_strategy_name, str(p2))

    def test_two_random_players(self):
        p1, p2 = axelrod.Random(0.5), axelrod.Random(0.25)
        random.seed(5)
        mp = MoranProcess((p1, p2))
        populations = mp.play()
        self.assertEqual(len(mp), 2)
        self.assertEqual(len(populations), 2)
        self.assertEqual(populations, mp.populations)
        self.assertEqual(mp.winning_strategy_name, str(p1))

    def test_two_players_with_mutation(self):
        p1, p2 = axelrod.Cooperator(), axelrod.Defector()
        random.seed(5)
        mp = MoranProcess((p1, p2), mutation_rate=0.2)
        self.assertDictEqual(mp.mutation_targets, {str(p1): [p2], str(p2): [p1]})
        # Test that mutation causes the population to alternate between fixations
        counters = [
            Counter({'Cooperator': 2}),
            Counter({'Defector': 2}),
            Counter({'Cooperator': 2}),
            Counter({'Defector': 2})
        ]
        for counter in counters:
            for _ in itertools.takewhile(lambda x: x.population_distribution() != counter, mp):
                pass
            self.assertEqual(mp.population_distribution(), counter)

    def test_play_exception(self):
        p1, p2 = axelrod.Cooperator(), axelrod.Defector()
        mp = MoranProcess((p1, p2), mutation_rate=0.2)
        with self.assertRaises(ValueError):
            mp.play()

    def test_three_players(self):
        players = [axelrod.Cooperator(), axelrod.Cooperator(),
                   axelrod.Defector()]
        random.seed(5)
        mp = MoranProcess(players)
        populations = mp.play()
        self.assertEqual(len(mp), 7)
        self.assertEqual(len(populations), 7)
        self.assertEqual(populations, mp.populations)
        self.assertEqual(mp.winning_strategy_name, str(axelrod.Defector()))

    def test_three_players_with_mutation(self):
        p1 = axelrod.Cooperator()
        p2 = axelrod.Random()
        p3 = axelrod.Defector()
        players = [p1, p2, p3]
        mp = MoranProcess(players, mutation_rate=0.2)
        self.assertDictEqual(mp.mutation_targets, {str(p1): [p3, p2], str(p2): [p1, p3], str(p3): [p1, p2]})
        # Test that mutation causes the population to alternate between fixations
        counters = [
            Counter({'Cooperator': 3}),
            Counter({'Defector': 3}),
        ]
        for counter in counters:
            for _ in itertools.takewhile(lambda x: x.population_distribution() != counter, mp):
                pass
            self.assertEqual(mp.population_distribution(), counter)

    def test_four_players(self):
        players = [axelrod.Cooperator() for _ in range(3)]
        players.append(axelrod.Defector())
        random.seed(10)
        mp = MoranProcess(players)
        populations = mp.play()
        self.assertEqual(len(mp), 9)
        self.assertEqual(len(populations), 9)
        self.assertEqual(populations, mp.populations)
        self.assertEqual(mp.winning_strategy_name, str(axelrod.Defector()))

    @given(strategies=strategy_lists(min_size=2, max_size=5))
    @settings(max_examples=5, timeout=0)  # Very low number of examples

    # Two specific examples relating to cloning of strategies
    @example(strategies=[axelrod.BackStabber, axelrod.MindReader])
    @example(strategies=[axelrod.ThueMorse, axelrod.MindReader])
    def test_property_players(self, strategies):
        """Hypothesis test that randomly checks players"""
        players = [s() for s in strategies]
        mp = MoranProcess(players)
        populations = mp.play()
        self.assertEqual(populations, mp.populations)
        self.assertIn(mp.winning_strategy_name, [str(p) for p in players])

    def test_reset(self):
        p1, p2 = axelrod.Cooperator(), axelrod.Defector()
        random.seed(8)
        mp = MoranProcess((p1, p2))
        mp.play()
        self.assertEqual(len(mp), 4)
        self.assertEqual(len(mp.score_history), 3)
        mp.reset()
        self.assertEqual(len(mp), 1)
        self.assertEqual(mp.winning_strategy_name, None)
        self.assertEqual(mp.score_history, [])
        # Check that players reset
        for player, initial_player in zip(mp.players, mp.initial_players):
            self.assertEqual(str(player), str(initial_player))

    def test_cache(self):
        p1, p2 = axelrod.Cooperator(), axelrod.Defector()
        mp = MoranProcess((p1, p2))
        mp.play()
        self.assertEqual(len(mp.deterministic_cache), 1)

        # Check that can pass a pre built cache
        cache = axelrod.DeterministicCache()
        mp = MoranProcess((p1, p2), deterministic_cache=cache)
        self.assertEqual(cache, mp.deterministic_cache)

    def test_iter(self):
        p1, p2 = axelrod.Cooperator(), axelrod.Defector()
        mp = MoranProcess((p1, p2))
        self.assertEqual(mp.__iter__(), mp)


class GraphMoranProcess(unittest.TestCase):

    def test_complete(self):
        """A complete graph should produce the same results as the default
        case."""
        seeds = range(0, 5)
        players = []
        N = 6
        graph = axelrod.graph.complete_graph(N)
        for _ in range(N // 2):
            players.append(axelrod.Cooperator())
            players.append(axelrod.Defector())
        for seed in seeds:
            axelrod.seed(seed)
            mp = MoranProcess(players)
            mp.play()
            winner = mp.winning_strategy_name
            axelrod.seed(seed)
            mp = MoranProcessGraph(players, graph)
            mp.play()
            winner2 = mp.winning_strategy_name
            self.assertEqual(winner, winner2)

    def test_cycle(self):
        """A cycle should sometimes produce different results vs. the default
        case."""
        seeds = [(1, True), (2, True), (3, False), (13, False)]
        players = []
        N = 6
        graph = axelrod.graph.cycle(N)
        for _ in range(N // 2):
            players.append(axelrod.Cooperator())
        for _ in range(N // 2):
            players.append(axelrod.Defector())
        for seed, outcome in seeds:
            axelrod.seed(seed)
            mp = MoranProcess(players)
            mp.play()
            winner = mp.winning_strategy_name
            axelrod.seed(seed)
            mp = MoranProcessGraph(players, graph)
            mp.play()
            winner2 = mp.winning_strategy_name
            self.assertEqual((winner == winner2), outcome)

    def test_asymmetry(self):
        """Asymmetry in interaction and reproduction should sometimes
        produce different results."""
        seeds = [(1, True), (2, True), (8, False), (12, False)]
        players = []
        N = 6
        graph1 = axelrod.graph.cycle(N)
        graph2 = axelrod.graph.complete_graph(N)
        for _ in range(N // 2):
            players.append(axelrod.Cooperator())
        for _ in range(N // 2):
            players.append(axelrod.Defector())
        for seed, outcome in seeds:
            axelrod.seed(seed)
            mp = MoranProcessGraph(players, graph1, graph2)
            mp.play()
            winner = mp.winning_strategy_name
            axelrod.seed(seed)
            mp = MoranProcessGraph(players, graph2, graph1)
            mp.play()
            winner2 = mp.winning_strategy_name
            self.assertEqual((winner == winner2), outcome)
