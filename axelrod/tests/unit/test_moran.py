import itertools
import random
import unittest
from collections import Counter

import axelrod
import matplotlib.pyplot as plt
from axelrod import ApproximateMoranProcess, MoranProcess, Pdf
from axelrod.moran import fitness_proportionate_selection
from axelrod.tests.property import strategy_lists

from hypothesis import example, given, settings

C, D = axelrod.Action.C, axelrod.Action.D


class TestMoranProcess(unittest.TestCase):
    def test_init(self):
        players = axelrod.Cooperator(), axelrod.Defector()
        mp = MoranProcess(players)
        self.assertEqual(mp.turns, axelrod.DEFAULT_TURNS)
        self.assertIsNone(mp.prob_end)
        self.assertIsNone(mp.game)
        self.assertEqual(mp.noise, 0)
        self.assertEqual(mp.initial_players, players)
        self.assertEqual(mp.players, list(players))
        self.assertEqual(mp.populations, [Counter({"Cooperator": 1, "Defector": 1})])
        self.assertIsNone(mp.winning_strategy_name)
        self.assertEqual(mp.mutation_rate, 0)
        self.assertEqual(mp.mode, "bd")
        self.assertEqual(mp.deterministic_cache, axelrod.DeterministicCache())
        self.assertEqual(
            mp.mutation_targets, {"Cooperator": [players[1]], "Defector": [players[0]]}
        )
        self.assertEqual(mp.interaction_graph._edges, [(0, 1), (1, 0)])
        self.assertEqual(mp.reproduction_graph._edges, [(0, 1), (1, 0), (0, 0), (1, 1)])
        self.assertEqual(mp.fitness_transformation, None)
        self.assertEqual(mp.locations, [0, 1])
        self.assertEqual(mp.index, {0: 0, 1: 1})

        # Test non default graph cases
        players = axelrod.Cooperator(), axelrod.Defector(), axelrod.TitForTat()
        edges = [(0, 1), (2, 0), (1, 2)]
        graph = axelrod.graph.Graph(edges, directed=True)
        mp = MoranProcess(players, interaction_graph=graph)
        self.assertEqual(mp.interaction_graph._edges, [(0, 1), (2, 0), (1, 2)])
        self.assertEqual(
            sorted(mp.reproduction_graph._edges),
            sorted([(0, 1), (2, 0), (1, 2), (0, 0), (1, 1), (2, 2)]),
        )

        mp = MoranProcess(players, interaction_graph=graph, reproduction_graph=graph)
        self.assertEqual(mp.interaction_graph._edges, [(0, 1), (2, 0), (1, 2)])
        self.assertEqual(mp.reproduction_graph._edges, [(0, 1), (2, 0), (1, 2)])

    def test_set_players(self):
        """Test that set players resets all players"""
        players = axelrod.Cooperator(), axelrod.Defector()
        mp = MoranProcess(players)
        players[0].history.append(C, D)
        mp.set_players()
        self.assertEqual(players[0].cooperations, 0)

    def test_mutate(self):
        """Test that a mutated player is returned"""
        players = axelrod.Cooperator(), axelrod.Defector(), axelrod.TitForTat()
        mp = MoranProcess(players, mutation_rate=0.5)
        axelrod.seed(0)
        self.assertEqual(mp.mutate(0), players[0])
        axelrod.seed(1)
        self.assertEqual(mp.mutate(0), players[2])
        axelrod.seed(4)
        self.assertEqual(mp.mutate(0), players[1])

    def test_death_in_db(self):
        players = axelrod.Cooperator(), axelrod.Defector(), axelrod.TitForTat()
        mp = MoranProcess(players, mutation_rate=0.5, mode="db")
        axelrod.seed(1)
        self.assertEqual(mp.death(), 0)
        self.assertEqual(mp.dead, 0)
        axelrod.seed(5)
        self.assertEqual(mp.death(), 1)
        self.assertEqual(mp.dead, 1)
        axelrod.seed(2)
        self.assertEqual(mp.death(), 2)
        self.assertEqual(mp.dead, 2)

    def test_death_in_bd(self):
        players = axelrod.Cooperator(), axelrod.Defector(), axelrod.TitForTat()
        edges = [(0, 1), (2, 0), (1, 2)]
        graph = axelrod.graph.Graph(edges, directed=True)
        mp = MoranProcess(players, mode="bd", interaction_graph=graph)
        axelrod.seed(1)
        self.assertEqual(mp.death(0), 0)
        axelrod.seed(5)
        self.assertEqual(mp.death(0), 1)
        axelrod.seed(2)
        self.assertEqual(mp.death(0), 0)

    def test_birth_in_db(self):
        players = axelrod.Cooperator(), axelrod.Defector(), axelrod.TitForTat()
        mp = MoranProcess(players, mode="db")
        axelrod.seed(1)
        self.assertEqual(mp.death(), 0)
        self.assertEqual(mp.birth(0), 2)

    def test_birth_in_bd(self):
        players = axelrod.Cooperator(), axelrod.Defector(), axelrod.TitForTat()
        mp = MoranProcess(players, mode="bd")
        axelrod.seed(1)
        self.assertEqual(mp.birth(), 0)

    def test_fixation_check(self):
        players = axelrod.Cooperator(), axelrod.Cooperator()
        mp = MoranProcess(players)
        self.assertTrue(mp.fixation_check())
        players = axelrod.Cooperator(), axelrod.Defector()
        mp = MoranProcess(players)
        self.assertFalse(mp.fixation_check())

    def test_next(self):
        players = axelrod.Cooperator(), axelrod.Defector()
        mp = MoranProcess(players)
        self.assertIsInstance(next(mp), MoranProcess)

    def test_matchup_indices(self):
        players = axelrod.Cooperator(), axelrod.Defector()
        mp = MoranProcess(players)
        self.assertEqual(mp._matchup_indices(), {(0, 1)})

        players = axelrod.Cooperator(), axelrod.Defector(), axelrod.TitForTat()
        edges = [(0, 1), (2, 0), (1, 2)]
        graph = axelrod.graph.Graph(edges, directed=True)
        mp = MoranProcess(players, mode="bd", interaction_graph=graph)
        self.assertEqual(mp._matchup_indices(), {(0, 1), (1, 2), (2, 0)})

    def test_fps(self):
        self.assertEqual(fitness_proportionate_selection([0, 0, 1]), 2)
        axelrod.seed(1)
        self.assertEqual(fitness_proportionate_selection([1, 1, 1]), 0)
        self.assertEqual(fitness_proportionate_selection([1, 1, 1]), 2)

    def test_exit_condition(self):
        p1, p2 = axelrod.Cooperator(), axelrod.Cooperator()
        mp = MoranProcess((p1, p2))
        mp.play()
        self.assertEqual(len(mp), 1)

    def test_two_players(self):
        p1, p2 = axelrod.Cooperator(), axelrod.Defector()
        axelrod.seed(17)
        mp = MoranProcess((p1, p2))
        populations = mp.play()
        self.assertEqual(len(mp), 5)
        self.assertEqual(len(populations), 5)
        self.assertEqual(populations, mp.populations)
        self.assertEqual(mp.winning_strategy_name, str(p2))

    def test_two_prob_end(self):
        p1, p2 = axelrod.Random(), axelrod.TitForTat()
        axelrod.seed(0)
        mp = MoranProcess((p1, p2), prob_end=0.5)
        populations = mp.play()
        self.assertEqual(len(mp), 4)
        self.assertEqual(len(populations), 4)
        self.assertEqual(populations, mp.populations)
        self.assertEqual(mp.winning_strategy_name, str(p1))

    def test_different_game(self):
        # Possible for Cooperator to become fixed when using a different game
        p1, p2 = axelrod.Cooperator(), axelrod.Defector()
        axelrod.seed(0)
        game = axelrod.Game(r=4, p=2, s=1, t=6)
        mp = MoranProcess((p1, p2), turns=5, game=game)
        populations = mp.play()
        self.assertEqual(mp.winning_strategy_name, str(p1))

    def test_death_birth(self):
        """Two player death-birth should fixate after one round."""
        p1, p2 = axelrod.Cooperator(), axelrod.Defector()
        seeds = range(0, 20)
        for seed in seeds:
            axelrod.seed(seed)
            mp = MoranProcess((p1, p2), mode="db")
            mp.play()
        self.assertIsNotNone(mp.winning_strategy_name)
        # Number of populations is 2: the original and the one after the first round.
        self.assertEqual(len(mp.populations), 2)

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
            mp = MoranProcess(players, mode="bd")
            mp.play()
            winner = mp.winning_strategy_name
            axelrod.seed(seed)
            mp = MoranProcess(players, mode="db")
            mp.play()
            winner2 = mp.winning_strategy_name
            self.assertEqual((winner == winner2), outcome)

    def test_two_random_players(self):
        p1, p2 = axelrod.Random(p=0.5), axelrod.Random(p=0.25)
        axelrod.seed(0)
        mp = MoranProcess((p1, p2))
        populations = mp.play()
        self.assertEqual(len(mp), 2)
        self.assertEqual(len(populations), 2)
        self.assertEqual(populations, mp.populations)
        self.assertEqual(mp.winning_strategy_name, str(p2))

    def test_two_players_with_mutation(self):
        p1, p2 = axelrod.Cooperator(), axelrod.Defector()
        axelrod.seed(5)
        mp = MoranProcess((p1, p2), mutation_rate=0.2, stop_on_fixation=False)
        self.assertDictEqual(mp.mutation_targets, {str(p1): [p2], str(p2): [p1]})
        # Test that mutation causes the population to alternate between
        # fixations
        counters = [
            Counter({"Cooperator": 2}),
            Counter({"Defector": 2}),
            Counter({"Cooperator": 2}),
            Counter({"Defector": 2}),
        ]
        for counter in counters:
            for _ in itertools.takewhile(
                lambda x: x.population_distribution() != counter, mp
            ):
                pass
            self.assertEqual(mp.population_distribution(), counter)

    def test_play_exception(self):
        p1, p2 = axelrod.Cooperator(), axelrod.Defector()
        mp = MoranProcess((p1, p2), mutation_rate=0.2)
        with self.assertRaises(ValueError):
            mp.play()

    def test_three_players(self):
        players = [axelrod.Cooperator(), axelrod.Cooperator(), axelrod.Defector()]
        axelrod.seed(11)
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
        mp = MoranProcess(players, mutation_rate=0.2, stop_on_fixation=False)
        self.assertDictEqual(
            mp.mutation_targets,
            {str(p1): [p3, p2], str(p2): [p1, p3], str(p3): [p1, p2]},
        )
        # Test that mutation causes the population to alternate between
        # fixations
        counters = [Counter({"Cooperator": 3}), Counter({"Defector": 3})]
        for counter in counters:
            for _ in itertools.takewhile(
                lambda x: x.population_distribution() != counter, mp
            ):
                pass
            self.assertEqual(mp.population_distribution(), counter)

    def test_four_players(self):
        players = [axelrod.Cooperator() for _ in range(3)]
        players.append(axelrod.Defector())
        axelrod.seed(29)
        mp = MoranProcess(players)
        populations = mp.play()
        self.assertEqual(len(mp), 9)
        self.assertEqual(len(populations), 9)
        self.assertEqual(populations, mp.populations)
        self.assertEqual(mp.winning_strategy_name, str(axelrod.Defector()))

    @given(strategies=strategy_lists(min_size=2, max_size=4))
    @settings(max_examples=5)

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
        axelrod.seed(45)
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

    def test_constant_fitness_case(self):
        # Scores between an Alternator and Defector will be: (1,  6)
        axelrod.seed(0)
        players = (
            axelrod.Alternator(),
            axelrod.Alternator(),
            axelrod.Defector(),
            axelrod.Defector(),
        )
        mp = MoranProcess(players, turns=2)
        winners = []
        for _ in range(100):
            mp.play()
            winners.append(mp.winning_strategy_name)
            mp.reset()
        winners = Counter(winners)
        self.assertEqual(winners["Defector"], 88)

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

    def test_population_plot(self):
        # Test that can plot on a given matplotlib axes
        axelrod.seed(15)
        players = [random.choice(axelrod.demo_strategies)() for _ in range(5)]
        mp = axelrod.MoranProcess(players=players, turns=30)
        mp.play()
        fig, axarr = plt.subplots(2, 2)
        ax = axarr[1, 0]
        mp.populations_plot(ax=ax)
        self.assertEqual(ax.get_xlim(), (-0.8, 16.8))
        self.assertEqual(ax.get_ylim(), (0, 5.25))
        # Run without a given axis
        ax = mp.populations_plot()
        self.assertEqual(ax.get_xlim(), (-0.8, 16.8))
        self.assertEqual(ax.get_ylim(), (0, 5.25))

    def test_cooperator_can_win_with_fitness_transformation(self):
        axelrod.seed(689)
        players = (
            axelrod.Cooperator(),
            axelrod.Defector(),
            axelrod.Defector(),
            axelrod.Defector(),
        )
        w = 0.95
        fitness_transformation = lambda score: 1 - w + w * score
        mp = MoranProcess(
            players, turns=10, fitness_transformation=fitness_transformation
        )
        populations = mp.play()
        self.assertEqual(mp.winning_strategy_name, "Cooperator")

    def test_atomic_mutation_fsm(self):
        axelrod.seed(12)
        players = [axelrod.EvolvableFSMPlayer(num_states=2, initial_state=1, initial_action=C)
                   for _ in range(5)]
        mp = MoranProcess(players, turns=10, mutation_method="atomic")
        population = mp.play()
        self.assertEqual(
            mp.winning_strategy_name,
            'Evolvable FSM Player: ((0, C, 1, D), (0, D, 1, C), (1, C, 0, D), (1, D, 1, C)), 1, C, 2, 0.1')
        self.assertEqual(len(mp.populations), 31)
        self.assertTrue(mp.fixated)

    def test_atomic_mutation_cycler(self):
        axelrod.seed(10)
        cycle_length = 5
        players = [axelrod.EvolvableCycler(cycle_length=cycle_length)
                   for _ in range(5)]
        mp = MoranProcess(players, turns=10, mutation_method="atomic")
        population = mp.play()
        self.assertEqual(mp.winning_strategy_name, 'EvolvableCycler: CDCDD, 5, 0.2, 1')
        self.assertEqual(len(mp.populations), 19)
        self.assertTrue(mp.fixated)

    def test_mutation_method_exception(self):
        axelrod.seed(10)
        cycle_length = 5
        players = [axelrod.EvolvableCycler(cycle_length=cycle_length)
                   for _ in range(5)]
        with self.assertRaises(ValueError):
            MoranProcess(players, turns=10, mutation_method="random")


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
            mp = MoranProcess(players, interaction_graph=graph)
            mp.play()
            winner2 = mp.winning_strategy_name
            self.assertEqual(winner, winner2)

    def test_cycle(self):
        """A cycle should sometimes produce different results vs. the default
        case."""
        seeds = [(1, True), (8, False)]
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
            mp = MoranProcess(players, interaction_graph=graph)
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
            mp = MoranProcess(
                players, interaction_graph=graph1, reproduction_graph=graph2
            )
            mp.play()
            winner = mp.winning_strategy_name
            axelrod.seed(seed)
            mp = MoranProcess(
                players, interaction_graph=graph2, reproduction_graph=graph1
            )
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
            mp = MoranProcess(players, interaction_graph=graph, mode="bd")
            mp.play()
            winner = mp.winning_strategy_name
            axelrod.seed(seed)
            mp = MoranProcess(players, interaction_graph=graph, mode="db")
            mp.play()
            winner2 = mp.winning_strategy_name
            self.assertEqual((winner == winner2), outcome)


