Writing tests for the new strategy
==================================

To write tests you either need to create a file called :code:`test_<library>.py`
where :code:`<library>.py` is the name of the file you have created or similarly
add tests to the test file that is already present in the
:code:`axelrod/tests/strategies/` directory.

Typically we want to test the following:

* That the strategy behaves as intended on the first move and subsequent
  moves, triggering any expected actions
* That the strategy initializes correctly

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

3. The member function :code:`versus_test` can be used to test how the player
   plays against a given opponent::

    self.versus_test(opponent=axelrod.MockPlayer(actions=[C, D]),
                     expected_actions=[(D, C), (C, D), (C, C)], seed=None)

   In this case the player is tested against an opponent that will cycle through
   :code:`C, D`. The :code:`expected_actions` are the actions player by both
   the tested player and the opponent in the match. In this case we see that the
   player is expected to play :code:`D, C, C` against :code:`C, D, C`.

   Note that you can either user a :code:`MockPlayer` that will cycle through a
   given sequence or you can use another strategy from the Axelrod library.

   The function :code:`versus_test` also accepts a dictionary parameter of
   attributes to check at the end of the match. For example this test checks
   if the player's internal variable :code:`opponent_class` is set to
   :code:`"Cooperative"`::

       actions = [(C, C)] * 6
       self.versus_test(axelrod.Cooperator(), expected_actions=actions
                        attrs={"opponent_class": "Cooperative"})

   Note here that instead of passing a sequence of actions as an opponent we are
   passing an actual player from the axelrod library.

   The function :code:`versus_test` also accepts a dictionary parameter of match
   attributes that dictate the knowledge of the players. For example this test
   assumes that players do not know the length of the match::

        actions = [(C, C), (C, D), (D, C), (C, D)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions,
                         match_attributes={"length": -1})

   The function :code:`versus_test` also accepts a dictionary parameter of
   keyword arguments that dictate how the player is initiated. For example this
   test how the player plays when initialised with :code:`p=1`::

        actions = [(C, C), (C, D), (C, C), (C, D)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions,
                         init_kwargs={"p": 1})

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
            'makes_use_of': set(),
            'inspects_source': False,
            'manipulates_source': False,
            'manipulates_state': False
        }

        def test_strategy(self):
            self.first_play_test(C)
            self.second_play_test(rCC=C, rCD=D, rDC=C, rDD=D)

            # Play against opponents
            actions = [(C, C), (C, D), (D, C), (C, D)]
            self.versus_test(axelrod.Alternator(), expected_actions=actions)

            actions = [(C, C), (C, C), (C, C), (C, C)]
            self.versus_test(axelrod.Cooperator(), expected_actions=actions)

            actions = [(C, D), (D, D), (D, D), (D, D)]
            self.versus_test(axelrod.Defector(), expected_actions=actions)

            # This behaviour is independent of knowledge of the Match length
            actions = [(C, C), (C, D), (D, C), (C, D)]
            self.versus_test(axelrod.Alternator(), expected_actions=actions,
                             match_attributes={"length": -1})

            # We can also test against random strategies
            actions = [(C, D), (D, D), (D, C), (C, C)]
            self.versus_test(axelrod.Random(), expected_actions=actions,
                             seed=0)

            actions = [(C, C), (C, D), (D, D), (D, C)]
            self.versus_test(axelrod.Random(), expected_actions=actions,
                             seed=1)

            #  If you would like to test against a sequence of moves you should use
            #  a MockPlayer
            opponent = axelrod.MockPlayer(actions=[C, D])
            actions = [(C, C), (C, D), (D, C), (C, D)]
            self.versus_test(opponent, expected_actions=actions)

            opponent = axelrod.MockPlayer(actions=[C, C, D, D, C, D])
            actions = [(C, C), (C, C), (C, D), (D, D), (D, C), (C, D)]
            self.versus_test(opponent, expected_actions=actions)


There are other examples of using this testing framework in
:code:`axelrod/tests/strategies/test_titfortat.py`.

The :code:`expected_classifier` dictionary tests that the classification of the
strategy is as expected (the tests for this is inherited in the :code:`init`
method). Please be sure to classify new strategies according to the already
present dimensions but if you create a new dimension you do not **need** to re
classify all the other strategies (but feel free to! :)), but please do add it
to the :code:`default_classifier` in the :code:`axelrod/player.py` parent class.
