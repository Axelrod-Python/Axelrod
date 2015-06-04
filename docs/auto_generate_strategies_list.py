"""
A script to generate the file needed for the strategy documentation.

Run:

    python strategies.py > strategies.rst
"""
import os
import sys

sys.path.insert(0, os.path.abspath("../"))
from axelrod import basic_strategies
from axelrod import ordinary_strategies
from axelrod import cheating_strategies


def print_header(string, character):
    print string
    print character * len(string)
    print ""


if __name__ == "__main__":

    print ".. currentmodule:: axelrod.strategies"
    print_header("List of strategies", '=')

    print_header("Basic strategies", '-')
    for strategy in basic_strategies:
        print ".. autoclass:: %s" % strategy.__name__

    print ""

    print_header("Further (honest) Strategies", '-')
    for strategy in ordinary_strategies:
        print ".. autoclass:: %s" % strategy.__name__

    print ""

    print_header("Cheating strategies", '-')
    for strategy in cheating_strategies:
        print ".. autoclass:: %s" % strategy.__name__
