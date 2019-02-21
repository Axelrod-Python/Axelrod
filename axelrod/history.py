from collections import Counter

from axelrod.action import Action, actions_to_str

C, D = Action.C, Action.D


class History(object):
    def __init__(self, history=None):
        self._history = []
        self.actions = Counter()
        self.state_distribution = Counter()
        if isinstance(history, History):
            history = history._history
        if history:
            self.extend(history)

    def append(self, play, op_play=None):
        self._history.append(play)
        self.actions[play] += 1
        if op_play:
            self.state_distribution[(play, op_play)] += 1

    def copy(self):
        new_history = History(history=self._history)
        return new_history

    def extend(self, plays, op_plays=None):
        self._history.extend(plays)
        self.actions.update(plays)
        if op_plays:
            self.state_distribution.update(zip(plays, op_plays))

    def pop(self, index):
        play = self._history.pop(index)
        self.actions[play] -= 1
        return play

    def reset(self):
        self._history.clear()
        self.actions.clear()
        self.state_distribution.clear()

    @property
    def cooperations(self):
        return self.actions[C]

    @property
    def defections(self):
        return self.actions[D]

    def __eq__(self, other):
        if isinstance(other, list):
            return self._history == other
        elif isinstance(other, History):
            return self._history == other._history
        raise ValueError("Cannot compare types.")

    def __add__(self, other):
        if isinstance(other, list):
            temp = self._history + other
        elif isinstance(other, History):
            temp = self._history + other._history
        return History(temp)

    def __getitem__(self, key):
        # Passthrough keys and slice objects
        return self._history[key]

    def __str__(self):
        return actions_to_str(self._history)

    def __list__(self):
        return self._history

    def __len__(self):
        return len(self._history)

    def __repr__(self):
        return repr(self.__list__())

