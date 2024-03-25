"""
A script to check that all strategy modules have been included in
`./docs/reference/all_strategies.rst`
"""

import pathlib
import sys

default_index_path = pathlib.Path("./docs/reference/strategy_index.rst")
excluded_modules = ("_strategies", "__init__", "_filters")


def check_module(
    module_path: pathlib.Path,
    index_path: pathlib.Path = default_index_path,
    excluded: tuple = excluded_modules,
) -> bool:
    """
    Check if a module name is written in the index of strategies.

    Parameters
    ----------
    module_path :
        A file path for a module file.
    index_path :
        A file path for the index file where all strategies are auto documented
    excluded :
        A collection of module names to be ignored

    Returns
    -------
    boolean :
        True/False if module is referenced.

    """
    strategies_index = index_path.read_text()
    module_name = module_path.stem
    if module_name not in excluded and module_name not in strategies_index:
        print("{} not in index".format(module_name))
        return False
    return True


if __name__ == "__main__":

    p = pathlib.Path(".")
    modules = p.glob("./axelrod/strategies/*.py")
    exit_codes = []

    for module_path in modules:
        exit_codes.append(int(not check_module(module_path)))

    sys.exit(max(exit_codes))
