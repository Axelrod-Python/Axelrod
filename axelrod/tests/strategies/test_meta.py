"""Tests for the various Meta strategies."""

from hypothesis import HealthCheck, given, settings
from hypothesis.strategies import integers

import axelrod as axl
from axelrod.classifier import Classifiers
from axelrod.tests.property import strategy_lists

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestMetaPlayer(TestPlayer):
    """This is a test class for meta players, primarily to test the classifier
    dictionary and the reset methods. Inherit from this class just as you would
    the TestPlayer class."""

    name = "Meta Player"
    player = axl.MetaPlayer
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "makes_use_of": {"game"},
        "long_run_time": True,
        "manipulates_source": False,
        "inspects_source": False,
        "manipulates_state": False,
    }

    def classifier_test(self, expected_class_classifier=None):
        player = self.player()
        classifier = dict()
        for key in [
            "stochastic",
            "inspects_source",
            "manipulates_source",
            "manipulates_state",
        ]:
            classifier[key] = any(axl.Classifiers[key](t) for t in player.team)
        classifier["memory_depth"] = float("inf")

        for t in player.team:
            try:
                classifier["makes_use_of"].update(
                    axl.Classifiers["make_use_of"](t)
                )
            except KeyError:
                pass

        for key in classifier:
            self.assertEqual(
                axl.Classifiers[key](player),
                classifier[key],
                msg="%s - Behaviour: %s != Expected Behaviour: %s"
                % (key, axl.Classifiers[key](player), classifier[key]),
            )

    def test_repr(self):
        player = self.player()
        team_size = len(player.team)
        self.assertEqual(
            str(player),
            "{}: {} player{}".format(
                self.name, team_size, "s" if team_size > 1 else ""
            ),
        )

    @given(seed=integers(min_value=1, max_value=20000000))
    @settings(
        max_examples=1,
        deadline=None,
        suppress_health_check=(HealthCheck.differing_executors,),
    )
    def test_clone(self, seed):
        # Test that the cloned player produces identical play
        player1 = self.player()
        player2 = player1.clone()
        self.assertEqual(len(player2.history), 0)
        self.assertEqual(player2.cooperations, 0)
        self.assertEqual(player2.defections, 0)
        self.assertEqual(player2.state_distribution, {})
        self.assertEqual(player2.classifier, player1.classifier)
        self.assertEqual(player2.match_attributes, player1.match_attributes)

        turns = 10
        for op in [
            axl.Cooperator(),
            axl.Defector(),
            axl.TitForTat(),
        ]:
            for p in [player1, player2]:
                match = axl.Match((p, op), turns=turns, reset=True, seed=seed)
                match.play()
            self.assertEqual(len(player1.history), turns)
            self.assertEqual(player1.history, player2.history)

    def test_update_histories(self):
        """Artificial test to ensure that an exception is thrown."""
        p = axl.MetaHunter()
        with self.assertRaises(TypeError):
            p.update_histories(C)

    @given(opponent_list=strategy_lists(max_size=1))
    @settings(
        max_examples=5,
        deadline=None,
        suppress_health_check=(HealthCheck.differing_executors,),
    )
    def test_players_return_valid_actions(self, opponent_list):
        """
        Whenever a new strategy is added to the library this potentially
        modifies the behaviour of meta strategies which in turn requires
        modification of the tests.

        In https://github.com/Axelrod-Python/Axelrod/pull/1373 specific
        behaviour tests for the meta strategies were removed.

        This test ensures that a valid example is always returned by checking
        that the actions played are a subset of {C, D}.
        """
        player = self.player()
        opponent = opponent_list[0]()
        match = axl.Match(players=(player, opponent))
        interactions = match.play()
        player_actions = set(player_action for player_action, _ in interactions)
        self.assertTrue(player_actions <= set((C, D)))


class TestMetaMajority(TestMetaPlayer):
    name = "Meta Majority"
    player = axl.MetaMajority
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "long_run_time": True,
        "manipulates_source": False,
        "makes_use_of": {"game", "length"},
        "inspects_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        P1 = axl.MetaMajority()
        P2 = axl.Player()

        # With more cooperators on the team than defectors, we should cooperate.
        P1.team = [axl.Cooperator(), axl.Cooperator(), axl.Defector()]
        self.assertEqual(P1.strategy(P2), C)

        # With more defectors, we should defect.
        P1.team = [axl.Cooperator(), axl.Defector(), axl.Defector()]
        self.assertEqual(P1.strategy(P2), D)


