Instructions
============

Here is the file structure for the Axelrod repository::

    .
    ├── axelrod
    │   └── __init__.py
    │   └── ecosystem.py
    │   └── game.py
    │   └── player.py
    │   └── plot.py
    │   └── result_set.py
    │   └── round_robin.py
    │   └── tournament.py
    │   └── /strategies/
    │       └── __init__.py
    │       └── _strategies.py
    │       └── cooperator.py
    │       └── defector.py
    │       └── grudger.py
    │       └── titfortat.py
    │       └── gobymajority.py
    │       └── ...
    │   └── /tests/
    │       └── functional
    │       └── unit
    │           └── test_*.py
    └── README.md

To contribute a strategy you need to follow as many of the following steps as possible:

1. Fork the `github repository <https://github.com/Axelrod-Python/Axelrod>`_.
2. Add a :code:`<strategy>.py` file to the strategies directory. (Take a look
   at the others in there: you need to write code for the strategy and one other
   simple thing.)
3. Update the :code:`./axelrod/strategies/_strategies.py` file (you need to
   write the import statement and add the strategy to the relevant python list).
4. Update :code:`./axelrod/docs/reference/overview_of_strategies.rst` with a description
   of what the strategy does and include an example of it working. If relevant
   please also add a source for the strategy (if it is not an original one).
5. This one is optional: write some unit tests in the :code:`./axelrod/tests/`
   directory.
6. This one is also optional: ping us a message and we'll add you to the
   Contributors team. This would add an Axelrod-Python organisation badge to
   your profile.
7. Send us a pull request.

**If you would like a hand with any of the above please do get in touch: we're
always delighted to have new strategies.**
