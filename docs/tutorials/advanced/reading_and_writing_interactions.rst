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

    Interaction index,Player index,Opponent index,Repetition,Player name,Opponent name,Actions,Score,Score difference,Turns,Score per turn,Score difference per turn,Win,Initial cooperation,Cooperation count,CC count,CD count,DC count,DD count,CC to C count,CC to D count,CD to C count,CD to D count,DC to C count,DC to D count,DD to C count,DD to D count,Good partner
    0,0,0,0,Alternator,Alternator,CDCD,8,0,4,2.0,0.0,0,True,2,2,0,0,2,0,2,0,0,0,0,1,0,1
    0,0,0,0,Alternator,Alternator,CDCD,8,0,4,2.0,0.0,0,True,2,2,0,0,2,0,2,0,0,0,0,1,0,1
    1,0,0,1,Alternator,Alternator,CDCD,8,0,4,2.0,0.0,0,True,2,2,0,0,2,0,2,0,0,0,0,1,0,1
    1,0,0,1,Alternator,Alternator,CDCD,8,0,4,2.0,0.0,0,True,2,2,0,0,2,0,2,0,0,0,0,1,0,1
    2,0,1,0,Alternator,Anti Tit For Tat,CDCD,8,0,4,2.0,0.0,0,True,2,2,0,0,2,0,2,0,0,0,0,1,0,1
    2,1,0,0,Anti Tit For Tat,Alternator,CDCD,8,0,4,2.0,0.0,0,True,2,2,0,0,2,0,2,0,0,0,0,1,0,1
    3,0,1,1,Alternator,Anti Tit For Tat,CDCD,8,0,4,2.0,0.0,0,True,2,2,0,0,2,0,2,0,0,0,0,1,0,1
    3,1,0,1,Anti Tit For Tat,Alternator,CDCD,8,0,4,2.0,0.0,0,True,2,2,0,0,2,0,2,0,0,0,0,1,0,1
    4,0,2,0,Alternator,Bully,CDCD,5,-5,4,1.25,-1.25,0,True,2,1,1,0,2,0,1,0,1,0,0,1,0,1
    4,2,0,0,Bully,Alternator,DDCD,10,5,4,2.5,1.25,1,False,1,1,0,1,2,0,1,0,0,0,1,1,0,0
    5,0,2,1,Alternator,Bully,CDCD,5,-5,4,1.25,-1.25,0,True,2,1,1,0,2,0,1,0,1,0,0,1,0,1
    5,2,0,1,Bully,Alternator,DDCD,10,5,4,2.5,1.25,1,False,1,1,0,1,2,0,1,0,0,0,1,1,0,0
    6,0,3,0,Alternator,Cooperator,CDCD,16,10,4,4.0,2.5,1,True,2,2,0,2,0,0,2,0,0,1,0,0,0,0
    6,3,0,0,Cooperator,Alternator,CCCC,6,-10,4,1.5,-2.5,0,True,4,2,2,0,0,2,0,1,0,0,0,0,0,1
    7,0,3,1,Alternator,Cooperator,CDCD,16,10,4,4.0,2.5,1,True,2,2,0,2,0,0,2,0,0,1,0,0,0,0
    7,3,0,1,Cooperator,Alternator,CCCC,6,-10,4,1.5,-2.5,0,True,4,2,2,0,0,2,0,1,0,0,0,0,0,1
    8,0,4,0,Alternator,Cycler DC,CDCD,10,0,4,2.5,0.0,0,True,2,0,2,2,0,0,0,0,2,1,0,0,0,1
    8,4,0,0,Cycler DC,Alternator,DCDC,10,0,4,2.5,0.0,0,False,2,0,2,2,0,0,0,0,1,2,0,0,0,1
    9,0,4,1,Alternator,Cycler DC,CDCD,10,0,4,2.5,0.0,0,True,2,0,2,2,0,0,0,0,2,1,0,0,0,1
    9,4,0,1,Cycler DC,Alternator,DCDC,10,0,4,2.5,0.0,0,False,2,0,2,2,0,0,0,0,1,2,0,0,0,1
    10,0,5,0,Alternator,Defector,CDCD,2,-10,4,0.5,-2.5,0,True,2,0,2,0,2,0,0,0,2,0,0,1,0,1
    10,5,0,0,Defector,Alternator,DDDD,12,10,4,3.0,2.5,1,False,0,0,0,2,2,0,0,0,0,0,2,0,1,0
    11,0,5,1,Alternator,Defector,CDCD,2,-10,4,0.5,-2.5,0,True,2,0,2,0,2,0,0,0,2,0,0,1,0,1
    11,5,0,1,Defector,Alternator,DDDD,12,10,4,3.0,2.5,1,False,0,0,0,2,2,0,0,0,0,0,2,0,1,0
    12,0,6,0,Alternator,Grudger,CDCD,9,0,4,2.25,0.0,0,True,2,1,1,1,1,0,1,0,1,1,0,0,0,1
    12,6,0,0,Grudger,Alternator,CCDD,9,0,4,2.25,0.0,0,True,2,1,1,1,1,1,0,0,1,0,1,0,0,1
    13,0,6,1,Alternator,Grudger,CDCD,9,0,4,2.25,0.0,0,True,2,1,1,1,1,0,1,0,1,1,0,0,0,1
    13,6,0,1,Grudger,Alternator,CCDD,9,0,4,2.25,0.0,0,True,2,1,1,1,1,1,0,0,1,0,1,0,0,1
    14,0,7,0,Alternator,Suspicious Tit For Tat,CDCD,10,0,4,2.5,0.0,0,True,2,0,2,2,0,0,0,0,2,1,0,0,0,1
    14,7,0,0,Suspicious Tit For Tat,Alternator,DCDC,10,0,4,2.5,0.0,0,False,2,0,2,2,0,0,0,0,1,2,0,0,0,1
    15,0,7,1,Alternator,Suspicious Tit For Tat,CDCD,10,0,4,2.5,0.0,0,True,2,0,2,2,0,0,0,0,2,1,0,0,0,1
    15,7,0,1,Suspicious Tit For Tat,Alternator,DCDC,10,0,4,2.5,0.0,0,False,2,0,2,2,0,0,0,0,1,2,0,0,0,1
    16,0,8,0,Alternator,Tit For Tat,CDCD,13,5,4,3.25,1.25,1,True,2,1,1,2,0,0,1,0,1,1,0,0,0,0
    16,8,0,0,Tit For Tat,Alternator,CCDC,8,-5,4,2.0,-1.25,0,True,3,1,2,1,0,1,0,0,1,1,0,0,0,1
    17,0,8,1,Alternator,Tit For Tat,CDCD,13,5,4,3.25,1.25,1,True,2,1,1,2,0,0,1,0,1,1,0,0,0,0
    17,8,0,1,Tit For Tat,Alternator,CCDC,8,-5,4,2.0,-1.25,0,True,3,1,2,1,0,1,0,0,1,1,0,0,0,1
    18,0,9,0,Alternator,Win-Shift Lose-Stay: D,CDCD,9,0,4,2.25,0.0,0,True,2,1,1,1,1,0,1,0,1,1,0,0,0,1
    18,9,0,0,Win-Shift Lose-Stay: D,Alternator,DCCD,9,0,4,2.25,0.0,0,False,2,1,1,1,1,0,1,1,0,1,0,0,0,1
    19,0,9,1,Alternator,Win-Shift Lose-Stay: D,CDCD,9,0,4,2.25,0.0,0,True,2,1,1,1,1,0,1,0,1,1,0,0,0,1
    19,9,0,1,Win-Shift Lose-Stay: D,Alternator,DCCD,9,0,4,2.25,0.0,0,False,2,1,1,1,1,0,1,1,0,1,0,0,0,1
    20,0,10,0,Alternator,Win-Stay Lose-Shift: C,CDCD,9,0,4,2.25,0.0,0,True,2,1,1,1,1,0,1,0,1,1,0,0,0,1
    20,10,0,0,Win-Stay Lose-Shift: C,Alternator,CCDD,9,0,4,2.25,0.0,0,True,2,1,1,1,1,1,0,0,1,0,1,0,0,1
    21,0,10,1,Alternator,Win-Stay Lose-Shift: C,CDCD,9,0,4,2.25,0.0,0,True,2,1,1,1,1,0,1,0,1,1,0,0,0,1
    21,10,0,1,Win-Stay Lose-Shift: C,Alternator,CCDD,9,0,4,2.25,0.0,0,True,2,1,1,1,1,1,0,0,1,0,1,0,0,1
    22,1,1,0,Anti Tit For Tat,Anti Tit For Tat,CDCD,8,0,4,2.0,0.0,0,True,2,2,0,0,2,0,2,0,0,0,0,1,0,1
    22,1,1,0,Anti Tit For Tat,Anti Tit For Tat,CDCD,8,0,4,2.0,0.0,0,True,2,2,0,0,2,0,2,0,0,0,0,1,0,1
    23,1,1,1,Anti Tit For Tat,Anti Tit For Tat,CDCD,8,0,4,2.0,0.0,0,True,2,2,0,0,2,0,2,0,0,0,0,1,0,1
    23,1,1,1,Anti Tit For Tat,Anti Tit For Tat,CDCD,8,0,4,2.0,0.0,0,True,2,2,0,0,2,0,2,0,0,0,0,1,0,1
    24,1,2,0,Anti Tit For Tat,Bully,CCCC,0,-20,4,0.0,-5.0,0,True,4,0,4,0,0,0,0,3,0,0,0,0,0,1
    24,2,1,0,Bully,Anti Tit For Tat,DDDD,20,20,4,5.0,5.0,1,False,0,0,0,4,0,0,0,0,0,0,3,0,0,0
    25,1,2,1,Anti Tit For Tat,Bully,CCCC,0,-20,4,0.0,-5.0,0,True,4,0,4,0,0,0,0,3,0,0,0,0,0,1
    25,2,1,1,Bully,Anti Tit For Tat,DDDD,20,20,4,5.0,5.0,1,False,0,0,0,4,0,0,0,0,0,0,3,0,0,0
    26,1,3,0,Anti Tit For Tat,Cooperator,CDDD,18,15,4,4.5,3.75,1,True,1,1,0,3,0,0,1,0,0,0,2,0,0,0
    26,3,1,0,Cooperator,Anti Tit For Tat,CCCC,3,-15,4,0.75,-3.75,0,True,4,1,3,0,0,1,0,2,0,0,0,0,0,1
    27,1,3,1,Anti Tit For Tat,Cooperator,CDDD,18,15,4,4.5,3.75,1,True,1,1,0,3,0,0,1,0,0,0,2,0,0,0
    27,3,1,1,Cooperator,Anti Tit For Tat,CCCC,3,-15,4,0.75,-3.75,0,True,4,1,3,0,0,1,0,2,0,0,0,0,0,1
    28,1,4,0,Anti Tit For Tat,Cycler DC,CCDC,7,-5,4,1.75,-1.25,0,True,3,2,1,0,1,0,1,1,0,0,0,1,0,1
    28,4,1,0,Cycler DC,Anti Tit For Tat,DCDC,12,5,4,3.0,1.25,1,False,2,2,0,1,1,0,1,0,0,1,0,1,0,0
    29,1,4,1,Anti Tit For Tat,Cycler DC,CCDC,7,-5,4,1.75,-1.25,0,True,3,2,1,0,1,0,1,1,0,0,0,1,0,1
    29,4,1,1,Cycler DC,Anti Tit For Tat,DCDC,12,5,4,3.0,1.25,1,False,2,2,0,1,1,0,1,0,0,1,0,1,0,0
    30,1,5,0,Anti Tit For Tat,Defector,CCCC,0,-20,4,0.0,-5.0,0,True,4,0,4,0,0,0,0,3,0,0,0,0,0,1
    30,5,1,0,Defector,Anti Tit For Tat,DDDD,20,20,4,5.0,5.0,1,False,0,0,0,4,0,0,0,0,0,0,3,0,0,0
    31,1,5,1,Anti Tit For Tat,Defector,CCCC,0,-20,4,0.0,-5.0,0,True,4,0,4,0,0,0,0,3,0,0,0,0,0,1
    31,5,1,1,Defector,Anti Tit For Tat,DDDD,20,20,4,5.0,5.0,1,False,0,0,0,4,0,0,0,0,0,0,3,0,0,0
    32,1,6,0,Anti Tit For Tat,Grudger,CDDC,9,0,4,2.25,0.0,0,True,2,1,1,1,1,0,1,0,0,0,1,1,0,1
    32,6,1,0,Grudger,Anti Tit For Tat,CCDD,9,0,4,2.25,0.0,0,True,2,1,1,1,1,1,0,0,1,0,0,0,1,1
    33,1,6,1,Anti Tit For Tat,Grudger,CDDC,9,0,4,2.25,0.0,0,True,2,1,1,1,1,0,1,0,0,0,1,1,0,1
    33,6,1,1,Grudger,Anti Tit For Tat,CCDD,9,0,4,2.25,0.0,0,True,2,1,1,1,1,1,0,0,1,0,0,0,1,1
    34,1,7,0,Anti Tit For Tat,Suspicious Tit For Tat,CCDD,9,0,4,2.25,0.0,0,True,2,1,1,1,1,0,1,1,0,0,1,0,0,1
    34,7,1,0,Suspicious Tit For Tat,Anti Tit For Tat,DCCD,9,0,4,2.25,0.0,0,False,2,1,1,1,1,1,0,0,1,1,0,0,0,1
    35,1,7,1,Anti Tit For Tat,Suspicious Tit For Tat,CCDD,9,0,4,2.25,0.0,0,True,2,1,1,1,1,0,1,1,0,0,1,0,0,1
    35,7,1,1,Suspicious Tit For Tat,Anti Tit For Tat,DCCD,9,0,4,2.25,0.0,0,False,2,1,1,1,1,1,0,0,1,1,0,0,0,1
    ...

Note that depending on the order in which the matches have been played, the rows
could also be in a different order.

It is possible to read in this data file to obtain interactions::

    >>> interactions = axl.interaction_utils.read_interactions_from_file("basic_tournament.csv")

This gives a dictionary mapping pairs of player indices to interaction
histories::

    >>> interactions[(0, 1)]
    [[(C, C), (D, D), (C, C), (D, D)], [(C, C), (D, D), (C, C), (D, D)]]

This should allow for easy manipulation of data outside of the capabilities
within the library.

Note that you can supply `build_results=False` as a keyword
argument to `tournament.play()` to prevent keeping or loading interactions in
memory, since the total memory footprint can be large for various combinations
of parameters. The memory usage scales as :math:`O(\text{players}^2 \times \text{turns} \times \text{repetitions})`.
