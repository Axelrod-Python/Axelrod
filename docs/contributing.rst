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
4. Update :code:`./axelrod/docs/overview_of_strategies.rst` with a description
   of what the strategy does and include an example of it working. If relevant
   please also add a source for the strategy (if it is not an original one).
5. This one is optional: write some unit tests in the ./axelrod/tests/ directory.
6. This one is also optional: add your name to the contributors list in the bottom of the :code:`README.md` file.
7. Send us a pull request.

**If you would like a hand with any of the above please do get in touch: we're
always delight to have new strategies.**

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

After that the only thing required is to write the :code:`strategy` method which
takes an opponent as an argument.  In the case of :code:`TitForTat` the strategy
attempts to play the same thing as the last strategy played by the opponent
(:code:`opponent.history[-1]`) and if this is not possible (in other words the
opponent has not played yet) will cooperate::

    def strategy(self, opponent):
        try:
            return opponent.history[-1]
        except IndexError:
            return 'C'

If your strategy creates any particular attribute along the way you need to make
sure that there is a :code:`reset` method that takes account of it.  An example
of this is the :code:`ForgetfulGrudger` strategy which creates a boolean
variable :code:`grudged` and a counter :code:`grudge_memory` which keeps track
of things during a duel.  Here is the :code:`reset` method which takes care of
resetting this in between rounds::

    def reset(self):
        """Resets scores and history."""
        self.history = []
        self.grudged = False
        self.grudge_memory = 0


You can also modify the name of the strategy with the `__repr__` method, which
is invoked when `str` is applied to a player instance. For example, the player
`Random` takes a parameter `p` for how often it cooperates, and the `__repr__`
method adds the value of this parameter to the name::

    def __repr__(self):
        return "%s: %s" % (self.name, round(self.p, 2))

Now we have separate names for different instantiations::

    import axelrod
    player1 = axelrod.Random(p=0.5)
    player2 = axelrod.Random(p=0.1)
    print(str(player1))
    print(str(player2))

This produces the following output::

    'Random: 0.5'
    'Random: 0.1'

This helps distinguish players in tournaments that have multiple instances of the
same strategy. If you modify the `__repr__` method of player, be sure to add an
appropriate test.

There is also a classifier dictionary that allows for easy classification of
strategies: take a look at the `Strategy classification`_ section for more
information.


Adding the strategy to the library
''''''''''''''''''''''''''''''''''

To get the strategy to be recognised by the library we need to add it to the files that initialise when someone types :code:`import axelrod`.
This is done in the :code:`axelrod/strategies/_strategies.py` file.

If you have added your strategy to a file that already existed (perhaps you added a new variant of :code:`titfortat` to the :code:`titfortat.py` file), **you do not need to do the following**: add a line similar to::

    from <file_name> import *

Where :code:`file_name.py` is the name of the file you created.
So for the :code:`TitForTat` strategy which is written in the :code:`titfortat.py` file we have::

    from titfortat import *

Once you have done that (**and you need to do this even if you have added a
strategy to an already existing file**), you need to add the class itself to one
of the :code:`strategies` list.


Strategy classification
'''''''''''''''''''''''

Every class has a classifier dictionary that gives some classification of the
strategy according to certain dimensions::

Let us take a look at :code:`TitForTat`::

    >>> classifier = axelrod.TitForTat.classifier
    >>> for key in classifier:
    ....    print key, classifier[key]
    manipulates_state False
    stochastic False
    manipulates_source False
    inspects_source False
    memory_depth 1

Note that when an instance of a class is created it gets it's own copy of the
default classifier dictionary from the class. This might sometimes be modified by
the initialisation depending on input parameters. A good example of this is the
:code:`Joss` strategy::

    >>> joss = axelrod.Joss()
    >>> boring_joss = axelrod.Joss(1)
    >>> joss.classifier['stochastic'], boring_joss.classifier['stochastic']
    (True, False)

Dimensions that are not classified have value `None` in the dictionary.

There are currently three important dimensions that help identify if a strategy
is 'honest' or not:

1. :code:`inspects_source` - does the strategy 'read' any source code that
   it would not normally have access to. An example of this is :code:`Geller`.
2. :code:`manipulates_source` - does the strategy 'write' any source code that
   it would not normally be able to. An example of this is :code:`Mind Bender`.
3. :code:`manipulates_state` - does the strategy 'change' any attributes that
   it would not normally be able to. An example of this is :code:`Mind Reader`.


How to write tests
''''''''''''''''''

To write tests you either need to create a file called :code:`test_<library>.py` where :code:`<library>.py` is the name of the file you have created or similarly add tests to the test file that is already present in the :code:`axelrod/tests/unit/` directory.

