.. _strategies:

Accessing strategies
====================

All of the strategies are accessible from the main name space of the library.
For example::

    >>> import axelrod
    >>> axelrod.TitForTat()
    Tit For Tat
    >>> axelrod.Cooperator()
    Cooperator

The **main strategies** which obey the rules of Axelrod's original tournament
can be found in a list: `axelrod.strategies`. This makes creating a full
tournament very straightforward:

    >>> players = [s() for s in axelrod.strategies]
    >>> tournament = axelrod.Tournament(players)

There are a list of various other strategies in the library to make it
easier to create a variety of tournaments:

- :code:`axelrod.demo_strategies`: 5 simple strategies useful for demonstration.
- :code:`axelrod.basic_strategies`: A set of basic strategies.
- :code:`axelrod.recursive_strategies`: These have a high computational cost so
  might want to be removed for some analysis.

Furthermore there are some strategies that 'cheat' (for example by modifying
their opponents source code). These can be found in
:code:`axelrod.cheating_strategies`.

All of the strategies in the library are contained in:
:code:`axelrod.all_strategies`.

All strategies are also classified, you can read more about that in
:ref:`classification-of-strategies`.
