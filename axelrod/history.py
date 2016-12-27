
def copy_history(history):
    """Copies a history object efficiently."""
    new_history = History()
    new_history.extend(history)
    return new_history


class History(object):
    def __init__(self, history=None):
        self._history = []
        self._counter = collections.Counter()
        if history:
            self.extend(history)

    def reset(self):
        self._history = []
        self._counter = collections.Counter()

    def append(self, play):
        self._history.append(play)
        self._counter[play] += 1

    def extend(self, list_):
        self._history.extend(list_)
        self._counter.update(list_)

    def pop(self, index):
        play = self._history.pop(index)
        self._counter[play] -= 1
        return play

    def __len__(self):
        return len(self._history)

    def cooperations(self):
        return self._counter['C']

    def defections(self):
        return self._counter['D']

    def __getitem__(self, key):
        # Passthrough keys and slice objects
        return self._history[key]

    def __eq__(self, other):
        # Allow comparison to lists
        if isinstance(other, list):
            other_history = other
        else:
            other_history = other._history

        return (self._history == other_history)

    def __repr__(self):
        return "History: " + self._history.__repr__()
