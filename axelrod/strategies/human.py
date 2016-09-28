from axelrod import Actions, Player, init_args
from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator, ValidationError

C, D = Actions.C, Actions.D


class ActionValidator(Validator):

    def validate(self, document):
        text = document.text

        if text and text not in ['C', 'D']:
            raise ValidationError(
                message='Action must be C or D',
                cursor_position=0)


def human_input():
    """
    A function to fetch keyboard input from a user, validate that is either
    'C' or 'D' and return the resulting action.

    Returns
    -------
    string
        Either 'C' or 'D'
    """

    action = prompt('Action [C or D]: ', validator=ActionValidator())

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
