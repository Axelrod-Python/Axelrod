import os
import pathlib
import pickle
import unittest

import axelrod as axl
from axelrod.load_data_ import axl_filename

C, D = axl.Action.C, axl.Action.D


class TestDeterministicCache(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_key = (axl.TitForTat(), axl.Defector())
        cls.test_value = [(C, D), (D, D), (D, D)]
        save_path = pathlib.Path("test_outputs/test_cache_save.txt")
        cls.test_save_file = axl_filename(save_path)
        load_path = pathlib.Path("test_outputs/test_cache_load.txt")
        cls.test_load_file = axl_filename(load_path)
        test_data_to_pickle = {
            ("Tit For Tat", "Defector"): [(C, D), (D, D), (D, D)]
        }
        cls.test_pickle = pickle.dumps(test_data_to_pickle)

        with open(cls.test_load_file, "wb") as f:
            f.write(cls.test_pickle)

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.test_save_file)
        os.remove(cls.test_load_file)

    def setUp(self):
        self.cache = axl.DeterministicCache()

    def test_basic_init(self):
        self.assertTrue(self.cache.mutable)

    def test_init_from_file(self):
        loaded_cache = axl.DeterministicCache(file_name=self.test_load_file)
        self.assertEqual(loaded_cache[self.test_key], self.test_value)

    def test_setitem(self):
        self.cache[self.test_key] = self.test_value
        self.assertEqual(self.cache[self.test_key], self.test_value)

    def test_setitem_invalid_key_not_tuple(self):
        invalid_key = "test"
        with self.assertRaises(ValueError):
            self.cache[invalid_key] = self.test_value

    def test_setitem_invalid_key_first_two_elements_not_player(self):
        invalid_key = ("test", "test")
        with self.assertRaises(ValueError):
            self.cache[invalid_key] = self.test_value

        invalid_key = (axl.TitForTat(), "test")
        with self.assertRaises(ValueError):
            self.cache[invalid_key] = self.test_value

        invalid_key = ("test", axl.TitForTat())
        with self.assertRaises(ValueError):
            self.cache[invalid_key] = self.test_value

    def test_setitem_invalid_key_too_many_players(self):
        invalid_key = (axl.TitForTat(), axl.TitForTat(), axl.TitForTat())
        with self.assertRaises(ValueError):
            self.cache[invalid_key] = self.test_value

    def test_setitem_invalid_key_stochastic_player(self):
        invalid_key = (axl.Random(), axl.TitForTat())
        with self.assertRaises(ValueError):
            self.cache[invalid_key] = self.test_value

        invalid_key = (axl.TitForTat(), axl.Random())
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
        path = pathlib.Path("test_outputs/test.cache")
        filename = axl_filename(path)
        with open(filename, "wb") as io:
            pickle.dump(range(5), io)

        with self.assertRaises(ValueError):
            self.cache.load(filename)

    def test_del_item(self):
        self.cache[self.test_key] = self.test_value
        self.assertTrue(self.test_key in self.cache)
        del self.cache[self.test_key]
        self.assertFalse(self.test_key in self.cache)
