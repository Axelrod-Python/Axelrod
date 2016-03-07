from .match import Match


def round_robin(players, opponents, turns, deterministic_cache,
                cache_mutable=True, noise=0):
    """
    Create a dictionary of match objects for a round robin tournament.

    Parameters
    ----------
    players : list
        A list of axelrod.Player objects
    opponents : list
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
            pair = (players[player1_index], opponents[player2_index])
            match = Match(
                pair, turns, deterministic_cache, cache_mutable, noise)
            matches[(player1_index, player2_index)] = match
    return matches
