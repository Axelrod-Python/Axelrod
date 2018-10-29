"""Tests for the various Meta strategies."""
import axelrod

from .test_player import TestPlayer

C, D = axelrod.Action.C, axelrod.Action.D


class TestMetaPlayer(TestPlayer):
    """This is a test class for meta players, primarily to test the classifier
    dictionary and the reset methods. Inherit from this class just as you would
    the TestPlayer class."""

    name = "Meta Player"
    player = axelrod.MetaPlayer
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
            classifier[key] = any(t.classifier[key] for t in player.team)
        classifier["memory_depth"] = float("inf")

        for t in player.team:
            try:
                classifier["makes_use_of"].update(t.classifier["makes_use_of"])
            except KeyError:
                pass

        for key in classifier:
            self.assertEqual(
                player.classifier[key],
                classifier[key],
                msg="%s - Behaviour: %s != Expected Behaviour: %s"
                % (key, player.classifier[key], classifier[key]),
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


class TestMetaMajority(TestMetaPlayer):

    name = "Meta Majority"
    player = axelrod.MetaMajority
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
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "long_run_time": True,
        "makes_use_of": {"game", "length"},
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
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
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "long_run_time": True,
        "makes_use_of": {"game", "length"},
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
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
            opponent=axelrod.Cooperator(),
            expected_actions=actions,
            init_kwargs={"team": [axelrod.Cooperator, axelrod.Defector]},
        )
        actions = [(C, D)] + [(D, D)] * 7
        self.versus_test(
            opponent=axelrod.Defector(),
            expected_actions=actions,
            init_kwargs={"team": [axelrod.Cooperator, axelrod.Defector]},
        )


class TestMetaHunter(TestMetaPlayer):

    name = "Meta Hunter"
    player = axelrod.MetaHunter
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
        #  cooperation.
        actions = [(C, C)] * 5
        self.versus_test(opponent=axelrod.Cooperator(), expected_actions=actions)

        # After long histories tit-for-tat should come into play.
        opponent = axelrod.MockPlayer([C] * 100 + [D])
        actions = [(C, C)] * 100 + [(C, D)] + [(D, C)]
        self.versus_test(opponent=opponent, expected_actions=actions)

        actions = [(C, C)] * 102
        self.versus_test(opponent=axelrod.Cooperator(), expected_actions=actions)

        # All these others, however, should trigger a defection for the hunter.
        actions = [(C, D), (C, D), (C, D), (C, D), (D, D)]
        self.versus_test(opponent=axelrod.Defector(), expected_actions=actions)

        actions = [(C, C), (C, D), (C, C), (C, D), (C, C), (C, D), (D, C)]
        self.versus_test(opponent=axelrod.Alternator(), expected_actions=actions)

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
        self.versus_test(opponent=axelrod.CyclerCCCD(), expected_actions=actions)


class TestMetaHunterAggressive(TestMetaPlayer):
    name = "Meta Hunter Aggressive"
    player = axelrod.MetaHunterAggressive
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
        self.versus_test(opponent=axelrod.Cooperator(), expected_actions=actions)

        # All these others, however, should trigger a defection for the hunter.
        actions = [(C, D), (C, D), (C, D), (C, D), (D, D)]
        self.versus_test(opponent=axelrod.Defector(), expected_actions=actions)

        actions = [(C, C), (C, D), (C, C), (C, D), (C, C), (C, D), (D, C)]
        self.versus_test(opponent=axelrod.Alternator(), expected_actions=actions)

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
        self.versus_test(opponent=axelrod.CyclerCCCD(), expected_actions=actions)

        # To test the TFT action of the strategy after 100 turns, we need to
        # remove two of the hunters from its team.
        # It is almost impossible to identify a history which reaches 100 turns
        # without triggering one of the hunters in the default team. As at
        # 16-Mar-2017, none of the strategies in the library does so.
        team = [
            axelrod.DefectorHunter,
            axelrod.AlternatorHunter,
            axelrod.RandomHunter,
            axelrod.CycleHunter,
            axelrod.EventualCycleHunter,
        ]
        opponent = axelrod.MockPlayer([C] * 100 + [D])
        actions = [(C, C)] * 100 + [(C, D), (D, C)]
        self.versus_test(
            opponent=opponent, expected_actions=actions, init_kwargs={"team": team}
        )


class TestMetaMajorityMemoryOne(TestMetaPlayer):
    name = "Meta Majority Memory One"
    player = axelrod.MetaMajorityMemoryOne
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "inspects_source": False,
        "long_run_time": False,
        "makes_use_of": set(["game"]),
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (C, D), (D, C), (C, D), (D, C)]
        self.versus_test(opponent=axelrod.Alternator(), expected_actions=actions)


