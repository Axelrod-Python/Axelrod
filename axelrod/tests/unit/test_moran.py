import itertools
import unittest
from collections import Counter

import matplotlib.pyplot as plt
from hypothesis import example, given, settings
from hypothesis.strategies import integers

import axelrod as axl
from axelrod import MoranProcess
from axelrod.tests.property import strategy_lists

C, D = axl.Action.C, axl.Action.D
random = axl.RandomGenerator()


class TestMoranProcess(unittest.TestCase):
    def test_init(self):
        players = axl.Cooperator(), axl.Defector()
        mp = axl.MoranProcess(players)
        self.assertEqual(mp.turns, axl.DEFAULT_TURNS)
        self.assertIsNone(mp.prob_end)
        self.assertIsNone(mp.game)
        self.assertEqual(mp.noise, 0)
        self.assertEqual(mp.initial_players, players)
        self.assertEqual(mp.players, list(players))
        self.assertEqual(
            mp.populations, [Counter({"Cooperator": 1, "Defector": 1})]
        )
        self.assertIsNone(mp.winning_strategy_name)
        self.assertEqual(mp.mutation_rate, 0)
        self.assertEqual(mp.mode, "bd")
        self.assertEqual(mp.deterministic_cache, axl.DeterministicCache())
        self.assertEqual(
            mp.mutation_targets,
            {"Cooperator": [players[1]], "Defector": [players[0]]},
        )
        self.assertEqual(mp.interaction_graph._edges, [(0, 1), (1, 0)])
        self.assertEqual(
            mp.reproduction_graph._edges, [(0, 1), (1, 0), (0, 0), (1, 1)]
        )
        self.assertEqual(mp.fitness_transformation, None)
        self.assertEqual(mp.locations, [0, 1])
        self.assertEqual(mp.index, {0: 0, 1: 1})

        # Test non default graph cases
        players = axl.Cooperator(), axl.Defector(), axl.TitForTat()
        edges = [(0, 1), (2, 0), (1, 2)]
        graph = axl.graph.Graph(edges, directed=True)
        mp = axl.MoranProcess(players, interaction_graph=graph)
        self.assertEqual(mp.interaction_graph._edges, [(0, 1), (2, 0), (1, 2)])
        self.assertEqual(
            sorted(mp.reproduction_graph._edges),
            sorted([(0, 1), (2, 0), (1, 2), (0, 0), (1, 1), (2, 2)]),
        )

        mp = axl.MoranProcess(
            players, interaction_graph=graph, reproduction_graph=graph
        )
        self.assertEqual(mp.interaction_graph._edges, [(0, 1), (2, 0), (1, 2)])
        self.assertEqual(mp.reproduction_graph._edges, [(0, 1), (2, 0), (1, 2)])

    def test_set_players(self):
        """Test that set players resets all players"""
        players = axl.Cooperator(), axl.Defector()
        mp = axl.MoranProcess(players)
        players[0].history.append(C, D)
        mp.set_players()
        self.assertEqual(players[0].cooperations, 0)

    def test_mutate(self):
        """Test that a mutated player is returned"""
        players = axl.Cooperator(), axl.Defector(), axl.TitForTat()
        mp = MoranProcess(players, mutation_rate=0.5, seed=0)
        self.assertEqual(mp.mutate(0), players[0])
        mp = MoranProcess(players, mutation_rate=0.5, seed=2)
        self.assertEqual(mp.mutate(0), players[2])
        mp = MoranProcess(players, mutation_rate=0.5, seed=7)
        self.assertEqual(mp.mutate(0), players[1])

    def test_death_in_db(self):
        players = axl.Cooperator(), axl.Defector(), axl.TitForTat()
        mp = MoranProcess(players, mutation_rate=0.5, mode="db", seed=1)
        self.assertEqual(mp.death(), 2)
        self.assertEqual(mp.dead, 2)
        mp = MoranProcess(players, mutation_rate=0.5, mode="db", seed=2)
        self.assertEqual(mp.death(), 0)
        self.assertEqual(mp.dead, 0)
        mp = MoranProcess(players, mutation_rate=0.5, mode="db", seed=9)
        self.assertEqual(mp.death(), 1)
        self.assertEqual(mp.dead, 1)

    def test_death_in_bd(self):
        players = axl.Cooperator(), axl.Defector(), axl.TitForTat()
        edges = [(0, 1), (2, 0), (1, 2)]
        graph = axl.graph.Graph(edges, directed=True)
        mp = MoranProcess(players, mode="bd", interaction_graph=graph, seed=1)
        self.assertEqual(mp.death(0), 1)
        mp = MoranProcess(players, mode="bd", interaction_graph=graph, seed=2)
        self.assertEqual(mp.death(0), 1)
        mp = MoranProcess(players, mode="bd", interaction_graph=graph, seed=3)
        self.assertEqual(mp.death(0), 0)

    def test_birth_in_db(self):
        players = axl.Cooperator(), axl.Defector(), axl.TitForTat()
        mp = MoranProcess(players, mode="db", seed=1)
        self.assertEqual(mp.death(), 2)
        self.assertEqual(mp.birth(0), 2)

    def test_birth_in_bd(self):
        players = axl.Cooperator(), axl.Defector(), axl.TitForTat()
        mp = MoranProcess(players, mode="bd", seed=2)
        self.assertEqual(mp.birth(), 0)

    def test_fixation_check(self):
        players = axl.Cooperator(), axl.Cooperator()
        mp = axl.MoranProcess(players)
        self.assertTrue(mp.fixation_check())
        players = axl.Cooperator(), axl.Defector()
        mp = axl.MoranProcess(players)
        self.assertFalse(mp.fixation_check())

    def test_next(self):
        players = axl.Cooperator(), axl.Defector()
        mp = axl.MoranProcess(players)
        self.assertIsInstance(next(mp), axl.MoranProcess)

    def test_matchup_indices(self):
        players = axl.Cooperator(), axl.Defector()
        mp = axl.MoranProcess(players)
        self.assertEqual(mp._matchup_indices(), {(0, 1)})

        players = axl.Cooperator(), axl.Defector(), axl.TitForTat()
        edges = [(0, 1), (2, 0), (1, 2)]
        graph = axl.graph.Graph(edges, directed=True)
        mp = axl.MoranProcess(players, mode="bd", interaction_graph=graph)
        self.assertEqual(mp._matchup_indices(), {(0, 1), (1, 2), (2, 0)})

    def test_fps(self):
        players = axl.Cooperator(), axl.Defector()
        mp = MoranProcess(players, seed=1)
        self.assertEqual(mp.fitness_proportionate_selection([0, 0, 1]), 2)
        self.assertEqual(mp.fitness_proportionate_selection([1, 1, 1]), 2)
        self.assertEqual(mp.fitness_proportionate_selection([1, 1, 1]), 0)

    def test_exit_condition(self):
        p1, p2 = axl.Cooperator(), axl.Cooperator()
        mp = axl.MoranProcess((p1, p2))
        mp.play()
        self.assertEqual(len(mp), 1)

    @given(seed=integers(min_value=1, max_value=4294967295))
    @settings(max_examples=5, deadline=None)
    def test_seeding_equality(self, seed):
        players = [axl.Random(x) for x in (0.2, 0.4, 0.6, 0.8)]
        mp1 = MoranProcess(players, seed=seed)
        mp1.play()
        mp2 = MoranProcess(players, seed=seed)
        mp2.play()
        self.assertEqual(mp1.populations, mp2.populations)

    def test_seeding_inequality(self):
        players = [axl.Random(x) for x in (0.2, 0.4, 0.6, 0.8)]
        mp1 = MoranProcess(players, seed=0)
        mp1.play()
        mp2 = MoranProcess(players, seed=1)
        mp2.play()
        self.assertNotEqual(mp1, mp2)

    def test_two_players(self):
        p1, p2 = axl.Cooperator(), axl.Defector()
        mp = MoranProcess((p1, p2), seed=99)
        populations = mp.play()
        self.assertEqual(len(mp), 2)
        self.assertEqual(len(populations), 2)
        self.assertEqual(populations, mp.populations)
        self.assertEqual(mp.winning_strategy_name, str(p2))

    def test_two_prob_end(self):
        p1, p2 = axl.Random(), axl.TitForTat()
        mp = MoranProcess((p1, p2), prob_end=0.5, seed=10)
        populations = mp.play()
        self.assertEqual(len(mp), 2)
        self.assertEqual(len(populations), 2)
        self.assertEqual(populations, mp.populations)
        self.assertEqual(mp.winning_strategy_name, str(p1))

    def test_different_game(self):
        # Possible for Cooperator to become fixed when using a different game
        p1, p2 = axl.Cooperator(), axl.Defector()
        game = axl.Game(r=4, p=2, s=1, t=6)
        mp = MoranProcess((p1, p2), turns=5, game=game, seed=3)
        populations = mp.play()
        self.assertEqual(mp.winning_strategy_name, str(p1))

    def test_different_match(self):
        """Test alternative Match class, mainly to show that the results are different
        than the results of `test_different_game` where the same seed is used.
        """

        # Using a different game where the scores are all constant
        class StandInMatch(axl.Match):
            """A Match were all players get a score of 3"""

            def final_score_per_turn(self):
                return 0, 3

        p1, p2 = axl.Cooperator(), axl.Defector()
        game = axl.Game(r=4, p=2, s=1, t=6)
        mp = MoranProcess(
            (p1, p2), turns=5, game=game, match_class=StandInMatch, seed=3
        )
        populations = mp.play()
        self.assertEqual(mp.winning_strategy_name, str(p2))

    def test_death_birth(self):
        """Two player death-birth should fixate after one round."""
        p1, p2 = axl.Cooperator(), axl.Defector()
        seeds = range(0, 20)
        for seed in seeds:
            mp = MoranProcess((p1, p2), mode="db", seed=seed)
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
            players.append(axl.Cooperator())
            players.append(axl.Defector())
        for seed, outcome in seeds:
            mp = MoranProcess(players, mode="bd", seed=seed)
            mp.play()
            winner = mp.winning_strategy_name
            mp = MoranProcess(players, mode="db", seed=seed)
            mp.play()
            winner2 = mp.winning_strategy_name
            self.assertEqual((winner == winner2), outcome)

    def test_two_random_players(self):
        p1, p2 = axl.Random(p=0.5), axl.Random(p=0.25)
        mp = MoranProcess((p1, p2), seed=66)
        populations = mp.play()
        self.assertEqual(len(mp), 2)
        self.assertEqual(len(populations), 2)
        self.assertEqual(populations, mp.populations)
        self.assertEqual(mp.winning_strategy_name, str(p1))

    def test_two_players_with_mutation(self):
        p1, p2 = axl.Cooperator(), axl.Defector()
        mp = MoranProcess(
            (p1, p2), mutation_rate=0.2, stop_on_fixation=False, seed=5
        )
        self.assertDictEqual(
            mp.mutation_targets, {str(p1): [p2], str(p2): [p1]}
        )
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
        p1, p2 = axl.Cooperator(), axl.Defector()
        mp = axl.MoranProcess((p1, p2), mutation_rate=0.2)
        with self.assertRaises(ValueError):
            mp.play()

    def test_three_players(self):
        players = [axl.Cooperator(), axl.Cooperator(), axl.Defector()]
        mp = MoranProcess(players, seed=11)
        populations = mp.play()
        self.assertEqual(len(mp), 7)
        self.assertEqual(len(populations), 7)
        self.assertEqual(populations, mp.populations)
        self.assertEqual(mp.winning_strategy_name, str(axl.Defector()))

    def test_three_players_with_mutation(self):
        p1 = axl.Cooperator()
        p2 = axl.Random()
        p3 = axl.Defector()
        players = [p1, p2, p3]
        mp = axl.MoranProcess(
            players, mutation_rate=0.2, stop_on_fixation=False
        )
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
        players = [axl.Cooperator() for _ in range(3)]
        players.append(axl.Defector())
        mp = MoranProcess(players, seed=29)
        populations = mp.play()
        self.assertEqual(len(mp), 8)
        self.assertEqual(len(populations), 8)
        self.assertEqual(populations, mp.populations)
        self.assertEqual(mp.winning_strategy_name, str(axl.Defector()))

    @given(strategies=strategy_lists(min_size=2, max_size=4))
    @settings(max_examples=5, deadline=None)
    # A specific example relating to cloning of strategies
    @example(strategies=[axl.ThueMorse, axl.BackStabber])
    def test_property_players(self, strategies):
        """Hypothesis test that randomly checks players"""
        players = [s() for s in strategies]
        mp = axl.MoranProcess(players)
        populations = mp.play()
        self.assertEqual(populations, mp.populations)
        self.assertIn(mp.winning_strategy_name, [str(p) for p in players])

    def test_reset(self):
        p1, p2 = axl.Cooperator(), axl.Defector()
        mp = MoranProcess((p1, p2), seed=45)
        mp.play()
        self.assertEqual(len(mp), 2)
        self.assertEqual(len(mp.score_history), 1)
        mp.reset()
        self.assertEqual(len(mp), 1)
        self.assertEqual(mp.winning_strategy_name, None)
        self.assertEqual(mp.score_history, [])
        # Check that players reset
        for player, initial_player in zip(mp.players, mp.initial_players):
            self.assertEqual(str(player), str(initial_player))

    def test_constant_fitness_case(self):
        # Scores between an Alternator and Defector will be: (1,  6)
        players = (
            axl.Alternator(),
            axl.Alternator(),
            axl.Defector(),
            axl.Defector(),
        )
        mp = MoranProcess(players, turns=2, seed=0)
        winners = []
        for _ in range(100):
            mp.play()
            winners.append(mp.winning_strategy_name)
            mp.reset()
        winners = Counter(winners)
        self.assertEqual(winners["Defector"], 86)

    def test_cache(self):
        p1, p2 = axl.Cooperator(), axl.Defector()
        mp = axl.MoranProcess((p1, p2))
        mp.play()
        self.assertEqual(len(mp.deterministic_cache), 1)

        # Check that can pass a pre-built cache
        cache = axl.DeterministicCache()
        mp = axl.MoranProcess((p1, p2), deterministic_cache=cache)
        self.assertEqual(cache, mp.deterministic_cache)

    def test_iter(self):
        p1, p2 = axl.Cooperator(), axl.Defector()
        mp = axl.MoranProcess((p1, p2))
        self.assertEqual(mp.__iter__(), mp)

    def test_population_plot(self):
        # Test that can plot on a given matplotlib axes
        rng = axl.RandomGenerator(seed=15)
        players = [rng.choice(axl.demo_strategies)() for _ in range(5)]
        mp = axl.MoranProcess(players=players, turns=30, seed=20)
        mp.play()
        fig, axarr = plt.subplots(2, 2)
        ax = axarr[1, 0]
        mp.populations_plot(ax=ax)
        self.assertEqual(ax.get_xlim(), (-0.7000000000000001, 14.7))
        self.assertEqual(ax.get_ylim(), (0, 5.25))
        # Run without a given axis
        ax = mp.populations_plot()
        self.assertEqual(ax.get_xlim(), (-0.7000000000000001, 14.7))
        self.assertEqual(ax.get_ylim(), (0, 5.25))

    def test_cooperator_can_win_with_fitness_transformation(self):
        players = (
            axl.Cooperator(),
            axl.Defector(),
            axl.Defector(),
            axl.Defector(),
        )
        w = 0.95
        fitness_transformation = lambda score: 1 - w + w * score
        mp = MoranProcess(
            players,
            turns=10,
            fitness_transformation=fitness_transformation,
            seed=3419,
        )
        populations = mp.play()
        self.assertEqual(mp.winning_strategy_name, "Cooperator")

    def test_atomic_mutation_fsm(self):
        players = [
            axl.EvolvableFSMPlayer(
                num_states=2, initial_state=1, initial_action=C, seed=4
            )
            for _ in range(5)
        ]
        mp = MoranProcess(players, turns=10, mutation_method="atomic", seed=12)
        rounds = 10
        for _ in range(rounds):
            next(mp)
        self.assertEqual(
            list(sorted(mp.populations[-1].items()))[0][0],
            "EvolvableFSMPlayer: ((0, C, 0, C), (0, D, 1, C), (1, C, 1, D), (1, D, 1, D)), 0, D, 2, 0.1, 2240802643",
        )
        self.assertEqual(len(mp.populations), 11)
        self.assertFalse(mp.fixated)

    def test_atomic_mutation_cycler(self):
        cycle_length = 5
        players = [
            axl.EvolvableCycler(cycle_length=cycle_length, seed=4)
            for _ in range(5)
        ]
        mp = MoranProcess(players, turns=10, mutation_method="atomic", seed=10)
        rounds = 10
        for _ in range(rounds):
            next(mp)
        self.assertEqual(
            list(mp.populations[-1].items())[0],
            ("EvolvableCycler: CCDDD, 5, 0.2, 1, 1164244177", 1),
        )
        self.assertEqual(len(mp.populations), 11)
        self.assertFalse(mp.fixated)

    def test_mutation_method_exceptions(self):
        cycle_length = 5
        players = [
            axl.EvolvableCycler(cycle_length=cycle_length, seed=4)
            for _ in range(5)
        ]
        with self.assertRaises(ValueError):
            MoranProcess(players, turns=10, mutation_method="random", seed=10)

        players = [
            axl.Cycler(cycle="CD" * random.randint(2, 10)) for _ in range(10)
        ]
        mp = MoranProcess(players, turns=10, mutation_method="atomic", seed=53)
        with self.assertRaises(TypeError):
            for _ in range(10):
                next(mp)


