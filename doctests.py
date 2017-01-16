import doctest
import os
import unittest
import warnings


# Note loader and ignore are required arguments for unittest even if unused.
def load_tests(loader, tests, ignore):
    for root, dirs, files in os.walk("."):
        for f in files:
            if f.endswith(".rst"):
                 tests.addTests(
                     doctest.DocFileSuite(os.path.join(root, f),
                                          optionflags=doctest.ELLIPSIS))

    return tests


if __name__ == '__main__':
    warnings.simplefilter("ignore")
    unittest.main()
