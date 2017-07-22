Tournaments
===========

Axelrod's first tournament
--------------------------

Axelrod's first tournament is described in his 1980 paper entitled `'Effective
choice in the Prisoner's Dilemma' <http://www.jstor.org/stable/173932>`_ [Axelrod1980]_. This
tournament included 14 strategies (plus a random "strategy") and they are listed
below, (ranked in the order in which they appeared).

An indication is given as to whether or not this strategy is implemented in the
:code:`axelrod` library. If this strategy is not implemented please do send us a
`pull request <https://github.com/Axelrod-Python/Axelrod/pulls>`_.

.. csv-table:: Strategies in Axelrod's first tournament
  :header: "Name", "Author", "Axelrod Library Name"

  "`Tit For Tat`_", "Unknown. Probably Robert Axelrod", ":class:`TitForTat <axelrod.strategies.titfortat.TitForTat>`"
  "`Tideman and Chieruzzi`_", "T Nicolaus Tideman and Paula Chieruzz", "Not Implemented "
  "`Nydegger`_", "Rudy Nydegger", ":class:`Nydegger <axelrod.strategies.axelrod_first.Nydegger>`"
  "`Grofman`_", "Bernard Grofman", ":class:`Grofman <axelrod.strategies.axelrod_first.Grofman>`"
  "`Shubik`_", "Martin Shubik", ":class:`Shubik <axelrod.strategies.axelrod_first.Shubik>`"
  "`Stein and Rapoport`_", "Stein and Anatol Rapoport", ":class:`SteinAndRapoport <axelrod.strategies.axelrod_first.SteinAndRapoport>`"
  "`Grudger`_", "James W Friedman", ":class:`Grudger <axelrod.strategies.grudger.Grudger>`"
  "`Davis`_", "Morton Davis", ":class:`Davis <axelrod.strategies.axelrod_first.Davis>`"
  "`Graaskamp`_", "Jim Graaskamp", "Not Implemented"
  "`Downing`_", "Leslie Downing", ":class:`RevisedDowning <axelrod.strategies.axelrod_first.RevisedDowning>`"
  "`Feld`_", "Scott Feld", ":class:`Feld <axelrod.strategies.axelrod_first.Feld>`"
  "`Joss`_", "Johann Joss", ":class:`Joss <axelrod.strategies.axelrod_first.Joss>`"
  "`Tullock`_",  "Gordon Tullock", ":class:`Tullock <axelrod.strategies.axelrod_first.Tullock>`"
  "`Unnamed Strategy`_", "Unknown", ":class:`UnnamedStrategy <axelrod.strategies.axelrod_first.UnnamedStrategy>`"
  ":ref:`random-strategy`", "Unknown. Probably Robert Axelrod", ":class:`Random <axelrod.strategies.rand.Random>`"


Tideman and Chieruzzi
^^^^^^^^^^^^^^^^^^^^^

**Not implemented yet**

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

Graaskamp
^^^^^^^^^

**Not implemented yet**

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

.. _random-strategy:

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

TESTER
^^^^^^

This strategy is a TFT variant that attempts to exploit certain strategies. It
defects on the first move. If the opponent ever defects, TESTER 'apologies' by
cooperating and then plays TFT for the rest of the game. Otherwise TESTER
alternates cooperation and defection.

*This strategy came 46th in Axelrod's second tournament.*

Stewart and Plotkin's Tournament (2012)
---------------------------------------

In 2012, `Alexander Stewart and Joshua Plotkin
<http://www.pnas.org/content/109/26/10134.full.pdf>`_ ran a variant of
Axelrod's tournament with 19 strategies to test the effectiveness of the then
newly discovered Zero-Determinant strategies.

The paper is identified as *doi: 10.1073/pnas.1208087109* and referred to as
[Stewart2012]_ below. Unfortunately the details of the tournament and the
implementation of  strategies is not clear in the manuscript. We can, however,
make reasonable guesses to the implementation of many strategies based on their
names and classical definitions.

The following classical strategies are included in the library:

