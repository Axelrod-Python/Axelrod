from collections import Counter

from axelrod.action import Action, actions_to_str

C, D = Action.C, Action.D


class History(object):
    """
    History class to track the history of play and metadata including
    the number of cooperations and defections, and if available, the
    opponents plays and the state distribution of the history of play.
    """

    def __init__(self, plays=None, coplays=None):
        """
        Parameters
        ----------
        plays:
            An ordered iterable of the actions of the player.
        coplays:
            An ordered iterable of the actions of the coplayer (aka opponent).
        """
        self._plays = []
        # Coplays is tracked mainly for computation of the state distribution
        # when cloning or dualing.
        self._coplays = []
        self._actions = Counter()
        self._state_distribution = Counter()
        if plays:
            self.extend(plays, coplays)

    def append(self, play, coplay):
        """Appends a new (play, coplay) pair an updates metadata for
        number of cooperations and defections, and the state distribution."""
        self._plays.append(play)
        self._actions[play] += 1
        self._coplays.append(coplay)
        self._state_distribution[(play, coplay)] += 1

    def copy(self):
        """Returns a new object with the same data."""
        return self.__class__(plays=self._plays, coplays=self._coplays)

    def flip_plays(self):
        """Creates a flipped plays history for use with DualTransformer."""
        flipped_plays = [action.flip() for action in self._plays]
        return self.__class__(plays=flipped_plays, coplays=self._coplays)

    def extend(self, plays, coplays):
        """A function that emulates list.extend."""
        # We could repeatedly call self.append but this is more efficient.
        self._plays.extend(plays)
        self._actions.update(plays)
        self._coplays.extend(coplays)
        self._state_distribution.update(zip(plays, coplays))

    def reset(self):
        """Clears all data in the History object."""
        self._plays.clear()
        self._coplays.clear()
        self._actions.clear()
        self._state_distribution.clear()

    @property
    def coplays(self):
        return self._coplays

    @property
    def cooperations(self):
        return self._actions[C]

    @property
    def defections(self):
        return self._actions[D]

    @property
    def state_distribution(self):
        return self._state_distribution

    def __eq__(self, other):
        if isinstance(other, list):
            return self._plays == other
        elif isinstance(other, History):
            return self._plays == other._plays and self._coplays == other._coplays
        raise TypeError("Cannot compare types.")

    def __getitem__(self, key):
        # Passthrough keys and slice objects
        return self._plays[key]

    def __str__(self):
        return actions_to_str(self._plays)

    def __list__(self):
        return self._plays

    def __len__(self):
        return len(self._plays)

    def __repr__(self):
        return repr(self.__list__())


class LimitedHistory(History):
    """
    History class that only tracks the last N rounds. Used for testing memory
    depth.
    """

    def __init__(self, memory_depth, plays=None, coplays=None):
        """
        Parameters
        ----------
        memory_depth, int:
            length of history to retain
        """
        super().__init__(plays=plays, coplays=coplays)
        self.memory_depth = memory_depth

    def flip_plays(self):
        """Creates a flipped plays history for use with DualTransformer."""
        flipped_plays = [action.flip() for action in self._plays]
        return self.__class__(self.memory_depth, plays=flipped_plays, coplays=self._coplays)

    def append(self, play, coplay):
        """Appends a new (play, coplay) pair an updates metadata for
        number of cooperations and defections, and the state distribution."""

        self._plays.append(play)
        self._actions[play] += 1
        if coplay:
            self._coplays.append(coplay)
            self._state_distribution[(play, coplay)] += 1
        if len(self._plays) > self.memory_depth:
            first_play, first_coplay = self._plays.pop(0), self._coplays.pop(0)
            self._actions[first_play] -= 1
            self._state_distribution[(first_play, first_coplay)] -= 1
