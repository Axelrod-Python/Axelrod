import doctest
import os
import unittest


def load_tests(loader, tests, ignore):
    for root, dirs, files in os.walk("./docs"):
        for f in files:
            if f.endswith(".rst"):
                 tests.addTests(doctest.DocFileSuite(os.path.join(root, f)))

    return tests


if __name__ == '__main__':
    unittest.main()
