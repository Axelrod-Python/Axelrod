from collections import Counter, defaultdict


class History(object):
    def __init__(self, history=None):
        if isinstance(history, History):
            history = history._history
        self._history = []
        self._counter = Counter()
        if history:
            self.extend(list(history))

    def append(self, play):
        self._history.append(play)
        self._counter[play] += 1

    def cooperations(self):
        return self._counter['C']

    def copy(self):
        new_history = History(self._history)
        return new_history

    def defections(self):
        return self._counter['D']

    def extend(self, list_):
        self._history.extend(list_)
        self._counter.update(list_)

    def pop(self, index):
        play = self._history.pop(index)
        self._counter[play] -= 1
        return play

    def reset(self):
        self._history = []
        self._counter = Counter()

    def __eq__(self, other):
        # Allow comparison to lists and strings
        if isinstance(other, str):
            other = list(str)
        if isinstance(other, list):
            other_history = other
        else:
            other_history = other._history

        return (self._history == other_history)

    def __getitem__(self, key):
        # Passthrough keys and slice objects
        return self._history[key]

    def __len__(self):
        return len(self._history)

    def __repr__(self):
        return "History: " + ''.join(self._history)


class JointHistory(object):
    def __init__(self, my_history, op_history):
        self._my_history = History(my_history)
        self._op_history = History(op_history)
        self._joint = defaultdict(int)
        for (h1, h2) in zip(my_history, op_history):
            self._joint[(h1, h2)] += 1

    def append(self, my_play, op_play):
        self._my_history.append(my_play)
        self._op_history.append(op_play)
        self._joint[(my_play, op_play)] += 1

    # def cooperations(self):
    #     return self._my_history.cooperations()

    def copy(self):
        new = JointHistory(self._my_history, self._op_history)
        return new

    # def defections(self):
    #     return self._my_history.defections()

    def pop(self, index):
        my_play = self._my_history.pop(index)
        op_play = self._my_history.pop(index)
        self._joint[(my_play, op_play)] -= 1
        return (my_play, op_play)


    def reset(self):
        self._my_history.reset()
        self._op_history.reset()
        self._joint = Counter()

    def __eq__(self, other):
        return (self._my_history == other._my_history) and \
               (self._op_history == other._op_history)

    def __getitem__(self, key):
        # Passthrough keys and slice objects
        return (self._my_history[key], self._op_history[key])

    def __len__(self):
        return len(self._my_history)


