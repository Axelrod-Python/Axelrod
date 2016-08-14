Reading and writing interactions from/to file
=============================================

When dealing with large tournaments it might be desirable to separate the
analysis from the actual running of the tournaments. This can be done by passing
a :code:`filename` argument to the :code:`play` method of a tournament::

    >>> import axelrod as axl
    >>> players = [s() for s in axl.basic_strategies]
    >>> tournament = axl.Tournament(players, turns=4, repetitions=2)
    >>> results = tournament.play(filename="basic_tournament.csv")

This will create a file `basic_tournament.csv` with data that looks something
like::

    0,0,Alternator,Alternator,CDCD,CDCD
    0,0,Alternator,Alternator,CDCD,CDCD
    0,1,Alternator,Anti Tit For Tat,CDCD,CDCD
    0,1,Alternator,Anti Tit For Tat,CDCD,CDCD
    0,2,Alternator,Bully,CDCD,DDCD
    0,2,Alternator,Bully,CDCD,DDCD
    0,3,Alternator,Cooperator,CDCD,CCCC
    0,3,Alternator,Cooperator,CDCD,CCCC
    0,4,Alternator,Defector,CDCD,DDDD
    0,4,Alternator,Defector,CDCD,DDDD
    0,5,Alternator,Suspicious Tit For Tat,CDCD,DCDC
    0,5,Alternator,Suspicious Tit For Tat,CDCD,DCDC
    0,6,Alternator,Tit For Tat,CDCD,CCDC
    0,6,Alternator,Tit For Tat,CDCD,CCDC
    0,7,Alternator,Win-Stay Lose-Shift,CDCD,CCDD
    0,7,Alternator,Win-Stay Lose-Shift,CDCD,CCDD
    1,1,Anti Tit For Tat,Anti Tit For Tat,CDCD,CDCD
    1,1,Anti Tit For Tat,Anti Tit For Tat,CDCD,CDCD
    1,2,Anti Tit For Tat,Bully,CCCC,DDDD
    1,2,Anti Tit For Tat,Bully,CCCC,DDDD
    1,3,Anti Tit For Tat,Cooperator,CDDD,CCCC
    1,3,Anti Tit For Tat,Cooperator,CDDD,CCCC
    1,4,Anti Tit For Tat,Defector,CCCC,DDDD
    1,4,Anti Tit For Tat,Defector,CCCC,DDDD
    1,5,Anti Tit For Tat,Suspicious Tit For Tat,CCDD,DCCD
    1,5,Anti Tit For Tat,Suspicious Tit For Tat,CCDD,DCCD
    1,6,Anti Tit For Tat,Tit For Tat,CDDC,CCDD
    1,6,Anti Tit For Tat,Tit For Tat,CDDC,CCDD
    1,7,Anti Tit For Tat,Win-Stay Lose-Shift,CDDC,CCDC
    1,7,Anti Tit For Tat,Win-Stay Lose-Shift,CDDC,CCDC
    2,2,Bully,Bully,DCDC,DCDC
    2,2,Bully,Bully,DCDC,DCDC
    2,3,Bully,Cooperator,DDDD,CCCC
    2,3,Bully,Cooperator,DDDD,CCCC
    2,4,Bully,Defector,DCCC,DDDD
    2,4,Bully,Defector,DCCC,DDDD
    2,5,Bully,Suspicious Tit For Tat,DCCD,DDCC
    2,5,Bully,Suspicious Tit For Tat,DCCD,DDCC
    2,6,Bully,Tit For Tat,DDCC,CDDC
    2,6,Bully,Tit For Tat,DDCC,CDDC
    2,7,Bully,Win-Stay Lose-Shift,DDCD,CDCC
    2,7,Bully,Win-Stay Lose-Shift,DDCD,CDCC
    3,3,Cooperator,Cooperator,CCCC,CCCC
    3,3,Cooperator,Cooperator,CCCC,CCCC
    3,4,Cooperator,Defector,CCCC,DDDD
    3,4,Cooperator,Defector,CCCC,DDDD
    3,5,Cooperator,Suspicious Tit For Tat,CCCC,DCCC
    3,5,Cooperator,Suspicious Tit For Tat,CCCC,DCCC
    3,6,Cooperator,Tit For Tat,CCCC,CCCC
    3,6,Cooperator,Tit For Tat,CCCC,CCCC
    3,7,Cooperator,Win-Stay Lose-Shift,CCCC,CCCC
    3,7,Cooperator,Win-Stay Lose-Shift,CCCC,CCCC
    4,4,Defector,Defector,DDDD,DDDD
    4,4,Defector,Defector,DDDD,DDDD
    4,5,Defector,Suspicious Tit For Tat,DDDD,DDDD
    4,5,Defector,Suspicious Tit For Tat,DDDD,DDDD
    4,6,Defector,Tit For Tat,DDDD,CDDD
    4,6,Defector,Tit For Tat,DDDD,CDDD
    4,7,Defector,Win-Stay Lose-Shift,DDDD,CDCD
    4,7,Defector,Win-Stay Lose-Shift,DDDD,CDCD
    5,5,Suspicious Tit For Tat,Suspicious Tit For Tat,DDDD,DDDD
    5,5,Suspicious Tit For Tat,Suspicious Tit For Tat,DDDD,DDDD
    5,6,Suspicious Tit For Tat,Tit For Tat,DCDC,CDCD
    5,6,Suspicious Tit For Tat,Tit For Tat,DCDC,CDCD
    5,7,Suspicious Tit For Tat,Win-Stay Lose-Shift,DCDD,CDDC
    5,7,Suspicious Tit For Tat,Win-Stay Lose-Shift,DCDD,CDDC
    6,6,Tit For Tat,Tit For Tat,CCCC,CCCC
    6,6,Tit For Tat,Tit For Tat,CCCC,CCCC
    6,7,Tit For Tat,Win-Stay Lose-Shift,CCCC,CCCC
    6,7,Tit For Tat,Win-Stay Lose-Shift,CCCC,CCCC
    7,7,Win-Stay Lose-Shift,Win-Stay Lose-Shift,CCCC,CCCC
    7,7,Win-Stay Lose-Shift,Win-Stay Lose-Shift,CCCC,CCCC