class TestMetaMinority(TestMetaPlayer):
    name = "Meta Minority"
    player = axl.MetaMinority
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "long_run_time": True,
        "makes_use_of": {"game", "length"},
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_team(self):
        team = [axl.Cooperator]
        player = self.player(team=team)
        self.assertEqual(len(player.team), 1)

    def test_strategy(self):
        P1 = axl.MetaMinority()
        P2 = axl.Player()

        # With more cooperators on the team, we should defect.
        P1.team = [axl.Cooperator(), axl.Cooperator(), axl.Defector()]
        self.assertEqual(P1.strategy(P2), D)

        # With defectors in the majority, we will cooperate here.
        P1.team = [axl.Cooperator(), axl.Defector(), axl.Defector()]
        self.assertEqual(P1.strategy(P2), C)


class TestMetaWinnerEnsemble(TestMetaPlayer):
    name = "Meta Winner Ensemble"
    player = axl.MetaWinnerEnsemble

    def test_singularity(self):
        """Test meta_strategy when the player is singular."""
        team = [axl.Cooperator]
        player = axl.MetaWinnerEnsemble(team=team)
        self.assertFalse(Classifiers["stochastic"](player))
        coplayer = axl.Defector()
        match = axl.Match((player, coplayer), turns=10)
        match.play()

    def test_stochasticity(self):
        # One player teams may be stochastic or not
        team = [axl.Cooperator]
        player = axl.MetaWinnerEnsemble(team=team)
        self.assertFalse(Classifiers["stochastic"](player))

        team = [axl.Random]
        player = axl.MetaWinnerEnsemble(team=team)
        self.assertTrue(Classifiers["stochastic"](player))

        # Multiplayer teams without repetition are always stochastic
        team = [axl.Cooperator, axl.Defector]
        player = axl.MetaWinnerEnsemble(team=team)
        self.assertTrue(Classifiers["stochastic"](player))

        # If the players are all identical, a multiplayer team might in fact
        # be deterministic, even though random values are being drawn.
        team = [axl.Cooperator, axl.Cooperator]
        player = axl.MetaWinnerEnsemble(team=team)
        self.assertFalse(Classifiers["stochastic"](player))


class TestNiceMetaWinner(TestMetaPlayer):
    name = "Nice Meta Winner"
    player = axl.NiceMetaWinner
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "long_run_time": True,
        "makes_use_of": {"game", "length"},
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        P1 = axl.NiceMetaWinner(team=[axl.Cooperator, axl.Defector])
        P2 = axl.Player()

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

        opponent = axl.Cooperator()
        player = axl.NiceMetaWinner(team=[axl.Cooperator, axl.Defector])
        match = axl.Match((player, opponent), turns=5)
        match.play()
        self.assertEqual(player.history[-1], C)

        opponent = axl.Defector()
        player = axl.NiceMetaWinner(team=[axl.Defector])
        match = axl.Match((player, opponent), turns=20)
        match.play()
        self.assertEqual(player.history[-1], D)

        opponent = axl.Defector()
        player = axl.MetaWinner(team=[axl.Cooperator, axl.Defector])
        match = axl.Match((player, opponent), turns=20)
        match.play()
        self.assertEqual(player.history[-1], D)


class TestNiceMetaWinnerEnsemble(TestMetaPlayer):
    name = "Nice Meta Winner Ensemble"
    player = axl.NiceMetaWinnerEnsemble
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "makes_use_of": {"game", "length"},
        "long_run_time": True,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C)] * 8
        self.versus_test(
            opponent=axl.Cooperator(),
            expected_actions=actions,
            init_kwargs={"team": [axl.Cooperator, axl.Defector]},
        )

    def test_strategy2(self):
        actions = [(C, D)] + [(D, D)] * 7
        self.versus_test(
            opponent=axl.Defector(),
            expected_actions=actions,
            init_kwargs={"team": [axl.Cooperator, axl.Defector]},
        )


