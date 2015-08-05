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

The following strategies are included in the library:

+----------------+--------------------------+--------------------------+
| Name           | Long name                | Axelrod Library Name     |
+================+==========================+==========================+
| `Tit For Tat`_ | Always Cooperate         | :code:`Cooperator`       |
+----------------+--------------------------+--------------------------+
| `Grofman`_     | Grofman (name of author) | :code:`Grofman`          |
+----------------+--------------------------+--------------------------+
| `Shubik`_      | Shubik (name of author)  | :code:`Shubik`           |
+----------------+--------------------------+--------------------------+
| `Grudger`_     | Grudger (name of author) | :code:`Grudger`          |
+----------------+--------------------------+--------------------------+
| `Davis`_       | Davis (name of author)   | :code:`Davis`            |
+----------------+--------------------------+--------------------------+
| `Joss`_        | Feld (name of author)    | :code:`Feld`             |
+----------------+--------------------------+--------------------------+
| `Tullock`_     | Tullock (name of author) | :code:`Tullock`          |
+----------------+--------------------------+--------------------------+

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
   p3 = axelrod.Defector()  # Create a player that always defects
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

Implementation
**************

Here is how Grofman is implemented in the library::

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

Implementation
**************

Here is how Shubik is implemented in the library::

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
   opponent is playing randomly.

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
first 10 moves and then plays Grudger.

*This strategy came 8th in Axelrod's original tournament.*

Implementation
**************

Davis is implemented as follows::

    import axelrod
    p1 = axelrod.Davis()  # Create a Davis player
    p2 = axelrod.Random()  # Create a player that plays randomly
    for round in range(15):
       p1.play(p2)

    print p1.history
    print p2.history

