Overview of strategies
======================

Axelrod's first tournament
--------------------------

Axelrod's first tournament is described in his 1980 paper entitled `'Effective
choice in the Prisoner's Dilemma' <http://www.jstor.org/stable/173932>`_. This
tournament included 14 strategies and they are listed below, (ranked in the
order in which they appeared).

An indication is given as to whether or not this strategy is implemented in the
:code:`axelrod` library. If this strategy is not implemented please do send us a
`pull request <https://github.com/Axelrod-Python/Axelrod/pulls>`_.

Tit for Tat
^^^^^^^^^^^

This strategy was referred to as the *'simplest'* strategy submitted. It
begins by cooperating and then simply repeats the last moves made by the
opponent.

*Tit for Tat came 1st in Axelrod's original tournament.*

Implementation
**************

Here is a quick implementation of this in the library::

   import axelrod
   p1 = axelrod.TitForTat()  # Create a player that plays tit for tat
   p2 = axelrod.Cooperator()  # Create a player that always cooperates
   for round in range(5):
       p1.play(p2)

   print p1.history

which gives::

   ['C', 'C', 'C', 'C', 'C']

We see that Tit for Tat cooperated every time, let us see how things change
when it plays against a player that always defects::

   p1 = axelrod.TitForTat()  # Create a player that plays tit for tat
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
   defections that this strategy retaliates with by 1.
2. The opponent is given a 'fresh start' if:

   * it is 10 points behind this strategy
   * **and** it has not just started a run of defections
   * **and** it has been at least 20 rounds since the last 'fresh start'
   * **and** there are more than 10 rounds remaining in the tournament
   * **and** the total number of defections differs from a 50-50 random sample by at
     least 3.0 standard deviations.

A 'fresh start' is a sequence of two cooperations followed by an assumption that
the game has just started (everything is forgotten).

*This strategy came 2nd in Axelrod's original tournament.*

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

*This strategy came 3rd in Axelrod's original tournament.*

Grofman
^^^^^^^

This is a pretty simple strategy: it cooperates with probability :math:`\frac{2}{7}`. In contemporary terminology, this is a memory-one player 
with all four conditional probabilities of cooperation equal to :math:`\frac{2}{7}`.

*This strategy came 4th in Axelrod's original tournament.*

Here is how this is implemented in the library::

    import axelrod
    p1 = axelrod.Grofman()  # Create a Grofman player
    p2 = axelrod.Random()  # Create a player that plays randomly
    for round in range(5):
        p1.play(p2)

    print p1.history

which gives::

    ['C', 'C', 'D', 'D', 'D']

Over a longer number of rounds::

    from collections import Counter
    for round in range(5):
        p1.play(p2)
    counter = Counter(p1.history)
    print(counter)
    Counter({'D': 367, 'C': 138})
    print float(counter['C']) / (counter['C'] + counter['D'])
    print 2./7

We have that Grofman cooperates roughly in :math:`\frac{2}{7}`-ths of the rounds::

    0.2732673267326733 # Grofman
    0.2857142857142857 # 2./7

Shubik
^^^^^^

This strategy plays a modification of Tit For Tat. It starts by retaliating
with a single defection but the number of defections increases by 1 each time
the opponent defects when this strategy cooperates.

*This strategy came 5th in Axelrod's original tournament.*

    import axelrod
    p1 = axelrod.Shubik()  # Create a Shubik player
    p2 = axelrod.Random()  # Create a player that plays randomly
    for round in range(13):
        p1.play(p2)

    print p1.history
    print p2.history

This yields the following history of play::

    ['C', 'D', 'C', 'D', 'D', 'D', 'C', 'C', 'C', 'D', 'D', 'D', 'C']
    ['D', 'C', 'D', 'C', 'D', 'C', 'C', 'C', 'D', 'C', 'C', 'C', 'D']

The increasing retaliation periods are visible in the output. Note that
 Shubik defects if both players defected in the previous round but does
 not increase the retaliation period.

**Not implemented**: Stein
^^^^^^^^^^^^^^^^^^^^^^^^^^

This strategy plays a modification of Tit For Tat.

1. It cooperates for the first 4 moves.
2. It defects on the last 2 moves.
3. Every 15 moves it makes use of a `chi-squared
   test<http://en.wikipedia.org/wiki/Chi-squared_test>`_ to check if the
   opponent  is playing randomly.

*This strategy came 6th in Axelrod's original tournament.*

Grudger
^^^^^^^

This strategy cooperates until the opponent defects and then defects forever.

*This strategy came 7th in Axelrod's original tournament.*

Implementation
**************

