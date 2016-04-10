try:
    from collections import UserDict
except ImportError:
    from UserDict import UserDict
import dill


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
            raise ValueError('Key must be a pair of axelrod Player classes')

        if not self._is_valid_value(value):
            raise ValueError(
                'Value must be a list with length of turns attribute')

        UserDict.__setitem__(self, key, value)

    def _is_valid_key(self, key):
        return True

    def _is_valid_value(self, value):
        return True

    def save(self, file_name):
        with open(file_name, 'wb') as io:
            dill.dump(self.data, io)
        return True

    def load(self, file_name):
        with open(file_name, 'rb') as io:
            self.data = dill.load(io)
