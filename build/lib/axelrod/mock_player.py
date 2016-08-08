import copy
from axelrod import Player, update_history, Actions

C, D = Actions.C, Actions.D


class MockPlayer(Player):
    """Creates a mock player that enforces a particular next move for a given
    player."""

    def __init__(self, player, move):
        # Need to retain history for opponents that examine opponents history
        # Do a deep copy just to be safe
        Player.__init__(self)
        self.history = copy.deepcopy(player.history)
        self.cooperations = player.cooperations
        self.defections = player.defections
        self.move = move

    def strategy(self, opponent):
        # Just return the saved move
        return self.move


def simulate_play(P1, P2, h1=None, h2=None):
    """
    Simulates play with or without forced history. If h1 and h2 are given, these
    moves are enforced in the players strategy. This generally should not be
    necessary, but various tests may force impossible or unlikely histories.
    """

    if h1 and h2:
        # Simulate Plays
        s1 = P1.strategy(MockPlayer(P2, h2))
        s2 = P2.strategy(MockPlayer(P1, h1))
        # Record intended history
        # Update Cooperation / Defection counts
        update_history(P1, h1)
        update_history(P2, h2)
        return (h1, h2)
    else:
        s1 = P1.strategy(P2)
        s2 = P2.strategy(P1)
        # Record history
        update_history(P1, s1)
        update_history(P2, s2)
        return (s1, s2)
