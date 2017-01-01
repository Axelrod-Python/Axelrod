from axelrod import Actions, random_choice, load_pso_tables
from .lookerup import LookerUp, create_lookup_table_from_pattern


C, D = Actions.C, Actions.D
tables = load_pso_tables("pso_gambler.csv", directory="data")


class Gambler(LookerUp):
    """
    A stochastic version of LookerUp which will select randomly an action in
    some cases.
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

    def strategy(self, opponent):
        action = LookerUp.strategy(self, opponent)
        # action could be 'C', 'D', or a float
        if action in [C, D]:
            return action
        return random_choice(action)


class PSOGamblerMem1(Gambler):
    """
    A 1x1x0 PSOGambler trained with pyswarm.
    See: https://gist.github.com/GDKO/60c3d0fd423598f3c4e4
    """

    name = "PSO Gambler Mem1"

    def __init__(self):
        pattern = tables[('Mem1', 1, 1, 0)]
        lookup_table = create_lookup_table_from_pattern(
            plays=1, op_plays=1, op_start_plays=0,
            pattern=pattern)
        Gambler.__init__(self, lookup_table=lookup_table)
        self.classifier['memory_depth'] = 1


class PSOGambler1_1_1(Gambler):
    """
    A 1x1x1 PSOGambler trained with pyswarm.
    See: https://gist.github.com/GDKO/60c3d0fd423598f3c4e4
    """

    name = "PSO Gambler 1_1_1"

    def __init__(self):
        pattern = tables[('2', 2, 2, 2)]
        lookup_table = create_lookup_table_from_pattern(
            plays=2, op_plays=2, op_start_plays=2,
            pattern=pattern)
        Gambler.__init__(self, lookup_table=lookup_table)


class PSOGambler2_2_2(Gambler):
    """
    A 2x2x2 PSOGambler trained with pyswarm.
    See: https://gist.github.com/GDKO/60c3d0fd423598f3c4e4
    """

    name = "PSO Gambler 2_2_2"

    def __init__(self):
        pattern = tables[('2', 2, 2, 2)]
        lookup_table = create_lookup_table_from_pattern(
            plays=2, op_plays=2, op_start_plays=2,
            pattern=pattern)
        Gambler.__init__(self, lookup_table=lookup_table)


class PSOGambler2_2_2_Noise05(Gambler):
    """
    A 2x2x2 PSO Gambler trained with noise=0.05.
    """

    name = "PSO Gambler Noise 05"

    def __init__(self):
        pattern = tables[('05_noise', 2, 2, 2)]
        lookup_table = create_lookup_table_from_pattern(
            plays=2, op_plays=2, op_start_plays=2,
            pattern=pattern)
        Gambler.__init__(self, lookup_table=lookup_table)