class GraphMoranProcess(unittest.TestCase):
    def test_complete(self):
        """A complete graph should produce the same results as the default
        case."""
        seeds = range(0, 5)
        players = []
        N = 6
        interaction_graph = axl.graph.complete_graph(N, loops=False)
        reproduction_graph = axl.graph.Graph(
            interaction_graph.edges, directed=interaction_graph.directed
        )
        reproduction_graph.add_loops()

        for _ in range(N // 2):
            players.append(axl.Cooperator())
            players.append(axl.Defector())
        for seed in seeds:
            mp = MoranProcess(players, seed=seed)
            mp.play()
            winner = mp.winning_strategy_name
            mp = MoranProcess(
                players,
                interaction_graph=interaction_graph,
                reproduction_graph=reproduction_graph,
                seed=seed,
            )
            mp.play()
            winner2 = mp.winning_strategy_name
            self.assertEqual(winner, winner2)

    def test_cycle(self):
        """A cycle should sometimes produce different results vs. the default
        case."""
        seeds = [(1, True), (3, False)]
        players = []
        N = 6
        graph = axl.graph.cycle(N)
        for _ in range(N // 2):
            players.append(axl.Cooperator())
        for _ in range(N // 2):
            players.append(axl.Defector())
        for seed, outcome in seeds:
            mp = MoranProcess(players, seed=seed)
            mp.play()
            winner = mp.winning_strategy_name
            mp = MoranProcess(players, interaction_graph=graph, seed=seed)
            mp.play()
            winner2 = mp.winning_strategy_name
            self.assertEqual((winner == winner2), outcome)

    def test_asymmetry(self):
        """Asymmetry in interaction and reproduction should sometimes
        produce different results."""
        seeds = [(1, True), (5, False)]
        players = []
        N = 6
        graph1 = axl.graph.cycle(N)
        graph2 = axl.graph.complete_graph(N)
        for _ in range(N // 2):
            players.append(axl.Cooperator())
        for _ in range(N // 2):
            players.append(axl.Defector())
        for seed, outcome in seeds:
            mp = MoranProcess(
                players,
                interaction_graph=graph1,
                reproduction_graph=graph2,
                seed=seed,
            )
            mp.play()
            winner = mp.winning_strategy_name
            mp = MoranProcess(
                players,
                interaction_graph=graph2,
                reproduction_graph=graph1,
                seed=seed,
            )
            mp.play()
            winner2 = mp.winning_strategy_name
            self.assertEqual((winner == winner2), outcome)

    def test_cycle_death_birth(self):
        """Test that death-birth can have different outcomes in the graph
        case."""
        seeds = [(1, True), (3, False)]
        players = []
        N = 6
        graph = axl.graph.cycle(N)
        for _ in range(N // 2):
            players.append(axl.Cooperator())
        for _ in range(N // 2):
            players.append(axl.Defector())
        for seed, outcome in seeds:
            mp = MoranProcess(
                players, interaction_graph=graph, mode="bd", seed=seed
            )
            mp.play()
            winner = mp.winning_strategy_name
            mp = MoranProcess(
                players, interaction_graph=graph, mode="db", seed=seed
            )
            mp.play()
            winner2 = mp.winning_strategy_name
            self.assertEqual((winner == winner2), outcome)


class TestApproximateMoranProcess(unittest.TestCase):
    """A suite of tests for the ApproximateMoranProcess"""

    players = [axl.Cooperator(), axl.Defector()]
    cached_outcomes = {}

    counter = Counter([(0, 5)])
    pdf = axl.Pdf(counter)
    cached_outcomes[("Cooperator", "Defector")] = pdf

    counter = Counter([(3, 3)])
    pdf = axl.Pdf(counter)
    cached_outcomes[("Cooperator", "Cooperator")] = pdf

    counter = Counter([(1, 1)])
    pdf = axl.Pdf(counter)
    cached_outcomes[("Defector", "Defector")] = pdf

    amp = axl.ApproximateMoranProcess(players, cached_outcomes)

    def test_init(self):
        """Test the initialisation process"""
        self.assertEqual(
            set(self.amp.cached_outcomes.keys()),
            {
                ("Cooperator", "Defector"),
                ("Cooperator", "Cooperator"),
                ("Defector", "Defector"),
            },
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
