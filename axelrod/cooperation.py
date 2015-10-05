def cooperation_matrix(results):
    """
    Arguments
    ---------
    results (list): a matrix of the form:

        [
            [[a, j], [b, k], [c, l]],
            [[d, m], [e, n], [f, o]],
            [[g, p], [h, q], [i, r]],
        ]

    i.e. one row per player, containing one element per opponent (in
    order of player index) which lists cooperation values for each
    repetition.

    Returns
    -------
    The cooperation matrix (C) of the form:

        [
            [[a + j], [b + k], [c + l]],
            [[d + m], [e + n], [f + o]],
            [[g + p], [h + q], [i + r]],
        ]

    i.e. an n by n matrix where n is the number of players. Each row (i)
    and column (j) represents an individual player and the the value Cij
    is the number of times player i cooperated against opponent j.
    """
    return[[sum(element) for element in row] for row in results]

def normalised_cooperation(cooperation, turns, repetitions):
    """
    Arguments
    ---------
    cooperation (list): the cooperation matrix (C)
    turns (integer): The number of turns in each round robin.
    repetitions (integer): The number of repetitions in the tournament.

    Returns
    -------
    A matrix (N) such that:

        N = C / t

    where t is the total number of turns played in the tournament.
    """
    turns = turns * repetitions
    return[
        [1.0 * element / turns for element in row]
        for row in cooperation]

def vengeful_cooperation(cooperation):
    """
    Arguments
    ---------
    cooperation(list): A cooperation matrix (C)

    Returns
    -------
    A matrix (D) such that:

        Dij = 2(Cij -0.5)
    """
    return [[2 * (element - 0.5) for element in row] for row in cooperation]

def cooperating_rating(cooperation, nplayers, turns, repetitions):
    """
    Arguments
    ---------
    cooperation (list): the cooperation matrix
    nplayers (integer): The number of players in the tournament.
    turns (integer): The number of turns in each round robin.
    repetitions (integer): The number of repetitions in the tournament.

    Returns
    -------
    a list of cooperation rates ordered by player index
    """
    total_turns = turns * repetitions * nplayers
    return [1.0 * sum(row) / total_turns for row in cooperation]
