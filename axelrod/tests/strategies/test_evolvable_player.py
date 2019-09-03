import random

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
        seed(0)
        player = self.player()
        variants_produced = False
        for seed_ in range(2, 200):
            seed(seed_)
            mutant = player.clone().mutate()
            if player != mutant:
                variants_produced = True
        self.assertFalse(variants_produced)

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
        player = self.player()
        other = EvolvableTestOpponent()
        self.assertRaises(TypeError, self.player_class.crossover, other=other)

    def test_serialization(self):
        """Serializing and deserializing should return the original player."""
        seed(0)
        player = self.player()
        serialized = player.serialize_parameters()
        deserialized_player = player.__class__.deserialize_parameters(serialized)
        self.assertEqual(player, deserialized_player)
        self.assertEqual(deserialized_player, deserialized_player.clone())


def compare_dicts(d1, d2):
    """For investigating issues above."""
    for k, v in d1.items():
        if d2[k] != v:
            print()
            print(k, d1[k])
            print(k, d2[k])
