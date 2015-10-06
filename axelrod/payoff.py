import math

def payoff_matrix(interactions, game):
    """
    Parameters
    ----------
    interactions : list
        A matrix of the form:

        e.g. for a tournament between Cooperator and Defector with 2 turns per
        round:
        [
            [('C', 'C'), ('C', 'C')], [('C', 'D'), ('C', 'D')],
            [('D', 'C'), ('D', 'C')], [('D', 'D'), ('D', 'D')]
        ]

        i.e. one list per player, containing one list per opponent (in order of
        player index) which contains a pair of interactions for each turn in a
        round robin.

    game : axelrod.Game
        The game object to score the tournament.

    Returns
    -------
    list
        A matrix of the form:

        [
            [[a, j], [b, k], [c, l]],
            [[d, m], [e, n], [f, o]],
            [[g, p], [h, q], [i, r]],
        ]

        i.e. one row per player, containing one element per opponent (in
        order of player index) which lists payoffs for each repetition.
    """
    pass

def scores(payoff, nplayers, repetitions):
    """
    Parameters
    ----------
    payoff : list
        A matrix of the form:

        [
            [[a, j], [b, k], [c, l]],
            [[d, m], [e, n], [f, o]],
            [[g, p], [h, q], [i, r]],
        ]

        i.e. one row per player, containing one element per opponent (in
        order of player index) which lists payoffs for each repetition.

    nplayers : integer
        The number of players in the tournament.
    repetitions : integer
        The number of repetitions in the tournament.

    Returns
    -------
    list
        A scores matrix of the form:

            [
                [a + b + c, j + k + l],
                [d + e + f, m + n+ o],
                [h + h + i, p + q + r],
            ]

        i.e. one row per player which lists the total score for each
        repetition.

        In Axelrod's original tournament, there were no self-interactions
        (e.g. player 1 versus player 1) and so these are also excluded from the
        scores here by the condition on ip and ires.
    """
    scores = []
    for ires, res in enumerate(payoff):
        scores.append([])
        for irep in range(repetitions):
            scores[-1].append(0)
            for ip in range(nplayers):
                if ip != ires:
                    scores[-1][-1] += res[ip][irep]
    return scores

def normalised_scores(scores, nplayers, turns):
    """
    Parameters
    ----------
    scores : list
        A scores matrix (S) of the form returned by the scores function.
    nplayers : integer
        The number of players in the tournament.
    turns : integer
        The number of turns in each round robin.

    Returns
    -------
    list
        A normalised scores matrix (N) such that:

            N = S / t

        where t is the total number of turns played per repetition for a given
        player excluding self-interactions.
    """
    normalisation = turns * (nplayers - 1)
    return [
        [1.0 * s / normalisation for s in r] for r in scores]

def median(list):
    """
    Parameters
    ----------
    list : list
        A list of numeric values

    Returns
    -------
    float
        The median value of the list.
    """
    list = sorted(list)
    if len(list) < 1:
        return None
    if len(list) % 2 == 1:
        return list[((len(list) + 1) // 2) - 1]
    if len(list) % 2 == 0:
        return float(sum(list[(len(list) // 2) - 1:(len(list) // 2) + 1])) / 2.0

def ranking(scores, nplayers):
    """
    Parameters
    ----------
    scores : list
        A scores matrix (S) of the form returned by the scores function.
    nplayers : integer
        The number of players in the tournament.

    Returns
    -------
    list
        A list of players (their index within the players list rather than
        a player instance) ordered by median score
    """
    ranking = sorted(
        range(nplayers),
        key=lambda i: -median(scores[i]))
    return ranking

def ranked_names(players, ranking):
    """
    Parameters
    ----------
    players : list
        The list of players in the tournament
    ranking : list
        A list of player index numbers - as returned by the ranking function

    Returns
    -------
    list
         A list of player names sorted by their ranked order.
    """
    ranked_names = [str(players[i]) for i in ranking]
    return ranked_names

def normalised_payoff(payoff_matrix, turns, repetitions):
    """
    Parameters
    ----------
    payoff : list
        A matrix of the form:

        [
            [[a, j], [b, k], [c, l]],
            [[d, m], [e, n], [f, o]],
            [[g, p], [h, q], [i, r]],
        ]

        i.e. one row per player, containing one element per opponent (in
        order of player index) which lists payoffs for each repetition.

    turns : integer
        The number of turns in each round robin.
    repetitions : integer
        The number of repetitions in the tournament.

    Returns
    -------
    list
        A per-turn averaged payoff matrix and its standard deviations.
    """
    averages = []
    stddevs = []
    for res in payoff_matrix:
        averages.append([])
        stddevs.append([])
        for s in res:
            perturn = [1.0 * rep / turns for rep in s]
            avg = sum(perturn) / repetitions
            dev = math.sqrt(
                sum([(avg - pt)**2 for pt in perturn]) / repetitions)
            averages[-1].append(avg)
            stddevs[-1].append(dev)
    return averages, stddevs

def winning_player(players, payoffs):
    """
    Parameters
    ----------
    players : tuple
        A pair of player indexes
    payoffs : tuple
        A pair of payoffs for the two players

    Returns
    -------
    integer
        The index of the winning player or None if a draw
    """
    if payoffs[0] == payoffs[1]:
        return None
    else:
        winning_payoff = max(payoffs)
        winning_payoff_index = payoffs.index(winning_payoff)
        winner = players[winning_payoff_index]
        return winner

def wins(payoff, nplayers, repetitions):
    """
    Parameters
    ----------
    payoff : list
        A matrix of the form:

        [
            [[a, j], [b, k], [c, l]],
            [[d, m], [e, n], [f, o]],
            [[g, p], [h, q], [i, r]],
        ]

        i.e. one row per player, containing one element per opponent (in
        order of player index) which lists payoffs for each repetition.

    nplayers : integer
        The number of players in the tournament.
    repetitions : integer
        The number of repetitions in the tournament.

    Returns
    -------
    list
        A wins matrix of the form:

        [
            [player1 wins in repetition1, player1 wins in repetition2],
            [player2 wins in repetition1, player2 wins in repetition2],
            [player3 wins in repetition1, player3 wins in repetition2],
        ]

        i.e. one row per player which lists the total wins for that player
        in each repetition.
    """
    wins = [
        [0 for r in range(repetitions)] for p in range(nplayers)]
    for player in range(nplayers):
        for opponent in range(nplayers):
            players = (player, opponent)
            for repetition in range(repetitions):
                payoffs = (
                    payoff[player][opponent][repetition],
                    payoff[opponent][player][repetition])
                winner = winning_player(players, payoffs)
                if winner is not None:
                    wins[winner][repetition] += 1
    return wins
