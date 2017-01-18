Writing tests for the new strategy
==================================

To write tests you either need to create a file called :code:`test_<library>.py`
where :code:`<library>.py` is the name of the file you have created or similarly
add tests to the test file that is already present in the
:code:`axelrod/tests/unit/` directory.

Typically we want to test the following:

* That the strategy behaves as intended on the first move and subsequent
  moves, triggering any expected actions
* That the strategy initializes correctly
* That the strategy resets and clones correctly

If the strategy does not use any internal variables then there are generic tests
that are automatically invoked to verify proper initialization, resetting, and
cloning.

A :code:`TestPlayer` class has been written that has a number of convenience
methods to help write tests efficiently for how a strategy plays. It has three
helpful methods. All three of these functions can take an optional keyword
argument :code:`seed` (useful and necessary for stochastic strategies,
:code:`None` by default).

1. The member function :code:`first_play_test` tests the first strategy, e.g.::

    self.first_play_test(play=C, seed=None)

   This is equivalent to::

    P1 = axelrod.TitForTat() # Or whatever player is in your test class
    P2 = axelrod.Player()
    self.assertEqual(P1.strategy(P2), C)

2. The member function :code:`second_play_test` takes a list of four plays, each
   following one round of CC, CD, DC, and DD respectively. So for example here
   we test that Tit for tat will cooperate if and only if the opponent
   cooperates in the previous round::

    self.second_play_test(rCC=C, rCD=D, rDC=D, rDD=C, seed=None)

   This is equivalent to choosing if an opponent will play :code:`C` or
   :code:`D` following the last round of play and checking the player's
   subsequent action.

3. The member function :code:`responses_test` takes arbitrary histories for each
   player and tests a list of expected next responses::

    self.responses_test(responses=[D, C, C, C], player_history=[C],
                        opponent_history=[C], seed=None)

   In this case each player has their history simulated to be :code:`[C]` and
   the expected responses are D, C, C, C. Note that the histories will elongate
   as the responses accumulated, with the opponent accruing cooperations.

   If the given histories are not possible for the strategy then the test will
   not be meaningful. For example, setting the history of Defector to have
   cooperations is not a possible history of play since Defector always defects,
   and so will not actually test the strategy correctly. The test suite will
   warn you if it detects a mismatch in simulated history and actual history.

   Note also that in general it is not a good idea to manually set the history
   of any player.

   The function :code:`responses_test` also accepts a dictionary parameter of
   attributes to check at the end of the checks. For example this test checks
   if the player's internal variable :code:`opponent_class` is set to
   :code:`"Cooperative"`::

       self.responses_test([C], [C] * 6, [C] * 6,
                           attrs={"opponent_class": "Cooperative"})

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
            # Starts by cooperating.
            self.first_play_test(C)
            # Repeats last action of opponent history.
            self.second_play_test(C, D, C, D)
            self.responses_test([C], [C, C, C, C], [C, C, C, C])
            self.responses_test([D], [C, C, C, C, C], [C, C, C, C, D])

The :code:`test_strategy` method mainly checks that the
:code:`strategy` method in the :code:`TitForTat` class works as expected:

1. If the opponent's last strategy was :code:`C`: then :code:`TitForTat` should
   cooperate::

    self.responses_test(responses=[C], player_history=[C], opponent_history=[C])

   Or simply::

    self.responses_test([C], [C], [C])

2. If the opponent's last strategy was :code:`D`: after four cooperates then
   :code:`TitForTat` should defect. Note that we need to give the history for
   :code:`TitForTat` as well::

    self.responses_test(responses=[D], player_history=[C, C, C, C, C],
                        opponent_history=[C, C, C, C, D])

   Or::

    self.responses_test([D], [C, C, C, C, C], [C, C, C, C, D])

The :code:`expected_classifier` dictionary tests that the classification of the
strategy is as expected (the tests for this is inherited in the :code:`init`
method). Please be sure to classify new strategies according to the already
present dimensions but if you create a new dimension you do not **need** to re
classify all the other strategies (but feel free to! :)), but please do add it
to the :code:`default_classifier` in the :code:`axelrod/player.py` parent class.

Finally, there is a :code:`TestMatch` class that streamlines the testing of
two strategies playing each other using a test function :code:`versus_test`. For
example, to test several rounds of play of :code:`TitForTwoTats` versus
:code:`Bully`::

    class TestTF2TvsBully(TestMatch):
        """Test Tit for Two Tats vs Bully"""
        def test_rounds(self):
            outcomes = [[C, D], [C, D], [D, D], [D, C], [C, C], [C, D], [C, D], [D, D]]
            self.versus_test(axelrod.TitFor2Tats, axelrod.Bully, outcomes)

Using :code:`TestMatch` is essentially equivalent to playing a short `Match`
between the players and checking the outcome.

The function :code:`versus_test` also accepts a :code:`seed` keyword, and
like :code:`responses_test` the history is accumulated.
