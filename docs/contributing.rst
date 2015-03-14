Contributing
============

All contributions to this repository are welcome via pull request on the `github repository <https://github.com/drvinceknight/Axelrod>`_.

The project follows the following guidelines:

1. Use the base Python library unless completely necessary.
2. If a non base Python library is deemed necessary, it should not hinder the running or contribution of the package when using the base Python library.
   For example, the `matplotlib library <http://matplotlib.org/>`_ is used in a variety of classes to be able to show results, such as this one:
   This has been done carefully with tests that are skipped if the library is not installed and also without any crashes if something using the library was run.
3. Try as best as possible to follow `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_ which includes **using descriptive variable names**.
4. Testing: the project uses the `unittest <https://docs.python.org/2/library/unittest.html>`_ library and has a nice testing suite that makes some things very easy to write tests for.

The rest of this page will consider two aspects:

1. `Contributing strategies`_
2. `Contributing to the library`_

Contributing strategies
-----------------------

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
    │       └── cooperator.py
    │       └── defector.py
    │       └── grudger.py
    │       └── titfortat.py
    │       └── gobymajority.py
    │       └── ...
    │   └── /tests/
    │       └── test_*.py
    └── README.md
    └── run_tournament.py

To contribute a strategy you need to follow as many of the following steps as possible:

1. Fork the `github repository <https://github.com/drvinceknight/Axelrod>`_.
2. Add a <strategy>.py file to the strategies directory. (Take a look at the others in there: you need to write code for the strategy and one other simple thing.)
3. Update the ./axelrod/strategies/__init__.py file (you need to write the import statement and add the strategy to the relevant python list).
4. This one is optional: write some unit tests in the ./axelrod/tests/ directory.
5. This one is also optional: add your name to the contributors list down below. If you don't I'll try and do it myself.
6. Send me a pull request.

Is your strategy honest?
^^^^^^^^^^^^^^^^^^^^^^^^

The rules for an 'honest' strategy are very simple:

1. It does not change what it's opponents do/know.
2. It forgets everything every time it starts playing someone (this is implemented with the :code:`reset` method).

If your strategy is not 'honest': that's not at all a problem though.
Things that break the above rules are very welcome, although they should be well documented.
There's a special list in which they must reside so that they are not run by the default tournament but this does not stop them being used by anyone wanting to build their own tournament.

Simply add your strategy to the correct place in :code:`strategies/__init__.py`::

    ...
    # These are strategies that do not follow the rules of Axelrods tournament
    cheating_strategies = [
        Geller,
        GellerCooperator,
        ...


Contributing to the library
---------------------------
