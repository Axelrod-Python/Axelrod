import doctest
import os
import unittest
import warnings


# Note loader and ignore are required arguments for unittest even if unused.
def load_tests(loader, tests, ignore):
    """
    Locates and returns a collection of unittests in a TestSuite object
    Parameters
    ----------
    loader :
        A required but unused parameter.
    tests :
        A unittest TestSuite object for collecting the needed test cases.
    ignore :
        A required but unused parameter.
    Returns
    -------
    tests :
        A unittest TestSuite object that holds test cases.
    """
    for root, dirs, files in os.walk("."):
        for f in files:
            if f.endswith(".rst"):
                tests.addTests(
                    doctest.DocFileSuite(
                        # ELLIPSIS option tells doctest to ignore portions of the verification value.
                        os.path.join(root, f),
                        optionflags=doctest.ELLIPSIS,
                    )
                )

    return tests


if __name__ == "__main__":
    warnings.simplefilter("ignore")
    unittest.main()