class TestMetaMajorityFiniteMemory(TestMetaPlayer):
    name = "Meta Majority Finite Memory"
    player = axelrod.MetaMajorityFiniteMemory
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "long_run_time": True,
        "inspects_source": False,
        "makes_use_of": {"game"},
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (C, D), (D, C), (C, D), (D, C)]
        self.versus_test(opponent=axelrod.Alternator(), expected_actions=actions)


class TestMetaMajorityLongMemory(TestMetaPlayer):
    name = "Meta Majority Long Memory"
    player = axelrod.MetaMajorityLongMemory
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "long_run_time": True,
        "inspects_source": False,
        "makes_use_of": {"game", "length"},
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (C, D), (D, C), (C, D), (D, C)]
        self.versus_test(
            opponent=axelrod.Alternator(), expected_actions=actions, seed=0
        )

        actions = [(C, C), (C, D), (D, C), (C, D), (D, C)]
        self.versus_test(
            opponent=axelrod.Alternator(), expected_actions=actions, seed=1
        )


class TestMetaWinnerMemoryOne(TestMetaPlayer):
    name = "Meta Winner Memory One"
    player = axelrod.MetaWinnerMemoryOne
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "makes_use_of": set(["game"]),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (D, D), (D, C), (D, D), (D, C)]
        self.versus_test(opponent=axelrod.Alternator(), expected_actions=actions)


class TestMetaWinnerFiniteMemory(TestMetaPlayer):
    name = "Meta Winner Finite Memory"
    player = axelrod.MetaWinnerFiniteMemory
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "long_run_time": True,
        "inspects_source": False,
        "makes_use_of": {"game"},
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (D, D), (D, C), (D, D), (D, C)]
        self.versus_test(opponent=axelrod.Alternator(), expected_actions=actions)


class TestMetaWinnerLongMemory(TestMetaPlayer):
    name = "Meta Winner Long Memory"
    player = axelrod.MetaWinnerLongMemory
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "long_run_time": True,
        "inspects_source": False,
        "makes_use_of": {"game", "length"},
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (D, D), (D, C), (D, D), (D, C)]
        self.versus_test(opponent=axelrod.Alternator(), expected_actions=actions)


class TestMetaWinnerDeterministic(TestMetaPlayer):
    name = "Meta Winner Deterministic"
    player = axelrod.MetaWinnerDeterministic
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "long_run_time": True,
        "inspects_source": False,
        "makes_use_of": {"game", "length"},
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (D, D), (D, C), (D, D), (D, C)]
        self.versus_test(opponent=axelrod.Alternator(), expected_actions=actions)


class TestMetaWinnerStochastic(TestMetaPlayer):
    name = "Meta Winner Stochastic"
    player = axelrod.MetaWinnerStochastic
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "long_run_time": True,
        "inspects_source": False,
        "makes_use_of": {"game", "length"},
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (D, D), (D, C), (D, D), (D, C)]
        self.versus_test(opponent=axelrod.Alternator(), expected_actions=actions)


class TestMetaMixer(TestMetaPlayer):

    name = "Meta Mixer"
    player = axelrod.MetaMixer
    expected_classifier = {
        "inspects_source": False,
        "long_run_time": True,
        "makes_use_of": {"game", "length"},
        "manipulates_source": False,
        "manipulates_state": False,
        "memory_depth": float("inf"),
        "stochastic": True,
    }

    def test_strategy(self):

        team = [axelrod.TitForTat, axelrod.Cooperator, axelrod.Grudger]
        distribution = [0.2, 0.5, 0.3]

        P1 = axelrod.MetaMixer(team=team, distribution=distribution)
        P2 = axelrod.Cooperator()
        actions = [(C, C)] * 20
        self.versus_test(
            opponent=axelrod.Cooperator(),
            expected_actions=actions,
            init_kwargs={"team": team, "distribution": distribution},
        )

        team.append(axelrod.Defector)
        distribution = [0.2, 0.5, 0.3, 0]  # If add a defector but does not occur
        self.versus_test(
            opponent=axelrod.Cooperator(),
            expected_actions=actions,
            init_kwargs={"team": team, "distribution": distribution},
        )

        distribution = [0, 0, 0, 1]  # If defector is only one that is played
        actions = [(D, C)] * 20
        self.versus_test(
            opponent=axelrod.Cooperator(),
            expected_actions=actions,
            init_kwargs={"team": team, "distribution": distribution},
        )

    def test_raise_error_in_distribution(self):
        team = [axelrod.TitForTat, axelrod.Cooperator, axelrod.Grudger]
        distribution = [0.2, 0.5, 0.5]  # Not a valid probability distribution

        player = axelrod.MetaMixer(team=team, distribution=distribution)
        opponent = axelrod.Cooperator()

        self.assertRaises(ValueError, player.strategy, opponent)


