.. _strategies:

Accessing strategies
====================

All of the strategies are accessible from the main name space of the library.
For example::

    >>> import axelrod as axl
    >>> axl.TitForTat()
    Tit For Tat
    >>> axl.Cooperator()
    Cooperator

The **main strategies** which obey the rules of Axelrod's original tournament
can be found in a list: `axelrod.strategies`::

    >>> axl.strategies
    [...

This makes creating a full
tournament very straightforward::

    >>> players = [s() for s in axl.strategies]
    >>> tournament = axl.Tournament(players)

There are a list of various other strategies in the library to make it
easier to create a variety of tournaments::

    >>> axl.demo_strategies  # 5 simple strategies useful for demonstration.
    [...
    >>> axl.basic_strategies  # A set of basic strategies.
    [...
    >>> axl.long_run_time_strategies  # These have a high computational cost
    [...

Furthermore there are some strategies that 'cheat' (for example by modifying
their opponents source code). These can be found in
:code:`axelrod.cheating_strategies`::

    >>> axl.cheating_strategies
    [...

All of the strategies in the library are contained in:
:code:`axelrod.all_strategies`::

    >>> axl.all_strategies
    [...

All strategies are also classified, you can read more about that in
:ref:`classification-of-strategies`.
