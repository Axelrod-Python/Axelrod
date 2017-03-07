"""Tests for the various Meta strategies."""

import random

import axelrod
from .test_player import TestPlayer, test_responses

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestMetaPlayer(TestPlayer):
    """This is a test class for meta players, primarily to test the classifier
    dictionary and the reset methods. Inherit from this class just as you would
    the TestPlayer class."""

    name = "Meta Player"
    player = axelrod.MetaPlayer
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': {'game'},
        'long_run_time': True,
        'manipulates_source': False,
        'inspects_source': False,
        'manipulates_state': False
    }

    def classifier_test(self, expected_class_classifier=None):
        player = self.player()
        classifier = dict()
        for key in ['stochastic',
                    'inspects_source', 'manipulates_source',
                    'manipulates_state']:
            classifier[key] = (any(t.classifier[key] for t in player.team))
        classifier['memory_depth'] = float('inf')

        for t in player.team:
            try:
                classifier['makes_use_of'].update(t.classifier['makes_use_of'])
            except KeyError:
                pass

        for key in classifier:
            self.assertEqual(player.classifier[key],
                             classifier[key],
                             msg="%s - Behaviour: %s != Expected Behaviour: %s" %
                                 (key, player.classifier[key], classifier[key]))

    def test_reset_history_and_attributes(self):
        player = self.player()
        clone = player.clone()
        opponent = axelrod.Cooperator()
        player.play(opponent)
        player.play(opponent)
        player.play(opponent)
        player.reset()
        for i, p in enumerate(player.team):
            self.assertEqual(len(p.history), 0)


        team_player_names = [p.__repr__() for p in player.team]
        team_clone_names = [p.__repr__() for p in clone.team]
        self.assertEqual(team_player_names, team_clone_names)

class TestMetaMajority(TestMetaPlayer):

    name = "Meta Majority"
    player = axelrod.MetaMajority
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'long_run_time': True,
        'manipulates_source': False,
        'makes_use_of': {'game', 'length'},
        'inspects_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):

        P1 = axelrod.MetaMajority()
        P2 = axelrod.Player()

        # With more cooperators on the team than defectors, we should cooperate.
        P1.team = [axelrod.Cooperator(), axelrod.Cooperator(), axelrod.Defector()]
        self.assertEqual(P1.strategy(P2), C)

        # With more defectors, we should defect.
        P1.team = [axelrod.Cooperator(), axelrod.Defector(), axelrod.Defector()]
        self.assertEqual(P1.strategy(P2), D)


class TestMetaMinority(TestMetaPlayer):

    name = "Meta Minority"
    player = axelrod.MetaMinority
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'long_run_time': True,
        'makes_use_of': {'game', 'length'},
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_team(self):
        team = [axelrod.Cooperator]
        player = self.player(team=team)
        self.assertEqual(len(player.team), 1)

    def test_strategy(self):

        P1 = axelrod.MetaMinority()
        P2 = axelrod.Player()

        # With more cooperators on the team, we should defect.
        P1.team = [axelrod.Cooperator(), axelrod.Cooperator(), axelrod.Defector()]
        self.assertEqual(P1.strategy(P2), D)

        # With defectors in the majority, we will cooperate here.
        P1.team = [axelrod.Cooperator(), axelrod.Defector(), axelrod.Defector()]
        self.assertEqual(P1.strategy(P2), C)


class TestNiceMetaWinner(TestMetaPlayer):

    name = "Nice Meta Winner"
    player = axelrod.NiceMetaWinner
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'long_run_time': True,
        'makes_use_of': {'game', 'length'},
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        P1 = axelrod.NiceMetaWinner(team=[axelrod.Cooperator, axelrod.Defector])
        P2 = axelrod.Player()

        # This meta player will simply choose the strategy with the highest
        # current score.
        P1.team[0].score = 0
        P1.team[1].score = 1
        self.assertEqual(P1.strategy(P2), C)
        P1.team[0].score = 1
        P1.team[1].score = 0
        self.assertEqual(P1.strategy(P2), C)

        # If there is a tie, choose to cooperate if possible.
        P1.team[0].score = 1
        P1.team[1].score = 1
        self.assertEqual(P1.strategy(P2), C)

        opponent = axelrod.Cooperator()
        player = axelrod.NiceMetaWinner(team=[axelrod.Cooperator, axelrod.Defector])
        for _ in range(5):
            player.play(opponent)
        self.assertEqual(player.history[-1], C)

        opponent = axelrod.Defector()
        player = axelrod.NiceMetaWinner(team=[axelrod.Defector])
        for _ in range(20):
            player.play(opponent)
        self.assertEqual(player.history[-1], D)

        opponent = axelrod.Defector()
        player = axelrod.MetaWinner(team=[axelrod.Cooperator, axelrod.Defector])
        for _ in range(20):
            player.play(opponent)
        self.assertEqual(player.history[-1], D)


