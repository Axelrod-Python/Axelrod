.. Axelrod documentation master file, created by
   sphinx-quickstart on Sat Mar  7 07:05:57 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the documentation for the Axelrod Python library
===========================================================

Here is quick overview of the current capabilities of the library:

* Over 100 strategies from the literature and some exciting original
  contributions

    * Classic strategies like TiT-For-Tat, WSLS, and variants
    * Zero-Determinant and other Memory-One strategies
    * Many generic strategies that can be used to define an array of popular
      strategies, including finite state machines, strategies that hunt for
      patterns in other strategies, and strategies that combine the effects of
      many others
    * Strategy transformers that augment the abilities of any strategy

* Head-to-Head matches

* Round Robin tournaments with a variety of options, including:

    * noisy environments
    * spatial tournaments
    * probabilistically chosen match lengths

* Population dynamics

    * The Moran process
    * An ecological model

* Multi-processor support (not currently supported on Windows), caching for
  deterministic interactions, automatically generate figures and statistics

Every strategy is categorized on a number of dimensions, including:

    * Deterministic or Stochastic
    * How many rounds of history used
    * Whether the strategy makes use of the game matrix, the length of the
      match, etc.

Furthermore the library is extensively tested with 99%+ coverage, ensuring
validity and reproducibility of results!


Quick start
-----------

Create matches between two players::

    >>> import axelrod as axl
    >>> players = (axl.Alternator(), axl.TitForTat())
    >>> match = axl.Match(players, 5)
    >>> interactions = match.play()
    >>> interactions
    [('C', 'C'), ('D', 'C'), ('C', 'D'), ('D', 'C'), ('C', 'D')]

Build full tournaments between groups of players::

    >>> import axelrod as axl
    >>> players = (axl.Cooperator(), axl.Alternator(), axl.TitForTat())
    >>> tournament = axl.Tournament(players)
    >>> results = tournament.play()
    >>> results.ranked_names
    ['Alternator', 'Tit For Tat', 'Cooperator']

Study the evolutionary process using a Moran process::

    >>> import axelrod as axl
    >>> players = (axl.Cooperator(), axl.Alternator(), axl.TitForTat())
    >>> mp = axl.MoranProcess(players)
    >>> populations = mp.play()
    >>> populations  # doctest: +SKIP
    [Counter({'Alternator': 1, 'Cooperator': 1, 'Tit For Tat': 1}),
     Counter({'Alternator': 1, 'Cooperator': 1, 'Tit For Tat': 1}),
     Counter({'Cooperator': 1, 'Tit For Tat': 2}),
     Counter({'Cooperator': 1, 'Tit For Tat': 2}),
     Counter({'Tit For Tat': 3})]

As well as this, the library has a growing collection of strategies. The
:ref:`strategies-index` gives a description of them.

For further details there is a library of :ref:`tutorials` available and a
:ref:`community` page with information about how to get support and/or make
contributions.

Table of Contents
-----------------

.. toctree::
   :maxdepth: 3

   tutorials/index.rst
   reference/index.rst
   community/index.rst
   citing_the_library.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

