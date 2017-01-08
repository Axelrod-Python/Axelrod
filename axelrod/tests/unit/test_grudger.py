"""Tests for grudger strategies."""

from random import randint
import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestGrudger(TestPlayer):

    name = "Grudger"
    player = axelrod.Grudger
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
        # If opponent defects at any point then the player will defect forever
        self.responses_test(C, C + D * 3, C * 4)
        self.responses_test(D, C * 2 + D * 3, C + D + C * 3)


class TestForgetfulGrudger(TestPlayer):

    name = "Forgetful Grudger"
    player = axelrod.ForgetfulGrudger
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
        self.responses_test(C, attrs={"grudged": False})
        self.responses_test(C, C, C, attrs={"grudged": False})
        self.responses_test(D, C, D, attrs={"grudged": True})
        for i in range(10):
            self.responses_test(D, C + C + D * i, C + D + C * i,
                                attrs={"grudged": True, "grudge_memory": i,
                                       "mem_length": 10})
        # Forgets the grudge eventually
        i = 10
        self.responses_test(C, C + C + D * i + C, C + D + C * i + C,
                            attrs={"grudged": False, "grudge_memory": 0,
                                   "mem_length": 10})

    def test_reset_method(self):
        """Tests the reset method."""
        P1 = axelrod.ForgetfulGrudger()
        P1.grudged = True
        P1.grudge_memory = 4
        P1.reset()
        self.assertEqual(P1.grudged, False)
        self.assertEqual(P1.grudge_memory, 0)


class TestOppositeGrudger(TestPlayer):

    name = 'Opposite Grudger'
    player = axelrod.OppositeGrudger
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
        self.responses_test(D, C + D * 3, D * 4)
        self.responses_test(C, C * 2 + D * 3, C + D + C * 3)


class TestAggravater(TestPlayer):

    name = "Aggravater"
    player = axelrod.Aggravater
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
        self.responses_test(C, C + D * 3, C * 4)
        self.responses_test(D, C * 2 + D * 3, C + D + C * 3)


class TestSoftGrudger(TestPlayer):

    name = "Soft Grudger"
    player = axelrod.SoftGrudger
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
        # Starts by cooperating
        self.first_play_test(C)
        # If opponent defects at any point then the player will respond with
        # D, D, D, D, C, C
        self.responses_test(C, C, C)
        expected = D + D + D + D + C + C
        for i in range(2, 10):
            h2 = C * (i - 1)
            h1 = C * (i - 1)
            self.responses_test(C, h1, h2)
            h2 = C * (i - 1) + D
            h1 = C * i
            self.responses_test(expected, h1, h2)
            self.responses_test(C, h1 + expected, h2 + C * 5 + C)
            self.responses_test(D, h1 + expected, h2 + C * 5 + D)

    def test_reset(self):
        p = axelrod.SoftGrudger()
        p.grudged = True
        p.grudge_memory = 5
        p.reset()
        self.assertFalse(p.grudged)
        self.assertEqual(p.grudge_memory, 0)


class TestGrudgerAlternator(TestPlayer):

    name = "GrudgerAlternator"
    player = axelrod.GrudgerAlternator
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
        # If opponent defects at any point then the player will alternate D C.
        for i in range(2, 10):
            self.responses_test(C, C * i, C * i)
            self.responses_test((D + C) * 5, C * i + C, C * i + D)

    def test_strategy_random_number_rounds(self):
        """Runs test_strategy for a random number of rounds."""
        # Hasn't defected yet
        for _ in range(20):
            i = randint(1, 30)
            j = randint(1, 30)
            self.responses_test(C * j, C * i, C * i)

        # Defected at least once
        for _ in range(20):
            i = randint(1, 30)
            j = randint(1, 30)
            opp_hist = C * i + D
            my_hist = C * (i + 1)
            expected_response = [D if (r % 2 == 0) else C for r in range(j)]
            self.responses_test(expected_response, my_hist, opp_hist)


class TestEasyGo(TestPlayer):

    name = "EasyGo"
    player = axelrod.EasyGo
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
        self.first_play_test(D)
        # If opponent defects at any point then the player will cooperate
        # forever.
        self.responses_test(D, C + D * 3, C * 4)
        self.responses_test(C, C * 2 + D * 3, C + D + C * 3)