.. csv-table:: Strategies in Stewart and Plotkin's tournament
  :header: "S&P Name", "Long Name", "Axelrod Library Name"

  "ALLC", "Always Cooperate", ":class:`Cooperator <axelrod.strategies.cooperator.Cooperator>`"
  "ALLD", "Always Defect", ":class:`Defector <axelrod.strategies.defector.Defector>`"
  "`EXTORT-2`_", "Extort-2", ":class:`ZDExtort2 <axelrod.strategies.memoryone.ZDExtort2>`"
  "`HARD_MAJO`_", "Hard majority", ":class:`HardGoByMajority <axelrod.strategies.gobymajority.HardGoByMajority>`"
  "`HARD_JOSS`_", "Hard Joss", ":class:`Joss <axelrod.strategies.axelrod_first.Joss>`"
  "`HARD_TFT`_", "Hard tit for tat", ":class:`HardTitForTat <axelrod.strategies.titfortat.HardTitForTat>`"
  "`HARD_TF2T`_", "Hard tit for 2 tats", ":class:`HardTitFor2Tats <axelrod.strategies.titfortat.HardTitFor2Tats>`"
  "TFT", "Tit-For-Tat", ":class:`TitForTat <axelrod.strategies.titfortat.TitForTat>`"
  "`GRIM`_", "Grim", ":class:`Grudger <axelrod.strategies.grudger.Grudger>`"
  "`GTFT`_", "Generous Tit-For-Tat", ":class:`GTFT <axelrod.strategies.memoryone.GTFT>`"
  "`TF2T`_", "Tit-For-Two-Tats", ":class:`TitFor2Tats <axelrod.strategies.titfortat.TitFor2Tats>`"
  "`WSLS`_", "Win-Stay-Lose-Shift", ":class:`WinStayLoseShift <axelrod.strategies.memoryone.WinStayLoseShift>`"
  "RANDOM", "Random", ":class:`Random <axelrod.strategies.rand.Random>`"
  "`ZDGTFT-2`_", "ZDGTFT-2", ":class:`ZDGTFT2 <axelrod.strategies.memoryone.ZDGTFT2>`"

ALLC, ALLD, TFT and RANDOM are defined above. The remaining classical
strategies are defined below. The tournament also included two Zero Determinant
strategies, both implemented in the library. The full table of strategies and
results is `available
online <http://www.pnas.org/content/109/26/10134/F1.expansion.html>`_.

Memory one strategies
^^^^^^^^^^^^^^^^^^^^^

In 2012 `Press and Dyson <http://www.pnas.org/content/109/26/10409.full.pdf>`_
[Press2012]_ showed interesting results with regards to so called memory one
strategies.  Stewart and Plotkin implemented a number of these. A memory one
strategy is simply a probabilistic strategy that is defined by 4 parameters.
These four parameters dictate the probability of cooperating given 1 of 4
possible outcomes of the previous round:

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

TF2T
^^^^

Tit-For-Two-Tats is like Tit-For-Tat but only retaliates after two defections
rather than one. This is not a memory-one strategy.

*TF2T came 3rd in average score and last (?) in wins in S&P's tournament.*

WSLS
^^^^

Win-Stay-Lose-Shift is a strategy that shifts if the highest payoff was not
earned in the previous round. WSLS is also known as "Win-Stay-Lose-Switch" and
"Pavlov". It can be seen as a memory-one strategy as follows:

- :math:`P(C\,|\,CC) = 1`
- :math:`P(C\,|\,CD) = 0`
- :math:`P(C\,|\,DC) = 0`
- :math:`P(C\,|\,DD) = 1`

*WSLS came 7th in average score and 13th in wins in S&P's tournament.*

RANDOM
^^^^^^

Random is a strategy that was defined in `Axelrod's first tournament`_, note that this is also a memory-one strategy:

- :math:`P(C\,|\,CC) = 0.5`
- :math:`P(C\,|\,CD) = 0.5`
- :math:`P(C\,|\,DC) = 0.5`
- :math:`P(C\,|\,DD) = 0.5`

*RANDOM came 8th in average score and 8th in wins in S&P's tournament.*

ZDGTFT-2
^^^^^^^^

This memory-one strategy is defined by the following four conditional
probabilities based on the last round of play:

- :math:`P(C\,|\,CC) = 1`
- :math:`P(C\,|\,CD) = 1/8`
- :math:`P(C\,|\,DC) = 1`
- :math:`P(C\,|\,DD) = 1/4`

*This strategy came 1st in average score and 16th in wins in S&P's tournament.*

EXTORT-2
^^^^^^^^

This memory-one strategy is defined by the following four conditional
probabilities based on the last round of play:

- :math:`P(C\,|\,CC) = 8/9`
- :math:`P(C\,|\,CD) = 1/2`
- :math:`P(C\,|\,DC) = 1/3`
- :math:`P(C\,|\,DD) = 0`

