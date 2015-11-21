"""Test APavlov."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestAPavlov2006(TestPlayer):
    name = "Adapative Pavlov 2006"
    player = axelrod.APavlov2006

    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)
        self.responses_test([C] * 6, [C] * 6, [C],
                            attrs={"opponent_class": "Cooperative"})
        self.responses_test([C, D, D, D, D, D], [D] * 6, [D],
                            attrs={"opponent_class": "ALLD"})
        self.responses_test([C, D, C, D, C, D], [D, C, D, C, D, C], [C, C],
                            attrs={"opponent_class": "STFT"})
        self.responses_test([C, D, D, C, D, D], [D, D, C, D, D, C], [D],
                            attrs={"opponent_class": "PavlovD"})
        self.responses_test([C, D, D, C, D, D, C], [D, D, C, D, D, C, D], [C],
                            attrs={"opponent_class": "PavlovD"})
        self.responses_test([C, D, D, C, D, D], [C, C, C, D, D, D], [D],
                            attrs={"opponent_class": "Random"})
        self.responses_test([C, D, D, D, C, C], [D, D, D, C, C, C], [D],
                            attrs={"opponent_class": "Random"})

    def test_reset(self):
        player = self.player()
        opponent = axelrod.Cooperator()
        [player.play(opponent) for _ in range(10)]
        player.reset()
        self.assertEqual(player.opponent_class, None)

class TestAPavlov2011(TestPlayer):
    name = "Adapative Pavlov 2011"
    player = axelrod.APavlov2011

    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)
        self.responses_test([C] * 6, [C] * 6, [C],
                            attrs={"opponent_class": "Cooperative"})
        self.responses_test([C, D, D, D, D, D], [D] * 6, [D],
                            attrs={"opponent_class": "ALLD"})
        self.responses_test([C, C, D, D, D, D], [C] + [D] * 5, [D],
                            attrs={"opponent_class": "ALLD"})
        self.responses_test([C, C, C, D, D, D], [C, C] + [D] * 4, [D],
                            attrs={"opponent_class": "ALLD"})
        self.responses_test([C, C, D, D, C, D], [C, D, D, C, D, D], [D],
                            attrs={"opponent_class": "ALLD"})

        self.responses_test([C, C, D, D, D, C], [C, D, D, C, C, D], [C],
                            attrs={"opponent_class": "STFT"})
        self.responses_test([C, C, D, C, D, C], [C, D, C, D, C, D], [C],
                            attrs={"opponent_class": "STFT"})
        self.responses_test([C, D, D, D, C, C], [D, D, D, C, C, C], [C],
                            attrs={"opponent_class": "STFT"})

        self.responses_test([C, C, C, C, C, D], [C, C, C, C, D, D], [D],
                            attrs={"opponent_class": "Random"})
        self.responses_test([C, D, D, C, C, C], [D, D, C, C, C, C], [D],
                            attrs={"opponent_class": "Random"})

    def test_reset(self):
        player = self.player()
        opponent = axelrod.Cooperator()
        [player.play(opponent) for _ in range(10)]
        player.reset()
        self.assertEqual(player.opponent_class, None)
