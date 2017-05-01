import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D

class TestBM(TestPlayer):
    """
    Note that this test is referred to in the documentation as an example on
    writing tests.  If you modify the tests here please also modify the
    documentation.
    """

    name = "Bush Mosteller: 0.5, 0.5, 3.0, 0.5"
    player = axelrod.BM
    expected_classifier = {
        'memory_depth': 1,  # Updates stimulus using last round
        'stochastic': True,
        'makes_use_of': set(["game"]),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(play=C , seed=1)

        actions = [(C,C), (D,C), (D,C)]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions, attrs={"_stimulus" : 1}, seed=1)

        #Making sure probabilities changes following payoffs
        actions = [(C, C), (D, D)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions, attrs={"_stimulus" : 0.4,"_c_probability" : 0.6 , "_d_probability" : 0.5}, seed=1)

        actions = [(C, D), (D, D), (D, D)]
        self.versus_test(axelrod.Defector(), expected_actions=actions, attrs={"_stimulus" : -0.20000000000000004, "_c_probability" : 0.375 , "_d_probability" : 0.45}, seed=1)