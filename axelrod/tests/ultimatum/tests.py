import random
import unittest

from axelrod.ultimatum import DoubleThresholdsPlayer, SimpleThresholdPlayer


class TestSimpleThresholdPlayer(unittest.TestCase):
    def test_consider(self):
        player = SimpleThresholdPlayer(0.6, 0.4)
        self.assertEqual(player.consider(0.39), False)
        self.assertEqual(player.consider(0.4), True)
        self.assertEqual(player.consider(0.41), True)

    def test_offer(self):
        player = SimpleThresholdPlayer(0.4, 0.6)
        self.assertEqual(player.offer(), 0.4)


class TestDoubleThresholdsPlayer(unittest.TestCase):
    def test_consider(self):
        player = DoubleThresholdsPlayer(0.4, 0.6, 0.4, 0.6)
        self.assertEqual(player.consider(0.39), False)
        self.assertEqual(player.consider(0.4), True)
        self.assertEqual(player.consider(0.41), True)
        self.assertEqual(player.consider(0.6), True)
        self.assertEqual(player.consider(0.61), False)

    def test_offer(self):
        a = random.random()
        b = random.uniform(a, 1)
        player = DoubleThresholdsPlayer(a, b, 0., 1.)
        for _ in range(10):
            offer = player.offer()
            self.assertTrue(a <= offer <= b)


class TestPlay(unittest.TestCase):
    def test_result(self):
        player = SimpleThresholdPlayer(0.6, 0.4)
        coplayer = SimpleThresholdPlayer(0.5, 0.5)
        result = player.play(coplayer)
        self.assertEqual(result[0].scores, (0.4, 0.6))
        result = coplayer.play(player)
        self.assertEqual(result[0].scores, (0.5, 0.5))
        player = SimpleThresholdPlayer(0.4, 0.6)
        result = player.play(coplayer)
        self.assertEqual(result[0].scores, (0.0, 0.0))
        result = coplayer.play(player)
        self.assertEqual(result[0].scores, (0.0, 0.0))


if __name__ == '__main__':
    unittest.main()
