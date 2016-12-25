from axelrod import Actions, init_args, random_choice, load_data
from .lookerup import LookerUp, create_lookup_table_keys


C, D = Actions.C, Actions.D

table = load_data("pso_gambler.csv", directory="data")
table2 = load_data("pso_gambler2.csv", directory="data")
table05 = load_data("pso_gambler05.csv", directory="data")


class Gambler(LookerUp):
    """
    A LookerUp class player which will select randomly an action in some cases.
    It will always defect the last 2 turns.
    """

    name = 'Gambler'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(['length']),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @init_args
    def __init__(self, lookup_table=None):
        """
        If no lookup table is provided to the constructor, then use the TFT one.
        """
        if not lookup_table:
            lookup_table = {
            ('', 'C', 'D'): 0,
            ('', 'D', 'D'): 0,
            ('', 'C', 'C'): 1,
            ('', 'D', 'C'): 1,
            }
        LookerUp.__init__(self, lookup_table=lookup_table, value_length=None)

    def strategy(self, opponent):
        action = LookerUp.strategy(self, opponent)
        # action could be 'C' or a float
        if action in [C, D]:
            return action
        return random_choice(action)


class PSOGambler(Gambler):
    """
    A LookerUp strategy that uses a lookup table with probability numbers
    generated using a Particle Swarm Optimisation (PSO) algorithm.

    A description of how this strategy was trained is given here:
    https://gist.github.com/GDKO/60c3d0fd423598f3c4e4
    """

    name = "PSO Gambler"

    def __init__(self):
        lookup_table_keys = create_lookup_table_keys(plays=2,
                                                     opponent_start_plays=2)

        # GK: Pattern of values determined previously with a pso algorithm.
        pattern_pso = table

        # Zip together the keys and the action pattern to get the lookup table.
        lookup_table = dict(zip(lookup_table_keys, pattern_pso))
        Gambler.__init__(self, lookup_table=lookup_table)


class PSOGambler2(Gambler):
    """
    A LookerUp strategy that uses a lookup table with probability numbers
    generated using a Particle Swarm Optimisation (PSO) algorithm.

    A description of how this strategy was trained is given here:
    https://gist.github.com/GDKO/60c3d0fd423598f3c4e4
    """

    name = "PSO Gambler 2"

    def __init__(self):
        lookup_table_keys = create_lookup_table_keys(plays=2,
                                                     opponent_start_plays=2)

        # GK: Pattern of values determined previously with a pso algorithm.
        pattern_pso = table2

        # Zip together the keys and the action pattern to get the lookup table.
        lookup_table = dict(zip(lookup_table_keys, pattern_pso))
        Gambler.__init__(self, lookup_table=lookup_table)


class PSOGambler05(Gambler):
    """
    A LookerUp strategy that uses a lookup table with probability numbers
    generated using a Particle Swarm Optimisation (PSO) algorithm.

    A description of how this strategy was trained is given here:
    https://gist.github.com/GDKO/60c3d0fd423598f3c4e4
    """

    name = "PSO Gambler 05"

    def __init__(self):
        lookup_table_keys = create_lookup_table_keys(plays=2,
                                                     opponent_start_plays=2)

        # GK: Pattern of values determined previously with a pso algorithm.
        pattern_pso = table05

        # Zip together the keys and the action pattern to get the lookup table.
        lookup_table = dict(zip(lookup_table_keys, pattern_pso))
        Gambler.__init__(self, lookup_table=lookup_table)
