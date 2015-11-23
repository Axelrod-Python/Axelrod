import math
from numpy import median, mean
from axelrod import Actions

C, D = Actions.C, Actions.D


def player_count(interactions):
    """
    The number of players derived from a dictionary of interactions

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

    Returns
    -------
    nplayers : integer
        The number of players in the round robin

        The number of ways (c) to select groups of r members from a set of n
        members is given by:

            c = n! / r!(n - r)!

        In this case, we are selecting pairs of players (p) and thus r = 2,
        giving:

            p = n(n-1) / 2 or p = (n^2 - n) / 2

        However, we also have the case where each player plays itself gving:

            p = (n^2 + n) / 2

        Using the quadratic equation to rearrange for n gives:

            n = (-1 +- sqrt(1 + 8p)) / 2

        Taking only the real roots allows us to derive the number of players
        given the number of pairs:

            n = (sqrt(8p + 1) -1) / 2
    """
    return int((math.sqrt(len(interactions) * 8 + 1) - 1) / 2)


# As yet unused until RoundRobin returns interactions
def payoff_matrix(interactions, game):
    """
    The payoff matrix from a single round robin.

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
    game : axelrod.Game
        The game object to score the tournament.

    Returns
    -------
    list
        A matrix (P) of the form:

        [
            [a, b, c],
            [d, e, f],
            [g, h, i]
        ]

        i.e. an n by n matrix where n is the number of players. Each row (i)
        and column (j) represents an individual player and the the value Pij
        is the payoff value for player (i) versus player (j).
    """
    nplayers = player_count(interactions)
    payoffs = [[0 for i in range(nplayers)] for j in range(nplayers)]
    for players, actions in interactions.items():
        payoff = interaction_payoff(actions, game)
        payoffs[players[0]][players[1]] += payoff[0]
        if players[0] != players[1]:
            payoffs[players[1]][players[0]] += payoff[1]
    return payoffs


# As yet unused until RoundRobin returns interactions
def interaction_payoff(actions, game):
    """
    The payoff values for a single interaction of n turns between two players.

    Parameters
    ----------
    actions : list
        A list of tuples of the form:

        [(C, C), (C, C)], [(C, D), (C, D)]

    game : axelrod.Game
        The game object to score the actions.

    Returns
    -------
    tuple
        A pair of payoffs for each of the two players in the interaction.

        i.e. for the actions list quoted above, the resulting payoff returned
        would be:
            (6, 16)
    """
    player1_payoff, player2_payoff = 0, 0
    for turn in actions:
        score = game.score(turn)
        player1_payoff += score[0]
        player2_payoff += score[1]
    return (player1_payoff, player2_payoff)


def scores(payoff):
    """
    The scores matrix excluding self-interactions

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
    nplayers = len(payoff)
    repetitions = len(payoff[0][0])
    scores = []
    for ires, res in enumerate(payoff):
        scores.append([])
        for irep in range(repetitions):
            scores[-1].append(0)
            for ip in range(nplayers):
                if ip != ires:
                    scores[-1][-1] += res[ip][irep]
    return scores


def normalised_scores(scores, turns):
    """
    The per-turn normalised scores matrix

    Parameters
    ----------
    scores : list
        A scores matrix (S) of the form returned by the scores function.
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
    nplayers = len(scores)
    normalisation = turns * (nplayers - 1)
    return [
        [1.0 * s / normalisation for s in r] for r in scores]


def ranking(scores):
    """
    Player index numbers listed by order of median score

    Parameters
    ----------
    scores : list
        A scores matrix (S) of the form returned by the scores function.

    Returns
    -------
    list
        A list of players (their index within the players list rather than
        a player instance) ordered by median score
    """
    nplayers = len(scores)
    ranking = sorted(
        range(nplayers),
        key=lambda i: -median(scores[i]))
    return ranking


def ranked_names(players, ranking):
    """
    Player names listed by their ranked order

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


def normalised_payoff(payoff_matrix, turns):
    """
    The per-turn averaged payoff matrix and standard deviations

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

    Returns
    -------
    list
        A per-turn averaged payoff matrix and its standard deviations.
    """
    repetitions = len(payoff_matrix[0][0])
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
    The index of a winning player from a pair of payoff values

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


def wins(payoff):
    """
    An n by n matrix of win counts for n players

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
    nplayers = len(payoff)
    repetitions = len(payoff[0][0])
    wins = [
        [0 for r in range(repetitions)] for p in range(nplayers)]
    for player in range(nplayers):
        for opponent in range(player + 1):  # Ensures we don't count wins twice
            players = (player, opponent)
            for repetition in range(repetitions):
                payoffs = (
                    payoff[player][opponent][repetition],
                    payoff[opponent][player][repetition])
                winner = winning_player(players, payoffs)
                if winner is not None:
                    wins[winner][repetition] += 1
    return wins


def payoff_diffs_means(payoff, turns):
    """
    An n by n matrix of mean payoff differences for n players

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

    Returns
    -------
    list (of lists)
        A matrix of mean payoff differences of the form with i, j entry:
        mean([player_i payoff - player_j payoff in repetition1,
         player_i payoff - player_j payoff in repetition2,
         ...])

        normalized by the number of turns. I.e. the nplayers x nplayers
        matrix of mean payoff differences between each player and opponent.
    """
    nplayers = len(payoff)
    repetitions = len(payoff[0][0])
    diffs_matrix = [[0] * nplayers for _ in range(nplayers)]
    for player in range(nplayers):
        for opponent in range(nplayers):
            diffs = []
            for repetition in range(repetitions):
                diff = (payoff[player][opponent][repetition] - payoff[opponent][player][repetition]) / float(turns)
                diffs.append(diff)
            diffs_matrix[player][opponent] = mean(diffs)

    return diffs_matrix


def score_diffs(payoff, turns):
    """
    An n by n matrix of per-turn normalised payoff differences for n players

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

    Returns
    -------
    list (of lists of lists)
        A matrix of payoff differences of the form with i, j entry:
        [player_i payoff - player_j payoff for each j and each repetition]
        where the payoffs have been normalized by the number of turns and summed
        over the repititions.
    """
    nplayers = len(payoff)
    repetitions = len(payoff[0][0])
    diffs = [
        [] for p in range(nplayers)]
    for player in range(nplayers):
        for opponent in range(nplayers):
            for repetition in range(repetitions):
                diff = (payoff[player][opponent][repetition] - payoff[opponent][player][repetition]) / float(turns)
                diffs[player].append(diff)

    return diffs
