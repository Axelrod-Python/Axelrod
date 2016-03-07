from .match import Match


def pair_of_players(players, player1_index, player2_index):
    """
    Create a pair of Player objects.

    If the two index numbers are the same, the second player object is
    created using the clone method of the first.

    Parameters
    ----------
    players : list
        A list of axelrod.Player objects
    player1_index : integer
        index number of player 1 within self.players list
    player2_index : integer
        index number of player 2 within self.players list

    Returns
    -------
    tuple
        A pair of axelrod.Player objects
    """
    player1 = players[player1_index]
    if player1_index == player2_index:
        player2 = player1.clone()
    else:
        player2 = players[player2_index]
    return (player1, player2)


def round_robin(players, turns, deterministic_cache,
                cache_mutable=True, noise=0):
    """
    Create a dictionary of match objects for a round robin tournament.

    Parameters
    ----------
    players : list
        A list of axelrod.Player objects
    turns : integer
        The number of turns per match
    deterministic_cache : dictionary
        A cache of resulting actions for deterministic matches
    cache_mutable : boolean
        Whether the deterministic cache should be updated
    noise : float
        The probability that a player's intended action should be flipped

    Returns
    -------
    dictionary
        Mapping a tuple of player index numbers to an axelrod Match object
    """
    matches = {}
    for player1_index in range(len(players)):
        for player2_index in range(player1_index, len(players)):
            pair = pair_of_players(players, player1_index, player2_index)
            match = Match(
                pair, turns, deterministic_cache, cache_mutable, noise)
            matches[(player1_index, player2_index)] = match
    return matches