class TestNiceMetaWinnerEnsemble(TestMetaPlayer):
    name = "Nice Meta Winner Ensemble"
    player = axelrod.NiceMetaWinnerEnsemble
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'makes_use_of': {'game', 'length'},
        'long_run_time': True,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)

        P1 = axelrod.NiceMetaWinner(team=[axelrod.Cooperator, axelrod.Defector])
        P2 = axelrod.Cooperator()
        test_responses(self, P1, P2, [C] * 4, [C] * 4, [C] * 4)

        P1 = axelrod.NiceMetaWinner(team=[axelrod.Cooperator, axelrod.Defector])
        P2 = axelrod.Defector()
        test_responses(self, P1, P2, [D] * 4, [C] * 4, [D] * 4)


class TestMetaHunter(TestMetaPlayer):

    name = "Meta Hunter"
    player = axelrod.MetaHunter
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'long_run_time': False,
        'inspects_source': False,
        'makes_use_of': set(),
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)

        # We are not using the Cooperator Hunter here, so this should lead to
        #  cooperation.
        self.responses_test([C], [C, C, C, C], [C, C, C, C])

        # After long histories tit-for-tat should come into play.
        self.responses_test([D], [C] * 101, [C] * 100 + [D])

        # All these others, however, should trigger a defection for the hunter.
        self.responses_test([D], [C] * 4, [D] * 4)
        self.responses_test([D], [C] * 6, [C, D] * 3)
        self.responses_test([D], [C] * 8, [C, C, C, D, C, C, C, D])
        # Test post 100 rounds responses
        self.responses_test([C], [C] * 101, [C] * 101)
        self.responses_test([D], [C] * 101, [C] * 100 + [D])


class TestMetaHunterAggressive(TestMetaPlayer):

    name = "Meta Hunter Aggressive"
    player = axelrod.MetaHunterAggressive
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'long_run_time': False,
        'inspects_source': False,
        'makes_use_of': set(),
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)

        # We are using CooperatorHunter here, so this should lead to
        # defection
        self.responses_test([D], [C, C, C, C], [C, C, C, C])

        # After long histories tit-for-tat should come into play.
        self.responses_test([D], [C] * 101, [C] * 100 + [D])

        # All these others, however, should trigger a defection for the hunter.
        self.responses_test([D], [C] * 4, [D] * 4)
        self.responses_test([D], [C] * 6, [C, D] * 3)
        self.responses_test([D], [C] * 8, [C, C, C, D, C, C, C, D])
        # Test post 100 rounds responses
        self.responses_test([D], [C] * 101, [C] * 101)
        self.responses_test([D], [C] * 101, [C] * 100 + [D])


class TestMetaMajorityMemoryOne(TestMetaPlayer):
    name = "Meta Majority Memory One"
    player = axelrod.MetaMajorityMemoryOne
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'inspects_source': False,
        'long_run_time': False,
        'makes_use_of': set(['game']),
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)


class TestMetaMajorityFiniteMemory(TestMetaPlayer):
    name = "Meta Majority Finite Memory"
    player = axelrod.MetaMajorityFiniteMemory
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'long_run_time': True,
        'inspects_source': False,
        'makes_use_of': {'game'},
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)


class TestMetaMajorityLongMemory(TestMetaPlayer):
    name = "Meta Majority Long Memory"
    player = axelrod.MetaMajorityLongMemory
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'long_run_time': True,
        'inspects_source': False,
        'makes_use_of': {'game', 'length'},
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)


class TestMetaWinnerMemoryOne(TestMetaPlayer):
    name = "Meta Winner Memory One"
    player = axelrod.MetaWinnerMemoryOne
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'makes_use_of': set(['game']),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)


