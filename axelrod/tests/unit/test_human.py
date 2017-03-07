from os import linesep
from unittest import TestCase
from prompt_toolkit.validation import ValidationError
from axelrod import Actions, Player
from axelrod.strategies.human import Human, ActionValidator
from .test_player import TestPlayer


C, D = Actions.C, Actions.D


class TestDocument(object):
    """
    A class to mimic a prompt-toolkit document having just the text attribute.
    """

    def __init__(self, text):
        self.text = text


class TestActionValidator(TestCase):

    def test_validator(self):
        test_documents = [TestDocument(x) for x in [C, C, D, D]]
        for test_document in test_documents:
            ActionValidator().validate(test_document)

        test_document = TestDocument('E')
        self.assertRaises(
            ValidationError, ActionValidator().validate, test_document)


class TestHumanClass(TestPlayer):

    name = "Human"
    player = Human
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(['length', 'game']),
        'long_run_time': True,
        'inspects_source': True,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_init(self):
        human = Human(name='test human', c_symbol='X', d_symbol='Y')
        self.assertEqual(human.name, 'test human')
        self.assertEqual(human.symbols, {C: 'X', D: 'Y'})

    def test_history_toolbar(self):
        human = Human()
        expected_content = ''
        actual_content = human._history_toolbar(None)[0][1]
        self.assertEqual(actual_content, expected_content)

        human.history = [C]
        human.opponent_history = [C]
        expected_content = "History (Human, opponent): [('C', 'C')]"
        actual_content = human._history_toolbar(None)[0][1]
        self.assertIn(actual_content, expected_content)

    def test_status_messages(self):
        human = Human()
        expected_messages = {
            'toolbar': None,
            'print': '{}Starting new match'.format(linesep)
        }
        actual_messages = human._status_messages()
        self.assertEqual(actual_messages, expected_messages)

        human.history = [C]
        human.opponent_history = [C]
        expected_print_message = (
            '{}Turn 1: Human played C, opponent played C'.format(linesep)
        )
        actual_messages = human._status_messages()
        self.assertEqual(actual_messages['print'], expected_print_message)
        self.assertIsNotNone(actual_messages['toolbar'])

    def test_get_human_input(self):
        # There are no tests for this method.
        # The method purely calls prompt_toolkit.prompt which is difficult to
        # test and we therefore rely upon the test suite of the prompt_toolkit
        # library itself.
        pass

    def test_strategy(self):
        human = Human()
        expected_action = C
        actual_action = human.strategy(Player(), lambda: C)
        self.assertEqual(actual_action, expected_action)

    def test_reset_history_and_attributes(self):
        """Overwrite the reset method for this strategy."""
        pass
