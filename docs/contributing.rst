Contributing
============

All contributions to this repository are welcome via pull request on the `github repository <https://github.com/Axelrod-Python/Axelrod>`_.

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
    │       └── _strategies.py
    │       └── cooperator.py
    │       └── defector.py
    │       └── grudger.py
    │       └── titfortat.py
    │       └── gobymajority.py
    │       └── ...
    │   └── /tests/
    │       └── test_*.py
    └── README.md
    └── run_axelrod

To contribute a strategy you need to follow as many of the following steps as possible:

1. Fork the `github repository <https://github.com/Axelrod-Python/Axelrod>`_.
2. Add a :code:`<strategy>.py` file to the strategies directory. (Take a look at the others in there: you need to write code for the strategy and one other simple thing.)
3. Update the :code:`./axelrod/strategies/_strategies.py` file (you need to write the import statement and add the strategy to the relevant python list).
4. This one is optional: write some unit tests in the ./axelrod/tests/ directory.
5. This one is also optional: add your name to the contributors list in the bottom of the :code:`README.md` file.
6. Send me a pull request.

Adding a strategy
^^^^^^^^^^^^^^^^^

Writing the strategy
''''''''''''''''''''

There are a couple of things that need to be created in a strategy.py file.
Let us take a look at the :code:`TitForTat` class (located in the :code:`axelrod/strategies/titfortat.py` file)::


    class TitForTat(Player):
        """A player starts by cooperating and then mimics previous move by opponent."""

        name = 'Tit For Tat'

        def strategy(self, opponent):
            try:
                return opponent.history[-1]
            except IndexError:
                return 'C'

The first thing that is needed is a docstring that explains what the strategy does::

    """A player starts by cooperating and then mimics previous move by opponent."""

After that simply add in the string that will appear as the name of the strategy::

    name = 'Tit For Tat'

Note that this is mainly used in plots by :code:`matplotlib` so you can use LaTeX if you want to.
For example there is strategy with :math:`\pi` as a name::

    name = '$\pi$'

After that the only thing required is to write the :code:`strategy` method which takes an opponent as an argument.
In the case of :code:`TitForTat` the strategy attempts to play the same thing as the last strategy played by the opponent (:code:`opponent.history[-1]`) and if this is not possible (in other words the opponent has not played yet) will cooperate::

    def strategy(self, opponent):
        try:
            return opponent.history[-1]
        except IndexError:
            return 'C'

If your strategy creates any particular attribute along the way you need to make sure that there is a :code:`reset` method that takes account of it.
An example of this is the :code:`ForgetfulGrudger` strategy which creates a boolean variable :code:`grudged` and a counter :code:`grudge_memory` which keeps track of things during a duel.
Here is the :code:`reset` method which takes care of resetting this in between rounds::

    def reset(self):
        """Resets scores and history."""
        self.history = []
        self.grudged = False
        self.grudge_memory = 0

