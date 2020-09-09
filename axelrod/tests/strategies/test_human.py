from os import linesep
from unittest import TestCase
from unittest.mock import patch

import axelrod as axl
from axelrod.strategies.human import ActionValidator, Human
from prompt_toolkit.validation import ValidationError

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestDocument(object):
    """
    A class to mimic a prompt-toolkit document having just the text attribute.
    """

    def __init__(self, text):
        self.text = text


class TestActionValidator(TestCase):
    def test_validator(self):
        test_documents = [TestDocument(x) for x in ["C", "c", "D", "d"]]
        for test_document in test_documents:
            ActionValidator().validate(test_document)

        test_document = TestDocument("E")
        self.assertRaises(
            ValidationError, ActionValidator().validate, test_document
        )


class TestHumanClass(TestPlayer):

    name = "Human: human, C, D"
    player = Human
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": True,
        "inspects_source": True,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_init(self):
        human = Human(name="test human", c_symbol="X", d_symbol="Y")
        self.assertEqual(human.human_name, "test human")
        self.assertEqual(human.symbols, {C: "X", D: "Y"})

    def test_history_toolbar(self):
        human = Human()
        expected_content = ""
        actual_content = human._history_toolbar()
        self.assertEqual(actual_content, expected_content)

        human.history.append(C, C)
        expected_content = "History (human, opponent): [('C', 'C')]"
        actual_content = human._history_toolbar()
        self.assertIn(actual_content, expected_content)

    def test_status_messages(self):
        human = Human()
        expected_messages = {
            "toolbar": None,
            "print": "{}Starting new match".format(linesep),
        }
        actual_messages = human._status_messages()
        self.assertEqual(actual_messages, expected_messages)

        human.history.append(C, C)
        expected_print_message = (
            "{}Turn 1: human played C, opponent played C".format(linesep)
        )
        actual_messages = human._status_messages()
        self.assertEqual(actual_messages["print"], expected_print_message)
        self.assertIsNotNone(actual_messages["toolbar"])

    def test_get_human_input_c(self):
        with patch("axelrod.human.prompt", return_value="c") as prompt_:
            actions = [(C, C)] * 5
            self.versus_test(axl.Cooperator(), expected_actions=actions)
            self.assertEqual(
                prompt_.call_args[0], ("Turn 5 action [C or D] for human: ",)
            )

    def test_get_human_input_C(self):
        with patch("axelrod.human.prompt", return_value="C") as prompt_:
            actions = [(C, C)] * 5
            self.versus_test(axl.Cooperator(), expected_actions=actions)
            self.assertEqual(
                prompt_.call_args[0], ("Turn 5 action [C or D] for human: ",)
            )

    def test_get_human_input_d(self):
        with patch("axelrod.human.prompt", return_value="d") as prompt_:
            actions = [(D, C)] * 5
            self.versus_test(axl.Cooperator(), expected_actions=actions)
            self.assertEqual(
                prompt_.call_args[0], ("Turn 5 action [C or D] for human: ",)
            )

    def test_get_human_input_D(self):
        with patch("axelrod.human.prompt", return_value="D") as prompt_:
            actions = [(D, C)] * 5
            self.versus_test(axl.Cooperator(), expected_actions=actions)
            self.assertEqual(
                prompt_.call_args[0], ("Turn 5 action [C or D] for human: ",)
            )

    def test_strategy(self):
        human = Human()
        expected_action = C
        actual_action = human.strategy(axl.Player(), lambda: C)
        self.assertEqual(actual_action, expected_action)

    def test_reset_history_and_attributes(self):
        """Overwrite the reset method for this strategy."""
        pass

    def test_repr(self):
        human = Human()
        self.assertEqual(human.__repr__(), "Human: human")

        human = Human(name="John Nash")
        self.assertEqual(human.__repr__(), "Human: John Nash")
        human = Human(name="John Nash", c_symbol="1", d_symbol="2")
        self.assertEqual(human.__repr__(), "Human: John Nash")

    def equality_of_players_test(self, p1, p2, seed, opponent):
        return True
