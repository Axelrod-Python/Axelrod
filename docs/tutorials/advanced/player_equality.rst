Player equality
===============

It is possible to test for player equality using :code:`==`::

    >>> import axelrod as axl
    >>> p1, p2, p3 = axl.Alternator(), axl.Alternator(), axl.TitForTat()
    >>> p1 == p2
    True
    >>> p1 == p3
    False

Note that this checks all the attributes of an instance::

    >>> p1.name = "John Nash"
    >>> p1 == p2
    False

This however does not check if the players will behave in the same way. For
example here are two equivalent players::

    >>> p1 = axl.Alternator()
    >>> p2 = axl.Cycler("CD")
    >>> p1 == p2
    False

To check if player strategies are equivalent you can use :ref:`fingerprinting`.