*This strategy came 18th in average score and 2nd in wins in S&P's tournament.*

GRIM
^^^^

Grim is not defined in [Stewart2012]_ but it is defined elsewhere as follows.
GRIM (also called "Grim trigger"), cooperates until the opponent defects and
then always defects thereafter. In the library this strategy is called
*Grudger*.

*GRIM came 10th in average score and 11th in wins in S&P's tournament.*

HARD_JOSS
^^^^^^^^^

HARD_JOSS is not defined in [Stewart2012]_ but is otherwise defined as a
strategy that plays like TitForTat but cooperates only with probability
:math:`0.9`. This is a memory-one strategy with the following probabilities:

- :math:`P(C\,|\,CC) = 0.9`
- :math:`P(C\,|\,CD) = 0`
- :math:`P(C\,|\,DC) = 1`
- :math:`P(C\,|\,DD) = 0`

*HARD_JOSS came 16th in average score and 4th in wins in S&P's tournament.*

HARD_JOSS as described above is implemented in the library as `Joss` and is
the same as the Joss strategy from `Axelrod's first tournament`_.

HARD_MAJO
^^^^^^^^^

HARD_MAJO is not defined in [Stewart2012]_ and is presumably the same as "Go by Majority", defined as follows: the strategy defects on the first move, defects
if the number of defections of the opponent is greater than or equal to the
number of times it has cooperated, and otherwise cooperates,

*HARD_MAJO came 13th in average score and 5th in wins in S&P's tournament.*

HARD_TFT
^^^^^^^^

Hard TFT is not defined in [Stewart2012]_ but is
[elsewhere](http://www.prisoners-dilemma.com/strategies.html)
defined as follows. The strategy cooperates on the
first move, defects if the opponent has defected on any of the previous three
rounds, and otherwise cooperates.

*HARD_TFT came 12th in average score and 10th in wins in S&P's tournament.*

HARD_TF2T
^^^^^^^^^

Hard TF2T is not defined in [Stewart2012]_ but is elsewhere defined as
follows. The strategy cooperates on the first move, defects if the opponent
has defected twice (successively) of the previous three rounds, and otherwise
cooperates.

*HARD_TF2T came 6th in average score and 17th in wins in S&P's tournament.*

Calculator
^^^^^^^^^^

This strategy is not unambiguously defined in [Stewart2012]_ but is defined
elsewhere. Calculator plays like Joss for 20 rounds. On the 21 round,
Calculator attempts to detect a cycle in the opponents history, and defects
unconditionally thereafter if a cycle is found. Otherwise Calculator plays like
TFT for the remaining rounds.

Prober
^^^^^^

PROBE is not unambiguously defined in [Stewart2012]_ but is defined
elsewhere as Prober. The strategy starts by playing D, C, C on the first three
rounds and then defects forever if the opponent cooperates on rounds
two and three. Otherwise Prober plays as TitForTat would.

*Prober came 15th in average score and 9th in wins in S&P's tournament.*

Prober2
^^^^^^^

PROBE2 is not unambiguously defined in [Stewart2012]_ but is defined
elsewhere as Prober2. The strategy starts by playing D, C, C on the first three
rounds and then cooperates forever if the opponent played D then C on rounds
two and three. Otherwise Prober2 plays as TitForTat would.

*Prober2 came 9th in average score and 12th in wins in S&P's tournament.*

Prober3
^^^^^^^

PROBE3 is not unambiguously defined in [Stewart2012]_ but is defined
elsewhere as Prober3. The strategy starts by playing D, C on the first two
rounds and then defects forever if the opponent cooperated on round two.
Otherwise Prober3 plays as TitForTat would.

*Prober3 came 17th in average score and 7th in wins in S&P's tournament.*

HardProber
^^^^^^^^^^

HARD_PROBE is not unambiguously defined in [Stewart2012]_ but is defined
elsewhere as HardProber. The strategy starts by playing D, D, C, C on the first
four rounds and then defects forever if the opponent cooperates on rounds
two and three. Otherwise Prober plays as TitForTat would.

*HardProber came 5th in average score and 6th in wins in S&P's tournament.*

NaiveProber
^^^^^^^^^^^

NAIVE_PROBER is a modification of Tit For Tat strategy which with a small
probability randomly defects. Default value for a probability of defection is
0.1.