class TestMetaHunter(TestMetaPlayer):
    name = "Meta Hunter"
    player = axl.MetaHunter
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "makes_use_of": set(),
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # We are not using the Cooperator Hunter here, so this should lead to
        # cooperation.
        actions = [(C, C)] * 5
        self.versus_test(opponent=axl.Cooperator(), expected_actions=actions)

        # After long histories tit-for-tat should come into play.
        opponent = axl.MockPlayer([C] * 100 + [D])
        actions = [(C, C)] * 100 + [(C, D)] + [(D, C)]
        self.versus_test(opponent=opponent, expected_actions=actions)

        actions = [(C, C)] * 102
        self.versus_test(opponent=axl.Cooperator(), expected_actions=actions)

        # All these others, however, should trigger a defection for the hunter.
        actions = [(C, D), (C, D), (C, D), (C, D), (D, D)]
        self.versus_test(opponent=axl.Defector(), expected_actions=actions)

        actions = [(C, C), (C, D), (C, C), (C, D), (C, C), (C, D), (D, C)]
        self.versus_test(opponent=axl.Alternator(), expected_actions=actions)

        actions = [
            (C, C),
            (C, C),
            (C, C),
            (C, D),
            (C, C),
            (C, C),
            (C, C),
            (C, D),
            (D, C),
        ]
        self.versus_test(opponent=axl.CyclerCCCD(), expected_actions=actions)


class TestMetaHunterAggressive(TestMetaPlayer):
    name = "Meta Hunter Aggressive"
    player = axl.MetaHunterAggressive
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "makes_use_of": set(),
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # We are using CooperatorHunter here, so this should lead to
        # defection
        actions = [(C, C)] * 4 + [(D, C)]
        self.versus_test(opponent=axl.Cooperator(), expected_actions=actions)

        # All these others, however, should trigger a defection for the hunter.
        actions = [(C, D), (C, D), (C, D), (C, D), (D, D)]
        self.versus_test(opponent=axl.Defector(), expected_actions=actions)

        actions = [(C, C), (C, D), (C, C), (C, D), (C, C), (C, D), (D, C)]
        self.versus_test(opponent=axl.Alternator(), expected_actions=actions)

        actions = [
            (C, C),
            (C, C),
            (C, C),
            (C, D),
            (C, C),
            (C, C),
            (C, C),
            (C, D),
            (D, C),
        ]
        self.versus_test(opponent=axl.CyclerCCCD(), expected_actions=actions)

        # To test the TFT action of the strategy after 100 turns, we need to
        # remove two of the hunters from its team.
        # It is almost impossible to identify a history which reaches 100 turns
        # without triggering one of the hunters in the default team. As at
        # 16-Mar-2017, none of the strategies in the library does so.
        team = [
            axl.DefectorHunter,
            axl.AlternatorHunter,
            axl.RandomHunter,
            axl.CycleHunter,
            axl.EventualCycleHunter,
        ]
        opponent = axl.MockPlayer([C] * 100 + [D])
        actions = [(C, C)] * 100 + [(C, D), (D, C)]
        self.versus_test(
            opponent=opponent,
            expected_actions=actions,
            init_kwargs={"team": team},
        )


