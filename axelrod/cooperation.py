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
