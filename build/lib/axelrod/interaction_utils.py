# -*- coding: utf-8 -*-
"""
Functions to calculate results from interactions. Interactions are lists of the
form:

    [('C', 'D'), ('D', 'C'),...]

This is used by both the Match class and the ResultSet class which analyse
interactions.
"""
from .game import Game
from axelrod import Actions


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
