Reading and writing interactions to file
========================================

When dealing with large tournaments it might be desirable to separate the
analysis from the actual running of the tournaments. This can be done by passing
a :code:`filename` argument to the :code:`play` method of a tournament::

    >>> import axelrod as axl
    >>> players = [s() for s in axl.basic_strategies]
    >>> tournament = axl.Tournament(players, turns=4, repetitions=2)
    >>> tournament.play(filename="basic_tournament.csv")

This will create a file `basic_tournament.csv` with data that looks something
like::

    1,2,Anti Tit For Tat,Bully,CDCDCDCD,CDCDCDCD
    4,7,Defector,Win-Stay Lose-Shift,DCDDDCDD,DCDDDCDD
    0,0,Alternator,Alternator,CCDDCCDD,CCDDCCDD
    6,6,Tit For Tat,Tit For Tat,CCCCCCCC,CCCCCCCC
    4,5,Defector,Suspicious Tit For Tat,DDDDDDDD,DDDDDDDD
    2,2,Bully,Bully,DDCCDDCC,DDCCDDCC
    2,7,Bully,Win-Stay Lose-Shift,DCDDCCDC,DCDDCCDC
    0,7,Alternator,Win-Stay Lose-Shift,CCDCCDDD,CCDCCDDD
    4,6,Defector,Tit For Tat,DCDDDDDD,DCDDDDDD
    5,6,Suspicious Tit For Tat,Tit For Tat,DCCDDCCD,DCCDDCCD
    2,6,Bully,Tit For Tat,DCDDCDCC,DCDDCDCC
    0,5,Alternator,Suspicious Tit For Tat,CDDCCDDC,CDDCCDDC
    1,4,Anti Tit For Tat,Defector,CDCDCDCD,CDCDCDCD
    3,7,Cooperator,Win-Stay Lose-Shift,CCCCCCCC,CCCCCCCC
    0,4,Alternator,Defector,CDDDCDDD,CDDDCDDD
    2,5,Bully,Suspicious Tit For Tat,DDCDCCDC,DDCDCCDC
    5,7,Suspicious Tit For Tat,Win-Stay Lose-Shift,DCCDDDDC,DCCDDDDC
    0,3,Alternator,Cooperator,CCDCCCDC,CCDCCCDC
    3,5,Cooperator,Suspicious Tit For Tat,CDCCCCCC,CDCCCCCC
    0,1,Alternator,Anti Tit For Tat,CCDDCCDD,CCDDCCDD
    7,7,Win-Stay Lose-Shift,Win-Stay Lose-Shift,CCCCCCCC,CCCCCCCC
    0,2,Alternator,Bully,CDDDCCDD,CDDDCCDD
    3,3,Cooperator,Cooperator,CCCCCCCC,CCCCCCCC
    6,7,Tit For Tat,Win-Stay Lose-Shift,CCCCCCCC,CCCCCCCC
    0,6,Alternator,Tit For Tat,CCDCCDDC,CCDCCDDC
    5,5,Suspicious Tit For Tat,Suspicious Tit For Tat,DDDDDDDD,DDDDDDDD
    4,4,Defector,Defector,DDDDDDDD,DDDDDDDD
    1,6,Anti Tit For Tat,Tit For Tat,CCDCDDCD,CCDCDDCD
    1,1,Anti Tit For Tat,Anti Tit For Tat,CCDDCCDD,CCDDCCDD
    1,5,Anti Tit For Tat,Suspicious Tit For Tat,CDCCDCDD,CDCCDCDD
    3,6,Cooperator,Tit For Tat,CCCCCCCC,CCCCCCCC
    1,7,Anti Tit For Tat,Win-Stay Lose-Shift,CCDCDDCC,CCDCDDCC
    1,3,Anti Tit For Tat,Cooperator,CCDCDCDC,CCDCDCDC
    2,3,Bully,Cooperator,DCDCDCDC,DCDCDCDC
    3,4,Cooperator,Defector,CDCDCDCD,CDCDCDCD
    2,4,Bully,Defector,DDCDCDCD,DDCDCDCD

The columns of this file are of the form:

1. Index of first player
2. Index of second player
3. Name of first player
4. Name of second player
5. All further columns are interactions written in a compressed format.

Alternator versus TitForTat has the following interactions: :code:`CCDCCDDC`:

- First turn: :code:`C` versus :code:`C` (the first two letters)
- Second turn: :code:`D` versus :code:`C` (the second pair of letters)
- Third turn: :code:`C` versus :code:`D` (the third pair of letters)
- Fourth turn: :code:`D` versus :code:`C` (the fourth pair of letters)

This can be transformed in to the usual interactions using the
:code:`interactions_util.string_to_interactions` function:

    >>> string = 'CCDCCDDC'
    >>> axl.interaction_utils.string_to_interactions(string)
    [('C', 'C'), ('D', 'C'), ('C', 'D'), ('D', 'C')]

This should allow for easy manipulation of data outside of the capabilities
within the library, but it is also possible to generate a standard result set
from the datafile::

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
