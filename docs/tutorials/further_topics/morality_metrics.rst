.. _morality-metrics:

Morality Metrics
================

Tyler Singer-Clark's June 2014 paper, "Morality Metrics On Iterated Prisoner’s
Dilemma Players" [Tyler-Clark2014]), describes several interesting metrics which
may be used to analyse IPD tournaments all of which are available within the
ResultSet class. (Tyler's paper is available here:
http://www.scottaaronson.com/morality.pdf).

Each metric depends upon the cooperation rate of the players, defined by Tyler
Singer-Clark as:

.. math::

    CR(b) = \frac{C(b)}{TT}

where C(b) is the total number of turns where a player chose to cooperate and TT
is the total number of turns played.

A matrix of cooperation rates is available within a tournament's ResultSet::

    >>> import axelrod as axl
    >>> players = [axl.Cooperator(), axl.Defector(),
    ...            axl.TitForTat(), axl.Grudger()]
    >>> tournament = axl.Tournament(players)
    >>> results = tournament.play()
    >>> [[round(float(ele), 3) for ele in row] for row in results.normalised_cooperation]
    [[1.0, 1.0, 1.0, 1.0], [0.0, 0.0, 0.0, 0.0], [1.0, 0.005, 1.0, 1.0], [1.0, 0.005, 1.0, 1.0]]

There is also a 'good partner' matrix showing how often a player cooperated at
least as much as its opponent::

    >>> results.good_partner_matrix
    [[0, 10, 10, 10], [0, 0, 0, 0], [10, 10, 0, 10], [10, 10, 10, 0]]

Each of the metrics described in Tyler's paper is available as follows (here they are rounded to 2 digits)::

    >>> [round(ele, 2) for ele in results.cooperating_rating]
    [1.0, 0.0, 0.67, 0.67]
    >>> [round(ele, 2) for ele in results.good_partner_rating]
    [1.0, 0.0, 1.0, 1.0]
    >>> [round(ele, 2) for ele in results.eigenjesus_rating]
    [0.58, 0.0, 0.58, 0.58]
    >>> [round(ele, 2) for ele in results.eigenmoses_rating]
    [0.37, -0.37, 0.6, 0.6]
