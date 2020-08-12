import base64
from pickle import dumps, loads
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

    def __init__(self, seed=None):
        # Parameter seed is required for reproducibility. Player will throw
        # a warning to the user otherwise.
        super().__init__()
        self.set_seed(seed=seed)

    def overwrite_init_kwargs(self, **kwargs):
        """Use to overwrite parameters for proper cloning and testing."""
        for k, v in kwargs.items():
            self.init_kwargs[k] = v

    def create_new(self, **kwargs):
        """Creates a new variant with parameters overwritten by kwargs. This differs from
        cloning the Player because it propagates a seed forward, and is intended to be
        used by the mutation and crossover methods."""
        init_kwargs = self.init_kwargs.copy()
        init_kwargs.update(kwargs)
        # Propagate seed forward for reproducibility.
        if "seed" not in kwargs:
            init_kwargs["seed"] = self._random.random_seed_int()
        return self.__class__(**init_kwargs)

    # Serialization and deserialization. You may overwrite to obtain more human readable serializations
    # but you must overwrite both.

    def serialize_parameters(self):
        """Serialize parameters."""
        pickled = dumps(self.init_kwargs)  # bytes
        s = base64.b64encode(pickled).decode('utf8')  # string
        return s

    @classmethod
    def deserialize_parameters(cls, serialized):
        """Deserialize parameters to a Player instance."""
        init_kwargs = loads(base64.b64decode(serialized))
        return cls(**init_kwargs)

    # Optional methods for evolutionary algorithms and Moran processes.

    def mutate(self):
        """Optional method to allow Player to produce a variant (not in place)."""
        pass  # pragma: no cover

    def crossover(self, other):
        """Optional method to allow Player to produce variants in combination with another player. Returns a new
        Player."""
        pass  # pragma: no cover

    # Optional methods for particle swarm algorithm.

    def receive_vector(self, vector):
        """Receive a vector of params and overwrite the Player."""
        pass  # pragma: no cover

    def create_vector_bounds(self):
        """Creates the bounds for the decision variables for Particle Swarm Algorithm."""
        pass  # pragma: no cover


def copy_lists(lists: List[List]) -> List[List]:
    return list(map(list, lists))


def crossover_lists(list1: List, list2: List, rng) -> List:
    cross_point = rng.randint(0, len(list1))
    new_list = list(list1[:cross_point]) + list(list2[cross_point:])
    return new_list


def crossover_dictionaries(table1: Dict, table2: Dict, rng) -> Dict:
    keys = list(table1.keys())
    cross_point = rng.randint(0, len(keys))
    new_items = [(k, table1[k]) for k in keys[:cross_point]]
    new_items += [(k, table2[k]) for k in keys[cross_point:]]
    new_table = dict(new_items)
    return new_table
