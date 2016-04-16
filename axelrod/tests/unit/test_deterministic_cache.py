import unittest
import os
import sys
from axelrod import DeterministicCache, TitForTat, Defector, Random


class TestDeterministicCache(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_key = (TitForTat, Defector, 3)
        cls.test_value = [('C', 'D'), ('D', 'D'), ('D', 'D')]
        cls.test_save_file = 'test_cache_save.txt'
        cls.test_load_file = 'test_cache_load.txt'
        if sys.version_info[0] == 2:
            # Python 2.x
            cls.test_pickle = '\x80\x02}q\x00caxelrod.strategies.titfortat\nTitForTat\nq\x01caxelrod.strategies.defector\nDefector\nq\x02K\x03\x87q\x03]q\x04(U\x01Cq\x05U\x01Dq\x06\x86q\x07h\x06h\x06\x86q\x08h\x06h\x06\x86q\tes.'
        else:
            # Python 3.x
            cls.test_pickle = b'\x80\x03}q\x00caxelrod.strategies.titfortat\nTitForTat\nq\x01caxelrod.strategies.defector\nDefector\nq\x02K\x03\x87q\x03]q\x04(X\x01\x00\x00\x00Cq\x05X\x01\x00\x00\x00Dq\x06\x86q\x07h\x06h\x06\x86q\x08h\x06h\x06\x86q\tes.'
        with open(cls.test_load_file, 'wb') as f:
            f.write(cls.test_pickle)

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.test_save_file)
        os.remove(cls.test_load_file)

    def test_basic_init(self):
        cache = DeterministicCache()
        self.assertTrue(cache.mutable)

    def test_init_from_file(self):
        cache = DeterministicCache(file_name=self.test_load_file)
        self.assertEqual(cache[self.test_key], self.test_value)

    def test_setitem(self):
        cache = DeterministicCache()
        cache[self.test_key] = self.test_value
        self.assertEqual(cache[self.test_key], self.test_value)

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
        # Should return false if tuple is not a triplet
        self.assertFalse(cache._is_valid_key(('test', 'test')))
        # Should return false if contents of tuple are not axelrod Players
        # and an integer
        self.assertFalse(cache._is_valid_key(('test', 'test', 'test')))
        self.assertFalse(cache._is_valid_key((TitForTat, 'test', 2)))
        self.assertFalse(cache._is_valid_key(('test', TitForTat, 2)))
        # Should return false if either player class is stochastic
        self.assertFalse(cache._is_valid_key((Random, TitForTat, 2)))
        self.assertFalse(cache._is_valid_key((TitForTat, Random, 2)))

    def test_is_valid_value(self):
        cache = DeterministicCache()
        self.assertTrue(cache._is_valid_value(self.test_value))
        # Should return false if value is not a list
        self.assertFalse(cache._is_valid_value('test'))

    def test_save(self):
        cache = DeterministicCache()
        cache[self.test_key] = self.test_value
        cache.save(self.test_save_file)
        with open(self.test_save_file, 'rb') as f:
            text = f.read()
        self.assertEqual(text, self.test_pickle)

    def test_load(self):
        cache = DeterministicCache()
        cache.load(self.test_load_file)
        self.assertEqual(cache[self.test_key], self.test_value)