class TestMetaMajorityMemoryOne(TestMetaPlayer):
    name = "Meta Majority Memory One"
    player = axl.MetaMajorityMemoryOne
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "inspects_source": False,
        "long_run_time": False,
        "makes_use_of": {"game"},
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestMetaMajorityFiniteMemory(TestMetaPlayer):
    name = "Meta Majority Finite Memory"
    player = axl.MetaMajorityFiniteMemory
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "long_run_time": True,
        "inspects_source": False,
        "makes_use_of": {"game"},
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestMetaMajorityLongMemory(TestMetaPlayer):
    name = "Meta Majority Long Memory"
    player = axl.MetaMajorityLongMemory
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "long_run_time": True,
        "inspects_source": False,
        "makes_use_of": {"game", "length"},
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestMetaWinnerMemoryOne(TestMetaPlayer):
    name = "Meta Winner Memory One"
    player = axl.MetaWinnerMemoryOne
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "makes_use_of": {"game"},
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestMetaWinnerFiniteMemory(TestMetaPlayer):
    name = "Meta Winner Finite Memory"
    player = axl.MetaWinnerFiniteMemory
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "long_run_time": True,
        "inspects_source": False,
        "makes_use_of": {"game"},
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestMetaWinnerLongMemory(TestMetaPlayer):
    name = "Meta Winner Long Memory"
    player = axl.MetaWinnerLongMemory
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "long_run_time": True,
        "inspects_source": False,
        "makes_use_of": {"game", "length"},
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestMetaWinnerDeterministic(TestMetaPlayer):
    name = "Meta Winner Deterministic"
    player = axl.MetaWinnerDeterministic
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "long_run_time": True,
        "inspects_source": False,
        "makes_use_of": {"game", "length"},
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestMetaWinnerStochastic(TestMetaPlayer):
    name = "Meta Winner Stochastic"
    player = axl.MetaWinnerStochastic
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "long_run_time": True,
        "inspects_source": False,
        "makes_use_of": {"game", "length"},
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestMetaMixer(TestMetaPlayer):
    name = "Meta Mixer"
    player = axl.MetaMixer
    expected_classifier = {
        "inspects_source": False,
        "long_run_time": True,
        "makes_use_of": {"game", "length"},
        "manipulates_source": False,
        "manipulates_state": False,
        "memory_depth": float("inf"),
        "stochastic": True,
    }

    def test_stochasticity(self):
        # If the distribution is deterministic, the strategy may be deterministic.
        team = [axl.TitForTat, axl.Cooperator, axl.Grudger]
        distribution = [1, 0, 0]
        player = self.player(team=team, distribution=distribution)
        self.assertFalse(Classifiers["stochastic"](player))

        team = [axl.Random, axl.Cooperator, axl.Grudger]
        distribution = [1, 0, 0]
        player = self.player(team=team, distribution=distribution)
        self.assertTrue(Classifiers["stochastic"](player))

        # If the team has only one player, the strategy may be deterministic.
        team = [axl.TitForTat]
        player = self.player(team=team)
        self.assertFalse(Classifiers["stochastic"](player))

        team = [axl.Random]
        player = self.player(team=team)
        self.assertTrue(Classifiers["stochastic"](player))

        # Stochastic if the distribution isn't degenerate.
        team = [axl.TitForTat, axl.Cooperator, axl.Grudger]
        distribution = [0.2, 0.5, 0.3]
        self.assertTrue(Classifiers["stochastic"](player))

    def test_strategy(self):
        # Distribution = None
        team = [axl.TitForTat, axl.Cooperator, axl.Grudger]
        distribution = None

        actions = [(C, C)] * 20
        self.versus_test(
            opponent=axl.Cooperator(),
            expected_actions=actions,
            init_kwargs={"team": team, "distribution": distribution},
        )

        # Distribution = [0, 0, 0]
        team = [axl.TitForTat, axl.Cooperator, axl.Grudger]
        distribution = [0, 0, 0]

        actions = [(C, C)] * 20
        self.versus_test(
            opponent=axl.Cooperator(),
            expected_actions=actions,
            init_kwargs={"team": team, "distribution": distribution},
        )

        team = [axl.TitForTat, axl.Cooperator, axl.Grudger]
        distribution = [0.2, 0.5, 0.3]

        actions = [(C, C)] * 20
        self.versus_test(
            opponent=axl.Cooperator(),
            expected_actions=actions,
            init_kwargs={"team": team, "distribution": distribution},
        )

        team.append(axl.Defector)
        distribution = [
            0.2,
            0.5,
            0.3,
            0,
        ]  # If add a defector but does not occur
        self.versus_test(
            opponent=axl.Cooperator(),
            expected_actions=actions,
            init_kwargs={"team": team, "distribution": distribution},
        )

        distribution = [0, 0, 0, 1]  # If defector is only one that is played
        actions = [(D, C)] * 20
        self.versus_test(
            opponent=axl.Cooperator(),
            expected_actions=actions,
            init_kwargs={"team": team, "distribution": distribution},
        )

    def test_raise_error_in_distribution(self):
        team = [axl.TitForTat, axl.Cooperator, axl.Grudger]
        distribution = [0.2, 0.5, 0.5]  # Not a valid probability distribution

        player = axl.MetaMixer(team=team, distribution=distribution)
        player.set_seed(100)
        opponent = axl.Cooperator()
        self.assertRaises(ValueError, player.strategy, opponent)


class TestNMWEDeterministic(TestMetaPlayer):
    name = "NMWE Deterministic"
    player = axl.NMWEDeterministic
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "long_run_time": True,
        "inspects_source": False,
        "makes_use_of": {"game", "length"},
        "manipulates_source": False,
        "manipulates_state": False,
    }

    # Skip this test
    def classifier_test(self, expected_class_classifier=None):
        pass

    def test_strategy(self):
        actions = [(C, C), (C, D), (C, C), (D, D), (D, C)]
        self.versus_test(
            opponent=axl.Alternator(), expected_actions=actions, seed=11
        )


