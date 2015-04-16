Background to Axelrod's Tournament
==================================

In the 1980s, professor of Political Science Robert Axelrod ran a tournament inviting strategies from collaborators all over the world for the **Iterated Prisoner's Dilemma**.
You can read about this more `here <http://en.wikipedia.org/wiki/The_Evolution_of_Cooperation#Axelrod.27s_tournaments>`_.

Another nice write up of Axelrod's work and this tournament on github was put together by `Artem Kaznatcheev <https://plus.google.com/101780559173703781847/posts>`_ `here <https://egtheory.wordpress.com/2015/03/02/ipd/>`_.

The Prisoner's Dilemma
----------------------

The `Prisoner's dilemma <http://en.wikipedia.org/wiki/Prisoner%27s_dilemma>`_ is the simple two player game shown below:

+----------+---------------+---------------+
|          | Cooperate     | Defect        |
+==========+===============+===============+
|Cooperate | (3,3)         | (5,0)         |
+----------+---------------+---------------+
|Defect    | (0,5)         | (1,1)         |
+----------+---------------+---------------+

If both players cooperate they will each go to prison for 2 years and receive an
equivalent utility of 3.
If one cooperates and the other defects: the defector does not go to prison and the cooperator goes to prison for 5 years, the cooperator receives a utility of 5 and the defector a utility of 0.
If both defect: they both go to prison for 4 years and receive an equivalent
utility of 1.

By simply investigating the best responses against both possible actions of each player it is immediate to see that the Nash equilibrium for this game is for both players to defect.

The iterated Prisoner's Dilemma
-------------------------------

We can use the basic Prisoner's Dilemma as a _stage_ game in a repeated game.
Players now aim to maximise the utility (corresponding to years in prison) over a repetition of the game.
Strategies can take in to account both players history and so can take the form:

    "I will cooperate unless you defect 3 times in a row at which point I will defect forever."

Axelrod ran such a tournament (twice) and invited strategies from anyone who would contribute.
The tournament was a round robin and the winner was the strategy who had the lowest total amount of time in prison.

This tournament has been used to study how cooperation can evolve from a very simple set of rules.
This is mainly because the winner of both tournaments was 'tit for tat': a strategy that would never defect first (referred to as a 'nice' strategy).