class TestApproximateMoranProcess(unittest.TestCase):
    """A suite of tests for the ApproximateMoranProcess"""

    players = [axelrod.Cooperator(), axelrod.Defector()]
    cached_outcomes = {}

    counter = Counter([(0, 5)])
    pdf = Pdf(counter)
    cached_outcomes[("Cooperator", "Defector")] = pdf

    counter = Counter([(3, 3)])
    pdf = Pdf(counter)
    cached_outcomes[("Cooperator", "Cooperator")] = pdf

    counter = Counter([(1, 1)])
    pdf = Pdf(counter)
    cached_outcomes[("Defector", "Defector")] = pdf

    amp = ApproximateMoranProcess(players, cached_outcomes)

    def test_init(self):
        """Test the initialisation process"""
        self.assertEqual(
            set(self.amp.cached_outcomes.keys()),
            {("Cooperator", "Defector"), ("Cooperator", "Cooperator"), ("Defector", "Defector")},
        )
        self.assertEqual(self.amp.players, self.players)
        self.assertEqual(self.amp.turns, 0)
        self.assertEqual(self.amp.noise, 0)

    def test_score_all(self):
        """Test the score_all function of the Moran process"""
        scores = self.amp.score_all()
        self.assertEqual(scores, [0, 5])
        scores = self.amp.score_all()
        self.assertEqual(scores, [0, 5])
        scores = self.amp.score_all()
        self.assertEqual(scores, [0, 5])

    def test_getting_scores_from_cache(self):
        """Test that read of scores from cache works (independent of ordering of
        player names"""
        scores = self.amp._get_scores_from_cache(("Cooperator", "Defector"))
        self.assertEqual(scores, (0, 5))
        scores = self.amp._get_scores_from_cache(("Defector", "Cooperator"))
        self.assertEqual(scores, (5, 0))
