"""Test for the punisher strategy."""

import random

import axelrod

from .test_player import TestPlayer

C, D = 'C', 'D'


def set_history(player, history):
    player.history = history
    player.cooperations = history.count(C)
    player.defections = history.count(D)

class TestPunisher(TestPlayer):

    name = "Punisher"
    player = axelrod.Punisher
    expected_behaviour = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic' : False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_init(self):
        """Tests for the __init__ method."""
        P1 = axelrod.Punisher()
        self.assertEqual(P1.history, [])
        self.assertEqual(P1.mem_length, 1)
        self.assertEqual(P1.grudged, False)
        self.assertEqual(P1.grudge_memory, 1)

    def test_strategy(self):
        """Starts by cooperating."""

        random.seed(4)

        P1 = axelrod.Punisher()
        P2 = axelrod.Player()
        history = [C, C, D, D, D, C]
        set_history(P2, history)

        self.assertEqual(P1.mem_length, 1)
        self.assertEqual(P1.grudged, False)

        # Starts by playing C
        self.assertEqual(P1.strategy(P2), C)
        self.assertEqual(P1.grudged, False)
        history.append(C)
        set_history(P2, history)

        self.assertEqual(P1.strategy(P2), C)
        self.assertEqual(P1.grudged, False)
        history.append(D)
        set_history(P2, history)

        self.assertEqual(P2.history, [C, C, D, D, D, C, C, D])
        self.assertEqual(P1.strategy(P2), D)
        self.assertEqual(P1.grudged, True)

        for turn in range(P1.mem_length-1):
            self.assertEqual(P1.mem_length, 10)
            self.assertEqual(P1.strategy(P2), D)
            # Doesn't matter what opponent plays now
            history.append(random.choice([C, D]))
            set_history(P2, history)
            self.assertEqual(P1.grudged, True)

        self.assertEqual(P1.strategy(P2), D)
        self.assertEqual(P1.grudged, True)
        history.append(C)
        set_history(P2, history)

        # Back to being not grudged
        self.assertEqual(P1.strategy(P2), C)
        self.assertEqual(P1.grudged, False)
        history.append(C)
        set_history(P2, history)

        self.assertEqual(P1.strategy(P2), C)
        self.assertEqual(P1.grudged, False)
        history.append(D)
        set_history(P2, history)

        # Now grudges again
        self.assertEqual(P1.strategy(P2), D)
        self.assertEqual(P1.mem_length, 8)
        self.assertEqual(P1.grudged, True)
        history.append(C)
        set_history(P2, history)

        for turn in range(P1.mem_length-1):
            self.assertEqual(P1.mem_length, 8)
            self.assertEqual(P1.strategy(P2), D)
            # Doesn't matter what opponent plays now
            history.append(random.choice([C, D]))
            set_history(P2, history)
            self.assertEqual(P1.grudged, True)

        self.assertEqual(P1.strategy(P2), D)
        self.assertEqual(P1.grudged, True)
        history.append(C)
        set_history(P2, history)

        # Back to being not grudged
        self.assertEqual(P1.strategy(P2), C)
        self.assertEqual(P1.grudged, False)

    def test_reset_method(self):
        """Tests the reset method."""
        P1 = axelrod.Punisher()
        P1.history = [C, D, D, D]
        P1.grudged = True
        P1.grudge_memory = 4
        P1.reset()
        self.assertEqual(P1.history, [])
        self.assertEqual(P1.grudged, False)
        self.assertEqual(P1.grudge_memory, 0)


class TestInversePunisher(TestPlayer):

    name = "Inverse Punisher"
    player = axelrod.InversePunisher
    expected_behaviour = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic' : False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_init(self):
        """Tests for the __init__ method."""
        P1 = axelrod.InversePunisher()
        self.assertEqual(P1.history, [])
        self.assertEqual(P1.mem_length, 1)
        self.assertEqual(P1.grudged, False)
        self.assertEqual(P1.grudge_memory, 1)

    def test_strategy(self):
        """Starts by cooperating."""

        random.seed(4)

        P1 = axelrod.InversePunisher()
        P2 = axelrod.Player()
        history = [C, C, D, D, D, C]
        set_history(P2, history)

        self.assertEqual(P1.mem_length, 1)
        self.assertEqual(P1.grudged, False)

        # Starts by playing C
        self.assertEqual(P1.strategy(P2), C)
        self.assertEqual(P1.grudged, False)
        history.append(C)
        set_history(P2, history)

        self.assertEqual(P1.strategy(P2), C)
        self.assertEqual(P1.grudged, False)
        history.append(D)
        set_history(P2, history)

        self.assertEqual(P2.history, [C, C, D, D, D, C, C, D])
        self.assertEqual(P1.strategy(P2), D)
        self.assertEqual(P1.grudged, True)

        for turn in range(P1.mem_length - 1):
            self.assertEqual(P1.mem_length, 10)
            self.assertEqual(P1.strategy(P2), D)
            # Doesn't matter what opponent plays now
            history.append(random.choice([C, D]))
            set_history(P2, history)
            self.assertEqual(P1.grudged, True)

        self.assertEqual(P1.strategy(P2), D)
        self.assertEqual(P1.grudged, True)
        history.append(C)
        set_history(P2, history)

        # Back to being not grudged
        self.assertEqual(P1.strategy(P2), C)
        self.assertEqual(P1.grudged, False)
        history.append(C)
        set_history(P2, history)

        self.assertEqual(P1.strategy(P2), C)
        self.assertEqual(P1.grudged, False)
        history.append(D)
        set_history(P2, history)

        # Now grudges again
        self.assertEqual(P1.strategy(P2), D)
        self.assertEqual(P1.mem_length, 12)
        self.assertEqual(P1.grudged, True)
        history.append(C)
        set_history(P2, history)

        for turn in range(P1.mem_length-1):
            self.assertEqual(P1.mem_length, 12)
            self.assertEqual(P1.strategy(P2), D)
            # Doesn't matter what opponent plays now
            history.append(random.choice([C, D]))
            set_history(P2, history)
            self.assertEqual(P1.grudged, True)

        self.assertEqual(P1.strategy(P2), D)
        self.assertEqual(P1.grudged, True)
        history.append(C)
        set_history(P2, history)

        # Back to being not grudged
        self.assertEqual(P1.strategy(P2), C)
        self.assertEqual(P1.grudged, False)
        history.append(C)
        set_history(P2, history)

    def test_reset_method(self):
        """
        tests the reset method
        """
        P1 = axelrod.InversePunisher()
        P1.history = [C, D, D, D]
        P1.grudged = True
        P1.grudge_memory = 4
        P1.reset()
        self.assertEqual(P1.history, [])
        self.assertEqual(P1.grudged, False)
        self.assertEqual(P1.grudge_memory, 0)
