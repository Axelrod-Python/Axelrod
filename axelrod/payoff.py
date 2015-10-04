def scores(payoff, nplayers, repetitions):
    """
    Args:
        payoff (list): a matrix of the form:

            [
                [[a, j], [b, k], [c, l]],
                [[d, m], [e, n], [f, o]],
                [[g, p], [h, q], [i, r]],
            ]

        i.e. one row per player, containing one element per opponent (in
        order of player index) which lists payoffs for each repetition.

        nplayers (integer): The number of players in the tournament.
        repetitions (integer): The number of repetition in the tournament.

    Returns:
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
