.. _moran-process:

Moran Process
=============

The strategies in the library can be pitted against one another in the
`Moran process <https://en.wikipedia.org/wiki/Moran_process>`_, a population
process simulating natural selection.

The process works as follows. Given an
initial population of players, the population is iterated in rounds consisting
of:

- matches played between each pair of players, with the cumulative total
  scores recored
- a player is chosen to reproduce proportional to the player's score in the
  round
- a player is chosen at random to be replaced

The process proceeds in rounds until the population consists of a single player
type. That type is declared the winner. To run an instance of the process with
the library, proceed as follows::

    >>> import axelrod as axl
    >>> players = [axl.Cooperator(), axl.Defector(),
    ...               axl.TitForTat(), axl.Grudger()]
    >>> mp = axl.MoranProcess(players)
    >>> populations = mp.play()
    >>> mp.winning_strategy_name   # doctest: +SKIP
    Defector

You can access some attributes of the process, such as the number of rounds::

    >>> len(mp)  # doctest: +SKIP
    6

The sequence of populations::

    >>> import pprint
    >>> pprint.pprint(populations)  # doctest: +SKIP
    [Counter({'Defector': 1, 'Cooperator': 1, 'Grudger': 1, 'Tit For Tat': 1}),
    Counter({'Defector': 1, 'Cooperator': 1, 'Grudger': 1, 'Tit For Tat': 1}),
    Counter({'Defector': 2, 'Cooperator': 1, 'Grudger': 1}),
    Counter({'Defector': 3, 'Grudger': 1}),
    Counter({'Defector': 3, 'Grudger': 1}),
    Counter({'Defector': 4})]

The scores in each round::

    >>> for row in mp.score_history: # doctest: +SKIP
    ...     print([round(element, 1) for element in row])
    [[6.0, 7.0800000000000001, 6.9900000000000002, 6.9900000000000002],
    [6.0, 7.0800000000000001, 6.9900000000000002, 6.9900000000000002],
    [3.0, 7.04, 7.04, 4.9800000000000004],
    [3.04, 3.04, 3.04, 2.9699999999999998],
    [3.04, 3.04, 3.04, 2.9699999999999998]]
