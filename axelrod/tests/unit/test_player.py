import copy
import random
import unittest
import axelrod

from axelrod import simulate_play, Player


C, D = 'C', 'D'


def cooperate(self):
    return C

def defect(self):
    return D


class TestPlayerClass(unittest.TestCase):

    name = "Player"
    player = Player
    stochastic = False

    def test_add_noise(self):
        random.seed(1)
        noise = 0.2
        s1, s2 = C, C
        noisy_s1, noisy_s2 = self.player()._add_noise(noise, s1, s2)
        self.assertEqual(noisy_s1, D)
        self.assertEqual(noisy_s2, C)

    def test_play(self):
        p1, p2 = self.player(), self.player()
        p1.strategy = cooperate
        p2.strategy = defect
        p1.play(p2)
        self.assertEqual(p1.history[0], C)
        self.assertEqual(p2.history[0], D)

        # Test cooperation / defection counts
        self.assertEqual(p1.cooperations, 1)
        self.assertEqual(p1.defections, 0)
        self.assertEqual(p2.cooperations, 0)
        self.assertEqual(p2.defections, 1)
        p1.play(p2)
        self.assertEqual(p1.history[-1], C)
        self.assertEqual(p2.history[-1], D)
        # Test cooperation / defection counts
        self.assertEqual(p1.cooperations, 2)
        self.assertEqual(p1.defections, 0)
        self.assertEqual(p2.cooperations, 0)
        self.assertEqual(p2.defections, 2)

    def test_noisy_play(self):
        random.seed(1)
        noise = 0.2
        p1, p2 = self.player(), self.player()
        p1.strategy = cooperate
        p2.strategy = defect
        p1.play(p2, noise)
        self.assertEqual(p1.history[0], D)
        self.assertEqual(p2.history[0], D)


def test_responses(test_class, P1, P2, history_1, history_2,
                   responses, random_seed=None):
    """
    Test responses to arbitrary histories. Used for the the following tests
    in TestPlayer: first_play_test, markov_test, and responses_test.
    Works for arbitrary players as well. Input response_lists is a list of
    lists, each of which consists of a list for the history of player 1, a
    list for the history of player 2, and a list for the subsequent moves
    by player one to test.
    """

    if random_seed:
        random.seed(random_seed)
    # Force the histories, In case either history is impossible or if some
    # internal state needs to be set, actually submit to moves to the strategy
    # method. Still need to append history manually.
    for h1, h2 in zip(history_1, history_2):
        simulate_play(P1, P2, h1, h2)
    # Run the tests
    for response in responses:
        s1, s2 = simulate_play(P1, P2)
        test_class.assertEqual(s1, response)


class TestPlayer(unittest.TestCase):
    "A Test class from which other player test classes are inherited"

    name = "Player"
    player = Player
    stochastic = False

    def test_initialisation(self):
        """Test that the player initiates correctly."""
        self.assertEqual(self.player().history, [])
        self.assertEqual(self.player().stochastic, self.stochastic)
        self.assertEqual(self.player().tournament_attributes, {})
        self.assertEqual(self.player().cooperations, 0)
        self.assertEqual(self.player().defections, 0)

    def test_repr(self):
        """Test that the representation is correct."""
        self.assertEqual(str(self.player()), self.name)

    def test_reset(self):
        """Make sure reseting works correctly."""
        p = self.player()
        p.history = [C, C]
        p.reset()
        self.assertEqual(p.history, [])
        self.assertEqual(self.player().cooperations, 0)
        self.assertEqual(self.player().defections, 0)

    def test_strategy(self):
        """Test that strategy method."""
        self.assertEqual(self.player().strategy(self.player()), None)

    def first_play_test(self, play, random_seed=None):
        """Tests first move of a strategy."""
        P1 = self.player()
        P2 = Player()
        test_responses(
            self, P1, P2, [], [], [play],
            random_seed=random_seed)

    def markov_test(self, responses, random_seed=None):
        """Test responses to the four possible one round histories. Input
        responses is simply the four responses to CC, CD, DC, and DD."""
        # Construct the test lists
        histories = [
            [[C], [C]], [[C], [D]], [[D], [C]],
            [[D], [D]]]
        for i, history in enumerate(histories):
            # Needs to be in the inner loop in case player retains some state
            P1 = self.player()
            P2 = Player()
            test_responses(self, P1, P2, history[0], history[1], responses[i],
                           random_seed=random_seed)

    def responses_test(self, history_1, history_2, responses,
                       random_seed=None, tournament_length=200):
        """Test responses to arbitrary histories. Input response_list is a
        list of lists, each of which consists of a list for the history of
        player 1, a list for the history of player 2, and a list for the
        subsequent moves by player one to test.
        """
        P1 = self.player()
        P1.tournament_length = tournament_length
        P2 = Player()
        P2.tournament_length = tournament_length
        test_responses(
            self, P1, P2, history_1, history_2, responses,
            random_seed=random_seed)


class TestHeadsUp(unittest.TestCase):
    """Test class for heads up play between two given players."""

    def versus_test(self, player_1_class, player_2_class, outcomes,
                    player_1_history=None, player_2_history=None,
                    random_seed=None):
        """Tests a sequence of outcomes for two given players."""
        if random_seed:
            random.seed(random_seed)
        player_1 = player_1_class()
        player_2 = player_2_class()
        # Set histories
        if player_1_history is None:
            player_1_history = []
        player_1.history = player_1_history
        if player_2_history is None:
            player_2_history = []
        player_2.history = player_2_history
        # Test sequence of play
        for outcome_1, outcome_2 in outcomes:
            player_1.play(player_2)
            self.assertEqual(player_1_history[-1], outcome_1)
            self.assertEqual(player_2_history[-1], outcome_2)


def test_four_vector(test_class, expected_dictionary):
    """
    Checks that two dictionaries match -- the four-vector defining
    a memory-one strategy and the given expected dictionary.
    """
    P1 = test_class.player()
    for key in sorted(expected_dictionary.keys()):
        test_class.assertAlmostEqual(
            P1._four_vector[key], expected_dictionary[key])
