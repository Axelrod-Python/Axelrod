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
    ...               axl.TitForTat(), axl.Grudger()]
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


Moran Process on Graphs
-----------------------

The library also provides a graph-based Moran process [Shakarian2013]_ with
:code:`MoranProcessGraph`.  To use this class you must supply at least one
:code:`Axelrod.graph.Graph` object, which can be initialized with just a list of
edges::

    edges = [(source_1, target1), (source2, target2), ...]

The nodes can be any hashable object (integers, strings, etc.). For example::

    >>> from axelrod.graph import Graph
    >>> edges = [(0, 1), (1, 2), (2, 3), (3, 1)]
    >>> graph = Graph(edges)

Graphs are undirected by default. Various intermediates such as the list of
neighbors are cached for efficiency by the graph object.

A Moran process can be invoked with one or two graphs. The first graph, the
*interaction graph*, dictates how players are matched up in the scoring phase.
Each player plays a match with each neighbor. The second graph dictates how
players replace another during reproduction. When an individual is selected to
reproduce, it replaces one of its neighbors in the *reproduction graph*. If only
one graph is supplied to the process, the two graphs are assumed to be the same.

To create a graph-based Moran process, use a graph as follows::

    >>> from axelrod.graph import Graph
    >>> axl.seed(40)
    >>> edges = [(0, 1), (1, 2), (2, 3), (3, 1)]
    >>> graph = Graph(edges)
    >>> players = [axl.Cooperator(), axl.Cooperator(), axl.Cooperator(), axl.Defector()]
    >>> mp = axl.MoranProcessGraph(players, interaction_graph=graph)
    >>> results = mp.play()
    >>> mp.population_distribution()
    Counter({'Cooperator': 4})

You can supply the :code:`reproduction_graph` as a keyword argument. The
standard Moran process is equivalent to using a complete graph for both graphs.


Approximate Moran Process
-------------------------

Due to the high computational cost of a single Moran process, an approximate
Moran process is implemented that can make use of cached outcomes of games. The
following code snippet will generate a Moran process in which a `Defector`
cooperates (gets a high score) against another `Defector`. First the cache is
built by passing counter objects of outcomes::

    >>> from collections import Counter
    >>> cached_outcomes = {}
    >>> cached_outcomes[("Cooperator", "Defector")] = axl.Pdf(Counter([(0, 5)]))
    >>> cached_outcomes[("Cooperator", "Cooperator")] = axl.Pdf(Counter([(3, 3)]))
    >>> cached_outcomes[("Defector", "Defector")] = axl.Pdf(Counter([(10, 10), (9, 9)]))

Now let us create an Approximate Moran Process::

    >>> axl.seed(0)
    >>> players = [axl.Cooperator(), axl.Defector(), axl.Defector(), axl.Defector()]
    >>> amp = axl.ApproximateMoranProcess(players, cached_outcomes)
    >>> results = amp.play()
    >>> amp.population_distribution()
    Counter({'Defector': 4})
