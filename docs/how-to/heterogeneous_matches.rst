.. _heterogeneous-matches:

Heterogeneous Matches
=====================

Axelrod Matches are homogeneous by nature but can be extended to utilize additional attributes of heterogeneous players. 
This tutorial indicates how the Axelrod :code:`Match` class can be manipulated in order to play heterogeneous tournaments and Moran processes using country mass as a score modifier.

The following lines of code creates a list of players from the available demo strategies along with an ascending list of values we will use for the players::

    >>> import axelrod as axl
    >>> players = [player() for player in axl.demo_strategies]
    >>> masses = [1 * i for i in range(len(players))]
    >>> players
    [Cooperator, Defector, Tit For Tat, Grudger, Random: 0.5]

Using the :code:`setattr()` method, additional attributes can be passed to players to enable access during matches and tournaments without manual modification of individual strategies::

    >>> def set_player_mass(players, masses):
    >>> """Add mass attribute to player strategy classes to be accessable via self.mass"""
    >>>     for player, mass in zip(players, masses):
    >>>         setattr(player, "mass", mass)
    >>>
    >>> set_player_mass(players, masses)

The :code:`Match` class can be partially altered to enable different behaviour. Here we extend :code:`axl.Match` and overwrite its :code:`final_score_per_turn()`
function to utilize the player mass attribute als a multiplier for the final score::

    >>> class MassBaseMatch(axl.Match):
    >>> """Axelrod Match object with a modified final score function to enable mass to influence the final score as a multiplier"""
    >>> def final_score_per_turn(self):
    >>>     base_scores = axl.Match.final_score_per_turn(self)
    >>>     return [player.mass * score for player, score in zip(self.players, base_scores)] 

We can now create a tournament like we normally would and pass our custom :code:`MassBaseMatch` to the tournament with the :code:`match_class` keyword argument::

    >>> tournament = axl.Tournament(players=players, match_class=MassBaseMatch)
    >>> results = tournament.play()
    >>> print(results.ranked_names)
    ['Defector', 'Grudger', 'Tit For Tat', 'Cooperator', 'Random: 0.5']

Additionally, Moran Processes can also be altered to incorporate heterogeneous matches. In order to 
use our previously defined :code:`MassBaseMatch`, we require one additional change to the :code:`MoranProcess` class::

    >>> class MassBasedMoranProcess(axl.MoranProcess):
    >>> """Axelrod MoranProcess class """
    >>> def __next__(self):
    >>>     set_player_mass(self.players, masses)
    >>>     super().__next__()
    >>>     return self

With this code snippet we can override the :code:`__next__()` call within the MoranProcess to include :code:`set_player_mass()` 
every round. This ensures that every player has mass attributes after the Moran process is triggered. 
Subsequently, with :code:`super().__next__()` the base MoranProcess :code:`__next__()` call is triggered. This method enables quick 
modifications to tournaments and moran processes with minimal repetitive code.

We can now create a Moran process as we normally would, with the inclusion of the match class as a keyword argument::

    >>> mp = MassBasedMoranProcess(players, match_class=MassBaseMatch)
    >>> mp.play()
    >>> print(mp.winning_strategy_name)
    Grudger

Note that the snippets here only influence the final score of matches. The behavior of matches, tournaments and moran 
processes can be more heavily influenced by partially overwriting other :code:`match` functions or :code:`birth` and :code:`death` functions within :code:`MoranProcess`.
