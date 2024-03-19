"""Tools for caching the results of deterministic matches.

The cache, in most cases, can simply be treated as a dictionary:

cache = DeterministicCache()
cache[key1] = result1
cache[key2] = result2
...
if some_key in cache:
    do_something(cache[some_key])
else:
    ...
"""

import pickle
from collections import UserDict
from typing import List, Tuple

from axelrod import Classifiers

from .action import Action
from .player import Player

CachePlayerKey = Tuple[Player, Player]
CacheKey = Tuple[str, str]


def _key_transform(key: CachePlayerKey) -> CacheKey:
    """Convert a CachePlayerKey to a CacheKey

    Parameters
    ----------
    key: tuple
        A 3-tuple: (player instance, player instance)
    """
    return key[0].name, key[1].name


def _is_valid_key(key: CachePlayerKey) -> bool:
    """Validate a deterministic cache player key.

    The key should always be a 2-tuple, with a pair of axelrod.Player
    instances and one integer. Both players should be deterministic.

    Parameters
    ----------
    key : object

    Returns
    -------
    Boolean indicating if the key is valid
    """
    if not isinstance(key, tuple) or len(key) != 2:
        return False

    if not (isinstance(key[0], Player) and isinstance(key[1], Player)):
        return False

    if Classifiers["stochastic"](key[0]) or Classifiers["stochastic"](key[1]):
        return False

    return True


def _is_valid_value(value: List) -> bool:
    """Validate a deterministic cache value.

    The value just needs to be a list, with any contents.

    Parameters
    ----------
    value : object

    Returns
    -------
    Boolean indicating if the value is valid
    """
    return isinstance(value, list)


class DeterministicCache(UserDict):
    """A class to cache the results of deterministic matches.

    For matches with no noise between pairs of deterministic players, the
    results will always be the same.  We can hold the results for the longest
    run in this class, so as to avoid repeatedly generating them in tournaments
    of multiple repetitions.  If a shorter or equal-length match is run, we can
    use the stored results.

    By also storing those cached results in a file, we can re-use the cache
    between multiple tournaments if necessary.

    The cache is a dictionary mapping pairs of Player classes to a list of
    resulting interactions. e.g. for a 3 turn Match between Cooperator and
    Alternator, the dictionary entry would be:

    (axelrod.Cooperator, axelrod.Alternator): [(C, C), (C, D), (C, C)]

    Most of the functionality is provided by the UserDict class (which uses an
    instance of dict as the 'data' attribute to hold the dictionary entries).

    This class overrides the __init__ and __setitem__ methods in order to limit
    and validate the keys and values to be as described above. It also adds
    methods to save/load the cache to/from a file.
    """

    def __init__(self, file_name: str = None) -> None:
        """Initialize a new cache.

        Parameters
        ----------
        file_name : string
            Path to a previously saved cache file
        """
        super().__init__()
        self.mutable = True
        if file_name is not None:
            self.load(file_name)

    def __delitem__(self, key: CachePlayerKey):
        return super().__delitem__(_key_transform(key))

    def __getitem__(self, key: CachePlayerKey) -> List[Tuple[Action, Action]]:
        return super().__getitem__(_key_transform(key))

    def __contains__(self, key):
        return super().__contains__(_key_transform(key))

    def __setitem__(self, key: CachePlayerKey, value):
        """Validate the key and value before setting them."""
        if not self.mutable:
            raise ValueError("Cannot update cache unless mutable is True.")

        if not _is_valid_key(key):
            raise ValueError(
                "Key must be a tuple of 2 deterministic axelrod Player classes"
            )

        if not _is_valid_value(value):
            raise ValueError(
                "Value must be a list with length equal to turns attribute"
            )

        super().__setitem__(_key_transform(key), value)

    def save(self, file_name: str) -> bool:
        """Serialise the cache dictionary to a file.

        Parameters
        ----------
        file_name : string
            File path to which the cache should be saved
        """
        with open(file_name, "wb") as io:
            pickle.dump(self.data, io)
        return True

    def load(self, file_name: str) -> bool:
        """Load a previously saved cache into the dictionary.

        Parameters
        ----------
        file_name : string
            Path to a previously saved cache file
        """
        with open(file_name, "rb") as io:
            data = pickle.load(io)

        if isinstance(data, dict):
            self.data = data
        else:
            raise ValueError(
                "Cache file exists but is not the correct format. "
                "Try deleting and re-building the cache file."
            )
        return True
