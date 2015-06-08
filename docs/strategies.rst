Overview of strategies
======================

Axelrod's first tournament
--------------------------

Axelrod's first tournament is described in his 1980 paper entitled `'Effective
choice in the Prisoner's Dilemma' <http://www.jstor.org/stable/173932>`_. This
tournament included 14 strategies and they are listed below, (ranked in the
order in which they appeared). _An indication is given as to whether or not
this strategy is implemented in the :code:`axelrod` library.

Tit for Tat
^^^^^^^^^^^

This strategy was referred to as the *'simplest'* strategy submitted. It
begins by cooperating and then simply repeats the last move made by the
opponent.

*Tit for Tat came fist in Axelrod's original tournament.*

Implementation
**************

Here is a quick implementation of this in the library::

   import axelrod
   p1 = axelrod.TitForTat()  # Create a player that players tit for tat
   p2 = axelrod.Cooperator()  # Create a player that always cooperates
   for round in range(5):
       p1.play(p2)
   print p1.history

which gives::

   ['C', 'C', 'C', 'C', 'C']

We see that Tit for Tat cooperated every time, let us see how things change
when it plays against a player that always defects::

   p1 = axelrod.TitForTat()  # Create a player that players tit for tat
   p3 = axelrod.Defector()  # Create a player that always cooperates
   for round in range(5):
       p1.play(p3)
   print p1.history

which gives::

   ['C', 'D', 'D', 'D', 'D']

We see that after cooperating once, Tit For Tat defects at every step.

**Not implemented**: Tideman and Chieruzzi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This strategy begins by playing Tit For Tat and then things get slightly
complicated:

1. Every run of defections played by the opponent increases the number of
   defections that this strategy retaliates with.
2. The opponent is given a 'fresh start' if:

   * it is 10 points behind this strategy
   * **and** it has not just started a run of defections
   * **and** it has been at least 20 rounds since the last 'fresh start'
   * **and** there are more than 10 rounds remaining in the tournament
   * **and** the total number of defections differs from a 50-50 random sample by at
     least 3.0 standard deviations.

A 'fresh start' is a sequence of two cooperations followed by an assumption that
the game has just started.

*This strategy came second in Axelrod's original tournament.*

**Not implemented**: Nydegger
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This strategy begins by playing Tit For Tat for the first 3 rounds with the
following modifications:

**If it is the only strategy to cooperate in the first round and the only
strategy to defect on the second round then it defects on the 3 round
(despite the fact that Tit For Tat would now cooperate).**

After these first 3 rounds the next move is made depending on the previous 3
rounds. A score is given to these rounds according to the following
calculation:

.. math::

    A = 16 a_1 + 4 a_2 + a_3

Where :math:`a_i` is dependent on the outcome of the previous :math:`i` th
round.  If both strategies defect, :math:`a_i=3`, if the opponent only defects:
:math:`a_i=2` and finally if it is only this strategy that defects then
:math:`a_i=1`.

Finally this strategy defects if and only if:

.. math::

    A \in \{1, 6, 7, 17, 22, 23, 26, 29, 30, 31, 33, 38, 39, 45, 49, 54, 55, 58, 61\}

*This strategy came third in Axelrod's original tournament.*

**Not implemented**: Grofman
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is a pretty simple strategy, it cooperates with probability :math:`\frac{2}{7}`.

*This strategy came fourth in Axelrod's original tournament.*

**Not implemented**: Shubik
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This strategy plays a modification of Tit For Tat. It starts be retaliating
with a single defection but the number of defections increases by 1 each time
the opponent defects when this strategy cooperates.

*This strategy came fifth in Axelrod's original tournament.*

Axelrod's second tournament
---------------------------

Strategies implemented in the module
------------------------------------
