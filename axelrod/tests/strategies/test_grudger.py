"""Tests for Grudger strategies."""

from random import randint
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
        # Starts by cooperating
        self.first_play_test(C)
        # If opponent defects at any point then the player will defect forever.
        self.versus_test(axl.Cooperator(), expected_actions=[(C, C)] * 20)
        self.versus_test(axl.TitForTat(), expected_actions=[(C, C)] * 20)
        self.versus_test(axl.Defector(),
                         expected_actions=[(C, D)] + [(D, D)] * 20)

        opponent = [C] * 10 + [D]
        expected = [(C, C)] * 10 + [(C, D)] + list(zip([D] * 11, opponent)) * 10
        self.versus_test(axl.MockPlayer(actions=opponent),
                         expected_actions=expected)


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
        self.first_play_test(C)
        self.versus_test(axl.Cooperator(), expected_actions=[(C, C)] * 20)
        vs_defector = [(C, D)] + [(D, D)] * 30
        # grudges for 10 rounds and then starts a new grudge every 10 rounds
        self.versus_test(axl.Defector(), expected_actions=vs_defector)
        vs_alternator = [(C, C), (C, D)] + [(D, C), (D, D)] * 15
        self.versus_test(axl.Alternator(), expected_actions=vs_alternator)

        opponent = [C] * 2 + [D] + [C] * 10
        expected = ([(C, C)] * 2 + [(C, D)] + [(D, C)] * 10) * 3
        self.versus_test(axl.MockPlayer(actions=opponent),
                         expected_actions=expected)

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
        # Starts by defecting.
        self.first_play_test(D)
        # If opponent cooperates at any point then the player will cooperate
        # forever.
        vs_cooperator = [(D, C)] + [(C, C)] * 20
        self.versus_test(axl.Cooperator(), expected_actions=vs_cooperator)
        vs_defector = [(D, D)] * 20
        self.versus_test(axl.Defector(), expected_actions=vs_defector)
        vs_alternator = [(D, C)] + [(C, D), (C, C)] * 20
        self.versus_test(axl.Alternator(), expected_actions=vs_alternator)

        opponent = [C] + [D] * 30
        expected = [(D, C)] + [(C, D)] * 30
        self.versus_test(axl.MockPlayer(opponent),
                         expected_actions=expected)


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
        # Starts by defecting
        self.first_play_test(D)
        # If opponent defects at any point then the player will defect forever.
        # Always defects on first three turns.
        vs_cooperator = [(D, C)] * 3 + [(C, C)] * 20
        self.versus_test(axl.Cooperator(), expected_actions=vs_cooperator)
        vs_defector = [(D, D)] * 20
        self.versus_test(axl.Defector(), expected_actions=vs_defector)
        vs_alternator = [(D, C), (D, D)] * 20
        self.versus_test(axl.Alternator(), expected_actions=vs_alternator)

        opponent = [C] * 10 + [D] + [C] * 20
        expected = [(D, C)] * 3 + [(C, C)] * 7 + [(C, D)] + [(D, C)] * 20
        self.versus_test(axl.MockPlayer(opponent),
                         expected_actions=expected)


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
        self.maxDiff = None
        # Starts by cooperating.
        self.first_play_test(C)
        # If opponent defects at any point then the player will respond with
        # D, D, D, D, C, C.
        vs_cooperator = [(C, C)] * 30
        self.versus_test(axl.Cooperator(), expected_actions=vs_cooperator)
        vs_defector = [(C, D)] + ([(D, D)] * 4 + [(C, D)] * 2) * 5
        self.versus_test(axl.Defector(), expected_actions=vs_defector)
        vs_alternator = ([(C, C), (C, D)] +
                         ([(D, C), (D, D)] * 2 + [(C, C), (C, D)]) * 10)
        self.versus_test(axl.Alternator(), expected_actions=vs_alternator)

        opponent = [D] * 6 + [C]
        expected = ([(C, D)] + [(D, D)] * 4 + [(C, D), (C, C)]) * 5
        self.versus_test(axl.MockPlayer(opponent),
                         expected_actions=expected)

    def test_reset(self):
        p = axl.SoftGrudger()
        p.grudged = True
        p.grudge_memory = 5
        p.reset()
        self.assertFalse(p.grudged)
        self.assertEqual(p.grudge_memory, 0)


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
        # Starts by cooperating.
        self.first_play_test(C)
        # If opponent defects at any point then the player will alternate D C.
        vs_cooperator = [(C, C)] * 30
        self.versus_test(axl.Cooperator(), expected_actions=vs_cooperator)
        vs_defector = [(C, D)] + [(D, D), (C, D)] * 20
        self.versus_test(axl.Defector(), expected_actions=vs_defector)
        vs_alternator = [(C, C), (C, D)] + [(D, C), (C, D)] * 20
        self.versus_test(axl.Alternator(), expected_actions=vs_alternator)

        opponent = [C] * 10 + [D] + [C] * 20
        expected = [(C, C)] * 10 + [(C, D)] + [(D, C), (C, C)] * 10
        self.versus_test(axl.MockPlayer(opponent),
                         expected_actions=expected)


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
        # Starts by defecting.
        self.first_play_test(D)
        # If opponent defects at any point then the player will cooperate
        # forever.
        vs_cooperator = [(D, C)] * 30
        self.versus_test(axl.Cooperator(), expected_actions=vs_cooperator)
        vs_defector = [(D, D)] + [(C, D)] * 20
        self.versus_test(axl.Defector(), expected_actions=vs_defector)
        vs_alternator = [(D, C), (D, D)] + [(C, C), (C, D)] * 20
        self.versus_test(axl.Alternator(), expected_actions=vs_alternator)

        opponent = [C] * 10 + [D] + [C] * 20
        expected = [(D, C)] * 10 + [(D, D)] + [(C, C)] * 20
        self.versus_test(axl.MockPlayer(opponent),
                         expected_actions=expected)


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
        init_kwargs = {'n': 3}
        response = [D, D, D, D, C, C]

        vs_defector = [(C, D)] * 3 + (list(zip(response, [D] * 6))) * 3
        self.versus_test(axl.Defector(), expected_actions=vs_defector,
                         init_kwargs=init_kwargs)
        vs_alternator = [(C, C), (C, D)] * 20
        self.versus_test(axl.Alternator(), expected_actions=vs_alternator,
                         init_kwargs=init_kwargs)

        opponent = [D] * 8 + [C] + [D] * 2 + [C]
        expected = ([(C, D)] * 3 + [(D, D)] * 4 + [(C, D), (C, C)] +
                    [(C, D)] * 2 + [(C, C)]) * 5
        self.versus_test(axl.MockPlayer(actions=opponent),
                         expected_actions=expected,
                         init_kwargs=init_kwargs)

    def test_set_d_and_c(self):
        init_kwargs = {'d': 3, 'c': 3}
        response = [D, D, D, C, C, C]

        vs_defector = [(C, D)] + (list(zip(response, [D] * 6))) * 3
        self.versus_test(axl.Defector(), expected_actions=vs_defector,
                         init_kwargs=init_kwargs)
        vs_alternator = [(C, C), (C, D)] + (list(zip(response, [C, D] * 3))) * 5
        self.versus_test(axl.Alternator(), expected_actions=vs_alternator,
                         init_kwargs=init_kwargs)
        opponent = [C] * 10 + [D] * 6 + [C] * 20
        expected = ([(C, C)] * 10 + [(C, D)] +
                    list(zip(response, [D] * 5 + [C])) + [(C, C)] * 19)
        self.versus_test(axl.MockPlayer(actions=opponent),
                         expected_actions=expected,
                         init_kwargs=init_kwargs)
