"""
A script to check that all strategy modules have been included in
`./docs/reference/all_strategies.rst`
"""
import glob
import sys
import os

def read_index(index_path):
    """
    Read the index of strategies

    Parameters
    ----------
    index_path : str
        A file path for the index file where all strategies are auto documented

    Returns
    -------
    strategies_reference : str
        The string value of the contents of the index file.
    """
    with open(index_path, "r") as f:
        strategies_reference = f.read()
    return strategies_reference

def get_module_name(module_path):
    """
    Take string of the form `./axelrod/strategies/titfortat.py` and returns
    `titfortat`.

    Parameters
    ----------
    module_path : str
        A file path for a module file.

    Returns
    -------
    module_name : str
        The name of the module
    """
    filename = os.path.basename(module_path)
    module_name = os.path.splitext(filename)[0]
    return module_name

def check_module(module_path,
                 index_path="./docs/reference/all_strategies.rst",
                 excluded=("_strategies", "__init__", "_filters", "human")):
    """
    Check if a module name is written in the index of strategies.

    Parameters
    ----------
    module_path : str
        A file path for a module file.
    index_path : str
        A file path for the index file where all strategies are auto documented
    excluded : tuple
        A collection of module names to be ignored

    Returns
    -------
    boolean : bool
        True/False if module is referenced.

    """
    strategies_index = read_index(index_path)
    module_name = get_module_name(module_path)
    if module_name not in excluded and module_name not in strategies_index:
            print("{} not in index".format(module_name))
            return False
    return True


if __name__ == "__main__":

    modules = glob.glob("./axelrod/strategies/*.py")
    exit_codes = []

    for module_path in modules:
        exit_codes.append(int(not check_module(module_path)))

    sys.exit(max(exit_codes))
