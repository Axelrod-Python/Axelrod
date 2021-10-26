.. _use-custom-matches:

Use custom matches
==================

At present it is possible to use a custom match class in a Moran process. Below
creates a new class of a match where both players end with a score of 2::


    >>> import axelrod as axl
    >>> class MassBaseMatch(axl.Match):
    ...     """Axelrod Match object with a modified final score function to enable mass to influence the final score as a multiplier"""
    ...     def final_score_per_turn(self):
    ...         return 2, 2

We can now create a Moran process like we normally would and pass our custom
:code:`MassBaseMatch` to the moran process with the :code:`match_class` keyword
argument::

    >>> players = [axl.Cooperator(), axl.Defector(), axl.TitForTat(), axl.Grudger()]
    >>> mp = axl.MoranProcess(players=players, match_class=MassBaseMatch, seed=0)
    >>> population = mp.play()
    >>> print(mp.winning_strategy_name)
    Defector
