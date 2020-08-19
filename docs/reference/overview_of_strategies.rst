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

  "Tit For Tat", "Anatol Rapoport", ":class:`TitForTat <axelrod.strategies.titfortat.TitForTat>`"
  "Tideman and Chieruzzi", "T Nicolaus Tideman and Paula Chieruzz", ":class:`TidemanAndChieruzzi <axelrod.strategies.axelrod_first.FirstByTidemanAndChieruzzi>`"
  "Nydegger", "Rudy Nydegger", ":class:`Nydegger <axelrod.strategies.axelrod_first.FirstByNydegger>`"
  "Grofman", "Bernard Grofman", ":class:`Grofman <axelrod.strategies.axelrod_first.FirstByGrofman>`"
  "Shubik", "Martin Shubik", ":class:`Shubik <axelrod.strategies.axelrod_first.FirstByShubik>`"
  "Stein and Rapoport", "Stein and Anatol Rapoport", ":class:`SteinAndRapoport <axelrod.strategies.axelrod_first.FirstBySteinAndRapoport>`"
  "Grudger", "James W Friedman", ":class:`Grudger <axelrod.strategies.grudger.Grudger>`"
  "Davis", "Morton Davis", ":class:`Davis <axelrod.strategies.axelrod_first.FirstByDavis>`"
  "Graaskamp", "Jim Graaskamp", ":class:`Graaskamp <axelrod.strategies.axelrod_first.FirstByGraaskamp>`"
  "FirstByDowning", "Leslie Downing", ":class:`RevisedDowning <axelrod.strategies.axelrod_first.FirstByDowning>`"
  "Feld", "Scott Feld", ":class:`Feld <axelrod.strategies.axelrod_first.FirstByFeld>`"
  "Joss", "Johann Joss", ":class:`Joss <axelrod.strategies.axelrod_first.FirstByJoss>`"
  "Tullock",  "Gordon Tullock", ":class:`Tullock <axelrod.strategies.axelrod_first.FirstByTullock>`"
  "(Name withheld)", "Unknown", ":class:`UnnamedStrategy <axelrod.strategies.axelrod_first.FirstByAnyonymous>`"
  "Random", "Unknownd", ":class:`Random <axelrod.strategies.rand.Random>`"

Axelrod's second tournament
---------------------------

The code for Axelrod's second touranment was originally published by the
`University of Michigan Center for the Study of Complex Systems <http://lsa.umich.edu/cscs/>`_
and is now available from
`Robert Axelrod's personal website <http://www-personal.umich.edu/~axe/research/Software/CC/CC2.html>`_
subject to a `disclaimer <http://www-personal.umich.edu/~axe/research/Software/CC/CCDisclaimer.html>`_
which states:

 "All materials in this archive are copyright (c) 1996, Robert Axelrod, unless
 otherwise noted. You are free to download these materials and use them without
 restriction."

The Axelrod-Python organisation has published a
`modified version of the original code <https://github.com/Axelrod-Python/TourExec>`_.
In the following table, links to original code point to the Axelrod-Python
repository.

.. include:: fortan_keys.rst