class TestNMWEDeterministic(TestMetaPlayer):
    name = "NMWE Deterministic"
    player = axelrod.NMWEDeterministic
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
        actions = [(C, C), (C, D), (D, C), (D, D), (D, C)]
        self.versus_test(opponent=axelrod.Alternator(), expected_actions=actions)


class TestNMWEStochastic(TestMetaPlayer):
    name = "NMWE Stochastic"
    player = axelrod.NMWEStochastic
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "long_run_time": True,
        "inspects_source": False,
        "makes_use_of": {"game", "length"},
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (C, D), (C, C), (D, D), (D, C)]
        self.versus_test(opponent=axelrod.Alternator(), expected_actions=actions)


class TestNMWEFiniteMemory(TestMetaPlayer):
    name = "NMWE Finite Memory"
    player = axelrod.NMWEFiniteMemory
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "long_run_time": True,
        "inspects_source": False,
        "makes_use_of": {"game"},
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (C, D), (D, C), (D, D), (D, C)]
        self.versus_test(opponent=axelrod.Alternator(), expected_actions=actions)


class TestNMWELongMemory(TestMetaPlayer):
    name = "NMWE Long Memory"
    player = axelrod.NMWELongMemory
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "long_run_time": True,
        "inspects_source": False,
        "makes_use_of": {"game", "length"},
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (C, D), (D, C), (D, D), (D, C)]
        self.versus_test(opponent=axelrod.Alternator(), expected_actions=actions)


class TestNMWEMemoryOne(TestMetaPlayer):
    name = "NMWE Memory One"
    player = axelrod.NMWEMemoryOne
    expected_classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "long_run_time": False,
        "inspects_source": False,
        "makes_use_of": {"game"},
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (C, D), (D, C), (D, D), (D, C)]
        self.versus_test(opponent=axelrod.Alternator(), expected_actions=actions)


"""Tests for the Memory Decay strategy"""


class TestMemoryDecay(TestPlayer):

    name = "Memory Decay: 0.1, 0.03, -2, 1, Tit For Tat, 15"
    player = axelrod.MemoryDecay
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
        opponent = axelrod.Cooperator()
        actions = list([(C, C)]) * 15
        self.versus_test(opponent, expected_actions=actions)

        opponent = axelrod.Defector()
        actions = [(C, D)] + list([(D, D)]) * 14
        self.versus_test(opponent, expected_actions=actions)

        opponent = axelrod.Alternator()
        actions = [(C, C)] + [(C, D), (D, C)] * 7
        self.versus_test(opponent, expected_actions=actions)

        opponent_actions = [C, D, D, C, D, C, C, D, C, D, D, C, C, D, D]
        opponent = axelrod.MockPlayer(actions=opponent_actions)
        mem_actions = [C, C, D, D, C, D, C, C, D, C, D, D, C, C, D]
        actions = list(zip(mem_actions, opponent_actions))
        self.versus_test(opponent, expected_actions=actions)

        opponent = axelrod.Random()
        actions = [(C, D), (D, D), (D, C), (C, C), (C, D), (D, C)]
        self.versus_test(opponent, expected_actions=actions, seed=0)

        # Test net-cooperation-score (NCS) based decisions in subsequent turns
        opponent = axelrod.Cooperator()
        actions = [(C, C)] * 15 + [(C, C)]
        self.versus_test(
            opponent,
            expected_actions=actions,
            seed=1,
            init_kwargs={"memory": [D] * 5 + [C] * 10},
        )

        opponent = axelrod.Cooperator()
        actions = [(C, C)] * 15 + [(C, C)]
        self.versus_test(
            opponent,
            expected_actions=actions,
            seed=1,
            init_kwargs={"memory": [D] * 4 + [C] * 11},
        )

        # Test alternative starting strategies
        opponent = axelrod.Cooperator()
        actions = list([(D, C)]) * 15
        self.versus_test(
            opponent,
            expected_actions=actions,
            init_kwargs={"start_strategy": axelrod.Defector},
        )

        opponent = axelrod.Cooperator()
        actions = list([(C, C)]) * 15
        self.versus_test(
            opponent,
            expected_actions=actions,
            init_kwargs={"start_strategy": axelrod.Cooperator},
        )

        opponent = axelrod.Cooperator()
        actions = [(C, C)] + list([(D, C), (C, C)]) * 7
        self.versus_test(
            opponent,
            expected_actions=actions,
            init_kwargs={"start_strategy": axelrod.Alternator},
        )

        opponent = axelrod.Defector()
        actions = [(C, D)] * 7 + [((D, D))]
        self.versus_test(
            opponent,
            expected_actions=actions,
            seed=4,
            init_kwargs={
                "memory": [C] * 12,
                "start_strategy": axelrod.Defector,
                "start_strategy_duration": 0,
            },
        )