Adding the strategy to the library
''''''''''''''''''''''''''''''''''

To get the strategy to be recognised by the library we need to add it to the files that initialise when someone types :code:`import axelrod`.
This is done in the :code:`axelrod/strategies/_strategies.py` file.

If you have added your strategy to a file that already existed (perhaps you added a new variant of :code:`titfortat` to the :code:`titfortat.py` file), **you do not need to do the following**: add a line similar to::

    from <file_name> import *

Where :code:`file_name.py` is the name of the file you created.
So for the :code:`TitForTat` strategy which is written in the :code:`titfortat.py` file we have::

    from titfortat import *

Once you have done that (**and you need to do this even if you have added a strategy to an already existing file**), you need to add the class itself to one of the following lists::

    basic_strategies
    ordinary_strategies
    cheating_strategies

You will most probably be adding the strategy to one of :code:`ordinary_strategies` or :code:`cheating_strategies`.
If you are unsure take a look at the section: `Is your strategy honest?`_.

For :code:`TitForTat` this looks like::

    basic_strategies = [
        Alternator,
        Cooperator,
        Defector,
        Random,
        TitForTat,
    ]

Note that :code:`TitForTat` is here added to the :code:`basic_strategies` list.
If you would like to check if your strategy is honest, read the next section, if you would like to take a look at how to write tests please skip to `How to write tests`_ (again though if you need a hand with testing please let us know!).

Is your strategy honest?
''''''''''''''''''''''''

The rules for an 'honest' strategy are very simple:

1. It does not change what it's opponents do/know.
2. It forgets everything every time it starts playing someone (this is implemented with the :code:`reset` method).

If your strategy is not 'honest': that's not at all a problem though.
Things that break the above rules are very welcome, although they should be well documented.
There's a special list in which they must reside so that they are not run by the default tournament but this does not stop them being used by anyone wanting to build their own tournament.

Simply add your strategy to the correct place in :code:`strategies/_strategies.py`::

    ...
    # These are strategies that do not follow the rules of Axelrods tournament
    cheating_strategies = [
        Geller,
        GellerCooperator,
        ...

How to write tests
''''''''''''''''''

To write tests you either need to create a file called :code:`test_<library>.py` where :code:`<library>.py` is the name of the file you have created or similarly add tests to the test file that is already present in the :code:`axelrod/tests/` directory.

As an example, the :code:`axelrod/tests/test_titfortat.py` contains the following code::


    import axelrod

    from test_player import TestPlayer


    class TestTitForTat(TestPlayer):

        name = "Tit For Tat"
        player = axelrod.TitForTat

        def test_strategy(self):
            """Starts by cooperating."""
            P1 = axelrod.TitForTat()
            P2 = axelrod.Player()
            self.assertEqual(P1.strategy(P2), 'C')

        def test_effect_of_strategy(self):
            """
            Repeats last action of opponent history
            """
            P1 = axelrod.TitForTat()
            P2 = axelrod.Player()
            P2.history = ['C', 'C', 'C', 'C']
            self.assertEqual(P1.strategy(P2), 'C')
            P2.history = ['C', 'C', 'C', 'C', 'D']
            self.assertEqual(P1.strategy(P2), 'D')

The :code:`test_effect_of_strategy` method mainly checks that the :code:`strategy` method in the :code:`TitForTat` class works as expected:

1. If the opponent's last strategy was :code:`C`: then :code:`TitForTat` should cooperate::

    P2.history = ['C', 'C', 'C', 'C']
    self.assertEqual(P1.strategy(P2), 'C')

2. If the opponent's last strategy was :code:`D`: then :code:`TitForTat` should defect::

    P2.history = ['C', 'C', 'C', 'C', 'D']
    self.assertEqual(P1.strategy(P2), 'D')

As mentioned in `Writing the strategy`_ if you write a strategy with a :code:`reset` method that should be tested.
Here is the test for the :code:`ForgetfulGrudger` strategy (in the :code:`test_grudger.py` file)::

    def test_reset_method(self):
        """
        tests the reset method
        """
        P1 = axelrod.ForgetfulGrudger()
        P1.history = ['C', 'D', 'D', 'D']
        P1.grudged = True
        P1.grudge_memory = 4
        P1.reset()
        self.assertEqual(P1.history, [])
        self.assertEqual(P1.grudged, False)
        self.assertEqual(P1.grudge_memory, 0)


How to run tests
''''''''''''''''

The project has an extensive test suite which is run each time a new contribution is made to the repository.
If you want to check that all the tests pass before you submit a pull request you can run the tests yourself::

    python -m unittest discover axelrod/tests/

If you are developing new tests for the suite, it is useful to run a single test file so that you don't have to wait for the entire suite each time.
For example, to run only the tests for the Grudger strategy::

    python -m unittest axelrod.tests.test_grudger

Note that this project is being taken care off by `travis-ci <https://travis-ci.org/>`_, so tests will be run automatically when opening a pull request.
You can see the latest build status `here <https://travis-ci.org/Axelrod-Python/Axelrod>`_.


Adding the strategy to the documentation
''''''''''''''''''''''''''''''''''''''''

To index all the strategies and make sure their docstrings get added to the
documentation::

    cd docs
    python strategies.py > strategies.rst

This will write the file that is automatically used by `<https://readthedocs.org/>`_ to generate this `list <http://axelrod.readthedocs.org/en/latest/strategies.html>`_ of strategies.

If you would like to build the documentation locally use::

    make html

Contributing to the library
---------------------------

All contributions (docs, tests, etc) are very welcome, if there is a specific functionality that you would like to add the please open an `issue <https://github.com/Axelrod-Python/Axelrod/issues>`_ (or indeed take a look at the ones already there and jump in the conversation!).

In general follow this library aims to follow the guidelines mentioned at the top of this page.
