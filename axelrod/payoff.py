import math

def scores(payoff, nplayers, repetitions):
    """
    Arguments
    ---------
    payoff (list): a matrix of the form:

        [
            [[a, j], [b, k], [c, l]],
            [[d, m], [e, n], [f, o]],
            [[g, p], [h, q], [i, r]],
        ]

    i.e. one row per player, containing one element per opponent (in
    order of player index) which lists payoffs for each repetition.

    nplayers (integer): The number of players in the tournament.
    repetitions (integer): The number of repetitions in the tournament.

    Returns
    -------
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
    Arguments
    ---------
    scores (list): A scores matrix (S) of the form returned by the scores
    function.
    nplayers (integer): The number of players in the tournament.
    turns (integer): The number of turns in each round robin.

    Returns
    -------
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
    Arguments
    ---------
    list (list): A list of numeric values

    Returns
    -------
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
    Arguments
    ---------
    scores (list): A scores matrix (S) of the form returned by the scores
    function.
    nplayers (integer): The number of players in the tournament.

    Returns
    -------
    A list of players (their index within the players list rather than
    a player instance) ordered by median score
    """
    ranking = sorted(
        range(nplayers),
        key=lambda i: -median(scores[i]))
    return ranking

def ranked_names(players, ranking):
    """
    Arguments
    ---------
    players (list): The list of players in the tournament
    ranking (list): A list of player index numbers - as returned by the ranking
    function

    Returns:
         A list of player names sorted by their ranked order.
    """
    ranked_names = [str(players[i]) for i in ranking]
    return ranked_names

def payoff_matrix(payoff, turns, repetitions):
    """
    Arguments
    ---------
    payoff (list): a matrix of the form:

        [
            [[a, j], [b, k], [c, l]],
            [[d, m], [e, n], [f, o]],
            [[g, p], [h, q], [i, r]],
        ]

    i.e. one row per player, containing one element per opponent (in
    order of player index) which lists payoffs for each repetition.

    turns (integer): The number of turns in each round robin.
    repetitions (integer): The number of repetitions in the tournament.

    Returns
    -------
    A per-turn averaged payoff matrix and its standard deviations.
    """
    averages = []
    stddevs = []
    for res in payoff:
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
