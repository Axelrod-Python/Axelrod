"""Tests for Finite State Machine Strategies."""
import unittest

import axelrod
from .test_player import TestHeadsUp, TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestFSMPlayer(unittest.TestCase):
    """Test a few sample tables to make sure that the finite state machines are
    working as intended."""

    def test_cooperator(self):
        """Tests that the player defined by the table for Cooperator is in fact
        Cooperator."""
        transitions = [(1, C, 1, C), (1, D, 1, C)]
        player = axelrod.FSMPlayer(transitions, initial_state=1, initial_action=C)
        opponent = axelrod.Alternator()
        for i in range(6):
            player.play(opponent)
        self.assertEqual(opponent.history, [C, D] * 3)
        self.assertEqual(player.history, [C] * 6)

    def test_defector(self):
        """Tests that the player defined by the table for Defector is in fact
        Defector."""
        transitions = [(1, C, 1, D), (1, D, 1, D)]
        player = axelrod.FSMPlayer(transitions, initial_state=1, initial_action=D)
        opponent = axelrod.Alternator()
        for i in range(6):
            player.play(opponent)
        self.assertEqual(opponent.history, [C, D] * 3)
        self.assertEqual(player.history, [D] * 6)

    def test_tft(self):
        """Tests that the player defined by the table for TFT is in fact
        TFT."""
        transitions = [(1, C, 1, C), (1, D, 1, D)]
        player = axelrod.FSMPlayer(transitions, initial_state=1, initial_action=C)
        opponent = axelrod.Alternator()
        for i in range(6):
            player.play(opponent)
        self.assertEqual(opponent.history, [C, D] * 3)
        self.assertEqual(player.history, [C, C, D, C, D, C])

    def test_wsls(self):
        """Tests that the player defined by the table for TFT is in fact
        WSLS (also known as Pavlov."""
        transitions = [(1, C, 1, C), (1, D, 2, D), (2, C, 2, D), (2, D, 1, C)]
        player = axelrod.FSMPlayer(transitions, initial_state=1, initial_action=C)
        opponent = axelrod.Alternator()
        for i in range(6):
            player.play(opponent)
        self.assertEqual(opponent.history, [C, D] * 3)
        self.assertEqual(player.history, [C, C, D, D, C, C])


class TestFortress3(TestPlayer):

    name = "Fortress3"
    player = axelrod.Fortress3
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Test initial play sequence
        self.first_play_test(D)


class TestFortress4(TestPlayer):

    name = "Fortress4"
    player = axelrod.Fortress4
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Test initial play sequence
        self.first_play_test(D)


class TestPredator(TestPlayer):

    name = "Predator"
    player = axelrod.Predator
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Test initial play sequence
        self.first_play_test(C)


class TestRaider(TestPlayer):

    name = "Raider"
    player = axelrod.Raider
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Test initial play sequence
        self.first_play_test(D)


class TestRipoff(TestPlayer):

    name = "Ripoff"
    player = axelrod.Ripoff
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Test initial play sequence
        self.first_play_test(D)


class TestSolutionB1(TestPlayer):

    name = "SolutionB1"
    player = axelrod.SolutionB1
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Test initial play sequence
        self.first_play_test(D)


class TestSolutionB5(TestPlayer):

    name = "SolutionB5"
    player = axelrod.SolutionB5
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Test initial play sequence
        self.first_play_test(D)


class TestThumper(TestPlayer):

    name = "Thumper"
    player = axelrod.Thumper
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Test initial play sequence
        self.first_play_test(C)


class TestFortress3vsFortress3(TestHeadsUp):
    """Test TFT vs WSLS"""
    def test_rounds(self):
        self.versus_test(axelrod.Fortress3(), axelrod.Fortress3(),
                         [D, D, C, C, C], [D, D, C, C, C])

class TestFortress3vsFortress3(TestHeadsUp):
    """Test TFT vs WSLS"""
    def test_rounds(self):
        self.versus_test(axelrod.Fortress3(), axelrod.TitForTat(),
                         [D, D, D, C], [C, D, D, D])
