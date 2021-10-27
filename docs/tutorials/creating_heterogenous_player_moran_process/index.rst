.. _create-heterogeneous-moran-processes:

Create Heterogeneous Moran Processes
====================================

Axelrod Matches are homogeneous by nature but can be extended to utilize
additional attributes of heterogeneous players. This tutorial indicates how the
Axelrod :code:`Match` class can be manipulated in order to play heterogeneous
tournaments and Moran processes using mass as a score modifier similarly to the
work of [Krapohl2020]_.

The following lines of code creates a list of players from the available demo
strategies along with an ascending list of masses we will use for the players.
This is equivalent in principle to the country masses discussed in
[Krapohl2020]_::

    >>> import axelrod as axl
    >>> players = [player() for player in axl.demo_strategies]
    >>> masses = [i for i in range(len(players))]
    >>> players
    [Cooperator, Defector, Tit For Tat, Grudger, Random: 0.5]

Using the :code:`setattr()` function, additional attributes can be passed to
players to enable access during matches and tournaments without manual
modification of individual strategies::

    >>> def set_player_mass(players, masses):
    ...     """Add mass attribute to player strategy classes to be accessable via self.mass"""
    ...     for player, mass in zip(players, masses):
    ...         setattr(player, "mass", mass)
    ...
    >>> set_player_mass(players, masses)

The :code:`Match` class can be partially altered to enable different behaviour
(see :ref:`use-custom-matches`).
Here we extend :code:`axl.Match` and overwrite its
:code:`final_score_per_turn()` function to utilize the player mass attribute as
a multiplier for the final score::

    >>> class MassBaseMatch(axl.Match):
    ...     """Axelrod Match object with a modified final score function to enable mass to influence the final score as a multiplier"""
    ...     def final_score_per_turn(self):
    ...         base_scores = axl.Match.final_score_per_turn(self)
    ...         return [player.mass * score for player, score in zip(self.players, base_scores)] 

In [Krapohl2020]_ a non standard Moran process is used where the mass of
individuals is not reproduced so we will use inheritance to create a new Moran
process that keeps the mass of the individuals constant::

    >>> class MassBasedMoranProcess(axl.MoranProcess):
    ...     """Axelrod MoranProcess class """
    ...     def __next__(self):
    ...         set_player_mass(self.players, masses)
    ...         super().__next__()
    ...         return self

    >>> mp = MassBasedMoranProcess(players, match_class=MassBaseMatch, seed=0)
    >>> populations = mp.play()
    >>> print(mp.winning_strategy_name)
    Random: 0.5

Note that the snippets here only influence the final score of matches. The
behavior of matches, and Moran processes can be more heavily influenced by
partially overwriting other :code:`match` functions or :code:`birth` and
:code:`death` functions within :code:`MoranProcess`.
