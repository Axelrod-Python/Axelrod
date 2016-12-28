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


class PSOGambler1_1_1(Gambler):
    """
    A 1x1x1 PSOGambler trained with pyswarm.
    See: https://gist.github.com/GDKO/60c3d0fd423598f3c4e4
    """

    name = "PSO Gambler 1_1_1"

    def __init__(self):
        pattern = tables[('2', 2, 2, 2)]
        lookup_table = create_lookup_table_from_pattern(
            plays=2, opp_plays=2, opponent_start_plays=2,
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
            plays=2, opp_plays=2, opponent_start_plays=2,
            pattern=pattern)
        Gambler.__init__(self, lookup_table=lookup_table)


class PSOGambler3_3_3(Gambler):
    """
    A 3x3x3 PSOGambler trained with pyswarm.
    """

    name = "PSO Gambler 3_3_3"

    def __init__(self):
        pattern = tables[('', 3, 3, 3)]
        lookup_table = create_lookup_table_from_pattern(
            plays=3, opp_plays=3, opponent_start_plays=3,
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
            plays=2, opp_plays=2, opponent_start_plays=2,
            pattern=pattern)
        Gambler.__init__(self, lookup_table=lookup_table)


class PSOGambler2_2_2_Moran(Gambler):
    """
    A 2x2x2 PSO Gambler trained to win the Moran process.
    """

    name = "PSO Gambler 2_2_2 Moran"

    def __init__(self):
        pattern = tables[("moran", 2, 2, 2)]
        lookup_table = create_lookup_table_from_pattern(
            plays=2, opp_plays=2, opponent_start_plays=2,
            pattern=pattern)
        Gambler.__init__(self, lookup_table=lookup_table)
