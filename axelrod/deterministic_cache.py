try:
    # Python 2.x
    from UserDict import UserDict
except ImportError:
    # Python 3.x
    from collections import UserDict
import pickle

from axelrod import Player


class DeterministicCache(UserDict):
    """A class to cache the results of deterministic matches

    For fixed length matches with no noise between pairs of deterministic
    players, the results will always be the same. We can hold those results
    in this class so as to avoid repeatedly generating them in tournaments
    of multiple repetitions.

    By also storing those cached results in a file, we can re-use the cache
    between multiple tournaments if necessary.

    The cache is a dictionary mapping pairs of Player classes to a list of
    resulting interactions. e.g. for a 3 turn Match between Cooperator and
    Alternator, the dictionary entry would be:

    (axelrod.Cooperator, axelrod.Alternator): [('C', 'C'), ('C', 'D'), ('C', 'C')]

    Most of the functionality is provided by the UserDict class (which uses an
    instance of dict as the 'data' attribute to hold the dictionary entries).

    This class overrides the __init__ and __setitem__ methods in order to limit
    and validate the keys and values to be as described above. It also adds
    methods to save/load the cache to/from a file.
    """

    def __init__(self, file_name=None):
        """
        Parameters
        ----------
        file_name : string
            Path to a previously saved cache file
        """
        UserDict.__init__(self)
        self.mutable = True
        if file_name is not None:
            self.load(file_name)

    def __setitem__(self, key, value):
        """Overrides the UserDict.__setitem__ method in order to validate
        the key/value and also to set the turns attribute"""
        if not self.mutable:
            raise ValueError('Cannot update cache unless mutable is True.')

        if not self._is_valid_key(key):
            raise ValueError(
                'Key must be a tuple of 2 deterministic axelrod Player classes and an integer')

        if not self._is_valid_value(value):
            raise ValueError(
                'Value must be a list with length equal to turns attribute')

        UserDict.__setitem__(self, key, value)

    def _is_valid_key(self, key):
        """Validate a proposed dictionary key

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

        # The triplet should be a pair of axelrod.Player sublclasses and an
        # integer
        try:
            if not (
                issubclass(key[0], Player) and
                issubclass(key[1], Player) and
                isinstance(key[2], int)
            ):
                return False
        except TypeError:
            return False

        # Each Player class should be deterministic
        if key[0].classifier['stochastic'] or key[1].classifier['stochastic']:
            return False

        return True

    def _is_valid_value(self, value):
        """Validate a proposed dictionary value

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

    def save(self, file_name):
        """Serialise the cache dictionary to a file

        Parameters
        ----------
        file_name : string
            File path to which the cache should be saved
        """
        with open(file_name, 'wb') as io:
            pickle.dump(self.data, io)
        return True

    def load(self, file_name):
        """Load a previously saved cache into the dictionary

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
                'Cache file exists but is not the correct format. Try deleting and re-building the cache file.')
        return True
