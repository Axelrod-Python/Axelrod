.. _tournament-results-summary:

Summarising tournament results
==============================


As shown in :ref:`creating_tournaments` let us create a tournament::

    >>> import axelrod as axl
    >>> players = [axl.Cooperator(), axl.Defector(),
    ...            axl.TitForTat(), axl.Grudger()]
    >>> tournament = axl.Tournament(players, turns=10, repetitions=3)
    >>> results = tournament.play()

The results set can return a list of named tuples, ordered by strategy rank
that summarises the results of the tournament::

    >>> summary = results.summarise()
    >>> import pprint
    >>> pprint.pprint(summary)
    [Player(Rank=0, Name='Defector', Median_score=2.6..., Cooperation_rating=0.0, Wins=3.0, Initial_C_rate=0.0, CC_rate=...),
     Player(Rank=1, Name='Tit For Tat', Median_score=2.3..., Cooperation_rating=0..., Wins=0.0, Initial_C_rate=1.0, CC_rate=...),
     Player(Rank=2, Name='Grudger', Median_score=2.3..., Cooperation_rating=0..., Wins=0.0, Initial_C_rate=1.0, CC_rate=...),
     Player(Rank=3, Name='Cooperator', Median_score=2.0..., Cooperation_rating=1.0, Wins=0.0, Initial_C_rate=1.0, CC_rate=...)]

It is also possible to write this data directly to a csv file using the
`write_summary` method::

    >>> results.write_summary('summary.csv')
    >>> import csv
    >>> with open('summary.csv', 'r') as outfile:
    ...     csvreader = csv.reader(outfile)
    ...     for row in csvreader:
    ...         print(row)
    ['Rank', 'Name', 'Median_score', 'Cooperation_rating', 'Wins', 'Initial_C_rate', 'CC_rate', 'CD_rate', 'DC_rate', 'DD_rate', 'CC_to_C_rate', 'CD_to_C_rate', 'DC_to_C_rate', 'DD_to_C_rate']
    ['0', 'Defector', '2.6...', '0.0', '3.0', '0.0', '0.0', '0.0', '0.4...', '0.6...', '0', '0', '0', '0']
    ['1', 'Tit For Tat', '2.3...', '0.7', '0.0', '1.0', '0.66...', '0.03...', '0.0', '0.3...', '1.0', '0', '0', '0']
    ['2', 'Grudger', '2.3...', '0.7', '0.0', '1.0', '0.66...', '0.03...', '0.0', '0.3...', '1.0', '0', '0', '0']
    ['3', 'Cooperator', '2.0...', '1.0', '0.0', '1.0', '0.66...', '0.33...', '0.0', '0.0', '1.0', '1.0', '0', '0']


The result set class computes a large number of detailed outcomes read about
those in :ref:`tournament-results`.