class TestNMWEStochastic(TestMetaPlayer):
    name = "NMWE Stochastic"
    player = axl.NMWEStochastic
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "long_run_time": True,
        "inspects_source": False,
        "makes_use_of": {"game", "length"},
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestNMWEFiniteMemory(TestMetaPlayer):
    name = "NMWE Finite Memory"
    player = axl.NMWEFiniteMemory
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "long_run_time": True,
        "inspects_source": False,
        "makes_use_of": {"game"},
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestNMWELongMemory(TestMetaPlayer):
    name = "NMWE Long Memory"
    player = axl.NMWELongMemory
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "long_run_time": True,
        "inspects_source": False,
        "makes_use_of": {"game", "length"},
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestNMWEMemoryOne(TestMetaPlayer):
    name = "NMWE Memory One"
    player = axl.NMWEMemoryOne
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "long_run_time": False,
        "inspects_source": False,
        "makes_use_of": {"game"},
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestMemoryDecay(TestPlayer):
    name = "Memory Decay: 0.1, 0.03, -2, 1, Tit For Tat, 15"
    player = axl.MemoryDecay
    expected_classifier = {
        "memory_depth": float("inf"),
        "long_run_time": False,
        "stochastic": True,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # Test TitForTat behavior in first 15 turns
        opponent = axl.Cooperator()
        actions = list([(C, C)]) * 15
        self.versus_test(opponent, expected_actions=actions, seed=1)

        opponent = axl.Defector()
        actions = [(C, D)] + list([(D, D)]) * 14
        self.versus_test(opponent, expected_actions=actions, seed=1)

        opponent = axl.Alternator()
        actions = [(C, C)] + [(C, D), (D, C)] * 7
        self.versus_test(opponent, expected_actions=actions, seed=1)

        opponent_actions = [C, D, D, C, D, C, C, D, C, D, D, C, C, D, D]
        opponent = axl.MockPlayer(actions=opponent_actions)
        mem_actions = [C, C, D, D, C, D, C, C, D, C, D, D, C, C, D]
        actions = list(zip(mem_actions, opponent_actions))
        self.versus_test(opponent, expected_actions=actions, seed=1)

    def test_strategy2(self):
        opponent = axl.Random()
        actions = [(C, D), (D, D), (D, C), (C, C), (C, D), (D, C)]
        self.versus_test(opponent, expected_actions=actions, seed=15)

    def test_strategy3(self):
        # Test net-cooperation-score (NCS) based decisions in subsequent turns
        opponent = axl.Cooperator()
        actions = [(C, C)] * 15 + [(C, C)]
        self.versus_test(
            opponent,
            expected_actions=actions,
            seed=1,
            init_kwargs={"memory": [D] * 5 + [C] * 10},
        )

    def test_strategy4(self):
        opponent = axl.Cooperator()
        actions = [(C, C)] * 15 + [(C, C)]
        self.versus_test(
            opponent,
            expected_actions=actions,
            seed=1,
            init_kwargs={"memory": [D] * 4 + [C] * 11},
        )

    def test_alternative_starting_strategies(self):
        # Test alternative starting strategies
        opponent = axl.Cooperator()
        actions = list([(D, C)]) * 15
        self.versus_test(
            opponent,
            expected_actions=actions,
            init_kwargs={"start_strategy": axl.Defector},
        )

        opponent = axl.Cooperator()
        actions = list([(C, C)]) * 15
        self.versus_test(
            opponent,
            expected_actions=actions,
            init_kwargs={"start_strategy": axl.Cooperator},
        )

        opponent = axl.Cooperator()
        actions = [(C, C)] + list([(D, C), (C, C)]) * 7
        self.versus_test(
            opponent,
            expected_actions=actions,
            init_kwargs={"start_strategy": axl.Alternator},
        )

        opponent = axl.Defector()
        actions = [(C, D)] * 7 + [(D, D)]
        self.versus_test(
            opponent,
            expected_actions=actions,
            seed=4,
            init_kwargs={
                "memory": [C] * 12,
                "start_strategy": axl.Defector,
                "start_strategy_duration": 0,
            },
        )

    def test_memory_alter_delete(self):
        """Trigger memory_alter and memory_delete."""
        opponent = axl.Cooperator()
        actions = list([(C, C)]) * 50
        self.versus_test(
            opponent,
            expected_actions=actions,
            init_kwargs={"start_strategy": axl.Cooperator},
            seed=11,
        )
