import warnings
from axelrod import (Actions, Player, update_history, update_state_distribution)

C, D = Actions.C, Actions.D


class MockPlayer(Player):
    """Creates a mock player that copies a history and state distribution to
    simulate a history of play, and then plays a given sequence of actions. If
    no actions are given, plays like Cooperator.
    """

    name = "Mock Player"

    def __init__(self, actions=None, history=None, state_dist=None):
        # Need to retain history for opponents that examine opponents history
        # Do a deep copy just to be safe
        super().__init__()
        if history:
            # Make sure we both copy the history and get the right counts
            # for cooperations and defections.
            for action in history:
                    update_history(self, action)
        if state_dist:
            self.state_distribution = dict(state_dist)
        if actions:
            self.actions = list(actions)
        else:
            self.actions = []

    def strategy(self, opponent):
        # Return the next saved action, if present.
        try:
            action = self.actions.pop(0)
            return action
        except IndexError:
            return C


def simulate_play(P1, P2, h1=None, h2=None):
    """
    Simulates play with or without forced history. If h1 and h2 are given, these
    actions are enforced in the players strategy. This generally should not be
    necessary, but various tests may force impossible or unlikely histories.
    """

    if h1 and h2:
        mock_P1 = MockPlayer(actions=[h1], history=P1.history)
        mock_P2 = MockPlayer(actions=[h2], history=P2.history)
        # Force plays
        s1 = P1.strategy(mock_P2)
        s2 = P2.strategy(mock_P1)
        if (s1 != h1) or (s2 != h2):
            warnings.warn(
            "Simulated play mismatch with expected history: Round was "
            "({}, {}) but ({}, {}) was expected for player: {}".format(
                s1, s2, h1, h2, str(P1))
            )
        # Record intended history
        # Update Cooperation / Defection counts
        update_history(P1, h1)
        update_history(P2, h2)
        update_state_distribution(P1, h1, h2)
        update_state_distribution(P2, h2, h1)
        return (s1, s2)
    else:
        s1 = P1.strategy(P2)
        s2 = P2.strategy(P1)
        # Record history
        update_history(P1, s1)
        update_history(P2, s2)
        update_state_distribution(P1, s1, s2)
        update_state_distribution(P2, s2, s1)
        return (s1, s2)
