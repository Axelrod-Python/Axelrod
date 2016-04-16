.. Axelrod documentation master file, created by
   sphinx-quickstart on Sat Mar  7 07:05:57 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the documentation for the Axelrod Python library
===========================================================

Here is quick overview of what can be done with the library.


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

For further details there is a library of tutorials available:

Tutorials
---------

.. toctree::
   :maxdepth: 3

   tutorials/index.rst
   reference/index.rst
   citing_the_library.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

