import os
import pickle
import unittest

from axelrod import Action, Defector, DeterministicCache, Random, TitForTat

C, D = Action.C, Action.D


class TestDeterministicCache(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_key = (TitForTat(), Defector(), 3)
        cls.test_value = [(C, D), (D, D), (D, D)]
        cls.test_save_file = "test_cache_save.txt"
        cls.test_load_file = "test_cache_load.txt"
        test_data_to_pickle = {("Tit For Tat", "Defector", 3): [(C, D), (D, D), (D, D)]}
        cls.test_pickle = pickle.dumps(test_data_to_pickle)

        with open(cls.test_load_file, "wb") as f:
            f.write(cls.test_pickle)

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.test_save_file)
        os.remove(cls.test_load_file)

    def setUp(self):
        self.cache = DeterministicCache()

    def test_basic_init(self):
        self.assertTrue(self.cache.mutable)

    def test_init_from_file(self):
        loaded_cache = DeterministicCache(file_name=self.test_load_file)
        self.assertEqual(loaded_cache[self.test_key], self.test_value)

    def test_setitem(self):
        self.cache[self.test_key] = self.test_value
        self.assertEqual(self.cache[self.test_key], self.test_value)

    def test_setitem_invalid_key_not_tuple(self):
        invalid_key = "test"
        with self.assertRaises(ValueError):
            self.cache[invalid_key] = self.test_value

    def test_setitem_invalid_key_too_short(self):
        invalid_key = self.test_key + (4,)
        with self.assertRaises(ValueError):
            self.cache[invalid_key] = self.test_value

    def test_setitem_invalid_key_too_long(self):
        invalid_key = self.test_key[:2]
        with self.assertRaises(ValueError):
            self.cache[invalid_key] = self.test_value

    def test_setitem_invalid_key_first_two_elements_not_player(self):
        invalid_key = ("test", "test", 2)
        with self.assertRaises(ValueError):
            self.cache[invalid_key] = self.test_value

        invalid_key = (TitForTat(), "test", 2)
        with self.assertRaises(ValueError):
            self.cache[invalid_key] = self.test_value

        invalid_key = ("test", TitForTat(), 2)
        with self.assertRaises(ValueError):
            self.cache[invalid_key] = self.test_value

    def test_setitem_invalid_key_last_element_not_integer(self):
        invalid_key = (TitForTat(), TitForTat(), TitForTat())
        with self.assertRaises(ValueError):
            self.cache[invalid_key] = self.test_value

    def test_setitem_invalid_key_stochastic_player(self):
        invalid_key = (Random(), TitForTat(), 2)
        with self.assertRaises(ValueError):
            self.cache[invalid_key] = self.test_value

        invalid_key = (TitForTat(), Random(), 2)
        with self.assertRaises(ValueError):
            self.cache[invalid_key] = self.test_value

    def test_setitem_invalid_value_not_list(self):
        with self.assertRaises(ValueError):
            self.cache[self.test_key] = 5

    def test_setitem_with_immutable_cache(self):
        self.cache.mutable = False
        with self.assertRaises(ValueError):
            self.cache[self.test_key] = self.test_value

    def test_save(self):
        self.cache[self.test_key] = self.test_value
        self.cache.save(self.test_save_file)
        with open(self.test_save_file, "rb") as f:
            text = f.read()
        self.assertEqual(text, self.test_pickle)

    def test_load(self):
        self.cache.load(self.test_load_file)
        self.assertEqual(self.cache[self.test_key], self.test_value)

    def test_load_error_for_inccorect_format(self):
        filename = "test_outputs/test.cache"
        with open(filename, "wb") as io:
            pickle.dump(range(5), io)

        with self.assertRaises(ValueError):
            self.cache.load(filename)

    def test_del_item(self):
        self.cache[self.test_key] = self.test_value
        self.assertTrue(self.test_key in self.cache)
        del self.cache[self.test_key]
        self.assertFalse(self.test_key in self.cache)
