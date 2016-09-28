from __future__ import print_function
from axelrod import Actions, Player, init_args
import sys

C, D = Actions.C, Actions.D


def human_input():
    """
    A function to fetch keyboard input from a user, validate that is either
    'C' or 'D' and return the resulting action.

    Returns
    -------
    string
        Either 'C' or 'D'
    """

    # Input functions changed between python 2 and python 3. This condition
    # checks the python version being used and sets the correct function
    # accordingly.
    if sys.version_info[0] >= 3:
        get_input = input
    else:
        get_input = raw_input

    prompt = 'Action [C or D]: '

    action = get_input(prompt)
    while action.upper() not in ['C', 'D']:
        action = input(prompt)

    return action.upper()


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

    def strategy(self, opponent):
        if not opponent.history:
            print('Starting new match')
        else:
            print('Them: ', opponent.history)
            print('You:  ', self.history)
        return human_input()
