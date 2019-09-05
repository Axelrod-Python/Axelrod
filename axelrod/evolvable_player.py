from pickle import dumps, loads
from random import randrange
from typing import Dict, List
from .player import Player


class InsufficientParametersError(Exception):
    """Error indicating that insufficient parameters were specified to initialize an Evolvable Player."""
    def __init__(self, *args):
        super().__init__(*args)


class EvolvablePlayer(Player):
    """A class for a player that can evolve, for use in the Moran process or with reinforcement learning algorithms.

    This is an abstract base class, not intended to be used directly.
    """

    name = "EvolvablePlayer"
    parent_class = Player
    parent_kwargs = []  # type: List[str]

    def overwrite_init_kwargs(self, **kwargs):
        """Use to overwrite parameters for proper cloning and testing."""
        for k, v in kwargs.items():
            self.init_kwargs[k] = v

    def create_new(self, **kwargs):
        """Creates a new variant with parameters overwritten by kwargs."""
        init_kwargs = self.init_kwargs.copy()
        init_kwargs.update(kwargs)
        return self.__class__(**init_kwargs)

    # Serialization and deserialization. You may overwrite to obtain more human readable serializations
    # but you must overwrite both.

    def serialize_parameters(self):
        """Serialize parameters."""
        return dumps(self.init_kwargs)

    @classmethod
    def deserialize_parameters(cls, serialized):
        """Deserialize parameters to a Player instance."""
        init_kwargs = loads(serialized)
        return cls(**init_kwargs)

    # Optional methods for evolutionary algorithms and Moran processes.

    def mutate(self):
        """Optional method to allow Player to produce a variant (not in place)."""
        pass

    def crossover(self, other):
        """Optional method to allow Player to produce variants in combination with another player. Returns a new
        Player."""
        pass

    # Optional methods for particle swarm algorithm.

    def receive_vector(self, vector):
        """Receive a vector of params and overwrite the Player."""
        pass

    def create_vector_bounds(self):
        """Creates the bounds for the decision variables for Particle Swarm Algorithm."""
        pass


def copy_lists(lists: List[List]) -> List[List]:
    return list(map(list, lists))


def crossover_lists(list1: List, list2: List) -> List:
    cross_point = randrange(len(list1))
    new_list = list(list1[:cross_point]) + list(list2[cross_point:])
    return new_list


def crossover_dictionaries(table1: Dict, table2: Dict) -> Dict:
    keys = list(table1.keys())
    cross_point = randrange(len(keys))
    new_items = [(k, table1[k]) for k in keys[:cross_point]]
    new_items += [(k, table2[k]) for k in keys[cross_point:]]
    new_table = dict(new_items)
    return new_table
