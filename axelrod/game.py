
class Game(object):
    """A class to hold the game matrix and to score a game accordingly."""

    def __init__(self, r=3, s=0, t=5, p=1):
        self.scores = {
            ('C', 'C'): (r, r),
            ('D', 'D'): (p, p),
            ('C', 'D'): (s, t),
            ('D', 'C'): (t, s),
        }

    def RPST(self):
        """Return the values in the game matrix in the Press and Dyson notation."""
        R = self.scores[('C', 'C')][0]
        P = self.scores[('D', 'D')][0]
        S = self.scores[('C', 'D')][0]
        T = self.scores[('D', 'C')][0]
        return (R, P, S, T)

    def score(self, pair):
        """Return the appropriate score for decision pair.

        Returns the appropriate score (as a tuple) from the scores dictionary
        for a given pair of plays (passed in as a tuple).
        e.g. score(('C', 'C')) returns (2, 2)
        """
        return self.scores[pair]

DefaultGame = Game()