Here is how this is implemented in the library::

   import axelrod
   p1 = axelrod.Grudger()  # Create a player that grudger
   p2 = axelrod.Random()  # Create a player that plays randomly
   for round in range(5):
       p1.play(p2)

   print p1.history
   print p2.history

which gives (for the random seed used)::

    ['C', 'C', 'D', 'D', 'D']
    ['C', 'D', 'C', 'D', 'D']

We see that as soon as :code:`p2` defected :code:`p1` defected for the rest of
the play.

Davis
^^^^^

This strategy is a modification of Grudger. It starts by cooperating for the
first 10 moves and then plays Grudger. It is implemented as follows:

   import axelrod
   p1 = axelrod.Davis()  # Create a Davis player
   p2 = axelrod.Random()  # Create a player that plays randomly
   for round in range(15):
       p1.play(p2)

   print p1.history
   print p2.history

This always produces 10 rounds of attempted cooperation followed by Grudger::

    ['C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'D', 'D', 'D', 'D', 'D']
    ['D', 'C', 'D', 'D', 'C', 'D', 'D', 'C', 'D', 'C', 'D', 'D', 'C', 'C', 'D']


*This strategy came 8th in Axelrod's original tournament.*

**Not implemented**: Graaskamp
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This strategy follows the following rules:

1. Play Tit For Tat for the first 50 rounds;
2. Defects on round 51;
3. Plays 5 further rounds of Tit For Tat;
4. A check is then made to see if the opponent is playing randomly in which case
   it defects for the rest of the game;
5. The strategy also checks to see if the opponent is playing Tit For Tat or
   another strategy from a preliminary tournament called 'Analogy'. If so it
   plays Tit For Tat. If not it cooperates and randomly defects every 5 to 15
   moves.

*This strategy came 9th in Axelrod's original tournament.*

**Not implemented**: Downing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This strategy attempts to estimate the next move of the opponent by estimating
the probability of cooperating given that they defected (:math:`p(C|D)`)or cooperated on the
previous round (:math:`p(C|C)`). These probabilities are continuously updated
during play and the strategy attempts to maximise the long term play.

Note that the initial values are :math:`p(C|C)=p(C|D)=.5`.

*This strategy came 10th in Axelrod's original tournament.*

**Not implemented**: Feld
^^^^^^^^^^^^^^^^^^^^^^^^^

This strategy plays Tit For Tat, always defecting if the opponent defects but
cooperating when the opponent cooperates with a gradually decreasing probability
until it is only .5.

*This strategy came 11th in Axelrod's original tournament.*

Joss
^^^^

This strategy plays Tit For Tat, always defecting if the opponent defects but
cooperating when the opponent cooperates with probability .9.

*This strategy came 12th in Axelrod's original tournament.*

This is a memory-one strategy with four-vector :math:`(0.9, 0, 1, 0)`. Here is how this is implemented in the library::

    import axelrod
    p1 = axelrod.Joss()  # Create a Joss player
    p2 = axelrod.Random()  # Create a player that plays randomly
    for round in range(10):
        p1.play(p2)

    print p1.history
    print p2.history

This gives::

    ['C', 'C', 'C', 'D', 'C', 'D', 'C', 'C', 'C', 'C']
    ['C', 'C', 'D', 'C', 'D', 'C', 'C', 'C', 'C', 'D']

Which is the same as Tit-For-Tat for these 10 rounds.

**Not implemented**: Tullock
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This strategy cooperates for the first 11 rounds and then (randomly) cooperates 10% less
often than the opponent has in the previous 10 rounds.

*This strategy came 13th in Axelrod's original tournament.*

**Not implemented**: 'Grad Student in Political Science'
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This strategy cooperates with a given probability :math:`P`. This probability
(which has initial value .3) is updated every 10 rounds based on whether the
opponent seems to be random, very cooperative or very uncooperative.
Furthermore, if after round 130 the strategy is losing then :math:`P` is also
adjusted.

*This strategy came 14th in Axelrod's original tournament.*

Random
^^^^^^

This strategy plays randomly (disregarding the history of play).

*This strategy came 15th in Axelrod's original tournament.*

Implementation
**************

Here is how this is implemented in the library::

   import axelrod
   p1 = axelrod.Random()  # Create a player that plays randomly
   p2 = axelrod.Random()  # Create a player that plays randomly
   for round in range(5):
       p1.play(p2)

   print p1.history
   print p2.history

which gives (for the random seed used)::

    ['D', 'D', 'C', 'C', 'C']
    ['D', 'C', 'D', 'D', 'C']

Axelrod's second tournament
---------------------------

Work in progress.

Strategies implemented in the module
------------------------------------

Work in progress.
