import random
import unittest

import axelrod

def test_four_vector(test_class, expected_dictionary):
    P1 = test_class.player()
    for key in sorted(expected_dictionary.keys()):
        test_class.assertAlmostEqual(P1._four_vector[key],
                expected_dictionary[key])

def test_responses(test_class, P1, P2, response_lists, random_seed=None):
    """Test responses to arbitrary histories. Used for the the following tests in TestPlayer: first_play_test, markov_test, and responses_test. Works for arbitrary players as well. Input response_lists is a list of lists, each of which consists of a list for the history of player 1, a list for the history of player 2, and a list for the subsequent moves by player one to test."""
    if random_seed:
        random.seed(random_seed)
    for response_list in response_lists:
        P1.history, P2.history, responses = response_list
        for response in responses:
            test_class.assertEqual(P1.strategy(P2), response)

class TestPlayer(unittest.TestCase):

    name = "Player"
    player = axelrod.Player
    stochastic = False

    def test_initialisation(self):
        """Test that the player initiates correctly."""
        self.assertEqual(self.player().history, [])
        self.assertEqual(self.player().stochastic, self.stochastic)

    def test_repr(self):
        """Test that the representation is correct."""
        self.assertEquals(str(self.player()), self.name)

    def test_reset(self):
        """Make sure reseting works correctly."""
        p = self.player()
        p.history = ['C', 'C']
        p.reset()
        self.assertEquals(p.history, [])
    
    def test_strategy(self):
        """Test that strategy method."""
        self.assertEquals(self.player().strategy(self.player()), None)
    
    def first_play_test(self, play, random_seed=None):
        """Tests first move of a strategy."""
        P1 = self.player()
        P2 = axelrod.Player()
        test_responses(self, P1, P2, [[[],[],[play]]], random_seed=random_seed)

    def markov_test(self, responses, random_seed=None):
        """Test responses to the four possible one round histories. Input responses is simply the four responses to CC, CD, DC, and DD."""
        P1 = self.player()
        P2 = axelrod.Player()
        # Construct the test lists
        histories = [[['C'],['C']], [['C'],['D']], [['D'],['C']], [['D'],['D']]]
        response_lists = []
        for i, history in enumerate(histories):
            response_lists.append([history[0], history[1], responses[i]])
        test_responses(self, P1, P2, response_lists, random_seed=random_seed)

    def responses_test(self, history_1, history_2, responses, random_seed=None):
        """Test responses to arbitrary histories. Input response_list is a list of lists, each of which consists of a list for the history of player 1, a list for the history of player 2, and a list for the subsequent moves by player one to test."""
        P1 = self.player()
        P2 = axelrod.Player()
        test_responses(self, P1, P2, [[history_1, history_2, responses]], random_seed=random_seed)

