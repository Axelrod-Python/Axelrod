import random
import unittest

from axelrod import EvolvablePlayer, seed
from axelrod.action import Action
from .test_player import TestPlayer


class EvolvableTestOpponent(EvolvablePlayer):
    name = "EvolvableTestOpponent"

    def __init__(self, value=None):
        super().__init__()
        if value:
            self.value = value
        else:
            self.randomize()

    @staticmethod
    def strategy(opponent):
        return Action.C

    def randomize(self):
        self.value = random.randint(2, 100)
        self.init_kwargs["value"] = self.value

    def mutate(self):
        self.value = random.randint(2, 100)
        self.init_kwargs["value"] = self.value

    def crossover(self, other):
        value = self.value + other.value
        return EvolvableTestOpponent(value)

    def serialize_parameters(self):
        return str(self.value)

    @classmethod
    def deserialize_parameters(cls, value):
        return EvolvableTestOpponent(int(value))


class TestEvolvablePlayer(TestPlayer):

    player_class = EvolvableTestOpponent
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

    def test_mutate(self):
        """Test that mutate produces different strategies."""
        seed(0)
        player = self.player()
        for seed_ in range(2, 20):
            seed(seed_)
            mutant = player.clone()
            mutant.mutate()
            if player != mutant:
                return
        self.assertFalse(True)

    def test_mutate_and_clone(self):
        """Test that mutated players clone properly."""
        seed(0)
        player = self.player()
        mutant = player.clone()
        mutant.mutate()
        clone = mutant.clone()
#        compare_dicts(mutant.__dict__, clone.__dict__)

        self.assertEqual(clone, mutant)

    def test_crossover(self):
        """Test that crossover produces different strategies."""
        seed(0)
        player1 = self.player()
        seed(1)
        player2 = self.player()
        crossed = player1.crossover(player2)
        self.assertNotEqual(player1, crossed)
        self.assertNotEqual(player2, crossed)
        self.assertEqual(crossed, crossed.clone())

    def test_serialization(self):
        """Serializing and deserializing should return the original player."""
        seed(0)
        player = self.player()
        serialized = player.serialize_parameters()
        deserialized_player = player.__class__.deserialize_parameters(serialized)
        # compare_dicts(player.__dict__, deserialized_player.__dict__)

        self.assertEqual(player, deserialized_player)
        self.assertEqual(deserialized_player, deserialized_player.clone())


# def compare_dicts(d1, d2):
#     for k, v in d1.items():
#         if d2[k] != v:
#             print(k, d1[k])
#             print(k, d2[k])
