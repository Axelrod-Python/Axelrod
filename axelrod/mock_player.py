from collections import defaultdict
import copy
from axelrod import (Actions, Player, get_state_distribution_from_history,
                     update_history, update_state_distribution)

C, D = Actions.C, Actions.D


class MockPlayer(Player):
    """Creates a mock player that enforces a particular next move for a given
    player."""

    def __init__(self, player, move):
        # Need to retain history for opponents that examine opponents history
        # Do a deep copy just to be safe
        super().__init__()
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
        # Simulate Players
        mock_P1 = MockPlayer(P1, h1)
        mock_P2 = MockPlayer(P2, h1)
        mock_P1.state_distribution = defaultdict(
            int, zip(P1.history, P2.history))
        mock_P2.state_distribution = defaultdict(
            int, zip(P2.history, P1.history))
        # Force plays

        s1 = P1.strategy(mock_P2)
        s2 = P2.strategy(mock_P1)
        # Record intended history
        # Update Cooperation / Defection counts
        update_history(P1, h1)
        update_history(P2, h2)
        update_state_distribution(P1, h1, h2)
        update_state_distribution(P2, h2, h1)
        return (h1, h2)
    else:
        s1 = P1.strategy(P2)
        s2 = P2.strategy(P1)
        # Record history
        update_history(P1, s1)
        update_history(P2, s2)
        update_state_distribution(P1, s1, s2)
        update_state_distribution(P2, s2, s1)
        return (s1, s2)
