import os
import sys

sys.path.insert(0, os.path.abspath("../"))
from axelrod import basic_strategies
from axelrod import strategies
from axelrod import cheating_strategies


def print_header(string, character):
    print string
    print character*len(string)
    print ""


if __name__ == "__main__":

    print ".. currentmodule:: axelrod.strategies"
    print_header("Here is a list of strategies", '=')

    print_header("Here are some of the basic strategies", '-')
    for strategy in basic_strategies:
        print ".. autoclass:: %s" % strategy.__name__

    print ""

    print_header("A list of all further (honest) strategies", '-')
    for strategy in strategies:
        if strategy not in basic_strategies:
            print ".. autoclass:: %s" % strategy.__name__

    print ""

    print_header("A list of the cheating strategies", '-')
    for strategy in cheating_strategies:
        print ".. autoclass:: %s" % strategy.__name__