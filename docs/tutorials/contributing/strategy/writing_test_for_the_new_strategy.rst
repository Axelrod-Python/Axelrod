Writing tests for the new strategy
==================================

To write tests you either need to create a file called :code:`test_<library>.py`
where :code:`<library>.py` is the name of the file you have created or similarly
add tests to the test file that is already present in the
:code:`axelrod/tests/unit/` directory.

As an example, the tests for Tit-For-Tat are as follows::

    import axelrod

    from test_player import TestPlayer

    C, D = axelrod.Actions.C, axelrod.Actions.D

    class TestTitForTat(TestPlayer):
        """
        Note that this test is referred to in the documentation as an example on
        writing tests.  If you modify the tests here please also modify the
        documentation.
        """

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
            self.first_play_test(C)

        def test_effect_of_strategy(self):
            """Repeats last action of opponent history."""
            self.markov_test([C, D, C, D])
            self.responses_test([C] * 4, [C, C, C, C], [C])
            self.responses_test([C] * 5, [C, C, C, C, D], [D])

The :code:`test_effect_of_strategy` method mainly checks that the
:code:`strategy` method in the :code:`TitForTat` class works as expected:

1. If the opponent's last strategy was :code:`C`: then :code:`TitForTat` should
   cooperate::

    self.responses_test([C] * 4, [C, C, C, C], [C])

2. If the opponent's last strategy was :code:`D`: then :code:`TitForTat` should
   defect::

    self.responses_test([C] * 5, [C, C, C, C, D], [D])

We have added some convenience member functions to the :code:`TestPlayer` class.
All three of these functions can take an optional keyword argument
:code:`random_seed` (useful for stochastic strategies).

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

2. The member function :code:`markov_test` takes a list of four plays, each
   following one round of CC, CD, DC, and DD respectively::

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

3. The member function :code:`responses_test` takes arbitrary histories for each
   player and tests a list of expected next responses::

    def test_effect_of_strategy(self):
        self.responses_test([C], [C], [D, C, C, C], random_seed=15)

   In this case each player has their history set to :code:`[C]` and the
   expected responses are D, C, C, C. Note that the histories will elongate as
   the responses accumulated.

   The function :code:`responses_test` also accepts a dictionary parameter of
   attributes to check at the end of the checks. For example this test checks
   if the player's internal variable :code:`opponent_class` is set to
   :code:`"Cooperative"`::

       self.responses_test([C] * 6, [C] * 6, [C],
                       attrs={"opponent_class": "Cooperative"})

Finally, there is a :code:`TestHeadsUp` class that streamlines the testing of
two strategies playing each other using a test function :code:`versus_test`. For
example, to test several rounds of play of :code:`TitForTwoTats` versus
:code:`Bully`::

    class TestTF2TvsBully(TestHeadsUp):
        """Test Tit for Two Tats vs Bully"""
        def test_rounds(self):
            outcomes = [[C, D], [C, D], [D, D], [D, C], [C, C], [C, D], [C, D], [D, D]]
            self.versus_test(axelrod.TitFor2Tats, axelrod.Bully, outcomes)

The function :code:`versus_test` also accepts a :code:`random_seed` keyword, and
like :code:`responses_test` the history is accumulated.

The :code:`expected_classifier` dictionary tests that the classification of the
strategy is as expected (the tests for this is inherited in the :code:`init`
method). Please be sure to classify new strategies according to the already
present dimensions but if you create a new dimension you do not **need** to re
classify all the other strategies (but feel free to! :)), but please do add it
to the :code:`default_classifier` in the :code:`axelrod/player.py` parent class.
