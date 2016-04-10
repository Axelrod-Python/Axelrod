import unittest
from axelrod import DeterministicCache, TitForTat, Defector


class TestDeterministicCache(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_key1 = (TitForTat, Defector)
        cls.test_value1 = [('C', 'D'), ('D', 'D'), ('D', 'D')]

    def test_basic_init(self):
        cache = DeterministicCache()
        self.assertTrue(cache.mutable)
        self.assertEqual(cache.turns, None)

    def test_init_from_file(self):
        pass

    def test_setitem(self):
        cache = DeterministicCache()
        cache[self.test_key1] = self.test_value1
        self.assertEqual(cache[self.test_key1], self.test_value1)

    def test_set_immutable_cache(self):
        cache = DeterministicCache()
        cache.mutable = False
        with self.assertRaises(ValueError):
            cache[self.test_key1] = self.test_value1

    def test_is_valid_key(self):
        cache = DeterministicCache()
        self.assertTrue(cache._is_valid_key(self.test_key1))
        # Should return false if key is not a tuple
        self.assertFalse(cache._is_valid_key('test'))
        # Should return false if tuple is not a pair
        self.assertFalse(cache._is_valid_key(('test', 'test', 'test')))
        # Should return false if contents of tuple are not axelrod Players
        self.assertFalse(cache._is_valid_key(('test', 'test')))

    def test_is_valid_value(self):
        cache = DeterministicCache()
        self.assertTrue(cache._is_valid_value(self.test_value1))
        # Should return false if value is not a list
        self.assertFalse(cache._is_valid_value('test'))
        # Should return false if length does not match turns attribute
        cache.turns = 20
        self.assertFalse(cache._is_valid_value(self.test_value1))

    def test_save(self):
        pass

    def test_load(self):
        pass