class TestMetaWinnerFiniteMemory(TestMetaPlayer):
    name = "Meta Winner Finite Memory"
    player = axelrod.MetaWinnerFiniteMemory
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'long_run_time': True,
        'inspects_source': False,
        'makes_use_of': {'game'},
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)


class TestMetaWinnerLongMemory(TestMetaPlayer):
    name = "Meta Winner Long Memory"
    player = axelrod.MetaWinnerLongMemory
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'long_run_time': True,
        'inspects_source': False,
        'makes_use_of': {'game', 'length'},
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)


class TestMetaWinnerDeterministic(TestMetaPlayer):
    name = "Meta Winner Deterministic"
    player = axelrod.MetaWinnerDeterministic
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'long_run_time': True,
        'inspects_source': False,
        'makes_use_of': {'game', 'length'},
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)


class TestMetaWinnerStochastic(TestMetaPlayer):
    name = "Meta Winner Stochastic"
    player = axelrod.MetaWinnerStochastic
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'long_run_time': True,
        'inspects_source': False,
        'makes_use_of': {'game', 'length'},
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)


class TestMetaMixer(TestMetaPlayer):

    name = "Meta Mixer"
    player = axelrod.MetaMixer
    expected_classifier = {
        'inspects_source': False,
        'long_run_time': True,
        'makes_use_of': {'game', 'length'},
        'manipulates_source': False,
        'manipulates_state': False,
        'memory_depth': float('inf'),
        'stochastic': True,
    }

    def test_strategy(self):

        team = [axelrod.TitForTat, axelrod.Cooperator, axelrod.Grudger]
        distribution = [.2, .5, .3]

        P1 = axelrod.MetaMixer(team, distribution)
        P2 = axelrod.Cooperator()

        for k in range(100):
            P1.play(P2)
            self.assertEqual(P1.history[-1], C)

        team.append(axelrod.Defector)
        distribution = [.2, .5, .3, 0]  # If add a defector but does not occur

        P1 = axelrod.MetaMixer(team, distribution)

        for k in range(100):
            P1.play(P2)
            self.assertEqual(P1.history[-1], C)

        distribution = [0, 0, 0, 1]  # If defector is only one that is played

        P1 = axelrod.MetaMixer(team, distribution)

        for k in range(100):
            P1.play(P2)
            self.assertEqual(P1.history[-1], D)

    def test_raise_error_in_distribution(self):
        team = [axelrod.TitForTat, axelrod.Cooperator, axelrod.Grudger]
        distribution = [.2, .5, .5]  # Not a valid probability distribution

        P1 = axelrod.MetaMixer(team, distribution)
        P2 = axelrod.Cooperator()

        self.assertRaises(ValueError, P1.strategy, P2)


class TestNMWEDeterministic(TestMetaPlayer):
    name = "NMWE Deterministic"
    player = axelrod.NMWEDeterministic
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'long_run_time': True,
        'inspects_source': False,
        'makes_use_of': {'game', 'length'},
        'manipulates_source': False,
        'manipulates_state': False
    }

    # Skip this test
    def classifier_test(self, expected_class_classifier=None):
        pass

    def test_strategy(self):
        self.first_play_test(C)


class TestNMWEStochastic(TestMetaPlayer):
    name = "NMWE Stochastic"
    player = axelrod.NMWEStochastic
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'long_run_time': True,
        'inspects_source': False,
        'makes_use_of': {'game', 'length'},
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)


class TestNMWEFiniteMemory(TestMetaPlayer):
    name = "NMWE Finite Memory"
    player = axelrod.NMWEFiniteMemory
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'long_run_time': True,
        'inspects_source': False,
        'makes_use_of': {'game'},
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)


class TestNMWELongMemory(TestMetaPlayer):
    name = "NMWE Long Memory"
    player = axelrod.NMWELongMemory
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'long_run_time': True,
        'inspects_source': False,
        'makes_use_of': {'game', 'length'},
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)


class TestNMWEMemoryOne(TestMetaPlayer):
    name = "NMWE Memory One"
    player = axelrod.NMWEMemoryOne
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'long_run_time': False,
        'inspects_source': False,
        'makes_use_of': {'game'},
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)
