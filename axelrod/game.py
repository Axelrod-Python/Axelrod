class Game(object):
    """A class to hold the game matrix and to score a game accordingly."""

    def __init__(self, r=2, s=0, t=5, p=4):
        self.scores = {
            ('C', 'C'): (r, r),
            ('D', 'D'): (p, p),
            ('C', 'D'): (t, s),
            ('D', 'C'): (s, t),
        }

    def score(self, pair):
        """Return the appropriate score for decision pair.

        Returns the appropriate score (as a tuple) from the scores dictionary
        for a given pair of plays (passed in as a tuple).
        e.g. score(('C', 'C')) returns (2, 2)
        """
        return self.scores[pair]
