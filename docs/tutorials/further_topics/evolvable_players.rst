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
