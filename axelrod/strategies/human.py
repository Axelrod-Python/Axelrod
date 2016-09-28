from axelrod import Actions, Player, init_args
from builtins import input

C, D = Actions.C, Actions.D


def human_input():
    action = input('Action [C or D]: ')
    while action not in ['C', 'D']:
        action = input('Action: ')
    return action


class Human(Player):
    """
    A strategy that prompts for keyboard input rather than deriving its own
    action.
    """

    name = 'Human'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(['length', 'game']),
        'long_run_time': True,
        'inspects_source': True,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @init_args
    def __init__(self, name='Human'):
        """
        Parameters
        ----------
        name: string
            The name of the human player
        """
        Player.__init__(self)
        self.name = name

    @staticmethod
    def strategy(opponent):
        return human_input()
