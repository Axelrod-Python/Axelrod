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
  scores recorded
- a player is chosen to reproduce proportional to the player's score in the
  round
- a player is chosen at random to be replaced

The process proceeds in rounds until the population consists of a single player
type. That type is declared the winner. To run an instance of the process with
the library, proceed as follows::

    >>> import axelrod as axl
    >>> axl.seed(0)
    >>> players = [axl.Cooperator(), axl.Defector(),
    ...            axl.TitForTat(), axl.Grudger()]
    >>> mp = axl.MoranProcess(players)
    >>> populations = mp.play()
    >>> mp.winning_strategy_name
    'Grudger'

You can access some attributes of the process, such as the number of rounds::

    >>> len(mp)
    14

The sequence of populations::

    >>> import pprint
    >>> pprint.pprint(populations)  # doctest: +SKIP
    [Counter({'Grudger': 1, 'Cooperator': 1, 'Defector': 1, 'Tit For Tat': 1}),
     Counter({'Grudger': 1, 'Cooperator': 1, 'Defector': 1, 'Tit For Tat': 1}),
     Counter({'Grudger': 1, 'Cooperator': 1, 'Defector': 1, 'Tit For Tat': 1}),
     Counter({'Tit For Tat': 2, 'Grudger': 1, 'Cooperator': 1}),
     Counter({'Grudger': 2, 'Cooperator': 1, 'Tit For Tat': 1}),
     Counter({'Grudger': 3, 'Cooperator': 1}),
     Counter({'Grudger': 3, 'Cooperator': 1}),
     Counter({'Grudger': 3, 'Cooperator': 1}),
     Counter({'Grudger': 3, 'Cooperator': 1}),
     Counter({'Grudger': 3, 'Cooperator': 1}),
     Counter({'Grudger': 3, 'Cooperator': 1}),
     Counter({'Grudger': 3, 'Cooperator': 1}),
     Counter({'Grudger': 3, 'Cooperator': 1}),
     Counter({'Grudger': 4})]


The scores in each round::

    >>> for row in mp.score_history:
    ...     print([round(element, 1) for element in row])
    [6.0, 7.1, 7.0, 7.0]
    [6.0, 7.1, 7.0, 7.0]
    [6.0, 7.1, 7.0, 7.0]
    [9.0, 9.0, 9.0, 9.0]
    [9.0, 9.0, 9.0, 9.0]
    [9.0, 9.0, 9.0, 9.0]
    [9.0, 9.0, 9.0, 9.0]
    [9.0, 9.0, 9.0, 9.0]
    [9.0, 9.0, 9.0, 9.0]
    [9.0, 9.0, 9.0, 9.0]
    [9.0, 9.0, 9.0, 9.0]
    [9.0, 9.0, 9.0, 9.0]
    [9.0, 9.0, 9.0, 9.0]


The :code:`MoranProcess` class also accepts an argument for a mutation rate.
Nonzero mutation changes the Markov process so that it no longer has absorbing
states, and will iterate forever. To prevent this, iterate with a loop (or
function like :code:`takewhile` from :code:`itertools`)::

    >>> import axelrod as axl
    >>> axl.seed(4) # for reproducible example
    >>> players = [axl.Cooperator(), axl.Defector(),
    ...               axl.TitForTat(), axl.Grudger()]
    >>> mp = axl.MoranProcess(players, mutation_rate=0.1)
    >>> for _ in mp:
    ...     if len(mp.population_distribution()) == 1:
    ...         break
    >>> mp.population_distribution()
    Counter({'Cooperator': 4})

Other types of implemented Moran processes:

- :ref:`moran-process-on-graphs`
- :ref:`approximate-moran-process`
