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
    >>> class StochasticMatchups(axl.RoundRobinMatches):
    ...     """Inherit from the `axelrod.match_generator.RoundRobinMatches` class"""
    ...
    ...     def build_matches(self, noise=0):
    ...         """
    ...         A generator that yields matches only with a given probability.
    ...
    ...         This over writes the
    ...         `axelrod.match_generator.RoundRobinMatches.build_matches` method.
    ...         """
    ...         for player1_index in range(len(self.players)):
    ...             for player2_index in range(player1_index, len(self.players)):
    ...                 if random.random() < 0.5:  # This is the modification
    ...                     pair = (
    ...                         self.players[player1_index], self.opponents[player2_index])
    ...                     match = self.build_single_match(pair, noise)
    ...                     yield (player1_index, player2_index), match

Using this class we can create a tournament with little effort::

    >>> players = [axl.Cooperator(), axl.Defector(), axl.TitForTat(),
    ...            axl.Grudger(), axl.Alternator()]
    >>> tournament = axl.Tournament(players, match_generator=StochasticMatchups, turns=5, repetitions=2)
    >>> results = tournament.play()

We can then look at the interactions (results may differ based on random seed)
for the first repetition::

    >>> for index_pair, interaction in tournament.interactions[0].items():
    ...     player1 = tournament.players[index_pair[0]]
    ...     player2 = tournament.players[index_pair[1]]
    ...     print('%s vs %s: %s' % (player1, player2, interaction))  # doctest: +SKIP
    Defector vs Tit For Tat: [('D', 'C'), ('D', 'D'), ('D', 'D'), ('D', 'D'), ('D', 'D')]
    Defector vs Grudger: [('D', 'C'), ('D', 'D'), ('D', 'D'), ('D', 'D'), ('D', 'D')]
    Grudger vs Grudger: [('C', 'C'), ('C', 'C'), ('C', 'C'), ('C', 'C'), ('C', 'C')]
    Alternator vs Alternator: [('C', 'C'), ('D', 'D'), ('C', 'C'), ('D', 'D'), ('C', 'C')]

and the second repetition::

    >>> for index_pair, interaction in tournament.interactions[1].items():
    ...     player1 = tournament.players[index_pair[0]]
    ...     player2 = tournament.players[index_pair[1]]
    ...     print('%s vs %s: %s' % (player1, player2, interaction))  # doctest: +SKIP
    Cooperator vs Defector: [('C', 'D'), ('C', 'D'), ('C', 'D'), ('C', 'D'), ('C', 'D')]
    Tit For Tat vs Grudger: [('C', 'C'), ('C', 'C'), ('C', 'C'), ('C', 'C'), ('C', 'C')]
    Grudger vs Grudger: [('C', 'C'), ('C', 'C'), ('C', 'C'), ('C', 'C'), ('C', 'C')]
    Tit For Tat vs Tit For Tat: [('C', 'C'), ('C', 'C'), ('C', 'C'), ('C', 'C'), ('C', 'C')]
    Cooperator vs Alternator: [('C', 'C'), ('C', 'D'), ('C', 'C'), ('C', 'D'), ('C', 'C')]
    Grudger vs Alternator: [('C', 'C'), ('C', 'D'), ('D', 'C'), ('D', 'D'), ('D', 'C')]
    Tit For Tat vs Alternator: [('C', 'C'), ('C', 'D'), ('D', 'C'), ('C', 'D'), ('D', 'C')]

We see that not all possible matches were played. The results can be viewed as
before::

    >>> results.ranked_names  # doctest: +SKIP
    ['Defector', 'Alternator', 'Grudger', 'Tit For Tat', 'Cooperator']

Note: the :code:`axelrod.MatchGenerator` also has a :code:`build_single_match`
method which can be overwritten (similarly to above) if the type of a particular
match should be changed.

For example the following could be used to create a tournament that randomly
builds matches that were either 200 turns or single 1 shot games::

    >>> import axelrod as axl
    >>> import random
    >>> class OneShotOrRepetitionMatchups(axl.RoundRobinMatches):
    ...     """Inherit from the `axelrod.match_generator.RoundRobinMatches` class"""
    ...
    ...
    ...     def build_single_match(self, pair, noise=0):
    ...         """Create a single match for a given pair"""
    ...         if random.random() < 0.5:
    ...             return Match(
    ...                 pair, 200, self.game, self.deterministic_cache, noise)
    ...         return Match(
    ...             pair, 1, self.game, self.deterministic_cache, noise)
