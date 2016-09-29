.. _human-interaction:

Human Interaction
=================

It is possible to play interactively using the Human strategy::

    >>> import axelrod as axl
    >>> me = axl.Human(name='me')
    >>> players = [axl.TitForTat(), me]
    >>> match = axl.Match(players, turns=3)
    >>> match.play() #doctest: +SKIP

You will be prompted for the action to play at each turn:

.. code-block:: bash

    Starting new match
    Turn 1 action [C or D] for me: C

    Turn 1: me played C, opponent played C
    Turn 2 action [C or D] for me: D

    Turn 2: me played D, opponent played C
    Turn 3 action [C or D] for me: C
    [('C', 'C'), ('C', 'D'), ('D', 'C')]

after this, the :code:`match` object can be manipulated as described in
:ref:`creating_matches`
