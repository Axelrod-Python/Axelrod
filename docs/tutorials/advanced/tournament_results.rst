.. _tournament-results:

Accessing tournament results
============================

This tutorial will show you how to access the various results of a tournament:

- Wins: the number of matches won by each player
- Match lengths: the number of turns of each match played by each player
  (relevant for tournaments with probabilistic ending).
- Scores: the total scores of each player.
- Normalised scores: the scores normalised by matches played and turns.
- Ranking: ranking of players based on median score.
- Ranked names: names of players in ranked order.
- Payoffs: average payoff per turn of each player.
- Payoff matrix: the payoff matrix showing the payoffs of each row player
  against each column player.
- Payoff standard deviation: the standard deviation of the payoffs matrix.
- Score differences: the score difference between each player.
- Payoff difference means: the mean score differences.
- Cooperation counts: the number of times each player cooperated.
- Normalised cooperation: cooperation count per turn.
- Normalised cooperation: cooperation count per turn.
- State distribution: the count of each type of state of a match
- Normalised state distribution: the normalised count of each type of state of a
  match
- State to action distribution: the count of each type of state to action pair
  of a match
- Normalised state distribution: the normalised count of each type of state to
  action pair of a match
- Initial cooperation count: the count of initial cooperation by each player.
- Initial cooperation rate: the rate of initial cooperation by each player.
- Cooperation rating: cooperation rating of each player
- Vengeful cooperation: a morality metric from the literature (see
  :ref:`morality-metrics`).
- Good partner matrix: a morality metric from [Singer-Clark2014]_.
- Good partner rating: a morality metric from [Singer-Clark2014]_.
- Eigenmoses rating: a morality metric from [Singer-Clark2014]_.
- Eigenjesus rating: a morality metric from [Singer-Clark2014]_.

As shown in :ref:`creating_tournaments` let us create a tournament::

    >>> import axelrod as axl
    >>> players = [axl.Cooperator(), axl.Defector(),
    ...            axl.TitForTat(), axl.Grudger()]
    >>> tournament = axl.Tournament(players, turns=10, repetitions=3)
    >>> results = tournament.play()

Wins
----

This gives the number of wins obtained by each player::

    >>> results.wins
    [[0, 0, 0], [3, 3, 3], [0, 0, 0], [0, 0, 0]]


The :code:`Defector` is the only player to win any matches (all other matches
are ties).

Match lengths
-------------

This gives the length of the matches played by each player::

    >>> import pprint  # Nicer formatting of output
    >>> pprint.pprint(results.match_lengths)
    [[[10.0, 10.0, 10.0, 10.0],
      [10.0, 10.0, 10.0, 10.0],
      [10.0, 10.0, 10.0, 10.0],
      [10.0, 10.0, 10.0, 10.0]],
     [[10.0, 10.0, 10.0, 10.0],
      [10.0, 10.0, 10.0, 10.0],
      [10.0, 10.0, 10.0, 10.0],
      [10.0, 10.0, 10.0, 10.0]],
     [[10.0, 10.0, 10.0, 10.0],
      [10.0, 10.0, 10.0, 10.0],
      [10.0, 10.0, 10.0, 10.0],
      [10.0, 10.0, 10.0, 10.0]]]


Every player plays 10 turns against every other player (including themselves)
for every repetition of the tournament.

Scores
------

This gives all the total tournament scores (per player and per repetition)::

    >>> results.scores
    [[60, 60, 60], [78, 78, 78], [69, 69, 69], [69, 69, 69]]

Normalised scores
-----------------

This gives the scores, averaged per opponent and turns::

    >>> results.normalised_scores  # doctest: +SKIP
    [[2.0, 2.0, 2.0], [2.6, 2.6, 2.6], [2.3, 2.3, 2.3], [2.3, 2.3, 2.3]]

We see that Cooperator got on average a score of 2 per turn per opponent::

    >>> results.normalised_scores[0]
    [2.0, 2.0, 2.0]

Ranking
-------

This gives the ranked index of each player::

    >>> results.ranking
    [1, 2, 3, 0]

The first player has index 1 (:code:`Defector`) and the last has index 0
(:code:`Cooperator`).

Ranked names
------------

This gives the player names in ranked order::

    >>> results.ranked_names
    ['Defector', 'Tit For Tat', 'Grudger', 'Cooperator']


Payoffs
-------

This gives for each player, against each opponent every payoff received for
each repetition::

    >>> pprint.pprint(results.payoffs)  # doctest: +SKIP
    [[[3.0, 3.0, 3.0], [0.0, 0.0, 0.0], [3.0, 3.0, 3.0], [3.0, 3.0, 3.0]],
     [[5.0, 5.0, 5.0], [1.0, 1.0, 1.0], [1.4, 1.4, 1.4], [1.4, 1.4, 1.4]],
     [[3.0, 3.0, 3.0], [0.9, 0.9, 0.9], [3.0, 3.0, 3.0], [3.0, 3.0, 3.0]],
     [[3.0, 3.0, 3.0], [0.9, 0.9, 0.9], [3.0, 3.0, 3.0], [3.0, 3.0, 3.0]]]


