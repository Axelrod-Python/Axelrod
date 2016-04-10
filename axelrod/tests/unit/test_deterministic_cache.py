import unittest
import os
from axelrod import DeterministicCache, TitForTat, Defector


class TestDeterministicCache(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_key = (TitForTat, Defector)
        cls.test_value = [('C', 'D'), ('D', 'D'), ('D', 'D')]
        cls.test_save_file = 'test_cache_save.txt'
        cls.test_load_file = 'test_cache_load.txt'
        cls.test_pickle = b'\x80\x03}q\x00caxelrod.strategies.titfortat\nTitForTat\nq\x01caxelrod.strategies.defector\nDefector\nq\x02\x86q\x03]q\x04(X\x01\x00\x00\x00Cq\x05X\x01\x00\x00\x00Dq\x06\x86q\x07h\x06h\x06\x86q\x08h\x06h\x06\x86q\tes.'

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.test_save_file)
        os.remove(cls.test_load_file)

    def test_basic_init(self):
        cache = DeterministicCache()
        self.assertTrue(cache.mutable)
        self.assertEqual(cache.turns, None)

    def test_init_from_file(self):
        pass

    def test_setitem(self):
        cache = DeterministicCache()
        cache[self.test_key] = self.test_value
        self.assertEqual(cache[self.test_key], self.test_value)
        # The first cached entry should set the turns attribute
        self.assertEqual(cache.turns, 3)

    def test_set_immutable_cache(self):
        cache = DeterministicCache()
        cache.mutable = False
        with self.assertRaises(ValueError):
            cache[self.test_key] = self.test_value

    def test_is_valid_key(self):
        cache = DeterministicCache()
        self.assertTrue(cache._is_valid_key(self.test_key))
        # Should return false if key is not a tuple
        self.assertFalse(cache._is_valid_key('test'))
        # Should return false if tuple is not a pair
        self.assertFalse(cache._is_valid_key(('test', 'test', 'test')))
        # Should return false if contents of tuple are not axelrod Players
        self.assertFalse(cache._is_valid_key(('test', 'test')))
        self.assertFalse(cache._is_valid_key((TitForTat, 'test')))
        self.assertFalse(cache._is_valid_key(('test', TitForTat)))

    def test_is_valid_value(self):
        cache = DeterministicCache()
        self.assertTrue(cache._is_valid_value(self.test_value))
        # Should return false if value is not a list
        self.assertFalse(cache._is_valid_value('test'))
        # Should return false if length does not match turns attribute
        cache.turns = 20
        self.assertFalse(cache._is_valid_value(self.test_value))

    def test_save(self):
        cache = DeterministicCache()
        cache[self.test_key] = self.test_value
        cache.save(self.test_save_file)
        with open(self.test_save_file, 'rb') as f:
            text = f.read()
        self.assertEqual(text, self.test_pickle)

    def test_load(self):
        with open(self.test_load_file, 'wb') as f:
            f.write(self.test_pickle)
        cache = DeterministicCache()
        cache.load(self.test_load_file)
        self.assertEqual(cache[self.test_key], self.test_value)
        self.assertEqual(cache.turns, 3)


