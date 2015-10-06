from . import eigen

def cooperation_matrix(results):
    """
    Parameters
    ----------
    results : list
        A matrix of the form:

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
    list
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
    Parameters
    ----------
    cooperation : list
        The cooperation matrix (C)
    turns : integer
        The number of turns in each round robin.
    repetitions : integer
        The number of repetitions in the tournament.

    Returns
    -------
    list
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
    Parameters
    ----------
    cooperation : list
        A cooperation matrix (C)

    Returns
    -------
    list
        A matrix (D) such that:

            Dij = 2(Cij -0.5)
    """
    return [[2 * (element - 0.5) for element in row] for row in cooperation]

def cooperating_rating(cooperation, nplayers, turns, repetitions):
    """
    Parameters
    ----------
    cooperation : list
        The cooperation matrix
    nplayers : integer
        The number of players in the tournament.
    turns : integer
        The number of turns in each round robin.
    repetitions : integer
        The number of repetitions in the tournament.

    Returns
    -------
    list
        a list of cooperation rates ordered by player index
    """
    total_turns = turns * repetitions * nplayers
    return [1.0 * sum(row) / total_turns for row in cooperation]

def null_matrix(nplayers):
    """
    Parameters
    ----------
    nplayers : integer
        The number of players in the tournament.
    Returns
    -------
    list
        A null n by n matrix where n is the number of players.
    """
    plist = list(range(nplayers))
    return [[0 for j in plist] for i in plist]

def good_partner_matrix(results, nplayers, repetitions):
    """
    Parameters
    ----------
    results : list
        A cooperation results matrix of the form:

        [
            [[a, j], [b, k], [c, l]],
            [[d, m], [e, n], [f, o]],
            [[g, p], [h, q], [i, r]],
        ]

        i.e. one row per player, containing one element per opponent (in
        order of player index) which lists cooperation values for each
        repetition.

    nplayers : integer
        The number of players in the tournament.
    repetitions : integer
        The number of repetitions in the tournament.

    Returns
    -------
    list
        The good partner matrix (P) of the form:

        [
            [0, 0 + (1 if b >= d) + (1 if k >= m), 0 + (1 if c >= g) + (1 if l >= p) ],
            [0 + (1 if e >= g) + (1 if n >= p), 0, 0 + (1 if f >= h) + (1 if o >= q)],
            [0 + (1 if g >= c) + (1 if p >= l), 0 + (1 if h >= f) + (1 if q >= o), 0]
        ]

        i.e. an n by n matrix where n is the number of players. Each row (i)
        and column (j) represents an individual player and the the value Pij
        is the sum of the number of repetitions where player i cooperated as
        often or more than opponent j.
    """
    matrix = null_matrix(nplayers)
    for r in range(repetitions):
        for i in range(nplayers):
            for j in range(nplayers):
                if i != j and results[i][j][r] >= results[j][i][r]:
                    matrix[i][j] += 1
    return matrix

def n_interactions(nplayers, repetitions):
    """
    Parameters
    ----------
    nplayers : integer
        The number of players in the tournament.
    repetitions : integer
        The number of repetitions in the tournament.

    Returns
    -------
    integer
        The number of interactions between players excluding self-interactions.
    """
    return repetitions * (nplayers - 1)

def good_partner_rating(good_partner_matrix, nplayers, repetitions):
    """
    Parameters
    ----------
    good_partner_matrix : list
        The good partner matrix
    nplayers : integer
        The number of players in the tournament.
    repetitions : integer
        The number of repetitions in the tournament.

    Returns
    -------
    list
        A list of good partner ratings ordered by player index.
    """
    return [1.0 * sum(row) / n_interactions(nplayers, repetitions)
        for row in good_partner_matrix]


def eigenvector(cooperation_matrix):
    """
    Parameters
    ----------
    cooperation_matrix : list
        A cooperation matrix

    Returns
    -------
    list
        The principal eigenvector of the cooperation matrix.
    """
    eigenvector, eigenvalue = eigen.principal_eigenvector(
        cooperation_matrix, 1000, 1e-3
    )
    return eigenvector.tolist()
