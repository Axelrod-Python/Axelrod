from collections import UserDict
import pickle

from .action import Action
from .player import Player

from typing import List, Tuple

CachePlayerKey = Tuple[Player, Player, int]
CacheKey = Tuple[str, str, int]


class DeterministicCache(UserDict):
    """A class to cache the results of deterministic matches.

    For fixed length matches with no noise between pairs of deterministic
    players, the results will always be the same. We can hold those results
    in this class so as to avoid repeatedly generating them in tournaments
    of multiple repetitions.

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

    def __init__(self, file_name: str=None) -> None:
        """
        Parameters
        ----------
        file_name : string
            Path to a previously saved cache file
        """
        super().__init__()
        self.mutable = True
        if file_name is not None:
            self.load(file_name)

    @staticmethod
    def _key_transform(key: CachePlayerKey) -> CacheKey:
        """
        Parameters
        ----------
        key: tuple
            A 3-tuple: (player instance, player instance, match length)
        """
        return key[0].name, key[1].name, key[2]

    def __delitem__(self, key: CachePlayerKey):
        return super().__delitem__(self._key_transform(key))

    def __getitem__(self, key: CachePlayerKey) -> List[Tuple[Action, Action]]:
        return super().__getitem__(self._key_transform(key))

    def __contains__(self, key):
        return super().__contains__(self._key_transform(key))

    def __setitem__(self, key: CachePlayerKey, value):
        """Overrides the UserDict.__setitem__ method in order to validate
        the key/value and also to set the turns attribute"""
        if not self.mutable:
            raise ValueError('Cannot update cache unless mutable is True.')

        if not self._is_valid_key(key):
            raise ValueError(
                "Key must be a tuple of 2 deterministic axelrod Player classes "
                "and an integer")

        if not self._is_valid_value(value):
            raise ValueError(
                'Value must be a list with length equal to turns attribute')

        super().__setitem__(self._key_transform(key), value)

    @staticmethod
    def _is_valid_key(key: CachePlayerKey) -> bool:
        """Validate a proposed dictionary key.

        Parameters
        ----------
        key : object

        Returns
        -------
        boolean
        """
        # The key should be a tuple
        if not isinstance(key, tuple):
            return False

        # The tuple should be a triplet
        if len(key) != 3:
            return False

        # The triplet should be a pair of axelrod.Player instances and an
        # integer
        if not (
            isinstance(key[0], Player) and
            isinstance(key[1], Player) and
            isinstance(key[2], int)
        ):
            return False

        # Each Player should be deterministic
        if key[0].classifier['stochastic'] or key[1].classifier['stochastic']:
            return False

        return True

    @staticmethod
    def _is_valid_value(value: List) -> bool:
        """Validate a proposed dictionary value.

        Parameters
        ----------
        value : object

        Returns
        -------
        boolean
        """
        # The value should be a list
        if not isinstance(value, list):
            return False

        return True

    def save(self, file_name: str) -> bool:
        """Serialise the cache dictionary to a file.

        Parameters
        ----------
        file_name : string
            File path to which the cache should be saved
        """
        with open(file_name, 'wb') as io:
            pickle.dump(self.data, io)
        return True

    def load(self, file_name: str) -> bool:
        """Load a previously saved cache into the dictionary.

        Parameters
        ----------
        file_name : string
            Path to a previously saved cache file
        """
        with open(file_name, 'rb') as io:
            data = pickle.load(io)

        if isinstance(data, dict):
            self.data = data
        else:
            raise ValueError(
                "Cache file exists but is not the correct format. "
                "Try deleting and re-building the cache file.")
        return True
