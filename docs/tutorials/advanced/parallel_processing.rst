Parallel processing
===================

When dealing with large tournaments on a multi core machine it is possible to
run the tournament in parallel **although this is not currently supported on
Windows**. Using :code:`processes=0` will simply use all available cores::

    >>> import axelrod as axl
    >>> players = [s() for s in axl.basic_strategies]
    >>> tournament = axl.Tournament(players, turns=4, repetitions=2)
    >>> results = tournament.play(processes=0)
