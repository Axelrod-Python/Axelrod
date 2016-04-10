try:
    # Python 2.x
    from UserDict import UserDict
except ImportError:
    # Python 3.x
    from collections import UserDict
import dill

from axelrod import Player


class DeterministicCache(UserDict):

    def __init__(self, file_name=None):
        UserDict.__init__(self)
        self.mutable = True
        self.turns = None
        if file_name is not None:
            self.load(file_name)

    def __setitem__(self, key, value):
        if not self.mutable:
            raise ValueError('Cannot update cache unles mutable is True.')

        if not self._is_valid_key(key):
            raise ValueError(
                'Key must be a pair of deterministic axelrod Player classes')

        if not self._is_valid_value(value):
            raise ValueError(
                'Value must be a list with length equal to turns attribute')

        UserDict.__setitem__(self, key, value)

        if self.turns is None:
            self.turns = len(value)

    def _is_valid_key(self, key):
        # The key should be a tuple
        if not isinstance(key, tuple):
            return False

        # The tuple should be a pair
        if len(key) != 2:
            return False

        # Each item in the pair should be a subclass of axelrod.Player
        try:
            if not (issubclass(key[0], Player) and issubclass(key[1], Player)):
                return False
        except TypeError:
            return False

        # Each Player class should be deterministic
        if key[0].classifier['stochastic'] or key[1].classifier['stochastic']:
            return False

        return True

    def _is_valid_value(self, value):
        # The value should be a list
        if not isinstance(value, list):
            return False

        # If the turns attribute has been set, the length of the list should
        # match it
        if self.turns is not None and len(value) != self.turns:
            return False

        return True

    def save(self, file_name):
        with open(file_name, 'wb') as io:
            dill.dump(self.data, io)
        return True

    def load(self, file_name):
        with open(file_name, 'rb') as io:
            self.data = dill.load(io)

        try:
            # Python 2.x
            self.turns = len(self.data.itervalues().next())
        except AttributeError:
            # Python 3.x
            self.turns = len(next(iter(self.data.values())))

        return True
