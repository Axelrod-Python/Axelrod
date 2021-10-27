.. _use-custom-matches:

Use custom matches
==================

The Moran process supports custom match classes. Below
creates a new class of a match where both players end with a score of 2::


    >>> import axelrod as axl
    >>> class MassBaseMatch(axl.Match):
    ...     """Axelrod Match object with a modified final score function to enable mass to influence the final score as a multiplier"""
    ...     def final_score_per_turn(self):
    ...         return 2, 2

We then create a Moran process with the custom match class by passing our custom
:code:`MassBaseMatch` to the Moran process with the :code:`match_class` keyword
argument::

    >>> players = [axl.Cooperator(), axl.Defector(), axl.TitForTat(), axl.Grudger()]
    >>> mp = axl.MoranProcess(players=players, match_class=MassBaseMatch, seed=0)
    >>> population = mp.play()
    >>> print(mp.winning_strategy_name)
    Defector
