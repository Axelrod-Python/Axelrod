"""Tests for the Grumpy strategy."""

import axelrod as axl
from .test_player import TestPlayer

C, D = axl.Actions.C, axl.Actions.D


class TestGrumpy(TestPlayer):

    name = "Grumpy: Nice, 10, -10"
    player = axl.Grumpy
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_default_strategy(self):
        vs_cooperator = [(C, C)] * 30
        vs_alternator = [(C, C), (C, D)] * 30
        vs_defector = [(C, D)] * 11 + [(D, D)] * 20
        self.versus_test(axl.Cooperator(), vs_cooperator)
        self.versus_test(axl.Alternator(), vs_alternator)
        self.versus_test(axl.Defector(), vs_defector)

        opponent = [D] * 11 + [C] * 22 + [D] * 11
        expected = [(C, D)] * 11 + [(D, C)] * 22 + [(C, D)] * 11
        self.versus_test(axl.MockPlayer(actions=opponent),
                         expected_actions=expected * 3)

    def test_starting_state(self):
        opponent = [D] * 11 + [C] * 22 + [D] * 11
        grumpy_start = [(D, D)] * 11 + [(D, C)] * 22 + [(C, D)] * 11
        expected = [(C, D)] * 11 + [(D, C)] * 22 + [(C, D)] * 11
        self.versus_test(axl.MockPlayer(actions=opponent),
                         expected_actions=grumpy_start + expected * 3,
                         init_kwargs={'starting_state': 'Grumpy'})

        self.versus_test(axl.MockPlayer(actions=opponent),
                         expected_actions=expected * 3,
                         init_kwargs={'starting_state': 'Nice'})

    def test_thresholds(self):
        init_kwargs = {'grumpy_threshold': 3, 'nice_threshold': -2}
        opponent, expected = get_actions(3, -2)
        self.versus_test(axl.MockPlayer(actions=opponent),
                         expected_actions=expected,
                         init_kwargs=init_kwargs)

        init_kwargs = {'grumpy_threshold': 0, 'nice_threshold': -2}
        opponent, expected = get_actions(0, -2)
        self.versus_test(axl.MockPlayer(actions=opponent),
                         expected_actions=expected,
                         init_kwargs=init_kwargs)

        init_kwargs = {'grumpy_threshold': 3, 'nice_threshold': 0}
        opponent, expected = get_actions(3, 0)
        self.versus_test(axl.MockPlayer(actions=opponent),
                         expected_actions=expected,
                         init_kwargs=init_kwargs)

    def test_reset_state_with_non_default_init(self):
        player = axl.Grumpy(starting_state='Grumpy')
        player.state = 'Nice'
        player.reset()
        self.assertEqual(player.state, 'Grumpy')

    def test_get_actions(self):
        opponent, expected = get_actions(2, -3)
        self.assertEqual(opponent, [D] * 3 + [C] * 7 + [D] * 4)
        base_expected = [(C, D)] * 3 + [(D, C)] * 7 + [(C, D)] * 4
        self.assertEqual(expected, base_expected * 3)

        opponent, expected = get_actions(2, 0)
        self.assertEqual(opponent, [D] * 3 + [C] * 4 + [D])
        base_expected = [(C, D)] * 3 + [(D, C)] * 4 + [(C, D)]
        self.assertEqual(expected, base_expected * 3)

        opponent, expected = get_actions(0, -3)
        self.assertEqual(opponent, [D] + [C] * 5 + [D] * 4)
        base_expected = [(C, D)] + [(D, C)] * 5 + [(C, D)] * 4
        self.assertEqual(expected, base_expected * 3)


def get_actions(grumpy_threshold, nice_threshold):
    becomes_grumpy = [D] * (grumpy_threshold + 1)
    becomes_zero = [C] * len(becomes_grumpy)
    becomes_nice = [C] * (abs(nice_threshold) + 1)
    return_to_zero = [D] * len(becomes_nice)

    opponent = becomes_grumpy + becomes_zero + becomes_nice + return_to_zero
    expected_actions = (
        [(C, D)] * len(becomes_grumpy) +
        [(D, C)] * (len(becomes_zero) + len(becomes_nice)) +
        [(C, D)] * len(return_to_zero)
        ) * 3
    return opponent, expected_actions
