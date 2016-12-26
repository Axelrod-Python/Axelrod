from axelrod import Actions, random_choice, load_data
from .lookerup import LookerUp, create_lookup_table_from_pattern


C, D = Actions.C, Actions.D

table = load_data("pso_gambler.csv", directory="data")
table2 = load_data("pso_gambler2.csv", directory="data")
table3_3 = load_data("pso_gambler3_3.csv", directory="data")
table05 = load_data("pso_gambler05.csv", directory="data")


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
        # action could be 'C' or a float
        if action in [C, D]:
            return action
        return random_choice(action)


class PSOGambler(Gambler):
    """
    A 2x2 PSOGambler trained with pyswarm.
    See: https://gist.github.com/GDKO/60c3d0fd423598f3c4e4
    """

    name = "PSO Gambler"

    def __init__(self):
        pattern = table
        lookup_table = create_lookup_table_from_pattern(
            plays=2, opp_plays=2, opponent_start_plays=2,
            pattern=pattern)
        Gambler.__init__(self, lookup_table=lookup_table)


class PSOGambler2(Gambler):
    """
    A 2x2 PSOGambler trained with pyswarm.
    See: https://gist.github.com/GDKO/60c3d0fd423598f3c4e4
    """

    name = "PSO Gambler 2"

    def __init__(self):
        pattern = table2
        lookup_table = create_lookup_table_from_pattern(
            plays=2, opp_plays=2, opponent_start_plays=2,
            pattern=pattern)
        Gambler.__init__(self, lookup_table=lookup_table)



class PSOGambler3_3(Gambler):
    """
    A 3x3 PSOGambler trained with pyswarm.
    """

    name = "PSO Gambler 3_3"

    def __init__(self):
        pattern = table3_3
        lookup_table = create_lookup_table_from_pattern(
            plays=3, opp_plays=3, opponent_start_plays=3,
            pattern=pattern)
        Gambler.__init__(self, lookup_table=lookup_table)


class PSOGambler05(Gambler):
    """
    A 2x2 PSO Gambler trained with noise=0.05.
    """

    name = "PSO Gambler 05"

    def __init__(self):
        pattern = table05
        lookup_table = create_lookup_table_from_pattern(
            plays=2, opp_plays=2, opponent_start_plays=2,
            pattern=pattern)
        Gambler.__init__(self, lookup_table=lookup_table)
