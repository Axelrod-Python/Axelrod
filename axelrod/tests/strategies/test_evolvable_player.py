import functools
import random
import unittest

import axelrod as axl
from axelrod import EvolvablePlayer, seed
from axelrod.action import Action
from axelrod.evolvable_player import copy_lists, crossover_lists, crossover_dictionaries
from .test_player import TestPlayer

C, D = Action.C, Action.D


def PartialClass(cls, **kwargs):

    class PartialedClass(cls):
        __init__ = functools.partialmethod(
            cls.__init__, **kwargs)

    return PartialedClass


class EvolvableTestOpponent(EvolvablePlayer):
    name = "EvolvableTestOpponent"

    def __init__(self, value=None):
        super().__init__()
        if value:
            self.value = value
        else:
            value = random.randint(2, 100)
            self.value = value
            self.overwrite_init_kwargs(value=value)

    @staticmethod
    def strategy(opponent):
        return Action.C

    def mutate(self):
        value = random.randint(2, 100)
        return EvolvableTestOpponent(value)

    def crossover(self, other):
        value = self.value + other.value
        return EvolvableTestOpponent(value)


class TestEvolvablePlayer(TestPlayer):

    player_class = EvolvableTestOpponent
    parent_class = None
    init_parameters = dict()

    def player(self):
        return self.player_class(**self.init_parameters)

    def test_initialisation(self):
        """Test that the player initiates correctly."""
        if not issubclass(self.__class__, TestPlayer):
            player = self.player()
            self.assertEqual(len(player.history), 0)
            self.assertEqual(player.cooperations, 0)
            self.assertEqual(player.defections, 0)

    def test_randomization(self):
        """Test that randomization on initialization produces different strategies."""
        if self.init_parameters:
            return
        seed(0)
        player1 = self.player()
        seed(0)
        player2 = self.player()
        self.assertEqual(player1, player2)
        for seed_ in range(2, 20):
            seed(seed_)
            player2 = self.player()
            if player1 != player2:
                return
        self.assertFalse(True)

    def test_mutate_variations(self):
        """Test that mutate produces different strategies."""
        if self.init_parameters:
            return
        seed(0)
        variants_produced = False
        for seed_ in range(2, 200):
            seed(seed_)
            player = self.player()
            mutant = player.clone().mutate()
            if player != mutant:
                variants_produced = True
        self.assertTrue(variants_produced)

    def test_mutate_and_clone(self):
        """Test that mutated players clone properly."""
        seed(0)
        player = self.player()
        mutant = player.clone().mutate()
        clone = mutant.clone()
        self.assertEqual(clone, mutant)

    def test_crossover(self):
        """Test that crossover produces different strategies."""
        for seed_ in range(20):
            seed(seed_)
            players = []
            for _ in range(2):
                player = self.player()
                # Mutate to randomize
                player = player.mutate()
                players.append(player)
            player1, player2 = players
            crossed = player1.crossover(player2)
            if player1 != crossed and player2 != crossed and crossed == crossed.clone():
                return
        self.assertFalse(True)

    def test_crossover_mismatch(self):
        other = axl.Cooperator()
        self.assertRaises(TypeError, self.player_class.crossover, other=other)

    def test_serialization(self):
        """Serializing and deserializing should return the original player."""
        seed(0)
        player = self.player()
        serialized = player.serialize_parameters()
        deserialized_player = player.__class__.deserialize_parameters(serialized)
        self.assertEqual(player, deserialized_player)
        self.assertEqual(deserialized_player, deserialized_player.clone())

    def behavior_test(self, player1, player2):
        """Test that the evolvable player plays the same as its (nonevolvable) parent class."""
        for opponent_class in [axl.Random, axl.TitForTat, axl.Alternator]:
            axl.seed(0)
            opponent = opponent_class()
            match = axl.Match((player1.clone(), opponent))
            results1 = match.play()

            axl.seed(0)
            opponent = opponent_class()
            match = axl.Match((player2.clone(), opponent))
            results2 = match.play()

            self.assertEqual(results1, results2)

    def test_behavior(self):
        """Test that the evolvable player plays the same as its (nonevolvable) parent class."""
        if not self.parent_class:
            return

        player = self.player_class(**self.init_parameters)
        init_kwargs = {k: player.init_kwargs[k] for k in self.parent_kwargs}
        parent_player = self.parent_class(**init_kwargs)
        self.behavior_test(player, parent_player)

        serialized = player.serialize_parameters()
        deserialized_player = player.__class__.deserialize_parameters(serialized)
        self.behavior_test(deserialized_player, parent_player)


def compare_dicts(d1, d2):
    """For investigating issues above."""
    for k, v in d1.items():
        if d2[k] != v:
            print()
            print(k, d1[k])
            print(k, d2[k])


class TestUtilityFunctions(unittest.TestCase):

    def test_copy_lists(self):
        l1 = [list(range(10)), list(range(20))]
        l2 = copy_lists(l1)
        self.assertIsNot(l1, l2)

    def test_crossover_lists(self):
        list1 = [[0, C, 1, D], [0, D, 0, D], [1, C, 1, C], [1, D, 1, D]]
        list2 = [[0, D, 1, C], [0, C, 0, C], [1, D, 1, D], [1, C, 1, C]]

        axl.seed(0)
        crossed = crossover_lists(list1, list2)
        self.assertEqual(crossed, list1[:3] + list2[3:])

        axl.seed(1)
        crossed = crossover_lists(list1, list2)
        self.assertEqual(crossed, list1[:1] + list2[1:])

    def test_crossover_dictionaries(self):
        dict1 = {'1': 1, '2': 2, '3': 3}
        dict2 = {'1': 'a', '2': 'b', '3': 'c'}

        axl.seed(0)
        crossed = crossover_dictionaries(dict1, dict2)
        self.assertEqual(crossed, {'1': 1, '2': 'b', '3': 'c'})

        axl.seed(1)
        crossed = crossover_dictionaries(dict1, dict2)
        self.assertEqual(crossed, dict2)