.. csv-table:: Strategies in Axelrod's second tournament
   :header: "Original Code", "Author", "Axelrod Library Name"

   "GRASR_", "Unknown", "Not Implemented"
   "K31R_", "Gail Grisell", ":class:`GoByMajority <axelrod.strategies.gobymajority.GoByMajority>`"
   "K32R_", "Charles Kluepfel", ":class:`SecondByKluepfel <axelrod.strategies.axelrod_second.SecondByKluepfel>`"
   "K33R_", "Harold Rabbie", "Not Implemented"
   "K34R_", "James W Friedman", ":class:`Grudger <axelrod.strategies.grudger.Grudger>`"
   "K35R_", "Abraham Getzler", "Not Implemented"
   "K36R_", "Roger Hotz", "Not Implemented"
   "K37R_", "George Lefevre", "Not Implemented"
   "K38R_", "Nelson Weiderman", "Not Implemented"
   "K39R_", "Tom Almy", "Not Implemented"
   "K40R_", "Robert Adams", "Not Implemented"
   "K41R_", "Herb Weiner", ":class:`SecondByWeiner <axelrod.strategies.axelrod_second.SecondByWeiner>`"
   "K42R_", "Otto Borufsen", ":class:`SecondByBorufsen <axelrod.strategies.axelrod_second.SecondByBorufsen>`"
   "K43R_", "R D Anderson", "Not Implemented"
   "K44R_", "William Adams", ":class:`SecondByWmAdams <axelrod.strategies.axelrod_second.SecondByWmAdams>`"
   "K45R_", "Michael F McGurrin", "Not Implemented"
   "K46R_", "Graham J Eatherley", ":class:`SecondByEatherley <axelrod.strategies.axelrod_second.SecondByEatherley>`"
   "K47R_", "Richard Hufford", ":class:`SecondByRichardHufford <axelrod.strategies.axelrod_second.SecondByRichardHufford>`"
   "K48R_", "George Hufford", "Not Implemented"
   "K49R_", "Rob Cave", ":class:`SecondByCave <axelrod.strategies.axelrod_second.SecondByCave>`"
   "K50R_", "Rik Smoody", "Not Implemented"
   "K51R_", "John Willaim Colbert", "Not Implemented"
   "K52R_", "David A Smith", "Not Implemented"
   "K53R_", "Henry Nussbacher", "Not Implemented"
   "K54R_", "William H Robertson", "Not Implemented"
   "K55R_", "Steve Newman", "Not Implemented"
   "K56R_", "Stanley F Quayle", "Not Implemented"
   "K57R_", "Rudy Nydegger", "Not Implemented"
   "K58R_", "Glen Rowsam", ":class:`SecondByRowsam <axelrod.strategies.axelrod_second.SecondByRowsam>`"
   "K59R_", "Leslie Downing", ":class:`RevisedDowning <axelrod.strategies.revised_downing.RevisedDowning>`"
   "K60R_", "Jim Graaskamp and Ken Katzen", ":class:`SecondByGraaskampKatzen <axelrod.strategies.axelrod_second.SecondByGraaskampKatzen>`"
   "K61R_", "Danny C Champion", ":class:`SecondByChampion <axelrod.strategies.axelrod_second.SecondByChampion>`"
   "K62R_", "Howard R Hollander", "Not Implemented"
   "K63R_", "George Duisman", "Not Implemented"
   "K64R_", "Brian Yamachi", ":class:`SecondByYamachi <axelrod.strategies.axelrod_second.SecondByYamachi>`"
   "K65R_", "Mark F Batell", "Not Implemented"
   "K66R_", "Ray Mikkelson", "Not Implemented"
   "K67R_", "Craig Feathers", ":class:`SecondByTranquilizer <axelrod.strategies.axelrod_second.SecondByTranquilizer>`"
   "K68R_", "Fransois Leyvraz", ":class:`SecondByLeyvraz <axelrod.strategies.axelrod_second.SecondByLeyvraz>`"
   "K69R_", "Johann Joss", "Not Implemented"
   "K70R_", "Robert Pebly", "Not Implemented"
   "K71R_", "James E Hall", "Not Implemented"
   "K72R_", "Edward C White Jr", ":class:`SecondByWhite <axelrod.strategies.axelrod_second.SecondByWhite>`"
   "K73R_", "George Zimmerman", "Not Implemented"
   "K74R_", "Edward Friedland", "Not Implemented"
   "K74RXX_", "Edward Friedland", "Not Implemented"
   "K75R_", "Paul D Harrington", ":class:`SecondByHarrington <axelrod.strategies.axelrod_second.SecondByHarrington>`"
   "K76R_", "David Gladstein", ":class:`SecondByGladstein <axelrod.strategies.axelrod_second.SecondByGladstein>`"
   "K77R_", "Scott Feld", "Not Implemented"
   "K78R_", "Fred Mauk", "Not Implemented"
   "K79R_", "Dennis Ambuehl and Kevin Hickey", Not Implemented
   "K80R_", "Robyn M Dawes and Mark Batell", Not Implemented
   "K81R_", "Martyn Jones", "Not Implemented"
   "K82R_", "Robert A Leyland", "Not Implemented"
   "K83R_", "Paul E Black", ":class:`SecondByWhite <axelrod.strategies.axelrod_second.SecondByWhite>`"
   "K84R_", "T Nicolaus Tideman and Paula Chieruzzi", ":class:`SecondByTidemanChieruzzi <axelrod.strategies.axelrod_second.SecondByTidemanAndChieruzzi>`"
   "K85R_", "Robert B Falk and James M Langsted", "Not Implemented"
   "K86R_", "Bernard Grofman", "Not Implemented"
   "K87R_", "E E H Schurmann",  "Not Implemented"
   "K88R_", "Scott Appold", ":class:`SecondByAppold <axelrod.strategies.axelrod_second.SecondByAppold>`"
   "K89R_", "Gene Snodgrass", "Not Implemented"
   "K90R_", "John Maynard Smith", ":class:`TitFor2Tats <axelrod.strategies.titfortat.TitFor2Tats>`"
   "K91R_", "Jonathan Pinkley", "Not Implemented"
   "K92R_", "Anatol Rapoport", ":class:`TitForTat <axelrod.strategies.titfortat.TitForTat>`"
   "K93R_", "Unknown", "Not Implemented"
   "KPAVLOVC_", "Unknown", ":class:`WinStayLoseShift <axelrod.strategies.memoryone.WinStayLoseShift>`"
   "KRANDOMC_", "Unknown", ":class:`Random <axelrod.strategies.rand.Random>`"
   "KTF2TC_", "Unknown", ":class:`TitFor2Tats <axelrod.strategies.titfortat.TitFor2Tats>`"
   "KTITFORTATC_", "Unknown", ":class:`TitForTat <axelrod.strategies.titfortat.TitForTat>`"


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
online <https://www.pnas.org/content/pnas/109/26/10134/F1.large.jpg?width=800&height=600&carousel=1>`_.

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
`elsewhere <http://www.prisoners-dilemma.com/strategies.html>`_
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

