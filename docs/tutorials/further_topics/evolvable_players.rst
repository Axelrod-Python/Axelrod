.. _evolvable_players:

Evolvable Players
=================

Several strategies in the library derive from :code:`EvolvablePlayer` which specifies methods
allowing evolutionary or particle swarm algorithms to be used with these strategies. The
`Axelrod Dojo library <https://github.com/Axelrod-Python/axelrod-dojo>`_ [Axelrod1980]_
contains implementations of both algorithms for use with the Axelrod library. Examples include
FSMPlayers, ANN (neural networks), and LookerUp and Gambler (lookup tables).

New :code:`EvolvablePlayer` subclasses can be added to the library. Any strategy that can
define :code:`mutation` and :code:`crossover` methods can be used with the evolutionary algorithm
and the atomic mutation version of the Moran process. To use the particle swarm algorithms, methods
to serialize the strategy to and from a vector of floats must be defined.

Moran Process: Atomic Mutation for Evolvable Players
----------------------------------------------------

Additionally, the Moran process implementation supports a second style of mutation suitable for
evolving new strategies utilizing the :code:`EvolvablePlayer` class via its :code:`mutate` method.
This is in contrast to the transitional mutation that selects one of the other player types rather than (possibly)
generating a new player variant. To use this mutation style set `mutation_method=atomic` in the initialisation
of the Moran process::

    >>> import axelrod as axl
    >>> C = axl.Action.C
    >>> players = [axl.EvolvableFSMPlayer(num_states=2, initial_state=1, initial_action=C) for _ in range(5)]
    >>> mp = axl.MoranProcess(players, turns=10, mutation_method="atomic", seed=1)
    >>> population = mp.play()  # doctest: +SKIP

Note that this may cause the Moran process to fail to converge, if the mutation rates are very high or the
population size very large.  See :ref:`moran-process` for more information.

Reproducible Seeding
--------------------

:code:`EvolvablePlayers` are inherently stochastic. For reproducibility of results, they can be seeded. When
using the Moran process, a process level seed is sufficient. Child seeds will be created and propagated
in a reproducible way. If initialized without a seed, an :code:`EvolvablePlayer` will be given a
random seed in a non-reproducible way.