Payoff matrix
-------------

This gives the mean payoff of each player against every opponent::

    >>> pprint.pprint(results.payoff_matrix)  # doctest: +SKIP
    [[3.0, 0.0, 3.0, 3.0],
     [5.0, 1.0, 1.4, 1.4],
     [3.0, 0.9, 3.0, 3.0],
     [3.0, 0.9, 3.0, 3.0]]

We see that the :code:`Cooperator` gets a mean score of 3 against all players
except the :code:`Defector`::

    >>> results.payoff_matrix[0]
    [3.0, 0.0, 3.0, 3.0]

Payoff standard deviation
-------------------------

This gives the standard deviation of the payoff of each player against
every opponent::

    >>> pprint.pprint(results.payoff_stddevs)  # doctest: +SKIP
    [[0.0, 0.0, 0.0, 0.0],
     [0.0, 0.0, 2.2, 2.2],
     [0.0, 0.0, 0.0, 0.0],
     [0.0, 0.0, 0.0, 0.0]]

We see that there is no variation for the payoff for :code:`Cooperator`::

    >>> results.payoff_stddevs[0]
    [0.0, 0.0, 0.0, 0.0]

Score differences
-----------------

This gives the score difference for each player against each opponent for every
repetition::

    >>> pprint.pprint(results.score_diffs)  # doctest: +SKIP
    [[[0.0, 0.0, 0.0], [-5.0, -5.0, -5.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
     [[5.0, 5.0, 5.0], [0.0, 0.0, 0.0], [0.5, 0.5, 0.5], [0.5, 0.5, 0.5]],
     [[0.0, 0.0, 0.0], [-0.5, -0.5, -0.5], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
     [[0.0, 0.0, 0.0], [-0.5, -0.5, -0.5], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]]

We see that :code:`Cooperator` has no difference in score with all players
except against the :code:`Defector`::

    >>> results.score_diffs[0][1]
    [-5.0, -5.0, -5.0]

Payoff difference means
-----------------------

This gives the mean payoff differences over each repetition::

    >>> pprint.pprint(results.payoff_diffs_means)  # doctest: +SKIP
    [[0.0, -5.0, 0.0, 0.0],
     [5.0, 0.0, 0.49999999999999983, 0.49999999999999983],
     [0.0, -0.49999999999999983, 0.0, 0.0],
     [0.0, -0.49999999999999983, 0.0, 0.0]]

Here is the mean payoff difference for the :code:`Cooperator` strategy, shows
that it has no difference with all players except against the
:code:`Defector`::

    >>> results.payoff_diffs_means[0]
    [0.0, -5.0, 0.0, 0.0]

Cooperation counts
------------------

This gives a total count of cooperation for each player against each opponent::

    >>> results.cooperation
    [[30, 30, 30, 30], [0, 0, 0, 0], [30, 3, 30, 30], [30, 3, 30, 30]]

Normalised cooperation
----------------------

This gives the average rate of cooperation against each opponent::

    >>> pprint.pprint(results.normalised_cooperation)  # doctest: +SKIP
    [[1.0, 1.0, 1.0, 1.0],
     [0.0, 0.0, 0.0, 0.0],
     [1.0, 0.1, 1.0, 1.0],
     [1.0, 0.1, 1.0, 1.0]]

We see that :code:`Cooperator` for all the rounds (as expected)::

    >>> results.normalised_cooperation[0]
    [1.0, 1.0, 1.0, 1.0]

State distribution counts
-------------------------

This gives a total state count against each opponent. A state corresponds to 1
turn of a match and can be one of :code:`(C, C), (C, D), (D, C),
(D, D)` where the first element is the action of the player in question and
the second the action of the opponent::

    >>> pprint.pprint(results.state_distribution)
    [[Counter(),
      Counter({(C, D): 30}),
      Counter({(C, C): 30}),
      Counter({(C, C): 30})],
     [Counter({(D, C): 30}),
      Counter(),
      Counter({(D, D): 27, (D, C): 3}),
      Counter({(D, D): 27, (D, C): 3})],
     [Counter({(C, C): 30}),
      Counter({(D, D): 27, (C, D): 3}),
      Counter(),
      Counter({(C, C): 30})],
     [Counter({(C, C): 30}),
      Counter({(D, D): 27, (C, D): 3}),
      Counter({(C, C): 30}),
      Counter()]]

Normalised state distribution
-----------------------------

This gives the average rate state distribution against each opponent.
A state corresponds to 1
turn of a match and can be one of :code:`(C, C), (C, D), (D, C),
(D, D)` where the first element is the action of the player in question and
the second the action of the opponent::

    >>> pprint.pprint(results.normalised_state_distribution)
    [[Counter(),
      Counter({(C, D): 1.0}),
      Counter({(C, C): 1.0}),
      Counter({(C, C): 1.0})],
     [Counter({(D, C): 1.0}),
      Counter(),
      Counter({(D, D): 0.9..., (D, C): 0.1...}),
      Counter({(D, D): 0.9..., (D, C): 0.1...})],
     [Counter({(C, C): 1.0}),
      Counter({(D, D): 0.9..., (C, D): 0.1...}),
      Counter(),
      Counter({(C, C): 1.0})],
     [Counter({(C, C): 1.0}),
      Counter({(D, D): 0.9..., (C, D): 0.1...}),
      Counter({(C, C): 1.0}),
      Counter()]]

State to action distribution counts
-----------------------------------

This gives a total state action pair count against each opponent. A state
corresponds to 1 turn of a match and can be one of :code:`(C, C), (C,
D), (D, C), (D, D)` where the first element is the action of the
player in question and the second the action of the opponent::

    >>> pprint.pprint(results.state_to_action_distribution)  # doctest: +SKIP
    [[Counter(),
      Counter({((C, D), C): 27}),
      Counter({((C, C), C): 27}),
      Counter({((C, C), C): 27})],
     [Counter({((D, C), D): 27}),
      Counter(),
      Counter({((D, D), D): 24, ((D, C), D): 3}),
      Counter({((D, D), D): 24, ((D, C), D): 3})],
     [Counter({((C, C), C): 27}),
      Counter({((D, D), D): 24, ((C, D), D): 3}),
      Counter(),
      Counter({((C, C), C): 27})],
     [Counter({((C, C), C): 27}),
      Counter({((D, D), D): 24, ((C, D), D): 3}),
      Counter({((C, C), C): 27}),
      Counter()]]

Normalised state to action distribution
---------------------------------------

This gives the average rate state to action pair distribution against each
opponent.  A state corresponds to 1 turn of a match and can be one of
:code:`(C, C), (C, D), (D, C), (D, D)` where the first element
is the action of the player in question and the second the action of the
opponent::

    >>> pprint.pprint(results.normalised_state_to_action_distribution) # doctest: +SKIP
    [[Counter(),
      Counter({((C, D), C): 1.0}),
      Counter({((C, C), C): 1.0}),
      Counter({((C, C), C): 1.0})],
     [Counter({((D, C), D): 1.0}),
      Counter(),
      Counter({((D, C), D): 1.0, ((D, D), D): 1.0}),
      Counter({((D, C), D): 1.0, ((D, D), D): 1.0})],
     [Counter({((C, C), C): 1.0}),
      Counter({((C, D), D): 1.0, ((D, D), D): 1.0}),
      Counter(),
      Counter({((C, C), C): 1.0})],
     [Counter({((C, C), C): 1.0}),
      Counter({((C, D), D): 1.0, ((D, D), D): 1.0}),
      Counter({((C, C), C): 1.0}),
      Counter()]]

Initial cooperation counts
--------------------------

This gives the count of cooperations made by each player during the first turn
of every match::

    >>> results.initial_cooperation_count
    [9.0, 0.0, 9.0, 9.0]

Each player plays an opponent a total of 9 times (3 opponents and 3
repetitions). Apart from the :code:`Defector`, they all cooperate on the first
turn.

Initial cooperation rates
-------------------------

This gives the rate of which a strategy cooperates during the first turn::

    >>> results.initial_cooperation_rate
    [1.0, 0.0, 1.0, 1.0]

Morality Metrics
----------------

The following morality metrics are available, they are calculated as a function
of the cooperation rating::

    >>> results.cooperating_rating  # doctest: +SKIP
    [1.0, 0.0, 0.7, 0.7]
    >>> pprint.pprint(results.vengeful_cooperation)  # doctest: +SKIP
    [[1.0, 1.0, 1.0, 1.0],
     [-1.0, -1.0, -1.0, -1.0],
     [1.0, -0.8, 1.0, 1.0],
     [1.0, -0.78 1.0, 1.0]]
    >>> pprint.pprint(results.good_partner_matrix)
    [[0, 3, 3, 3], [0, 0, 0, 0], [3, 3, 0, 3], [3, 3, 3, 0]]
    >>> pprint.pprint(results.good_partner_rating)
    [1.0, 0.0, 1.0, 1.0]
    >>> results.eigenmoses_rating
    [0.37..., -0.37..., 0.59..., 0.59...]
    >>> results.eigenjesus_rating
    [0.57..., 0.0, 0.57..., 0.57...]

For more information about these see :ref:`morality-metrics`.
