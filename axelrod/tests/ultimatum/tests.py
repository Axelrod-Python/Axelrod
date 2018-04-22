import unittest

from axelrod.ultimatum import DoubleThresholdPlayer, SimpleThresholdPlayer


class TestSimpleThresholdPlayer(unittest.TestCase):
    def test_offer(self):
        player = SimpleThresholdPlayer(0.4, 0.6)
        self.assertEqual(player.offer(), 0.4)

    def test_consider(self):
        player = SimpleThresholdPlayer(0.6, 0.4)
        self.assertEqual(player.consider(0.39), False)
        self.assertEqual(player.consider(0.4), True)
        self.assertEqual(player.consider(0.41), True)


class TestDoubleThresholdPlayer(unittest.TestCase):
    def test_offer(self):
        player = DoubleThresholdPlayer(0.4, 0.4, 0.6)
        self.assertEqual(player.offer(), 0.4)

    def test_consider(self):
        player = DoubleThresholdPlayer(0.6, 0.4, 0.6)
        self.assertEqual(player.consider(0.39), False)
        self.assertEqual(player.consider(0.4), True)
        self.assertEqual(player.consider(0.41), True)
        self.assertEqual(player.consider(0.6), True)
        self.assertEqual(player.consider(0.61), False)


class TestPlay(unittest.TestCase):
    def test_result(self):
        player = SimpleThresholdPlayer(0.6, 0.4)
        coplayer = SimpleThresholdPlayer(0.5, 0.5)
        result = player.play(coplayer)
        self.assertEqual(result, (0.4, 0.6))
        result = coplayer.play(player)
        self.assertEqual(result, (0.5, 0.5))
        player = SimpleThresholdPlayer(0.4, 0.6)
        result = player.play(coplayer)
        self.assertEqual(result, (0.0, 0.0))
        result = coplayer.play(player)
        self.assertEqual(result, (0.0, 0.0))


if __name__ == '__main__':
    unittest.main()