The columns of this file are of the form:

1. Index of first player
2. Index of second player
3. Name of first player
4. Name of second player
5. History of play of the first player
6. History of play of the second player

Note that depending on the order in which the matches have been played, the rows
could also be in a different order.

:code:`Alternator` versus :code:`TitForTat` has the following interactions:
:code:`CCDC, CDCD`:

- First turn: :code:`C` versus :code:`C` (the first two letters)
- Second turn: :code:`D` versus :code:`C` (the second pair of letters)
- Third turn: :code:`C` versus :code:`D` (the third pair of letters)
- Fourth turn: :code:`D` versus :code:`C` (the fourth pair of letters)

This can be transformed in to the usual interactions by zipping:

    >>> list(zip("CCDC", "CDCD"))
    [('C', 'C'), ('C', 'D'), ('D', 'C'), ('C', 'D')]

This should allow for easy manipulation of data outside of the capabilities
within the library. Note that you can supply `build_results=False` as a keyword
argument to `tournament.play()` to prevent keeping or loading interactions in
memory, since the total memory footprint can be large for various combinations
of parameters. The memory usage scales as :math:`O(\text{players}^2 * \text{turns} * \text{repetitions})`.

It is also possible to generate a standard result set from a datafile::

    >>> results = axl.ResultSetFromFile(filename="basic_tournament.csv")
    >>> results.ranked_names  # doctest: +SKIP
    ['Defector',
     'Bully',
     'Suspicious Tit For Tat',
     'Alternator',
     'Tit For Tat',
     'Anti Tit For Tat',
     'Win-Stay Lose-Shift',
     'Cooperator']