This always produces (at least) 10 rounds of attempted cooperation followed by
Grudger::

    ['C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'D', 'D', 'D', 'D', 'D']
    ['D', 'C', 'D', 'D', 'C', 'D', 'D', 'C', 'D', 'C', 'D', 'D', 'C', 'C', 'D']

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
the probability of cooperating given that they defected (:math:`p(C|D)`) or
cooperated on the previous round (:math:`p(C|C)`). These probabilities are
continuously updated during play and the strategy attempts to maximise the long
term play.

Note that the initial values are :math:`p(C|C)=p(C|D)=.5`.

*This strategy came 10th in Axelrod's original tournament.*

Feld
^^^^

This strategy plays Tit For Tat, always defecting if the opponent defects but
cooperating when the opponent cooperates with a gradually decreasing probability
until it is only .5.

*This strategy came 11th in Axelrod's original tournament.*

Implementation
**************

Feld is implemented in the library as follows::

    import axelrod
    p1 = axelrod.Feld()  # Create a Feld player
    p2 = axelrod.Random()  # Create a player that plays randomly
    for round in range(10):
        p1.play(p2)

    print p1.history
    print p2.history

We can see from the output that Feld defects when its opponent does::

    ['C', 'D', 'C', 'D', 'D', 'D', 'D', 'C', 'D', 'D']
    ['D', 'C', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'D']

The defection times lengthen each time the opponent defects when Feld
cooperates.

Joss
^^^^

This strategy plays Tit For Tat, always defecting if the opponent defects but
cooperating when the opponent cooperates with probability .9.

*This strategy came 12th in Axelrod's original tournament.*

Implementation
**************

This is a memory-one strategy with four-vector :math:`(0.9, 0, 1, 0)`. Here is
how Joss is implemented in the library::

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

Tullock
^^^^^^^

This strategy cooperates for the first 11 rounds and then (randomly) cooperates
10% less often than the opponent has in the previous 10 rounds.

*This strategy came 13th in Axelrod's original tournament.*

Implementation
**************

Tullock is implemented in the library as follows::

    import axelrod
    p1 = axelrod.Tullock()  # Create a Tullock player
    p2 = axelrod.Random()  # Create a player that plays randomly
    for round in range(15):
        p1.play(p2)

    print p1.history
    print p2.history

This gives::

    ['C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'D', 'D', 'C', 'D']
    ['D', 'C', 'C', 'D', 'D', 'C', 'C', 'D', 'D', 'D', 'C', 'D', 'C', 'D', 'C']

We have 10 rounds of cooperation and some apparently random plays afterward.

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

EATHERLEY
^^^^^^^^^

This strategy was submitted by Graham Eatherley to Axelrod's second tournament
and generally cooperates unless the opponent defects, in which case Eatherley
defects with a probability equal to the proportion of rounds that the opponent
has defected.

*This strategy came  in Axelrod's second tournament.*

Implementation
**************

Here is how Eatherley is implemented in the library::

    import axelrod
    p1 = axelrod.Eatherley()  # Create a Eatherley player
    p2 = axelrod.Random()  # Create a player that plays randomly
    for round in range(5):
        p1.play(p2)

    print p1.history
    print p2.history

which gives (for a particular random seed)::

    ['C', 'C', 'C', 'D', 'C']
    ['C', 'D', 'D', 'C', 'C']


CHAMPION
^^^^^^^^

This strategy was submitted by Danny Champion to Axelrod's second tournament and
operates in three phases. The first phase lasts for the first 1/20-th of the
rounds and Champion always cooperates. In the second phase, lasting until
4/50-th of the rounds have passed, Champion mirrors its opponent's last move. In
the last phase, Champion cooperates unless
- the opponent defected on the last round, and
- the opponent has cooperated less than 60% of the rounds, and
- a random number is greater than the proportion of rounds defected

Implementation
**************

Here is how Champion is implemented in the library::

    import axelrod
    p1 = axelrod.Champion()  # Create a Champion player
    p2 = axelrod.Random()  # Create a player that plays randomly
    for round in range(5):
        p1.play(p2)

    print p1.history
    print p2.history

which gives (for a particular random seed)::

    ['C', 'C', 'C', 'C', 'C']
    ['D', 'C', 'D', 'D', 'C']


TESTER
^^^^^^

This strategy is a TFT variant that attempts to exploit certain strategies. It
defects on the first move. If the opponent ever defects, TESTER 'apologies' by
cooperating and then plays TFT for the rest of the game. Otherwise TESTER
alternates cooperation and defection.

*This strategy came 46th in Axelrod's second tournament.*

Implementation
**************

Here is how this is implemented in the library::

    import axelrod
    p1 = axelrod.Tester()  # Create a Tester player
    p2 = axelrod.Random()  # Create a player that plays randomly
    for round in range(5):
        p1.play(p2)

    print p1.history
    print p2.history

which gives (for a particular random seed)::

    ['D', 'C', 'C', 'D', 'D']
    ['C', 'D', 'D', 'D', 'C']



Stewart and Plotkin's Tournament (2012)
---------------------------------------

In 2012, `Alexander Stewart and Joshua Plotkin
<http://www.pnas.org/content/109/26/10134.full.pdf>`_ ran a variant of
Axelrod's tournament with 19 strategies to test the effectiveness of the then
newly discovered Zero-Determinant strategies.

The paper is identified as *doi: 10.1073/pnas.1208087109* and referred to as
[S&P, PNAS 2012] below. Unfortunately the details of the tournament and the
implementation of  strategies is not clear in the manuscript. We can, however,
make reasonable guesses to the implementation of many strategies based on their
names and classical definitions.

The following classical strategies are included in the library:

+--------------+----------------------+--------------------------+
| S&P Name     | Long name            | Axelrod Library Name     |
+==============+======================+==========================+
| ALLC         | Always Cooperate     | :code:`Cooperator`       |
+--------------+----------------------+--------------------------+
| ALLD         | Always Defect        | :code:`Defector`         |
+--------------+----------------------+--------------------------+
| `EXTORT-2`_  | Extort-2             | :code:`ZDExtort2`        |
+--------------+----------------------+--------------------------+
| `HARD_MAJO`_ | Hard majority        | :code:`GoByMajority`     |
+--------------+----------------------+--------------------------+
| `HARD_JOSS`_ | Hard Joss            | :code:`Joss`             |
+--------------+----------------------+--------------------------+
| `HARD_TFT`_  | Hard tit for tat     | :code:`HardTitForTat`    |
+--------------+----------------------+--------------------------+
| `HARD_TF2T`_ | Hard tit for 2 tats  | :code:`HardTitFor2Tats`  |
+--------------+----------------------+--------------------------+
| TFT          | Tit-For-Tat          | :code:`TitForTat`        |
+--------------+----------------------+--------------------------+
| `GRIM`_      | Grim                 | :code:`Grudger`          |
+--------------+----------------------+--------------------------+
| `GTFT`_      | Generous Tit-For-Tat | :code:`GenerousTitForTat`|
+--------------+----------------------+--------------------------+
| `TF2T`_      | Tit-For-Two-Tats     | :code:`TitFor2Tats`      |
+--------------+----------------------+--------------------------+
| `WSLS`_      | Win-Stay-Lose-Shift  | :code:`WinStayLoseShift` |
+--------------+----------------------+--------------------------+
| RANDOM       | Random               | :code:`Random`           |
+--------------+----------------------+--------------------------+
| `ZDGTFT-2`_  | ZDGTFT-2             | :code:`ZDGTFT2`          |
+--------------+----------------------+--------------------------+

ALLC, ALLD, TFT and RANDOM are defined above. The remaining classical
strategies are defined below. The tournament also included two Zero Determinant
strategies, both implemented in the library. The full table of strategies and
results is `available
online <http://www.pnas.org/content/109/26/10134/F1.expansion.html)>`_.

Memory one strategies
^^^^^^^^^^^^^^^^^^^^^

In 2012 `Press and Dyson <http://www.pnas.org/content/109/26/10409.full.pdf>`_
showed interesting results with regards to so called memory one strategies.
Stewart and Poltkin implemented a number of these. A memory one strategy is
simply a probabilistic strategy that is defined by 4 parameters.  These four
parameters dictate the probability of cooperating given 1 of 4 possible
outcomes of the previous round:

- :math:`P(C\,|\,CC) = p_1`
- :math:`P(C\,|\,CD) = p_2`
- :math:`P(C\,|\,DC) = p_3`
- :math:`P(C\,|\,DD) = p_4`

The memory one strategy class is used to define a number of strategies below.

GTFT
^^^^

Generous-Tit-For-Tat plays Tit-For-Tat with occasional forgiveness, which
prevents cycling defections against itself.

GTFT is defined as a memory-one strategy as follows:

- :math:`P(C\,|\,CC) = 1`
- :math:`P(C\,|\,CD) = p`
- :math:`P(C\,|\,DC) = 1`
- :math:`P(C\,|\,DD) = p`

where :math:`p = \min\left(1 - \frac{T-R}{R-S}, \frac{R-P}{T-P}\right)`.

*GTFT came 2nd in average score and 18th in wins in S&P's tournament.*

Implementation
**************

Here is a quick implementation of this in the library::

   import axelrod
   p1 = axelrod.GTFT()  # Create a player that plays GTFT
   p2 = axelrod.Defector()  # Create a player that always defects
   for round in range(10):
       p1.play(p2)

   print p1.history

this gives (for the random seed used)::

    ['C', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'D', 'D']

which shows that :code:`GTFT` tried to forgive :code:`Defector`.

TF2T
^^^^

Tit-For-Two-Tats is like Tit-For-Tat but only retaliates after two defections
rather than one. This is not a memory-one strategy.

*TF2T came 3rd in average score and last (?) in wins in S&P's tournament.*

Implementation
**************

Here is the implementation of this in the library::

   import axelrod
   p1 = axelrod.TitFor2Tats()  # Create a player that plays TF2T
   p2 = axelrod.Defector()  # Create a player that always defects
   for round in range(3):
       p1.play(p2)

   print p1.history

which gives::

    ['C', 'C', 'D']

we see that it takes 2 defections to trigger a defection by :code:`TitFor2Tats`.

WSLS
^^^^

Win-Stay-Lose-Shift is a strategy that shifts if the highest payoff was not
earned in the previous round. WSLS is also known as "Win-Stay-Lose-Switch" and
"Pavlov". It can be seen as a memory-one strategy as follows:

- :math:`P(C\,|\,CC) = 1`
- :math:`P(C\,|\,CD) = 0`
- :math:`P(C\,|\,DC) = 0`
- :math:`P(C\,|\,DD) = 1`

*TF2T came 7th in average score and 13th in wins in S&P's tournament.*

Implementation
**************

Here is a quick implementation of this in the library::

   import axelrod
   p1 = axelrod.WinStayLoseShift()  # Create a player that plays WSLS
   p2 = axelrod.Alternator()  # Create a player that alternates
   for round in range(5):
       p1.play(p2)

   print p1.history

this gives::

    ['C', 'C', 'D', 'D', 'C']

which shows that :code:`WSLS` will choose the strategy that was a best response
in the previous round.

RANDOM
^^^^^^

Random is a strategy that was defined in `Axelrod's first tournament`_, note that this is also a memory-one strategy:

- :math:`P(C\,|\,CC) = 0.5`
- :math:`P(C\,|\,CD) = 0.5`
- :math:`P(C\,|\,DC) = 0.5`
- :math:`P(C\,|\,DD) = 0.5`

*RANDOM came 8th in average score and 8th in wins in S&P's tournament.*

ZDGTFT-2
^^^^^^^

This memory-one strategy is defined by the following four conditional
probabilities based on the last round of play:

- :math:`P(C\,|\,CC) = 1`
- :math:`P(C\,|\,CD) = 1/8`
- :math:`P(C\,|\,DC) = 1`
- :math:`P(C\,|\,DD) = 1/4`

*This strategy came 1st in average score and 16th in wins in S&P's tournament.*

Implementation
**************

Here is how ZDGTFT-2 is implemented in the library::

    import axelrod
    p1 = axelrod.ZDGTFT2()  # Create a ZDGTFT-2 player
    p2 = axelrod.Random()  # Create a player that plays randomly
    for round in range(5):
        p1.play(p2)

    print p2.history
    print p1.history

which gives (for the particular random seed used)::

    ['D', 'D', 'D', 'C', 'C', 'D', 'C', 'D', 'D', 'D']
    ['C', 'C', 'D', 'D', 'C', 'C', 'D', 'C', 'D', 'D']

looking closely (and repeating the above) will show that the above
probabilities are respected.

EXTORT-2
^^^^^^^^

This memory-one strategy is defined by the following four conditional
probabilities based on the last round of play:

- :math:`P(C\,|\,CC) = 8/9`
- :math:`P(C\,|\,CD) = 1/2`
- :math:`P(C\,|\,DC) = 1/3`
- :math:`P(C\,|\,DD) = 0`

*This strategy came 18th in average score and 2nd in wins in S&P's tournament.*

Implementation
**************

Here is how EXTORT-2 is implemented in the library::

    import axelrod
    p1 = axelrod.ZDExtort2()  # Create a EXTORT-2 player
    p2 = axelrod.Random()  # Create a player that plays randomly
    for round in range(10):
        p1.play(p2)

    print p2.history
    print p1.history

which gives (for the particular seed used)::

    ['D', 'C', 'C', 'C', 'D', 'D', 'D', 'D', 'C', 'D']
    ['C', 'C', 'D', 'C', 'C', 'D', 'D', 'D', 'D', 'D']

you can see that :code:`ZDExtort2` never cooperates after both strategies defect.

GRIM
^^^^

Grim is not defined in [S&P, PNAS 2012] but it is defined elsewhere as follows.
GRIM (also called "Grim trigger"), cooperates until the opponent defects and
then always defects thereafter. In the library this strategy is called
*Grudger*.

*GRIM came 10th in average score and 11th in wins in S&P's tournament.*

Implementation
**************

Here is how GRIM is implemented in the library::

    import axelrod
    p1 = axelrod.Grudger()  # Create a GRIM player
    p2 = axelrod.Defector()  # Create a player that always defects
    for round in range(5):
        p1.play(p2)

    print p1.history

this gives::

    ['C', 'D', 'D', 'D', 'D']

HARD_JOSS
^^^^^^^^^

HARD_JOSS is not defined in [S&P, PNAS 2012] but is otherwise defined as a
strategy that plays like TitForTat but cooperates only with probability
:math:`0.9`. This is a memory-one strategy with the following probabilities:

- :math:`P(C\,|\,CC) = 0.9`
- :math:`P(C\,|\,CD) = 0`
- :math:`P(C\,|\,DC) = 1`
- :math:`P(C\,|\,DD) = 0`

*HARD_JOSS came 16th in average score and 4th in wins in S&P's tournament.*

Implementation
**************

HARD_JOSS as described above is implemented in the library as `Joss` and is
the same as the Joss strategy from `Axelrod's first tournament`_.

HARD_MAJO
^^^^^^^^^

HARD_MAJO is not defined in [S&P, PNAS 2012] and is presumably the same as "Go by Majority", defined as follows: the strategy defects on the first move, defects
if the number of defections of the opponent is greater than or equal to the
number of times it has cooperated, and otherwise cooperates,

*HARD_MAJO came 13th in average score and 5th in wins in S&P's tournament.*

Implementation
**************

HARD_MAJO is implemented in the library::

    import axelrod
    p1 = axelrod.GoByMajority()  # Create a HARD_TFT player
    p2 = axelrod.Random()  # Create a player that plays randomly
    for round in range(5):
        p1.play(p2)

    print p2.history
    print p1.history

which gives (for this seed)::


    ['D', 'C', 'C', 'D', 'D']
    ['C', 'D', 'C', 'C', 'C']

we see that following the third round (at which point the opponent has cooperated a lot), :code:`GoByMajority` cooperates.

HARD_TFT
^^^^^^^^

Hard TFT is not defined in [S&P, PNAS 2012] but is
[elsewhere](http://www.prisoners-dilemma.com/strategies.html)
defined as follows. The strategy cooperates on the
first move, defects if the opponent has defected on any of the previous three
rounds, and otherwise cooperates.

*HARD_TFT came 12th in average score and 10th in wins in S&P's tournament.*

Implementation
**************

HARD_TFT is implemented in the library::

    import axelrod
    p1 = axelrod.HardTitForTat()  # Create a HARD_TFT player
    p2 = axelrod.Alternator()  # Create a player that alternates
    for round in range(5):
        p1.play(p2)

    print p1.history

which gives::

    ['C', 'C', 'D', 'D', 'D']

we see that :code:`HardTitForTat` cooperates for the first two moves but then
constantly defetcts as there is always a defection in it's opponent's recent
history.

HARD_TF2T
^^^^^^^^^

Hard TF2T is not defined in [S&P, PNAS 2012] but is elsewhere defined as
follows. The strategy cooperates on the first move, defects if the opponent
has defected twice (successively) of the previous three rounds, and otherwise
cooperates.

*HARD_TF2T came 6th in average score and 17th in wins in S&P's tournament.*

Implementation
**************

HARD_TF2T is implemented in the library::

    import axelrod
    p1 = axelrod.HardTitFor2Tats()  # Create a HARD_TF2T player
    p2 = axelrod.Random()  # Create a player that plays randomly
    for round in range(5):
        p1.play(p2)

    print p2.history
    print p1.history

which gives (for this particular seed)::

    ['D', 'D', 'C', 'D', 'C']
    ['C', 'C', 'D', 'D', 'C']

we see that :code:`HardTitFor2Tats` waited for 2 defects before defecting, but
also continued to defect on the 4th round (as there were 2 defections in the
previous 3 moves by the opponent).

Calculator
^^^^^^^^^^

This strategy is not unambiguously defined in [S&P, PNAS 2012] but is defined
elsewhere. Calculator plays like Joss for 20 rounds. On the 21 round,
Calculator attempts to detect a cycle in the opponents history, and defects
unconditionally thereafter if a cycle is found. Otherwise Calculator plays like
TFT for the remaining rounds.

Calculator is implemented in the library as follows:

    import axelrod
    p1 = axelrod.Calculator()  # Create a HARD_TF2T player
    p2 = axelrod.Cooperator()  # Create a player that always cooperates
    for round in range(5):
        p1.play(p2)

    print p1.history
    print p2.history

This returns (for a particular random seed)::

    ['C', 'C', 'C', 'C', 'C']
    ['C', 'C', 'C', 'C', 'C']

Prober
^^^^^^

PROBE is not unambiguously defined in [S&P, PNAS 2012] but is defined
elsewhere as Prober. The strategy starts by playing D, C, C on the first three
rounds and then defects forever if the opponent cooperates on rounds
two and three. Otherwise Prober plays as TitForTat would.

*Prober came 15th in average score and 9th in wins in S&P's tournament.*

Implementation
**************

Prober is implemented in the library::

    import axelrod
    p1 = axelrod.Prober()  # Create a Prober player
    p2 = axelrod.Cooperator()  # Create a player that always cooperates
    for round in range(5):
        p1.play(p2)

    print p2.history
    print p1.history

which gives::

    ['D', 'C', 'C', 'D', 'D']
    ['C', 'C', 'C', 'C', 'C']

Prober2
^^^^^^^

PROBE2 is not unambiguously defined in [S&P, PNAS 2012] but is defined
elsewhere as Prober2. The strategy starts by playing D, C, C on the first three
rounds and then cooperates forever if the opponent played D then C on rounds
two and three. Otherwise Prober2 plays as TitForTat would.

*Prober2 came 9th in average score and 12th in wins in S&P's tournament.*

Implementation
**************

Prober2 is implemented in the library::

    import axelrod
    p1 = axelrod.Prober2()  # Create a Prober2 player
    p2 = axelrod.Cooperator()  # Create a player that always cooperates
    for round in range(5):
        p1.play(p2)

    print p2.history
    print p1.history

which gives::

    ['D', 'C', 'C', 'C', 'C']
    ['C', 'C', 'C', 'C', 'C']

Prober3
^^^^^^^

PROBE3 is not unambiguously defined in [S&P, PNAS 2012] but is defined
elsewhere as Prober3. The strategy starts by playing D, C on the first two
rounds and then defects forever if the opponent cooperated on round two.
Otherwise Prober3 plays as TitForTat would.

*Prober3 came 17th in average score and 7th in wins in S&P's tournament.*

Implementation
**************

Prober3 is implemented in the library::

    import axelrod
    p1 = axelrod.Prober3()  # Create a Prober3 player
    p2 = axelrod.Cooperator()  # Create a player that always cooperates
    for round in range(5):
        p1.play(p2)

    print p2.history
    print p1.history

which gives::

    ['D', 'C', 'D', 'D', 'D']
    ['C', 'C', 'C', 'C', 'C']

HardProber
^^^^^^^^^^

HARD_PROBE is not unambiguously defined in [S&P, PNAS 2012] but is defined
elsewhere as HardProber. The strategy starts by playing D, D, C, C on the first
four rounds and then defects forever if the opponent cooperates on rounds
two and three. Otherwise Prober plays as TitForTat would.

*Prober2 came 5th in average score and 6th in wins in S&P's tournament.*

Implementation
**************

HardProber is implemented in the library::

    import axelrod
    p1 = axelrod.HardProber()  # Create a Prober3 player
    p2 = axelrod.Cooperator()  # Create a player that always cooperates
    for round in range(5):
        p1.play(p2)

    print p2.history
    print p1.history

which gives::

    ['D', 'D', 'C', 'C', 'D']
    ['C', 'C', 'C', 'C', 'C']


Strategies implemented in the module
------------------------------------

There are several original strategies which have been created as part of this project and have never (to our knowledge) appeared in previous tournaments.

Fool Me Once
^^^^^^^^^^^

This strategy begins by cooperating but will defect if at any point the opponent has defected more than once.

Backstabber
^^^^^^^^^^^

Forgives the first 3 defections but on the fourth will defect forever. Defects after the 198th round unconditionally.

DoubleCrosser
^^^^^^^^^^^^^

Forgives the first 3 defections but on the fourth will defect forever. If the opponent did not defect in the first 6 rounds the player will cooperate until the 180th round. Defects after the 198th round unconditionally.

Aggravater
^^^^^^^^^^^

This strategy begins by defecting 3 times and then will cooperate until the opponent defects. After the opponent defects it will defect unconditionally. Essentially Grudger, but begins by defecting 3 times.