Beaufils et al.'s tournament (1997)
-----------------------------------

In 1997, [Beaufils1997]_ the authors used a tournament to describe a new
strategy of their called "Gradual". The description given in the paper of
"Gradual" is:

    This strategy acts as tit-for-tat, except when it is time to forgive and
    remember the past. It uses cooperation on the first move and then continues
    to do so as long as the other player cooperates. Then after the first
    defection of the other player, it defects one time and cooperates two times;
    after the second defection of the opponent, it defects two times and
    cooperates two times, ... after the nth defection it reacts with n
    consecutive defections and then calms down its opponent with two
    cooperations.

This is the only description of the strategy however the paper does include a
table of results of the tournament. The scores of "Gradual" against the
opponents (including itself) are:


.. csv-table:: Score of Gradual reported in [Beaufils1997]_
   :header: "Name", "Name used in [Beaufils1997]_", "Score (1000 turns)"

   "Cooperator", "coop", 3000
   "Defector", "def", 915
   "Random", "rand", 2815
   "Tit For Tat", "tft", 3000
   "Grudger", "spite", 3000
   "Cycler DDC", "p_nst", 2219
   "Cycler CCD", "p_kn", 3472
   "Go By Majority", "sft_mj", 3000
   "Suspicious Tit For Tat", "mist", 2996
   "Prober", "prob", 2999
   "Gradual", "grad", 3000
   "Win Stay Lose Shift", "pav", 3000

The following code reproduces the above::

    >>> import axelrod as axl
    >>> players = [axl.Cooperator(),
    ...            axl.Defector(),
    ...            axl.Random(),
    ...            axl.TitForTat(),
    ...            axl.Grudger(),
    ...            axl.CyclerDDC(),
    ...            axl.CyclerCCD(),
    ...            axl.GoByMajority(),
    ...            axl.SuspiciousTitForTat(),
    ...            axl.Prober(),
    ...            axl.OriginalGradual(),
    ...            axl.WinStayLoseShift(),
    ...            ]
    >>> turns = 1000
    >>> tournament = axl.Tournament(players, turns=turns, repetitions=1, seed=75)
    >>> results = tournament.play(progress_bar=False)
    >>> for average_score_per_turn in results.payoff_matrix[-2]:
    ...     print(round(average_score_per_turn * turns, 1))
    3000.0
    915.0
    2763.0
    3000.0
    3000.0
    2219.0
    3472.0
    3000.0
    2996.0
    2999.0
    3000.0
    3000.0

The :code:`OriginalGradual` strategy implemented has the following description:

    A player that punishes defections with a growing number of defections
    but after punishing for `punishment_limit` number of times enters a calming
    state and cooperates no matter what the opponent does for two rounds.

    The `punishment_limit` is incremented whenever the opponent defects and the
    strategy is not in either calming or punishing state.

Note that a different version of Gradual appears in [CRISTAL-SMAC2018]_.
This was brought to the attention of the maintainers of the library by one of the
authors of [Beaufils1997]_ and is documented here `<https://github.com/Axelrod-Python/Axelrod/issues/1294>`_.

The strategy implemented in [CRISTAL-SMAC2018]_ and defined here as :code:`Gradual` has the following description:

    Similar to OriginalGradual, this is a player that punishes defections with a
    growing number of defections but after punishing for `punishment_limit`
    number of times enters a calming state and cooperates no matter what the
    opponent does for two rounds.

    This version of Gradual is an update of `OriginalGradual` and the difference
    is that the `punishment_limit` is incremented whenever the opponent defects
    (regardless of the state of the player).

This highlights the importance of best practice and reproducible computational
research. Both strategies implemented in this library are fully tested and
documented clearly and precisely.
