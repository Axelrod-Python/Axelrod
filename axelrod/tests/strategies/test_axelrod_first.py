"""Tests for the First Axelrod strategies."""

import axelrod

from .test_player import TestPlayer, test_four_vector

C, D = axelrod.Action.C, axelrod.Action.D


class TestDavis(TestPlayer):

    name = "Davis: 10"
    player = axelrod.Davis
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # Cooperates for the first ten rounds
        actions = [(C, C)] * 10
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        actions = [(C, D)] * 10
        self.versus_test(axelrod.Defector(), expected_actions=actions)

        actions = [(C, C), (C, D)] * 5
        self.versus_test(axelrod.Alternator(), expected_actions=actions)

        # If opponent defects at any point then the player will defect forever
        # (after 10 rounds)
        opponent = axelrod.MockPlayer(actions=[C] * 10 + [D])
        actions = [(C, C)] * 10 + [(C, D), (D, C)]
        self.versus_test(opponent, expected_actions=actions)

        opponent = axelrod.MockPlayer(actions=[C] * 15 + [D])
        actions = [(C, C)] * 15 + [(C, D), (D, C)]
        self.versus_test(opponent, expected_actions=actions)


class TestRevisedDowning(TestPlayer):

    name = "Revised Downing: True"
    player = axelrod.RevisedDowning
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (C, C), (C, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        actions = [(C, D), (C, D), (D, D)]
        self.versus_test(axelrod.Defector(), expected_actions=actions)

        opponent = axelrod.MockPlayer(actions=[D, C, C])
        actions = [(C, D), (C, C), (C, C), (C, D)]
        self.versus_test(opponent, expected_actions=actions)

        opponent = axelrod.MockPlayer(actions=[D, D, C])
        actions = [(C, D), (C, D), (D, C), (D, D)]
        self.versus_test(opponent, expected_actions=actions)

        opponent = axelrod.MockPlayer(actions=[C, C, D, D, C, C])
        actions = [(C, C), (C, C), (C, D), (C, D), (D, C), (D, C), (D, C)]
        self.versus_test(opponent, expected_actions=actions)

        opponent = axelrod.MockPlayer(actions=[C, C, C, C, D, D])
        actions = [(C, C), (C, C), (C, C), (C, C), (C, D), (C, D), (C, C)]
        self.versus_test(opponent, expected_actions=actions)

    def test_not_revised(self):
        # Test not revised
        player = self.player(revised=False)
        opponent = axelrod.Cooperator()
        match = axelrod.Match((player, opponent), turns=2)
        self.assertEqual(match.play(), [(D, C), (D, C)])


class TestFeld(TestPlayer):

    name = "Feld: 1.0, 0.5, 200"
    player = axelrod.Feld
    expected_classifier = {
        "memory_depth": 200,
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_cooperation_probability(self):
        # Test cooperation probabilities
        p1 = self.player(start_coop_prob=1.0, end_coop_prob=0.8, rounds_of_decay=100)
        self.assertEqual(1.0, p1._cooperation_probability())
        p2 = axelrod.Cooperator()
        match = axelrod.Match((p1, p2), turns=50)
        match.play()
        self.assertEqual(0.9, p1._cooperation_probability())
        match = axelrod.Match((p1, p2), turns=100)
        match.play()
        self.assertEqual(0.8, p1._cooperation_probability())

        # Test cooperation probabilities, second set of params
        p1 = self.player(start_coop_prob=1.0, end_coop_prob=0.5, rounds_of_decay=200)
        self.assertEqual(1.0, p1._cooperation_probability())
        match = axelrod.Match((p1, p2), turns=100)
        match.play()
        self.assertEqual(0.75, p1._cooperation_probability())
        match = axelrod.Match((p1, p2), turns=200)
        match.play()
        self.assertEqual(0.5, p1._cooperation_probability())

    def test_decay(self):
        # Test beyond 200 rounds
        for opponent in [axelrod.Cooperator(), axelrod.Defector()]:
            player = self.player()
            self.assertEqual(player._cooperation_probability(), player._start_coop_prob)
            match = axelrod.Match((player, opponent), turns=201)
            match.play()
            self.assertEqual(player._cooperation_probability(), player._end_coop_prob)

    def test_strategy(self):
        actions = [(C, C)] * 41 + [(D, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions, seed=1)

        actions = [(C, C)] * 16 + [(D, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions, seed=2)

        actions = [(C, D)] + [(D, D)] * 20
        self.versus_test(axelrod.Defector(), expected_actions=actions)


class TestGraaskamp(TestPlayer):

    name = "Graaskamp"
    player = axelrod.Graaskamp
    expected_classifier = {
        'memory_depth': float("inf"),
        'stochastic': True,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Play against opponents
        actions = [(C, D), (D, C), (C, C), (C, C), (C, D), (D, D)]
        self.versus_test(axelrod.Random(), expected_actions=actions, seed=0)

        actions = [(C, C), (C, C), (C, D), (D, C), (C, D), (D, D)]
        self.versus_test(axelrod.Random(), expected_actions=actions, seed=1)

        actions = [(C, C), (C, D), (D, C), (C, D), (D, C)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions)

        actions = [(C, C) * 50, (D, C), (C, C) * 5]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        actions = [(C, D), (D, D) * 49, (D, D) * 6]
        self.versus_test(axelrod.Defector(), expected_actions=actions)

        actions = [(C, C) * 50, (D, C), (C, C) * 5]
        self.versus_test(axelrod.Grumpy(), expected_actions=actions)

        actions = [(C, C) * 50, (D, C), (C, D) * 5]
        self.versus_test(axelrod.Grudger(), expected_actions=actions)


class TestGrofman(TestPlayer):

    name = "Grofman"
    player = axelrod.Grofman
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C)] * 7
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        actions = [(C, C), (C, D), (D, C)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions)

        opponent = axelrod.MockPlayer(actions=[D] * 8)
        actions = [(C, D)] * 2 + [(D, D)] * 5 + [(C, D)] + [(C, D)]
        self.versus_test(opponent, expected_actions=actions, seed=1)

        opponent = axelrod.MockPlayer(actions=[D] * 8)
        actions = [(C, D)] * 2 + [(D, D)] * 5 + [(C, D)] + [(D, D)]
        self.versus_test(opponent, expected_actions=actions, seed=2)


class TestJoss(TestPlayer):

    name = "Joss: 0.9"
    player = axelrod.Joss
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 0.9, (C, D): 0, (D, C): 0.9, (D, D): 0}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        actions = [(C, C), (C, C), (C, C), (C, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions, seed=1)

        actions = [(C, C), (D, C), (D, C), (C, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions, seed=2)

        actions = [(C, D), (D, D), (D, D), (D, D)]
        self.versus_test(axelrod.Defector(), expected_actions=actions, seed=1)

        actions = [(C, D), (D, D), (D, D), (D, D)]
        self.versus_test(axelrod.Defector(), expected_actions=actions, seed=2)


class TestNydegger(TestPlayer):

    name = "Nydegger"
    player = axelrod.Nydegger
    expected_classifier = {
        "memory_depth": 3,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_score_history(self):
        """Tests many (but not all) possible combinations."""
        player = self.player()
        score_map = player.score_map
        score = player.score_history([C, C, C], [C, C, C], score_map)
        self.assertEqual(score, 0)
        score = player.score_history([D, C, C], [C, C, C], score_map)
        self.assertEqual(score, 1)
        score = player.score_history([C, C, C], [D, C, C], score_map)
        self.assertEqual(score, 2)
        score = player.score_history([D, D, C], [D, C, C], score_map)
        self.assertEqual(score, 7)
        score = player.score_history([C, D, C], [C, D, C], score_map)
        self.assertEqual(score, 12)
        score = player.score_history([D, C, D], [C, C, C], score_map)
        self.assertEqual(score, 17)
        score = player.score_history([D, D, D], [D, D, D], score_map)
        self.assertEqual(score, 63)

    def test_strategy(self):
        # Test TFT-type initial play
        # Test trailing post-round 3 play

        actions = [(C, C)] * 9
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        actions = [(C, D), (D, D), (D, D), (C, D), (C, D), (C, D), (C, D), (C, D)]
        self.versus_test(axelrod.Defector(), expected_actions=actions)

        actions = [(C, C), (C, D), (D, C), (C, D), (D, C), (C, D), (D, C), (C, D)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions)

        opponent = axelrod.MockPlayer(actions=[D, C])
        actions = [(C, D), (D, C), (D, D), (D, C), (D, D), (D, C), (D, D), (D, C)]
        self.versus_test(opponent, expected_actions=actions)


class TestShubik(TestPlayer):

    name = "Shubik"
    player = axelrod.Shubik
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (C, C), (C, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        actions = [(C, C), (C, D), (D, C)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions)

        opponent = axelrod.MockPlayer(actions=[D, C, C])
        actions = [(C, D), (D, C), (C, C), (C, D)]
        self.versus_test(opponent, expected_actions=actions)

        opponent = axelrod.MockPlayer(actions=[D, C, D, C, C])
        actions = [(C, D), (D, C), (C, D), (D, C), (D, C), (C, D), (D, C)]
        self.versus_test(opponent, expected_actions=actions)

        opponent = axelrod.MockPlayer(actions=[D, C, D, D, C])
        actions = [(C, D), (D, C), (C, D), (D, D), (D, C), (C, D), (D, C)]
        self.versus_test(opponent, expected_actions=actions)

        opponent = axelrod.MockPlayer(actions=[D, C, D, C, C, D])
        actions = [
            (C, D),
            (D, C),
            (C, D),
            (D, C),
            (D, C),
            (C, D),
            (D, D),
            (D, C),
            (D, D),
            (D, C),
        ]
        self.versus_test(opponent, expected_actions=actions)


class TestTullock(TestPlayer):

    name = "Tullock: 11"
    player = axelrod.Tullock
    expected_classifier = {
        "memory_depth": 11,
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        """Cooperates for first ten rounds"""
        actions = [(C, C), (C, D)] * 5
        self.versus_test(axelrod.Alternator(), expected_actions=actions)

        actions = [(C, D)] * 11 + [(D, D)] * 2
        self.versus_test(axelrod.Defector(), expected_actions=actions)

        opponent = axelrod.MockPlayer(actions=[D] * 10 + [C])
        actions = [(C, D)] * 10 + [(C, C), (D, D)]
        self.versus_test(opponent, expected_actions=actions)

        # Test beyond 10 rounds
        opponent = axelrod.MockPlayer(actions=[D] * 5 + [C] * 6)
        actions = [(C, D)] * 5 + [(C, C)] * 6 + [(D, D)] * 4
        self.versus_test(opponent, expected_actions=actions, seed=20)

        opponent = axelrod.MockPlayer(actions=[D] * 5 + [C] * 6)
        actions = [(C, D)] * 5 + [(C, C)] * 6 + [(C, D), (D, D), (D, D), (C, D)]
        self.versus_test(opponent, expected_actions=actions, seed=1)

        opponent = axelrod.MockPlayer(actions=[C] * 9 + [D] * 2)
        actions = [(C, C)] * 9 + [(C, D)] * 2 + [(C, C), (D, C), (D, C), (C, C)]
        self.versus_test(opponent, expected_actions=actions, seed=1)

        opponent = axelrod.MockPlayer(actions=[C] * 9 + [D] * 2)
        actions = [(C, C)] * 9 + [(C, D)] * 2 + [(D, C), (D, C), (C, C), (C, C)]
        self.versus_test(opponent, expected_actions=actions, seed=2)


class TestUnnamedStrategy(TestPlayer):

    name = "Unnamed Strategy"
    player = axelrod.UnnamedStrategy
    expected_classifier = {
        "memory_depth": 0,
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(D, C), (C, C), (C, C), (D, C), (C, C), (C, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions, seed=1)

        actions = [(C, C), (C, C), (D, C), (C, C), (C, C), (D, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions, seed=10)


class TestSteinAndRapoport(TestPlayer):

    name = "Stein and Rapoport: 0.05: (D, D)"
    player = axelrod.SteinAndRapoport
    expected_classifier = {
        "memory_depth": float("inf"),
        "long_run_time": False,
        "stochastic": False,
        "makes_use_of": {"length"},
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_init(self):
        player = self.player()
        self.assertEqual(player.alpha, 0.05)
        self.assertFalse(player.opponent_is_random)

        player = self.player(alpha=0.5)
        self.assertEqual(player.alpha, 0.5)
        self.assertFalse(player.opponent_is_random)

    def test_strategy(self):
        # Our Player (SteinAndRapoport) vs Cooperator
        # After 15th round (pvalue < alpha) still plays TitForTat.
        # Note it always defects on the last two rounds.
        opponent = axelrod.Cooperator()
        actions = [(C, C)] * 17 + [(D, C)] * 2
        self.versus_test(
            opponent, expected_actions=actions, attrs={"opponent_is_random": False}
        )

        actions = actions[:-2] + [(C, C)] * 2
        self.versus_test(
            opponent,
            expected_actions=actions[:-2],
            match_attributes={"length": -1},
            attrs={"opponent_is_random": False},
        )

        # SteinAndRapoport vs Defector
        # After 15th round (p-value < alpha) still plays TitForTat.
        opponent = axelrod.Defector()
        actions = [(C, D)] * 4 + [(D, D)] * 15
        self.versus_test(
            opponent, expected_actions=actions, attrs={"opponent_is_random": False}
        )

        # SteinAndRapoport vs Alternator
        # After 15th round (p-value > alpha) starts defecting.
        opponent = axelrod.Alternator()
        actions = [(C, C), (C, D), (C, C), (C, D)]

        # On 15th round carry out chi-square test.
        actions += [(D, C), (C, D)] * 5 + [(D, C)]

        # Defect throughout.
        actions += [(D, D), (D, C), (D, D), (D, C)]

        self.versus_test(
            opponent, expected_actions=actions, attrs={"opponent_is_random": True}
        )

        # The test is carried out again every 15 rounds.
        # If the strategy alternates for the first 12 rounds and then cooperates
        # it is no longer recognised as random.
        opponent = axelrod.MockPlayer([C, D] * 6 + [C] * 50)

        actions = [(C, C), (C, D), (C, C), (C, D)]
        # On 15th round carry out chi-square test.
        actions += [(D, C), (C, D)] * 4 + [(D, C), (C, C), (D, C)]
        # Defect throughout and carry out chi-square test on round 30.
        # Opponent is no longer recognised as random, revert to TFT.
        actions += [(D, C)] * 14 + [(C, C)]
        self.versus_test(
            opponent,
            expected_actions=actions,
            match_attributes={"length": -1},
            attrs={"opponent_is_random": False},
        )


class TestTidemanAndChieruzzi(TestPlayer):

    name = "Tideman and Chieruzzi"
    player = axelrod.TidemanAndChieruzzi
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": {"game", "length"},
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # Cooperator Test
        opponent = axelrod.Cooperator()
        actions = [(C, C), (C, C), (C, C), (C, C)]
        self.versus_test(opponent, expected_actions=actions)

        # Defector Test
        opponent = axelrod.Defector()
        actions = [(C, D), (D, D), (D, D), (D, D)]
        self.versus_test(opponent, expected_actions=actions)

        # Test increasing retaliation
        opponent = axelrod.MockPlayer([D, C])
        actions = [
            (C, D),
            (D, C),
            (C, D),
            (D, C),
            (D, D),
            (D, C),
            (D, D),
            (D, C),
            (C, D),
            (D, C),
        ]
        self.versus_test(
            opponent,
            expected_actions=actions,
            attrs={
                "is_retaliating": True,
                "retaliation_length": 4,
                "retaliation_remaining": 3,
            },
        )

        opponent = axelrod.Cycler("DDCDD")
        actions = [
            (C, D),
            (D, D),
            (D, C),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, C),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, C),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, C),
            (D, D),
            (D, D),
        ]
        self.versus_test(
            opponent,
            expected_actions=actions,
            attrs={
                "current_score": 34,
                "opponent_score": 19,
                "last_fresh_start": 0,
                "retaliation_length": 6,
                "retaliation_remaining": 2,
            },
        )

        # When the length is given this strategy will not give a fresh start
        opponent = axelrod.Cycler("DDCDD")
        actions = [
            (C, D),
            (D, D),
            (D, C),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, C),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, C),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, C),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, C),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, C),
            (C, D),
            (C, D),
        ]
        self.versus_test(
            opponent, expected_actions=actions, match_attributes={"length": 50}
        )

        # When the length is not given this strategy will give a fresh start.
        opponent = axelrod.Cycler("DDCDD")
        actions = [
            (C, D),
            (D, D),
            (D, C),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, C),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, C),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, C),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, C),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, C),
            (C, D),
            (C, D),
        ]
        self.versus_test(
            opponent,
            expected_actions=actions,
            match_attributes={"length": float("inf")},
        )

        # Check standard deviation conditions.
        # The opponent is similar to the one above except the stddev condition
        # is not met, therefore no fresh start will be given.
        opponent = axelrod.Cycler("DDCDDDDCDDCDCCC")
        actions = [
            (C, D),
            (D, D),
            (D, C),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, C),
            (D, D),
            (D, D),
            (D, C),
            (C, D),
            (D, C),
            (D, C),
            (D, C),
            (D, D),
            (D, D),
            (D, C),
            (D, D),
            (D, D),
            (D, D),
            (D, D),
            (D, C),
            (C, D),
            (D, D),
        ]

        self.versus_test(
            opponent, expected_actions=actions, attrs={"last_fresh_start": 0}
        )

        # Check the fresh start condition
        opponent = axelrod.TitForTat()
        actions = [(C, C), (C, C), (C, C), (C, C)]
        self.versus_test(
            opponent, expected_actions=actions, attrs={"fresh_start": False}
        )

        # check the fresh start condition: least 20 rounds since the last ‘fresh start’
        opponent = axelrod.Cycler("CCCCD")
        actions = [
            (C, C),
            (C, C),
            (C, C),
            (C, C),
            (C, D),
            (D, C),
            (C, C),
            (C, C),
            (C, C),
            (C, D),
            (D, C),
            (D, C),
            (C, C),
            (C, C),
            (C, D),
            (D, C),
            (D, C),
            (D, C),
            (C, C),
            (C, D),
            (D, C),
            (D, C),
            (D, C),
            (C, C),
            (C, D),
            (D, C),
            (C, C),
            (C, C),
            (C, C),
            (C, D),
            (D, C),
            (D, C),
            (C, C),
            (C, C),
            (C, D),
        ]
        self.versus_test(
            opponent,
            expected_actions=actions,
            match_attributes={"length": 35},
            attrs={
                "current_score": 108,
                "opponent_score": 78,
                "last_fresh_start": 24,
                "retaliation_length": 2,
                "retaliation_remaining": 0,
            },
        )
