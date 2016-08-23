from axelrod import Actions, Player, init_args, random_choice
from axelrod.strategy_transformers import FinalTransformer
from .lookerup import LookerUp, create_lookup_table_keys


C, D = Actions.C, Actions.D


# End with two defections if tournament length is known
@FinalTransformer((D, D), name_prefix=None)
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
        pattern_pso = [1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 1.0, 0.93, 0.0, 1.0, 0.67, 0.42, 0.0,
                       0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.48, 0.0,
                       0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.19, 1.0, 1.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0,
                       0.0, 1.0, 0.36, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        # Zip together the keys and the action pattern to get the lookup table.
        lookup_table = dict(zip(lookup_table_keys, pattern_pso))
        Gambler.__init__(self, lookup_table=lookup_table)
