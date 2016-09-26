# -*- coding: utf-8 -*-
"""
Functions to calculate results from interactions. Interactions are lists of the
form:

    [('C', 'D'), ('D', 'C'),...]

This is used by both the Match class and the ResultSet class which analyse
interactions.
"""
import csv
from collections import Counter

from .game import Game
from axelrod import Actions

import tqdm

C, D = Actions.C, Actions.D


def compute_scores(interactions, game=None):
    """Returns the scores of a given set of interactions."""
    if not game:
        game = Game()
    return [game.score(plays) for plays in interactions]


def compute_final_score(interactions, game=None):
    """Returns the final score of a given set of interactions."""
    scores = compute_scores(interactions, game)
    if len(scores) == 0:
        return None

    final_score = tuple(sum([score[player_index] for score in scores])
                        for player_index in [0, 1])
    return final_score


def compute_final_score_per_turn(interactions, game=None):
    """Returns the mean score per round for a set of interactions"""
    scores = compute_scores(interactions, game)
    num_turns = len(interactions)

    if len(scores) == 0:
        return None

    final_score_per_turn = tuple(
        sum([score[player_index] for score in scores]) / (float(num_turns))
        for player_index in [0, 1])
    return final_score_per_turn


def compute_winner_index(interactions, game=None):
    """Returns the index of the winner of the Match"""
    scores = compute_final_score(interactions, game)

    if scores is not None:
        if scores[0] == scores[1]:
            return False  # No winner
        return max([0, 1], key=lambda i: scores[i])
    return None


def compute_cooperations(interactions):
    """Returns the count of cooperations by each player for a set of
    interactions"""

    if len(interactions) == 0:
        return None

    cooperation = tuple(sum([play[player_index] == C for play in interactions])
                        for player_index in [0, 1])
    return cooperation


def compute_normalised_cooperation(interactions):
    """Returns the count of cooperations by each player per turn for a set of
    interactions"""
    if len(interactions) == 0:
        return None

    num_turns = len(interactions)
    cooperation = compute_cooperations(interactions)

    normalised_cooperation = tuple([c / float(num_turns) for c in cooperation])

    return normalised_cooperation


def compute_state_distribution(interactions):
    """
    Returns the count of each state for a set of interactions.

    Parameters
    ----------
    interactions : list of tuples
        A list containing the interactions of the match as shown at the top of
        this file.

    Returns
    ----------
    Counter(interactions) : Counter Object
        Dictionary where the keys are the states and the values are the number
        of times that state occurs.
    """
    if not interactions:
        return None
    return Counter(interactions)


def compute_normalised_state_distribution(interactions):
    """
    Returns the normalized count of each state for a set of interactions.

    Parameters
    ----------
    interactions : list of tuples
        A list containing the interactions of the match as shown at the top of
        this file.

    Returns
    ----------
    normalized_count : Counter Object
        Dictionary where the keys are the states and the values are a normalized
        count of the number of times that state occurs.
    """
    if not interactions:
        return None

    interactions_count = Counter(interactions)
    total = sum(interactions_count.values(), 0.0)
    # By starting the sum with 0.0 we make sure total is a floating point value,
    # avoiding the Python 2 floor division behaviour of / with integer operands
    # (Stack Overflow)

    normalized_count = Counter({key: value / total for key, value in
                                interactions_count.items()})
    return normalized_count


def sparkline(actions, c_symbol=u'█', d_symbol=u' '):
    return u''.join([
        c_symbol if play == 'C' else d_symbol for play in actions])


def compute_sparklines(interactions, c_symbol=u'█', d_symbol=u' '):
    """Returns the sparklines for a set of interactions"""
    if len(interactions) == 0:
        return None

    histories = list(zip(*interactions))
    return (
        sparkline(histories[0], c_symbol, d_symbol) +
        u'\n' +
        sparkline(histories[1], c_symbol, d_symbol))


def read_interactions_from_file(filename, progress_bar=True,
                                num_interactions=False):
    """
    Reads a file and returns a dictionary mapping tuples of player pairs to
    lists of interactions
    """
    if progress_bar:
        if not num_interactions:
            with open(filename) as f:
                num_interactions = sum(1 for line in f)
        progress_bar = tqdm.tqdm(total=num_interactions, desc="Loading")

    pairs_to_interactions = {}
    with open(filename, 'r') as f:
        for row in csv.reader(f):
            index_pair = (int(row[0]), int(row[1]))
            interaction = list(zip(row[4], row[5]))

            try:
                pairs_to_interactions[index_pair].append(interaction)
            except KeyError:
                pairs_to_interactions[index_pair] = [interaction]

            if progress_bar:
                progress_bar.update()

    if progress_bar:
        progress_bar.close()
    return pairs_to_interactions


def string_to_interactions(string):
    """
    Converts a compact string representation of an interaction to an
    interaction:

    'CDCDDD' -> [('C', 'D'), ('C', 'D'), ('D', 'D')]
    """
    interactions = []
    interactions_list = list(string)
    while interactions_list:
        p1action = interactions_list.pop(0)
        p2action = interactions_list.pop(0)
        interactions.append((p1action, p2action))
    return interactions
