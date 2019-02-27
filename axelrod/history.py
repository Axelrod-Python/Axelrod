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
        if coplay:
            self._coplays.append(coplay)
            self._state_distribution[(play, coplay)] += 1

    def copy(self):
        """Returns a new object with the same data."""
        return History(plays=self._plays, coplays=self._coplays)

    def flip_plays(self):
        """Creates a flip_plays history for use with DualTransformer."""
        flipped_plays = [action.flip() for action in self._plays]
        return History(plays=flipped_plays, coplays=self._coplays)

    def extend(self, plays, coplays=None):
        """A function that emulates list.extend."""
        # We could repeatedly call self.append but this is more efficient.
        self._plays.extend(plays)
        self._actions.update(plays)
        if coplays:
            self._coplays.extend(coplays)
            self._state_distribution.update(zip(plays, coplays))

    def reset(self):
        """Clears all data in the History object."""
        self._plays.clear()
        self._coplays.clear()
        self._actions.clear()
        self._state_distribution.clear()

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

