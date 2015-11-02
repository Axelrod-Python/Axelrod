from math import sqrt
from . import eigen
from axelrod import Actions
from axelrod.payoff import player_count

C, D = Actions.C, Actions.D


# As yet unused until RoundRobin returns interactions
def cooperation_matrix(interactions):
    """
    The cooperation matrix from a single round robin.

    Parameters
    ----------
    interactions : dictionary
        A dictionary of the form:

        e.g. for a round robin between Cooperator, Defector and Alternator
        with 2 turns per round:
        {
            (0, 0): [(C, C), (C, C)].
            (0, 1): [(C, D), (C, D)],
            (0, 2): [(C, C), (C, D)],
            (1, 1): [(D, D), (D, D)],
            (1, 2): [(D, C), (D, D)],
            (2, 2): [(C, C), (D, D)]
        }

        i.e. the key is a pair of player index numbers and the value, a list of
        plays. The list contains one pair per turn in the round robin.
        The dictionary contains one entry for each combination of players.

    nplayers : integer
        The number of players in the round robin

    Returns
    -------
    list
        The cooperation matrix (C) of the form:

            [
                [a, b, c],
                [d, e, f],
                [g, h, i],
            ]

        i.e. an n by n matrix where n is the number of players. Each row (i)
        and column (j) represents an individual player and the the value Cij
        is the number of times player i cooperated against opponent j.
    """
    nplayers = player_count(interactions)
    cooperation = [[0 for i in range(nplayers)] for j in range(nplayers)]
    for players, actions in interactions.items():
        p1_actions, p2_actions = zip(*actions)
        p1_cooperation = p1_actions.count(C)
        p2_cooperation = p2_actions.count(C)
        cooperation[players[0]][players[1]] = p1_cooperation
        if players[0] != players[1]:
            cooperation[players[1]][players[0]] = p2_cooperation
    return cooperation


def cooperation(results):
    """
    The total cooperation matrix from a tournament of multiple repetitions.

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
    The per-turn normalised cooperation matrix for a tournament of n repetitions.

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
    The vengeful cooperation matrix derived from the cooperation matrix.

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
    A list of cooperation ratings for each player

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
    A null n by n matrix for n players

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
    An n by n matrix of good partner ratings for n players

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
    The number of interactions between n players

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
    A list of good partner ratings for n players in order of rating

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
    The principal eigenvector of the cooperation matrix

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