As an example, you code write tests for Tit-For-Tat as follows::

    import axelrod

    from test_player import TestPlayer


    class TestTitForTat(TestPlayer):

        name = "Tit For Tat"
        player = axelrod.TitForTat
        expected_classifier = {
            'memory_depth': 1,
            'stochastic': False,
            'inspects_source': False,
            'manipulates_source': False,
            'manipulates_state': False
        }

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


We have added some convenience member functions to the :code:`TestPlayer` class. All three of these functions can take an optional keyword argument :code:`random_seed` (useful for stochastic strategies).

1. The member function :code:`first_play_test` tests the first strategy, e.g.::

    def test_strategy(self):
        self.first_play_test('C')

This is equivalent to::

    def test_effect_of_strategy(self):
        P1 = axelrod.TitForTat() # Or whatever player is in your test class
        P2 = axelrod.Player()
        P2.history = []
        P2.history = []
        self.assertEqual(P1.strategy(P2), 'C')

2. The member function :code:`markov_test` takes a list of four plays, each following one round of CC, CD, DC, and DD respectively::

    def test_effect_of_strategy(self):
        self.markov_test(['C', 'D', 'D', 'C'])

This is equivalent to::

    def test_effect_of_strategy(self):
        P1 = axelrod.TitForTat() # Or whatever player is in your test class
        P2 = axelrod.Player()
        P2.history = ['C']
        P2.history = ['C']
        self.assertEqual(P1.strategy(P2), 'C')
        P2.history = ['C']
        P2.history = ['D']
        self.assertEqual(P1.strategy(P2), 'D')
        P2.history = ['D']
        P2.history = ['C']
        self.assertEqual(P1.strategy(P2), 'D')
        P2.history = ['D']
        P2.history = ['D']
        self.assertEqual(P1.strategy(P2), 'C')

3. The member function :code:`responses_test` takes arbitrary histories for each player and tests a list of expected next responses::

    def test_effect_of_strategy(self):
        self.responses_test([C], [C], [D, C, C, C], random_seed=15)

In this case each player has their history set to :code:`[C]` and the expected responses are D, C, C, C. Note that the histories will elongate as the responses accumulated.


Finally, there is a :code:`TestHeadsUp` class that streamlines the testing of two strategies playing each other using a test function :code:`versus_test`. For example, to test several rounds of play of Tit-For-Two-Tats versus Bully::

    class TestTF2TvsBully(TestHeadsUp):
        """Test Tit for Two Tats vs Bully"""
        def test_rounds(self):
            outcomes = [[C, D], [C, D], [D, D], [D, C], [C, C], [C, D], [C, D], [D, D]]
            self.versus_test(axelrod.TitFor2Tats, axelrod.Bully, outcomes)

The function :code:`versus_test` also accepts a :code:`random_seed` keyword, and like :code:`responses_test` the history is accumulated.

The :code:`expected_classifier` dictionary tests that the classification of the
strategy is as expected (the tests for this is inherited in the :code:`init`
method). Please be sure to classify new strategies according to the already
present dimensions but if you create a new dimension you do not **need** to re
classify all the other strategies (but feel free to! :)), but please do add it
to the :code:`default_classifier` in the :code:`axelrod/player.py` parent class.

How to run tests
''''''''''''''''

The project has an extensive test suite which is run each time a new contribution is made to the repository.
If you want to check that all the tests pass before you submit a pull request you can run the tests yourself::

    python -m unittest discover

If you are developing new tests for the suite, it is useful to run a single test file so that you don't have to wait for the entire suite each time.
For example, to run only the tests for the Grudger strategy::

    python -m unittest axelrod.tests.unit.test_grudger

The test suite is dvided into two categories: unit tests and integration tests. Each can be run individually::

    python -m unittest discover -s axelrod.tests.unit
    python -m unittest discover -s axelrod.tests.integration

Note that this project is being taken care off by `travis-ci <https://travis-ci.org/>`_, so tests will be run automatically when opening a pull request.
You can see the latest build status `here <https://travis-ci.org/Axelrod-Python/Axelrod>`_.


Adding the strategy to the documentation
''''''''''''''''''''''''''''''''''''''''

To index all the strategies and make sure their docstrings get added to the
documentation::

    cd docs
    python auto_generate_strategies_list.py > index_of_strategies.rst

This will write the file that is automatically used by `<https://readthedocs.org/>`_ to generate this `list <http://axelrod.readthedocs.org/en/latest/strategies.html>`_ of strategies.

If you would like to build the documentation locally use::

    make html

Contributing to the library
---------------------------

All contributions (docs, tests, etc) are very welcome, if there is a specific functionality that you would like to add the please open an `issue <https://github.com/Axelrod-Python/Axelrod/issues>`_ (or indeed take a look at the ones already there and jump in the conversation!).

In general follow this library aims to follow the guidelines mentioned at the top of this page.
