from __future__ import unicode_literals
from os import linesep
from axelrod import Actions, Player, init_args
from prompt_toolkit import prompt
from prompt_toolkit.token import Token
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.validation import Validator, ValidationError

C, D = Actions.C, Actions.D


class ActionValidator(Validator):
    """
    A class to validate input from prompt_toolkit.prompt
    """

    def validate(self, document):
        text = document.text

        if text and text.upper() not in ['C', 'D']:
            raise ValidationError(
                message='Action must be C or D',
                cursor_position=0)


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
    def __init__(self, name='Human', c_symbol='C', d_symbol='D'):
        """
        Parameters
        ----------
        name: string
            The name of the human player
        """
        Player.__init__(self)
        self.name = name
        self.symbols = {
            C: c_symbol,
            D: d_symbol
        }

    def history_toolbar(self, cli):
        my_history = [self.symbols[action] for action in self.history]
        opponent_history = [self.symbols[action] for action in self.opponent_history]
        history = list(zip(my_history, opponent_history))
        if self.history:
            content = 'History ({}, opponent): {}'.format(self.name, history)
        return [(Token.Toolbar, content)]

    def strategy(self, opponent):
        toolbar_style = style_from_dict({
            Token.Toolbar: '#ffffff bg:#333333',
        })

        self.opponent_history = opponent.history

        current_turn = len(self.history) + 1
        if self.history:
            toolbar = self.history_toolbar
            print('{}Turn {}: {} played {}, opponent played {}'.format(
                linesep, current_turn - 1, self.name,
                self.symbols[self.history[-1]],
                self.symbols[opponent.history[-1]]))
        else:
            print('{}Starting new match'.format(linesep))
            toolbar = None

        action = prompt(
            'Turn {} action [C or D] for {}: '.format(
                current_turn, self.name),
            validator=ActionValidator(),
            get_bottom_toolbar_tokens=toolbar,
            style=toolbar_style)

        return action.upper()
