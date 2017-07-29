"""Stochastic variants of Lookup table based-strategies, trained with particle
swarm algorithms.

For the original see:
 https://gist.github.com/GDKO/60c3d0fd423598f3c4e4
"""

from axelrod.action import Action
from axelrod.load_data_ import load_pso_tables
from axelrod.player import Player
from axelrod.random_ import random_choice
from .lookerup import LookerUp, Plays


C, D = Action.C, Action.D
tables = load_pso_tables("pso_gambler.csv", directory="data")


class Gambler(LookerUp):
    """
    A stochastic version of LookerUp which will select randomly an action in
    some cases.

    Names:

    - Gambler: Original name by Georgios Koutsovoulos
    """

    name = 'Gambler'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent: Player) -> Action:
        actions_or_float = super(Gambler, self).strategy(opponent)
        if isinstance(actions_or_float, Action):
            return actions_or_float
        return random_choice(actions_or_float)


class PSOGamblerMem1(Gambler):
    """
    A 1x1x0 PSOGambler trained with pyswarm. This is the 'optimal' memory one
    strategy trained against the set of short run time strategies in the
    Axelrod library.

    Names:

    - PSO Gambler Mem1: Original name by Marc Harper
    """

    name = "PSO Gambler Mem1"

    def __init__(self) -> None:
        pattern = tables[("PSO Gambler Mem1", 1, 1, 0)]
        parameters = Plays(self_plays=1, op_plays=1, op_openings=0)

        super().__init__(parameters=parameters, pattern=pattern)


class PSOGambler1_1_1(Gambler):
    """
    A 1x1x1 PSOGambler trained with pyswarm.

    Names:

    - PSO Gambler 1_1_1: Original name by Marc Harper
    """

    name = "PSO Gambler 1_1_1"

    def __init__(self) -> None:
        pattern = tables[("PSO Gambler 1_1_1", 1, 1, 1)]
        parameters = Plays(self_plays=1, op_plays=1, op_openings=1)

        super().__init__(parameters=parameters, pattern=pattern)


class PSOGambler2_2_2(Gambler):
    """
    A 2x2x2 PSOGambler trained with a particle swarm algorithm (implemented in
    pyswarm). Original version by Georgios Koutsovoulos.

    Names:

    - PSO Gambler 2_2_2: Original name by Marc Harper
    """

    name = "PSO Gambler 2_2_2"

    def __init__(self) -> None:
        pattern = tables[("PSO Gambler 2_2_2", 2, 2, 2)]
        parameters = Plays(self_plays=2, op_plays=2, op_openings=2)

        super().__init__(parameters=parameters, pattern=pattern)


class PSOGambler2_2_2_Noise05(Gambler):
    """
    A 2x2x2 PSOGambler trained with pyswarm with noise=0.05.

    Names:

    - PSO Gambler 2_2_2 Noise 05: Original name by Marc Harper
    """

    name = "PSO Gambler 2_2_2 Noise 05"

    def __init__(self) -> None:
        pattern = tables[("PSO Gambler 2_2_2 Noise 05", 2, 2, 2)]
        parameters = Plays(self_plays=2, op_plays=2, op_openings=2)

        super().__init__(parameters=parameters, pattern=pattern)


class ZDMem2(Gambler):
    """
    A memory two generalization of a zero determinant player.

    Names:

    - ZDMem2: Original name by Marc Harper
    - Unnamed [LiS2014]_

    """

    name = "ZD-Mem2"

    classifier = {
        'memory_depth': 2,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        pattern = [11 / 12, 4 / 11, 7 / 9, 1 / 10,
                   5 / 6, 3 / 11, 7 / 9, 1 / 10,
                   2 / 3, 1 / 11, 7 / 9, 1 / 10,
                   3 / 4, 2 / 11, 7 / 9, 1 / 10]
        parameters = Plays(self_plays=2, op_plays=2, op_openings=0)

        super().__init__(parameters=parameters, pattern=pattern)
