import axelrod
from Axelrod.axelrod.tests.strategies.test_player import TestPlayer
import unittest

C, D = axelrod.Action.C, axelrod.Action.D


class TestTitForTat(TestPlayer):
    """
 Note that this test is referred to in the documentation as an example on
 writing tests.  If you modify the tests here please also modify the
 documentation.
 """

    name = "Tit For Tat"
    player = axelrod.TitForTat
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)
        self.second_play_test(rCC=C, rCD=D, rDC=C, rDD=D)

        # Play against opponents
        actions = [(C, C), (C, D), (D, C), (C, D)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions)

        actions = [(C, C), (C, C), (C, C), (C, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        actions = [(C, D), (D, D), (D, D), (D, D)]
        self.versus_test(axelrod.Defector(), expected_actions=actions)

        # This behaviour is independent of knowledge of the Match length
        actions = [(C, C), (C, D), (D, C), (C, D)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions,
                         match_attributes={"length": -1})

        # We can also test against random strategies
        actions = [(C, D), (D, D), (D, C), (C, C)]
        self.versus_test(axelrod.Random(), expected_actions=actions,
                         seed=0)

        actions = [(C, C), (C, D), (D, D), (D, C)]
        self.versus_test(axelrod.Random(), expected_actions=actions,
                         seed=1)

        #  If you would like to test against a sequence of moves you should use
        #  a MockPlayer
        opponent = axelrod.MockPlayer(actions=[C, D])
        actions = [(C, C), (C, D), (D, C), (C, D)]
        self.versus_test(opponent, expected_actions=actions)

        opponent = axelrod.MockPlayer(actions=[C, C, D, D, C, D])
        actions = [(C, C), (C, C), (C, D), (D, D), (D, C), (C, D)]
        self.versus_test(opponent, expected_actions=actions)
