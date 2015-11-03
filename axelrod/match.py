def actions(self, players, player1_index, player2_index, turns,
            deterministic_cache=None, cache_mutable=True, noise=0):
    """
    Plays two players against each other and returns the list of actions.

    Parameters
    ----------
    players : list
        A list of Axelrod.Player instances
    player1_index : integer
        The index within the players list for player 1
    player2_index : integer
        The index within the players list for player 2
    turns : integer
        The number of turns per match
    deterministic_cache : dictionary
        A cache of resulting actions for stochastic matches
    cache_mutable : boolean
        Whether the deterministic cache can be updated or not
    noise : float
        The probability that a player's intended action should be flipped

    Returns
    -------
    A list of the form:

    e.g. for a 2 turn match between Cooperator and Defector:

        [(C, C), (C, D)]

    i.e. One entry per turn containing a pair of actions.
    """
    player1, player2, classes = self._pair_of_players(
        player1_index, player2_index)
    play_required = (
        self._stochastic_interaction(player1, player2) or
        classes not in self.deterministic_cache)
    if play_required:
        pass
    else:
        pass
    return


def pair_of_players(players, player1_index, player2_index):
    """
    A pair of player objects and their classes

    Parameters
    ----------
    players : list
        A list of Axelrod.Player instances
    player1_index : integer
        The index within the players list for player 1.
    player2_index : integer
        The index within the players list for player 2.

    Returns
    -------
    Two Axelrod.Player instances and a tuple of their classes
    """
    player1 = players[player1_index]
    class1 = player1.__class__
    if player1_index == player2_index:
        player2 = player1.clone()
    else:
        player2 = players[player2_index]
    class2 = player2.__class__
    return player1, player2, (class1, class2)


def is_stochastic_match(player1, player2, noise):
    """
    A boolean to show whether a match between two players would be stochastic

    Parameters
    ----------
    player1 : axelrod.Player
    player2 : axelrod.Player
    noise : float
        The probability that a player's intended action should be flipped

    Returns
    -------
    boolean

    """
    return (
        noise or
        player1.classifier['stochastic'] or
        player2.classifier['stochastic'])


def play_match(player1, player2, classes, turns, deterministic_cache,
               cache_mutable, noise):
    turn = 0
    player1.reset()
    player2.reset()
    while turn < turns:
        turn += 1
        player1.play(player2, noise)
    if cache_update_required(player1, player2, noise):
        deterministic_cache[classes] = {}
    return


def cache_update_required(p1, p2, cache_mutable, noise):
    return (
        not noise and
        cache_mutable and
        not (p1.classifier['stochastic'] or p2.classifier['stochastic']))
