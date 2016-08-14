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
2. Add a :code:`<strategy>.py` file to the strategies directory or add a
   strategy to a pre existing :code:`<strategy>.py` file.
3. Update the :code:`./axelrod/strategies/_strategies.py` file.
4. If you created a new :code:`<strategy>.py` file add it to
   :code:`.docs/reference/all_strategies.rst`.
5. Write some unit tests in the :code:`./axelrod/tests/` directory.
6. This one is also optional: ping us a message and we'll add you to the
   Contributors team. This would add an Axelrod-Python organisation badge to
   your profile.
7. Send us a pull request.

**If you would like a hand with any of the above please do get in touch: we're
always delighted to have new strategies.**
