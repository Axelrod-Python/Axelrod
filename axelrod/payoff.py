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
