import functools
import unittest

import axelrod as axl
from axelrod.action import Action
from axelrod.evolvable_player import (
    copy_lists,
    crossover_dictionaries,
    crossover_lists,
)

from .test_player import TestPlayer

C, D = Action.C, Action.D


def PartialClass(cls, **kwargs):
    class PartialedClass(cls):
        # Set a seed to avoid undefined behavior in tests.
        try:
            seed = kwargs["seed"]
        except KeyError:
            kwargs["seed"] = 1
        __init__ = functools.partialmethod(cls.__init__, **kwargs)

    return PartialedClass


class EvolvableTestOpponent(axl.EvolvablePlayer):
    name = "EvolvableTestOpponent"

    def __init__(self, value=None, seed=1):
        super().__init__(seed=seed)
        if value:
            self.value = value
        else:
            value = self._random.randint(2, 100)
            self.value = value
            self.overwrite_init_kwargs(value=value)

    @staticmethod
    def strategy(opponent):
        return Action.C

    def mutate(self):
        value = self._random.randint(2, 100)
        return EvolvableTestOpponent(value)

    def crossover(self, other):
        if other.__class__ != self.__class__:
            raise TypeError(
                "Crossover must be between the same player classes."
            )
        value = self.value + other.value
        return EvolvableTestOpponent(value)


class TestEvolvablePlayer(TestPlayer):
    """Additional tests for EvolvablePlayers, in addition to the many tests
    inherited from TestPlayer."""

    player_class = EvolvableTestOpponent
    parent_class = None
    init_parameters = dict()

    def player(self, seed=1):
        params = self.init_parameters.copy()
        if "seed" not in params:  # pragma: no cover
            params["seed"] = seed
        return self.player_class(**params)

    def test_repr(self):
        """Test that the representation is correct."""
        if self.__class__ != TestEvolvablePlayer:
            self.assertIn(self.name, str(self.player()))
        pass

    def test_initialisation(self):
        """Test that the player initiates correctly."""
        if self.__class__ != TestEvolvablePlayer:
            player = self.player()
            self.assertEqual(len(player.history), 0)
            self.assertEqual(player.cooperations, 0)
            self.assertEqual(player.defections, 0)

    def test_randomization(self):
        """Test that randomization on initialization produces different strategies."""
        if self.init_parameters:
            return
        player1 = self.player(seed=1)
        player2 = self.player(seed=1)
        self.assertEqual(player1, player2)

        for seed_ in range(2, 200):
            player2 = self.player(seed=seed_)
            if player1 != player2:
                return
        # Should never get here unless a change breaks the test, so don't include in coverage.
        self.assertFalse(True)  # pragma: no cover

    def test_mutate_variations(self):
        """Generate many variations to test that mutate produces different strategies."""
        if not self.init_parameters:
            return
        variants_produced = False
        for seed_ in range(2, 400):
            player = self.player(seed=seed_)
            mutant = player.mutate()
            if player != mutant:
                variants_produced = True
                break
        self.assertTrue(variants_produced)

    def test_mutate_and_clone(self):
        """Test that mutated players clone properly."""
        player = self.player(seed=1)
        mutant = player.clone().mutate()
        clone = mutant.clone()
        self.assertEqual(clone, mutant)

    def test_crossover(self):
        """Test that crossover produces different strategies."""
        rng = axl.RandomGenerator(seed=1)
        for _ in range(20):
            players = []
            for _ in range(2):
                player = self.player(seed=rng.random_seed_int())
                # Mutate to randomize
                player = player.mutate()
                players.append(player)
            player1, player2 = players
            crossed = player1.crossover(player2)
            if (
                player1 != crossed
                and player2 != crossed
                and crossed == crossed.clone()
            ):
                return
        # Should never get here unless a change breaks the test, so don't include in coverage.
        self.assertFalse(True)  # pragma: no cover

    def test_crossover_mismatch(self):
        other = axl.Cooperator()
        player = self.player()
        with self.assertRaises(TypeError):
            player.crossover(other)

    def test_serialization(self):
        """Serializing and deserializing should return the original player."""
        player = self.player(seed=1)
        serialized = player.serialize_parameters()
        deserialized_player = player.__class__.deserialize_parameters(
            serialized
        )
        self.assertEqual(player, deserialized_player)
        self.assertEqual(deserialized_player, deserialized_player.clone())

    def test_serialization_csv(self):
        """Serializing and deserializing should return the original player."""
        player = self.player(seed=1)
        serialized = player.serialize_parameters()
        s = "0, 1, {}, 3".format(serialized)
        s2 = s.split(",")[2]
        deserialized_player = player.__class__.deserialize_parameters(s2)
        self.assertEqual(player, deserialized_player)
        self.assertEqual(deserialized_player, deserialized_player.clone())

    def behavior_test(self, player1, player2, seed=7):
        """Test that the evolvable player plays the same as its (nonevolvable) parent class."""
        for opponent_class in [axl.Random, axl.TitForTat, axl.Alternator]:
            opponent = opponent_class()
            match = axl.Match((player1.clone(), opponent), seed=seed)
            results1 = match.play()

            opponent = opponent_class()
            match = axl.Match((player2.clone(), opponent), seed=seed)
            results2 = match.play()

            self.assertEqual(results1, results2)

    def test_behavior(self):
        """Test that the evolvable player plays the same as its (nonevolvable) parent class."""
        if not self.parent_class:
            return

        player = self.player()
        init_kwargs = {k: player.init_kwargs[k] for k in self.parent_kwargs}
        parent_player = self.parent_class(**init_kwargs)
        self.behavior_test(player, parent_player)

        serialized = player.serialize_parameters()
        deserialized_player = player.__class__.deserialize_parameters(
            serialized
        )
        self.behavior_test(deserialized_player, parent_player)

    def test_seed_propagation(self):
        """Tests that _create_new should typically alter the random seed."""
        player = self.player(seed=1)
        for _ in range(100):
            player = player.create_new()
            if player._seed != 1:
                return

        # Should never get here unless a change breaks the test, so don't include in coverage.
        self.assertFalse(True)  # pragma: no cover

    def test_seed_preservation(self):
        """Tests that method function clone preserves the random seed. The seed
        is intentionally not checked by Player.__eq__ so an explicit extra test
        is needed."""
        player = self.player(seed=1)
        clone = player.clone()
        self.assertEqual(player._seed, clone._seed)


