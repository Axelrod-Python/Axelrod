import unittest
import axelrod as axl


class TestPlayerConfig(unittest.TestCase):

    def test_call(self):
        pc = axl.PlayerConfig("Cooperator")
        player = pc()
        print(player)
        self.assertTrue(issubclass(type(player), axl.Player))
        self.assertTrue(isinstance(player, axl.Cooperator))

