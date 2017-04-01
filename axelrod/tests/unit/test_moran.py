from collections import Counter
import itertools
import random
import unittest

from hypothesis import given, example, settings

import axelrod
from axelrod import (Match, MoranProcess,
                     ApproximateMoranProcess, MoranProcessGraph)
from axelrod.moran import fitness_proportionate_selection, Pdf
from axelrod.tests.property import strategy_lists


class MockMatch(object):
    """Mock Match class to always return the same score for testing purposes."""

    def __init__(self, players, *args, **kwargs):
        self.players = players
        score_dict = {"Cooperator": 2, "Defector": 1}
        self.score_dict = score_dict

    def play(self):
        pass

    def final_score_per_turn(self):
        s = (self.score_dict[str(self.players[0])],
             self.score_dict[str(self.players[1])])
        return s


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

    def test_death_birth(self):
        """Two player death-birth should fixate after one round."""
        p1, p2 = axelrod.Cooperator(), axelrod.Defector()
        seeds = range(0, 20)
        for seed in seeds:
            random.seed(seed)
            mp = MoranProcess((p1, p2), mode='db')
            next(mp)
            self.assertIsNotNone(mp.winning_strategy_name)

    def test_death_birth_outcomes(self):
        """Show that birth-death and death-birth can produce different
        outcomes."""
        seeds = [(1, True), (23, False)]
        players = []
        N = 6
        for _ in range(N // 2):
            players.append(axelrod.Cooperator())
            players.append(axelrod.Defector())
        for seed, outcome in seeds:
            axelrod.seed(seed)
            mp = MoranProcess(players, mode='bd')
            mp.play()
            winner = mp.winning_strategy_name
            axelrod.seed(seed)
            mp = MoranProcess(players, mode='db')
            mp.play()
            winner2 = mp.winning_strategy_name
            self.assertEqual((winner == winner2), outcome)

    def test_two_random_players(self):
        p1, p2 = axelrod.Random(p=0.5), axelrod.Random(p=0.25)
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
        self.assertDictEqual(mp.mutation_targets,
                             {str(p1): [p2], str(p2): [p1]})
        # Test that mutation causes the population to alternate between
        # fixations
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
        self.assertDictEqual(mp.mutation_targets, {
            str(p1): [p3, p2], str(p2): [p1, p3], str(p3): [p1, p2]})
        # Test that mutation causes the population to alternate between
        # fixations
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

    def test_standard_fixation(self):
        """Test a traditional Moran process with a MockMatch."""
        axelrod.seed(0)
        players = (axelrod.Cooperator(), axelrod.Cooperator(),
                   axelrod.Defector(), axelrod.Defector())
        mp = MoranProcess(players, match_class=MockMatch)
        winners = []
        for i in range(100):
            mp.play()
            winner = mp.winning_strategy_name
            winners.append(winner)
            mp.reset()
        winners = Counter(winners)
        self.assertEqual(winners["Cooperator"], 82)

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
        seeds = [(1, True), (13, False)]
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
        seeds = [(1, True), (21, False)]
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

    def test_cycle_death_birth(self):
        """Test that death-birth can have different outcomes in the graph
        case."""
        seeds = [(1, True), (5, False)]
        players = []
        N = 6
        graph = axelrod.graph.cycle(N)
        for _ in range(N // 2):
            players.append(axelrod.Cooperator())
        for _ in range(N // 2):
            players.append(axelrod.Defector())
        for seed, outcome in seeds:
            axelrod.seed(seed)
            mp = MoranProcessGraph(players, graph, mode='bd')
            mp.play()
            winner = mp.winning_strategy_name
            axelrod.seed(seed)
            mp = MoranProcessGraph(players, graph, mode='db')
            mp.play()
            winner2 = mp.winning_strategy_name
            self.assertEqual((winner == winner2), outcome)


class TestPdf(unittest.TestCase):
    """A suite of tests for the Pdf class"""
    observations = [('C', 'D')] * 4 + [('C', 'C')] * 12 + \
                   [('D', 'C')] * 2 + [('D', 'D')] * 15
    counter = Counter(observations)
    pdf = Pdf(counter)

    def test_init(self):
        self.assertEqual(set(self.pdf.sample_space), set(self.counter.keys()))
        self.assertEqual(set(self.pdf.counts), set([4, 12, 2, 15]))
        self.assertEqual(self.pdf.total, sum([4, 12, 2, 15]))
        self.assertAlmostEqual(sum(self.pdf.probability), 1)

    def test_sample(self):
        """Test that sample maps to correct domain"""
        all_samples = []

        axelrod.seed(0)
        for sample in range(100):
            all_samples.append(self.pdf.sample())

        self.assertEqual(len(all_samples), 100)
        self.assertEqual(set(all_samples), set(self.observations))

    def test_seed(self):
        """Test that numpy seeds the sample properly"""

        for seed in range(10):
            axelrod.seed(seed)
            sample = self.pdf.sample()
            axelrod.seed(seed)
            self.assertEqual(sample, self.pdf.sample())


class TestApproximateMoranProcess(unittest.TestCase):
    """A suite of tests for the ApproximateMoranProcess"""
    players = [axelrod.Cooperator(), axelrod.Defector()]
    cached_outcomes = {}

    counter = Counter([(0, 5)])
    pdf = Pdf(counter)
    cached_outcomes[('Cooperator', 'Defector')] = pdf

    counter = Counter([(3, 3)])
    pdf = Pdf(counter)
    cached_outcomes[('Cooperator', 'Cooperator')] = pdf

    counter = Counter([(1, 1)])
    pdf = Pdf(counter)
    cached_outcomes[('Defector', 'Defector')] = pdf

    amp = ApproximateMoranProcess(players, cached_outcomes)

    def test_init(self):
        """Test the initialisation process"""
        self.assertEqual(set(self.amp.cached_outcomes.keys()),
                         set([('Cooperator', 'Defector'),
                              ('Cooperator', 'Cooperator'),
                              ('Defector', 'Defector')]))
        self.assertEqual(self.amp.players, self.players)
        self.assertEqual(self.amp.turns, 0)
        self.assertEqual(self.amp.noise, 0)

    def test_next(self):
        """Test the next function of the Moran process"""
        scores = self.amp._play_next_round()
        self.assertEqual(scores, [0, 5])
        scores = self.amp._play_next_round()
        self.assertEqual(scores, [0, 5])
        scores = self.amp._play_next_round()
        self.assertEqual(scores, [0, 5])

    def test_getting_scores_from_cache(self):
        """Test that read of scores from cache works (independent of ordering of
        player names"""
        scores = self.amp._get_scores_from_cache(("Cooperator", "Defector"))
        self.assertEqual(scores, (0, 5))
        scores = self.amp._get_scores_from_cache(("Defector", "Cooperator"))
        self.assertEqual(scores, (5, 0))
