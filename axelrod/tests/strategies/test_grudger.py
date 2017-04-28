"""Tests for Grudger strategies."""

import axelrod as axl
from .test_player import TestPlayer

C, D = axl.Actions.C, axl.Actions.D


class TestGrudger(TestPlayer):

    name = "Grudger"
    player = axl.Grudger
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # If opponent defects at any point then the player will defect forever.
        opponent = axl.Cooperator()
        actions = [(C, C)] * 20
        self.versus_test(opponent, expected_actions=actions)

        opponent = axl.Defector()
        actions = [(C, D)] + [(D, D)] * 20
        self.versus_test(opponent, expected_actions=actions)

        opponent_actions = [C] * 10 + [D] + [C] * 20
        opponent = axl.MockPlayer(actions=opponent_actions)
        actions = [(C, C)] * 10 + [(C, D)] + [(D, C)] * 20
        self.versus_test(opponent, expected_actions=actions)


class TestForgetfulGrudger(TestPlayer):

    name = "Forgetful Grudger"
    player = axl.ForgetfulGrudger
    expected_classifier = {
        'memory_depth': 10,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # If opponent defects at any point then the player will respond with
        # D ten times and then continue to check for defections.
        opponent = axl.Cooperator()
        actions = [(C, C)] * 20
        self.versus_test(opponent, expected_actions=actions)

        opponent = axl.Defector()
        actions = [(C, D)] + [(D, D)] * 20
        self.versus_test(opponent, expected_actions=actions)

        opponent_actions = [C] * 2 + [D] + [C] * 10
        opponent = axl.MockPlayer(actions=opponent_actions)
        expected = ([(C, C)] * 2 + [(C, D)] + [(D, C)] * 10) * 3
        self.versus_test(opponent, expected_actions=expected)

    def test_reset_method(self):
        """Tests the reset method."""
        player = axl.ForgetfulGrudger()
        player.history = [C, D, D, D]
        player.grudged = True
        player.grudge_memory = 4
        player.reset()
        self.assertEqual(player.grudged, False)
        self.assertEqual(player.grudge_memory, 0)


class TestOppositeGrudger(TestPlayer):

    name = 'Opposite Grudger'
    player = axl.OppositeGrudger
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # If opponent cooperates at any point then the player will cooperate
        # forever.
        opponent = axl.Cooperator()
        actions = [(D, C)] + [(C, C)] * 20
        self.versus_test(opponent, expected_actions=actions)

        opponent = axl.Defector()
        actions = [(D, D)] * 20
        self.versus_test(opponent, expected_actions=actions)

        opponent_actions = [C] + [D] * 30
        opponent = axl.MockPlayer(actions=opponent_actions)
        expected = [(D, C)] + [(C, D)] * 30
        self.versus_test(opponent, expected_actions=expected)


class TestAggravater(TestPlayer):

    name = "Aggravater"
    player = axl.Aggravater
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # If opponent defects at any point then the player will defect forever.
        # Always defects on first three turns.
        opponent = axl.Cooperator()
        actions = [(D, C)] * 3 + [(C, C)] * 20
        self.versus_test(opponent, expected_actions=actions)

        opponent = axl.Defector()
        actions = [(D, D)] * 20
        self.versus_test(opponent, expected_actions=actions)

        opponent_actions = [C] * 10 + [D] + [C] * 20
        opponent = axl.MockPlayer(actions=opponent_actions)
        actions = [(D, C)] * 3 + [(C, C)] * 7 + [(C, D)] + [(D, C)] * 20
        self.versus_test(opponent, expected_actions=actions)


class TestSoftGrudger(TestPlayer):

    name = "Soft Grudger"
    player = axl.SoftGrudger
    expected_classifier = {
        'memory_depth': 6,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # If opponent defects at any point then the player will respond with
        # D, D, D, D, C, C and then continue to check for defections.
        grudge_response_d = [(D, D)] * 4 + [(C, D)] * 2
        grudge_response_c = [(D, C)] * 4 + [(C, C)] * 2

        opponent = axl.Cooperator()
        actions = [(C, C)] * 20
        self.versus_test(opponent, expected_actions=actions)

        opponent = axl.Defector()
        actions = [(C, D)] + grudge_response_d * 5
        self.versus_test(opponent, expected_actions=actions)

        opponent_actions = [C] * 10 + [D]
        opponent = axl.MockPlayer(actions=opponent_actions)
        actions_start = [(C, C)] * 10 + [(C, D)]
        subsequent = grudge_response_c + [(C, C)] * 4 + [(C, D)]
        actions = actions_start + subsequent * 5
        self.versus_test(opponent, expected_actions=actions)

    def test_reset(self):
        player = self.player()
        player.grudged = True
        player.grudge_memory = 5
        player.reset()
        self.assertFalse(player.grudged)
        self.assertEqual(player.grudge_memory, 0)


class TestGrudgerAlternator(TestPlayer):

    name = "GrudgerAlternator"
    player = axl.GrudgerAlternator
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # If opponent defects at any point then the player will alternate D C.
        opponent = axl.Cooperator()
        actions = [(C, C)] * 20
        self.versus_test(opponent, expected_actions=actions)

        opponent = axl.Defector()
        actions = [(C, D)] + [(D, D), (C, D)] * 20
        self.versus_test(opponent, expected_actions=actions)

        opponent_actions = [C] * 10 + [D] + [C] * 20
        opponent = axl.MockPlayer(actions=opponent_actions)
        actions = [(C, C)] * 10 + [(C, D)] + [(D, C), (C, C)] * 10
        self.versus_test(opponent, expected_actions=actions)


class TestEasyGo(TestPlayer):

    name = "EasyGo"
    player = axl.EasyGo
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # If opponent defects at any point then the player will cooperate
        # forever.
        opponent = axl.Cooperator()
        actions = [(D, C)] * 20
        self.versus_test(opponent, expected_actions=actions)

        opponent = axl.Defector()
        actions = [(D, D)] + [(C, D)] * 20
        self.versus_test(opponent, expected_actions=actions)

        opponent_actions = [C] * 10 + [D, C] * 20
        opponent = axl.MockPlayer(actions=opponent_actions)
        actions = [(D, C)] * 10 + [(D, D)] + [(C, C), (C, D)] * 19
        self.versus_test(opponent, expected_actions=actions)


class TestGeneralSoftGrudger(TestSoftGrudger):

    name = "General Soft Grudger: n=1,d=4,c=2"
    player = axl.GeneralSoftGrudger
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # the default follows SoftGrudger
        super(TestGeneralSoftGrudger, self).test_strategy()

    def test_set_n(self):
        # grudge response only activates if opponent's last 'n' plays were D
        init_kwargs = {'n': 3}
        grudge_response_d = [(D, D)] * 4 + [(C, D)] * 2
        grudge_response_c = [(D, C)] * 4 + [(C, C)] * 2

        opponent = axl.Defector()
        actions = [(C, D)] * 3 + grudge_response_d * 5
        self.versus_test(opponent, expected_actions=actions,
                         init_kwargs=init_kwargs)

        two_defections = [C, D, D]
        opponent = axl.MockPlayer(actions=two_defections)
        actions = [(C, C), (C, D), (C, D)] * 5
        self.versus_test(opponent, expected_actions=actions,
                         init_kwargs=init_kwargs)

        three_defections = [C] * 10 + [D, D, D]
        opponent = axl.MockPlayer(actions=three_defections)
        actions_start = [(C, C)] * 10 + [(C, D)] * 3
        subsequent = grudge_response_c + [(C, C)] * 4 + [(C, D)] * 3
        actions = actions_start + subsequent * 5
        self.versus_test(opponent, expected_actions=actions,
                         init_kwargs=init_kwargs)

    def test_set_d_and_c(self):
        # Sets the number of D's then C's in the grudge response.
        init_kwargs = {'d': 3, 'c': 3}
        grudge_response_d = [(D, D)] * 3 + [(C, D)] * 3
        grudge_response_c = [(D, C)] * 3 + [(C, C)] * 3

        opponent = axl.Defector()
        actions = [(C, D)] + grudge_response_d * 5
        self.versus_test(opponent, expected_actions=actions,
                         init_kwargs=init_kwargs)

        opponent_actions = [C] * 10 + [D]
        opponent = axl.MockPlayer(actions=opponent_actions)
        actions_start = [(C, C)] * 10 + [(C, D)]
        subsequent = grudge_response_c + [(C, C)] * 4 + [(C, D)]
        actions = actions_start + subsequent * 5
        self.versus_test(opponent, expected_actions=actions,
                         init_kwargs=init_kwargs)

    def test_edge_case_n_is_zero(self):
        # Always uses grudge response.
        init_kwargs = {'n': 0}
        grudge_response_d = [(D, D)] * 4 + [(C, D)] * 2
        grudge_response_c = [(D, C)] * 4 + [(C, C)] * 2

        opponent = axl.Defector()
        actions = grudge_response_d * 5
        self.versus_test(opponent, expected_actions=actions,
                         init_kwargs=init_kwargs)

        opponent = axl.Cooperator()
        actions = grudge_response_c * 5
        self.versus_test(opponent, expected_actions=actions,
                         init_kwargs=init_kwargs)

    def test_edge_case_d_is_zero(self):
        # Grudge response is only C, so acts like Cooperator.
        init_kwargs = {'d': 0}

        opponent = axl.Defector()
        actions = [(C, D)] * 5
        self.versus_test(opponent, expected_actions=actions,
                         init_kwargs=init_kwargs)

        opponent = axl.Alternator()
        actions = [(C, C), (C, D)] * 5
        self.versus_test(opponent, expected_actions=actions,
                         init_kwargs=init_kwargs)

    def test_edge_case_c_is_zero(self):
        # Grudge response is a set number of D's (defaults to 4)
        init_kwargs = {'c': 0}

        opponent = axl.Defector()
        actions = [(C, D)] + [(D, D)] * 10
        self.versus_test(opponent, expected_actions=actions,
                         init_kwargs=init_kwargs)

        opponent_actions = [C] * 10 + [D]
        opponent = axl.MockPlayer(actions=opponent_actions)
        actions_start = [(C, C)] * 10 + [(C, D)]
        subsequent = [(D, C)] * 4 + [(C, C)] * 6 + [(C, D)]
        actions = actions_start + subsequent * 5
        self.versus_test(opponent, expected_actions=actions,
                         init_kwargs=init_kwargs)

    def test_repr(self):
        default_player = self.player()
        self.assertEqual(repr(default_player),
                         "General Soft Grudger: n=1,d=4,c=2")

        set_params_player = self.player(n=2, d=3, c=4)
        self.assertEqual(repr(set_params_player),
                         "General Soft Grudger: n=2,d=3,c=4")
