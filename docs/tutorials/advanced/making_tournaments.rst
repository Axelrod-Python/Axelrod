.. _making_tournaments:

Build new types of tournaments
==============================

It is possible to create new tournaments not yet implemented in the library
itself. There are two tools that make up a tournament:

- The :code:`MatchGenerator` class: this class is responsible for generating the
  required matches.
- The :code:`Tournament` class: this class is responsible for playing the
  matches generated.

Let us aim to create a round robin tournament of matches with 5 turns each with
the modification that two players only play each other with .5 probability.

To do this let us create a new class to generate matches::

    >>> import axelrod as axl
    >>> import random
    >>> axl.seed(0)  # Setting a seed.
    >>> class StochasticMatchups(axl.RoundRobinMatches):
    ...     """Inherit from the `axelrod.match_generator.RoundRobinMatches` class"""
    ...
    ...     def build_match_chunks(self):
    ...         """
    ...         A generator that yields match parameters only with a given probability.
    ...
    ...         This over writes the
    ...         `axelrod.match_generator.RoundRobinMatches.build_match_chunks` method.
    ...         """
    ...         for player1_index in range(len(self.players)):
    ...             for player2_index in range(player1_index, len(self.players)):
    ...                 if random.random() < 0.5:  # This is the modification
    ...                     match_params = self.build_single_match_params()
    ...                     index_pair = (player1_index, player2_index)
    ...                     yield (index_pair, match_params, self.repetitions)

Using this class we can create a tournament with little effort::

    >>> players = [axl.Cooperator(), axl.Defector(), axl.TitForTat(),
    ...            axl.Grudger(), axl.Alternator()]
    >>> tournament = axl.Tournament(players, match_generator=StochasticMatchups, turns=2, repetitions=2)
    >>> results = tournament.play(keep_interactions=True)

We can then look at the interactions (results may differ based on random seed)
for the first repetition::

    >>> for index_pair, interaction in results.interactions.items():
    ...     player1 = tournament.players[index_pair[0]]
    ...     player2 = tournament.players[index_pair[1]]
    ...     print('%s vs %s: %s' % (player1, player2, interaction))  # doctest: +SKIP
    Cooperator vs Defector: [[('C', 'D'), ('C', 'D')], [('C', 'D'), ('C', 'D')]]
    Alternator vs Alternator: [[('C', 'C'), ('D', 'D')], [('C', 'C'), ('D', 'D')]]
    Tit For Tat vs Grudger: [[('C', 'C'), ('C', 'C')], [('C', 'C'), ('C', 'C')]]
    Grudger vs Grudger: [[('C', 'C'), ('C', 'C')], [('C', 'C'), ('C', 'C')]]
    Tit For Tat vs Tit For Tat: [[('C', 'C'), ('C', 'C')], [('C', 'C'), ('C', 'C')]]
    Cooperator vs Alternator: [[('C', 'C'), ('C', 'D')], [('C', 'C'), ('C', 'D')]]
    Defector vs Defector: [[('D', 'D'), ('D', 'D')], [('D', 'D'), ('D', 'D')]]

We see that not all possible matches were played (for example `Cooperator` has
not played `TitForTat`). The results can be viewed as before::

    >>> results.ranked_names
    ['Cooperator', 'Defector', 'Tit For Tat', 'Grudger', 'Alternator']

Note: the :code:`axelrod.MatchGenerator` also has a :code:`build_single_match`
method which can be overwritten (similarly to above) if the type of a particular
match should be changed.

For example the following could be used to create a tournament that randomly
builds matches that were either 200 turns or single 1 shot games::

    >>> class OneShotOrRepetitionMatchups(axl.RoundRobinMatches):
    ...     """Inherit from the `axelrod.match_generator.RoundRobinMatches` class"""
    ...
    ...
    ...     def build_single_match_params(self):
    ...         """Create a single set of match parameters"""
    ...         turns = 1
    ...         if random.random() < 0.5:
    ...             turns = 200
    ...         return (turns, self.game, None, self.noise)

We can take a look at the match lengths when using this generator::

    >>> players = [axl.Cooperator(), axl.Defector(), axl.TitForTat(),
    ...            axl.Grudger(), axl.Alternator()]
    >>> tournament = axl.Tournament(players, match_generator=OneShotOrRepetitionMatchups,
    ...                             turns=float("inf"), repetitions=1)
    >>> results = tournament.play(keep_interactions=True)
    >>> sorted(list(set([len(matches[0]) for matches in results.interactions.values()])))
    [1, 200]
