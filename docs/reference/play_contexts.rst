Play Contexts and Generic Prisoner's Dilemma
============================================

There are four possible round outcomes:

- Mutual cooperation: :math:`(C, C)`
- Defection: :math:`(C, D)` or :math:`(D, C)`
- Mutual defection: :math:`(D, D)`

Each of these corresponds to one particular set of payoffs in the following
generic Prisoner's dilemma:


+----------+---------------+---------------+
|          | Cooperate     | Defect        |
+==========+===============+===============+
|Cooperate | (R,R)         | (S,T)         |
+----------+---------------+---------------+
|Defect    | (T,S)         | (P,P)         |
+----------+---------------+---------------+

For the above to constitute a Prisoner's dilemma, the following must hold:
:math:`T>R>P>S`.

These payoffs are commonly referred to as:

- :math:`R`: the **Reward** payoff (default value in the library: 3)
- :math:`P`: the **Punishment** payoff (default value in the library: 1)
- :math:`S`: the **Sucker** payoff (default value in the library: 0)
- :math:`T`: the **Temptation** payoff (default value in the library: 5)

A particular Prisoner's Dilemma is often described by the 4-tuple: :math:`(R, P,
S, T)`::

    >>> import axelrod
    >>> axelrod.game.DefaultGame.RPST()
    (3, 1, 0, 5)