class TestUtilityFunctions(unittest.TestCase):
    def test_copy_lists(self):
        l1 = [list(range(10)), list(range(20))]
        l2 = copy_lists(l1)
        self.assertIsNot(l1, l2)

    def test_crossover_lists(self):
        list1 = [[0, C, 1, D], [0, D, 0, D], [1, C, 1, C], [1, D, 1, D]]
        list2 = [[0, D, 1, C], [0, C, 0, C], [1, D, 1, D], [1, C, 1, C]]

        rng = axl.RandomGenerator(seed=5)
        crossed = crossover_lists(list1, list2, rng)
        self.assertEqual(crossed, list1[:3] + list2[3:])

        rng = axl.RandomGenerator(seed=1)
        crossed = crossover_lists(list1, list2, rng)
        self.assertEqual(crossed, list1[:1] + list2[1:])

    def test_crossover_dictionaries(self):
        dict1 = {"1": 1, "2": 2, "3": 3}
        dict2 = {"1": "a", "2": "b", "3": "c"}

        rng = axl.RandomGenerator(seed=1)
        crossed = crossover_dictionaries(dict1, dict2, rng)
        self.assertEqual(crossed, {"1": 1, "2": "b", "3": "c"})

        rng = axl.RandomGenerator(seed=2)
        crossed = crossover_dictionaries(dict1, dict2, rng)
        self.assertEqual(crossed, dict2)
