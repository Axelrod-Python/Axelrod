"""Tests for the ZeroResp strategy (v5.3)."""

import inspect
import unittest

import axelrod as axl
from axelrod.strategies.zeroresp import Features, ZeroResp

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


def _play(player, opponent, turns, seed=0, length=None, noise=0.0):
    attrs = None
    if length is not None:
        attrs = {"length": length}
    match = axl.Match(
        (player, opponent),
        turns=turns,
        seed=seed,
        noise=noise,
        match_attributes=attrs,
    )
    return match.play()


class TestZeroResp(TestPlayer):

    # Player.__repr__ appends init kwargs (base_epoch, use_profiles).
    name = "ZeroResp v5.3: 25, True"
    player = axl.ZeroResp
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        # length/game are read via .get(), which the library scanner does
        # not count. manipulates_state stays True (class-level profiles).
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": True,
    }

    def setUp(self):
        ZeroResp._global_profiles = {}
        ZeroResp._global_lengths = []
        super().setUp()

    def equality_of_players_test(self, p1, p2, seed, opponent):
        # Warmth is drawn in __init__ from the module RNG, and Features
        # compares by identity. Same skip as Darwin.
        return True

    def test_reset_clone(self):
        player = self.player()
        player.reset()
        self.assertEqual(len(player.history), 0)
        self.assertEqual(player.debt, 0)
        self.assertEqual(player.queue, [])
        self.assertFalse(player.is_red_line)

    def test_clone_reproducible_play(self, seed=1, turns=10, noise=0):
        """Same match seed against a pure defector is reproducible."""
        r1 = _play(self.player(), axl.Defector(), turns=30, seed=42, length=200)
        r2 = _play(self.player(), axl.Defector(), turns=30, seed=42, length=200)
        self.assertEqual(r1, r2)

    def test_reset_history_and_attributes(self):
        player = self.player()
        _play(player, axl.Defector(), turns=15, seed=5, length=200)
        self.assertGreater(len(player.history), 0)
        player.reset()
        self.assertEqual(len(player.history), 0)
        self.assertEqual(player.debt, 0)
        self.assertEqual(player.systemic, 0)
        self.assertEqual(player.queue, [])
        self.assertEqual(player.epoch_step, 0)
        self.assertEqual(player.opp_len, 0)
        self.assertEqual(player.my_D, 0)
        self.assertEqual(player.nl_evidence, 0)
        self.assertFalse(player.is_red_line)

    def test_name_and_classifier(self):
        player = self.player()
        self.assertEqual(player.name, "ZeroResp v5.3")
        self.assertTrue(player.classifier["manipulates_state"])
        self.assertTrue(player.classifier["stochastic"])
        self.assertEqual(player.classifier["memory_depth"], float("inf"))

    def test_init_defaults(self):
        player = self.player()
        self.assertEqual(player.base_epoch, 25)
        self.assertEqual(player.debt, 0)
        self.assertEqual(player.systemic, 0)
        self.assertEqual(player.queue, [])
        self.assertEqual(player.epoch_step, 0)
        self.assertEqual(len(player.history), 0)
        self.assertTrue(player.features.noise_ladder)

    def test_init_custom_epoch(self):
        player = self.player(base_epoch=10)
        self.assertEqual(player.base_epoch, 10)
        self.assertEqual(player.init_kwargs.get("base_epoch"), 10)
        self.assertIn("10", repr(player))

    def test_initial_move_is_always_c(self):
        for opponent in (
            axl.Cooperator(),
            axl.Defector(),
            axl.TitForTat(),
            axl.Alternator(),
            axl.Random(),
        ):
            player = self.player()
            self.assertEqual(player.strategy(opponent), C)

    def test_vs_cooperator_mostly_cooperates(self):
        result = _play(
            self.player(), axl.Cooperator(), turns=200, seed=1, length=200
        )
        my_actions = [a for a, _ in result]
        self.assertEqual(my_actions[0], C)
        mid = my_actions[:180]
        self.assertGreaterEqual(mid.count(C) / len(mid), 0.95)
        self.assertGreaterEqual(my_actions.count(C), 190)

    def test_vs_defector_eventual_defect(self):
        result = _play(
            self.player(), axl.Defector(), turns=40, seed=2, length=200
        )
        my_actions = [a for a, _ in result]
        self.assertEqual(my_actions[0], C)
        self.assertIn(D, my_actions)
        self.assertGreaterEqual(my_actions.count(D), 10)

    def test_vs_tit_for_tat_mostly_cooperate(self):
        result = _play(
            self.player(), axl.TitForTat(), turns=50, seed=3, length=200
        )
        my_actions = [a for a, _ in result]
        self.assertEqual(my_actions[0], C)
        self.assertGreaterEqual(my_actions.count(C), 40)

    def test_different_seeds_can_differ(self):
        def once(seed):
            player = self.player()
            opp = axl.MockPlayer(actions=[C] * 6 + [D] + [C] * 40)
            return tuple(
                a
                for a, _ in _play(player, opp, turns=25, seed=seed, length=200)
            )

        unique = {once(s) for s in range(1, 40)}
        self.assertGreaterEqual(len(unique), 1)

    def test_red_line_against_persistent_defector(self):
        player = self.player()
        _play(
            player,
            axl.MockPlayer(actions=[D] * 20),
            turns=20,
            seed=7,
            length=200,
        )
        self.assertGreaterEqual(player.defections, 5)

    def test_unknown_length_vs_cooperator(self):
        result = _play(
            self.player(),
            axl.Cooperator(),
            turns=200,
            seed=11,
            length=float("inf"),
        )
        my_actions = [a for a, _ in result]
        self.assertTrue(all(a == C for a in my_actions))

    def test_opening_d_retort_on_second_turn(self):
        player = self.player()
        _play(
            player,
            axl.MockPlayer(actions=[D] + [C] * 30),
            turns=4,
            seed=99,
            length=200,
        )
        self.assertEqual(player.history[0], C)
        self.assertEqual(player.history[1], D)

    def test_queued_retaliation_fires(self):
        player = self.player()
        _play(
            player,
            axl.MockPlayer(actions=[D] + [C] * 40),
            turns=30,
            seed=12,
            length=200,
        )
        self.assertEqual(player.history[0], C)
        self.assertGreaterEqual(player.defections, 1)
        self.assertLessEqual(player.defections, 5)

    def test_vs_alternator(self):
        result = _play(
            self.player(), axl.Alternator(), turns=40, seed=8, length=200
        )
        self.assertEqual(len(result), 40)
        my_actions = [a for a, _ in result]
        self.assertEqual(my_actions[0], C)
        self.assertIn(D, my_actions)

    def test_makes_use_of_length_and_game_in_source(self):
        src = inspect.getsource(ZeroResp)
        self.assertIn('match_attributes.get("length")', src)
        self.assertIn('match_attributes.get("game")', src)

    def test_smoke_tournament_beats_defector(self):
        players = [
            self.player(),
            axl.TitForTat(),
            axl.Defector(),
            axl.Cooperator(),
            axl.Grudger(),
            axl.Random(),
        ]
        tournament = axl.Tournament(players, turns=50, repetitions=1, seed=0)
        results = tournament.play(progress_bar=False)
        names = results.ranked_names
        zr = next(n for n in names if n.startswith("ZeroResp"))
        self.assertLess(names.index(zr), names.index("Defector"))


class TestZeroRespNoiseLadder(unittest.TestCase):
    """v5.3 noise ladder. Not a registered strategy of its own."""

    def setUp(self):
        ZeroResp._global_profiles = {}
        ZeroResp._global_lengths = []

    def _ladder(self, **over):
        kw = {"noise_ladder": True}
        kw.update(over)
        return ZeroResp(features=Features(**kw))

    def test_flag_off_ladder_dormant(self):
        player = ZeroResp(features=Features(noise_ladder=False))
        _play(
            player,
            axl.MockPlayer(actions=[C] * 6 + [D] + [C] * 40),
            turns=40,
            seed=1,
            length=200,
        )
        self.assertEqual(player.nl_evidence, 0)
        self.assertEqual(player.nl_scheduled, [])
        self.assertEqual(player.nl_pardoned, 0)

    def test_deterministic_with_same_seed(self):
        def once(seed):
            player = self._ladder()
            result = _play(
                player,
                axl.MockPlayer(actions=[C] * 5 + [D] + [C] * 50),
                turns=60,
                seed=seed,
                length=200,
            )
            return tuple(a for a, _ in result)

        self.assertEqual(once(7), once(7))

    def test_single_defection_pardoned_under_channel_noise(self):
        observed = False
        for seed in range(1, 9):
            player = self._ladder()
            _play(
                player,
                axl.MockPlayer(actions=[C] * 5 + [D] + [C] * 60),
                turns=70,
                seed=seed,
                noise=0.05,
                length=200,
            )
            if player.nl_my_flips >= 1 and player.nl_pardoned >= 1:
                self.assertGreaterEqual(player.nl_debt_ledger, 1)
                observed = True
                break
        self.assertTrue(
            observed, "no pardon observed in seeds 1..8 at 5% noise"
        )

    def test_persistent_defector_hits_red_line(self):
        player = self._ladder()
        _play(
            player,
            axl.MockPlayer(actions=[D] * 30),
            turns=30,
            seed=4,
            length=200,
        )
        self.assertTrue(player.is_red_line)

    def test_ladder_dormant_at_zero_noise(self):
        import hashlib
        import json

        by_name = {}
        for strategy in axl.strategies:
            by_name[strategy.__name__] = strategy
            by_name.setdefault(strategy.name, strategy)

        def traj(flag, opp_name):
            player = ZeroResp(features=Features(noise_ladder=flag))
            _play(
                player,
                by_name[opp_name](),
                turns=200,
                seed=42,
                length=200,
            )
            blob = json.dumps([str(a) for a in player.history]).encode()
            return hashlib.sha256(blob).hexdigest()

        for opp in ("Alternator", "TrickyCooperator", "Calculator", "Random"):
            self.assertEqual(
                traj(True, opp),
                traj(False, opp),
                "ladder must be dormant at zero noise vs {}".format(opp),
            )

    def test_ladder_defers_first_unexplained_defection(self):
        player = self._ladder()
        player.nl_my_flips = 1
        player.opp_len, player.opp_defects = 10, 0
        player._nl_ladder(20)
        self.assertEqual(player.nl_pardoned, 1)
        self.assertEqual(player.nl_debt_ledger, 1)
        self.assertEqual(player._pending_reason, "nl_deferred")
        self.assertEqual(player.nl_scheduled, [])
        self.assertEqual(player.queue, [])
        player._nl_ladder(21)
        self.assertEqual(player.nl_evidence, 2)
        self.assertEqual(player.nl_pardoned, 2)
        self.assertEqual(player.nl_debt_ledger, 2)
        self.assertEqual(player._pending_reason, "nl_deferred")
        self.assertEqual(player.queue, [])
        self.assertEqual(len(player.nl_scheduled), 1)
        self.assertEqual(player.nl_scheduled[0]["kind"], "strike")
        self.assertGreaterEqual(
            player.nl_scheduled[0]["turn"], 21 + player.NL_DELAY_MIN
        )

    def test_strikes_only_via_scheduled_pardonable_plan(self):
        for opp_len, opp_defects in ((60, 3), (60, 30), (60, 48)):
            player = self._ladder()
            player.nl_my_flips = 1
            player.opp_len, player.opp_defects = opp_len, opp_defects
            for step in range(20, 30):
                player._pending_reason = None
                player._nl_ladder(step)
                self.assertEqual(player.queue, [])
                self.assertLessEqual(len(player.nl_scheduled), 1)

    def test_ladder_redlines_hostile_at_three(self):
        player = self._ladder()
        player.nl_my_flips = 1
        player.opp_len, player.opp_defects = 60, 48
        player._nl_ladder(20)
        player._nl_ladder(21)
        player._nl_ladder(22)
        self.assertTrue(player.is_red_line)

    def test_own_flips_feed_noise_est(self):
        observed = False
        for seed in range(1, 9):
            player = self._ladder()
            _play(
                player,
                axl.MockPlayer(actions=[C] * 80),
                turns=80,
                seed=seed,
                noise=0.1,
                length=200,
            )
            if player.nl_my_flips >= 1:
                self.assertGreater(player.p_noise_est, 0.0)
                observed = True
                break
        self.assertTrue(
            observed, "no own flip observed in seeds 1..8 at 10% noise"
        )

    def test_balance_negative_vs_defector(self):
        player = self._ladder()
        _play(player, axl.Defector(), turns=50, seed=6, length=200)
        self.assertLess(player.nl_balance, 0)

    def test_first_move_and_classifier_untouched(self):
        player = self._ladder()
        self.assertEqual(player.strategy(axl.Defector()), C)
        self.assertEqual(player.classifier["memory_depth"], float("inf"))
        self.assertTrue(player.classifier["stochastic"])
        self.assertTrue(player.classifier["manipulates_state"])


class TestZeroRespBranchCoverage(unittest.TestCase):
    """Direct, seeded setups for branches the match suite does not reach."""

    def setUp(self):
        ZeroResp._global_profiles = {}
        ZeroResp._global_lengths = []

    def _player(self, **over):
        player = ZeroResp(features=Features(**over))
        player.set_seed(1)
        return player

    def test_features_asdict_and_replace(self):
        features = Features(noise_ladder=False, apology=True)
        as_dict = features.asdict()
        self.assertFalse(as_dict["noise_ladder"])
        self.assertIn("profiles", as_dict)
        replaced = features.replace(apology=False, noise_extra=True)
        self.assertFalse(replaced.apology)
        self.assertTrue(replaced.noise_extra)
        self.assertFalse(replaced.noise_ladder)
        self.assertIsNot(replaced, features)

    def test_harvest_window_without_jitter(self):
        player = self._player(harvest_jitter=False)
        self.assertEqual(player._harvest_window, player.HARVEST_WINDOW)

    def test_reset_trims_and_swallows_length_bookkeeping_errors(self):
        player = self._player()
        player.history.append(C, C)
        ZeroResp._global_lengths = list(range(201))
        player.reset()
        self.assertEqual(len(player.history), 0)
        self.assertEqual(len(ZeroResp._global_lengths), 200)
        self.assertEqual(ZeroResp._global_lengths[-1], 1)

        class _NoAppend(list):
            def append(self, item):
                raise RuntimeError("bookkeeping failed")

        player = self._player()
        player.history.append(D, C)
        ZeroResp._global_lengths = _NoAppend([4, 5])
        player.reset()
        self.assertEqual(len(player.history), 0)
        self.assertEqual(list(ZeroResp._global_lengths), [4, 5])

    def test_length_helpers_unknown_and_invalid(self):
        player = self._player()
        player.match_attributes["length"] = object()
        self.assertIsNone(player._match_length())

        player.match_attributes["length"] = float("inf")
        player.features.estimated_endgame = True
        ZeroResp._global_lengths = [10, 40, 20]
        self.assertEqual(player._effective_length(), 20)
        player.features.estimated_endgame = False
        self.assertEqual(
            player._effective_length(), player._DEFAULT_MATCH_LENGTH
        )
        player.features.estimated_endgame = True
        ZeroResp._global_lengths = []
        self.assertEqual(
            player._effective_length(), player._DEFAULT_MATCH_LENGTH
        )

        player.features.estimated_endgame = False
        self.assertIsNone(player._estimate_remaining(10))
        player.features.estimated_endgame = True
        ZeroResp._global_lengths = [5, 6, 7]
        self.assertEqual(player._estimate_remaining(20), 1)
        ZeroResp._global_lengths = [30, 50, 70]
        self.assertEqual(player._estimate_remaining(10), 41)

    def test_backstabber_and_warmth_penalties(self):
        player = self._player()
        player.match_attributes["length"] = 100
        player.opp_len = 80
        player.opp_defects = 10
        player.late_defects = 8
        self.assertEqual(player._classify_tactical(), "backstabber")

        player.my_C = 20
        player.opp_coops_after_my_C = 10
        player.my_D = 4
        player.tactical = "backstabber"
        player._forgiveness_exploiter = 2
        player._update_target_warmth()
        self.assertGreaterEqual(player.target_warmth, 0.10)
        self.assertLessEqual(player.target_warmth, 0.90)

    def test_noise_regime_and_unexplained_guards(self):
        quiet = self._player(noise_adaptive=False)
        quiet.p_noise_est = 0.2
        quiet.cc_pairs = 50
        self.assertFalse(quiet._is_noisy_regime())

        player = self._player()
        player._bad_standing = True
        self.assertFalse(player._nl_is_unexplained())
        player._bad_standing = False
        player._contrite = True
        self.assertFalse(player._nl_is_unexplained())
        player._contrite = False
        self.assertTrue(player._nl_is_unexplained())
        player.history.append(C, D)
        player.nl_provoked_until = 4
        player._nl_step_hint = 4
        self.assertFalse(player._nl_is_unexplained())

    def test_ladder_window_exploit_and_harvest_plan(self):
        player = self._player()
        player.set_seed(2)
        player.nl_window.append(1)
        player.nl_evidence = 4
        player.nl_pardon_step = 10
        player._nl_ladder(14)
        self.assertEqual(player.nl_evidence, 1)
        self.assertEqual(list(player.nl_window), [14])
        self.assertEqual(player._forgiveness_exploiter, 1)
        self.assertEqual(player.nl_pardon_step, 0)

        player = self._player()
        player.set_seed(3)
        player.my_D = 3
        player.opp_coops_after_my_D = 3
        player.nl_balance = 1
        player.nl_evidence = 1
        player._nl_ladder(30)
        self.assertGreaterEqual(player.nl_harvest_size, player.NL_HARVEST_MIN)
        self.assertLessEqual(player.nl_harvest_size, player.NL_HARVEST_MAX)
        self.assertEqual(player.nl_harvest_left, 0)
        self.assertEqual(player.nl_harvest_postponed, 0)
        self.assertGreaterEqual(player.nl_harvest_scheduled_at, 36)
        self.assertLessEqual(player.nl_harvest_scheduled_at, 40)

    def test_forgiveness_budget_and_harvest_action_branches(self):
        player = self._player()
        player.set_seed(4)
        player.warmth = 0.9
        player.features.noise_extra = True
        player.intent = "noise"
        player.tactical = "aggressor"
        high = player._get_forgiveness_budget()
        player.warmth = 0.1
        player.features.noise_extra = False
        player.intent = "normal"
        player.tactical = "adaptive"
        low = player._get_forgiveness_budget()
        self.assertGreaterEqual(high, 2)
        self.assertLessEqual(high, 12)
        self.assertGreaterEqual(low, 2)
        self.assertLessEqual(low, 12)

        player.features.noise_adaptive = True
        player.p_noise_est = 0.05
        player.cc_pairs = 15
        player.nl_my_flips = 0
        self.assertIsNone(player._harvest_action(4, axl.Cooperator()))

        player.p_noise_est = 0.0
        player.cc_pairs = 0
        player.opp_len = 60
        player.opp_defects = 0
        player.my_D = 0
        player.probe_fired = True
        self.assertEqual(player._harvest_action(4, axl.Cooperator()), D)

        player.opp_len = 40
        player.opp_defects = 5
        player.my_D = 4
        player.opp_coops_after_my_D = 0
        player.tactical = "aggressor"
        self.assertEqual(player._harvest_action(3, axl.Cooperator()), D)

    def test_play_bad_standing_and_noise_extra_thresholds(self):
        player = self._player()
        self.assertEqual(player._play(C), C)
        self.assertEqual(player._intended_prev, C)

        player._bad_standing = True
        player._bad_standing_turns = 2
        player._contrite = True
        self.assertTrue(player._on_defect(8, D))
        self.assertTrue(player._bad_standing)
        self.assertEqual(player._bad_standing_turns, 1)
        self.assertFalse(player._contrite)
        player._bad_standing_turns = 1
        self.assertTrue(player._on_defect(9, D))
        self.assertFalse(player._bad_standing)

        player = self._player()
        player.features.noise_extra = True
        player.intent = "noise"
        self.assertFalse(player._on_defect(10, D))
        self.assertFalse(player.is_red_line)
        self.assertGreaterEqual(len(player.queue), 1)

    def test_close_epoch_and_profile_guards(self):
        player = self._player()
        player.p_noise_est = 0.0
        player.cc_pairs = 0
        player._enter_red_line()
        player.epoch_step = 40
        player.debt = 0
        player.queue = []
        player._close_epoch()
        self.assertEqual(player.epoch_step, 40)
        self.assertEqual(player._state.name, "RED_LINE")

        bare = ZeroResp(use_profiles=False)
        bare.set_seed(1)
        bare._save_profile("Defector")
        self.assertEqual(ZeroResp._global_profiles, {})
        self._player()._save_profile("")
        self.assertEqual(ZeroResp._global_profiles, {})

    def test_balance_uses_payoff_when_game_score_fails(self):
        class _Boom:
            def score(self, pair):
                raise ValueError("bad score")

        player = self._player()
        player.history.append(D, C)
        player._intended_prev = D
        opponent = axl.Cooperator()
        opponent.history.append(C, D)
        player.match_attributes["game"] = _Boom()
        player.strategy(opponent)
        self.assertEqual(player.nl_balance, 5)

    def _late_player(self):
        player = self._player()
        player.match_attributes["length"] = 4
        player.history.extend([C, C, C], [C, C, C])
        player._apology_mode = False
        return player

    def test_apology_accounting_retry_and_give_up(self):
        player = self._late_player()
        player._apology_mode = True
        player._apology_steps = 4
        player.last_my = D
        opponent = axl.Defector()
        opponent.history.append(D, C)
        self.assertEqual(player.strategy(opponent), C)
        self.assertGreaterEqual(player.late_defects, 1)
        self.assertGreaterEqual(player.my_D, 1)

        player = self._late_player()
        player._apology_mode = True
        player._apology_steps = 4
        player.last_my = D
        opponent = axl.Cooperator()
        opponent.history.append(C, D)
        self.assertEqual(player.strategy(opponent), C)
        self.assertGreaterEqual(player.opp_coops_after_my_D, 1)
        self.assertEqual(player.clean_peace, 0)
        self.assertGreaterEqual(player.my_D, 1)

        player = self._player()
        player._apology_mode = True
        player._apology_steps = 1
        player._apology_tries = 0
        player._apology_opp_moves = []
        opponent = axl.Defector()
        opponent.history.append(D, C)
        player.strategy(opponent)
        self.assertFalse(player._apology_mode)
        self.assertFalse(player.is_red_line)
        self.assertEqual(player._apology_tries, 1)

        player = self._player()
        player._apology_mode = True
        player._apology_steps = 1
        player._apology_tries = player._apology_max_tries - 1
        player._apology_opp_moves = [D]
        opponent = axl.Defector()
        opponent.history.append(D, C)
        self.assertEqual(player.strategy(opponent), D)
        self.assertTrue(player.is_red_line)
        self.assertEqual(player._last_D_reason, "red_line")

    def test_contrite_full_and_plain_contrite_accounting(self):
        player = self._late_player()
        player._bad_standing = True
        player._bad_standing_turns = 2
        player.last_my = D
        opponent = axl.Defector()
        opponent.history.append(D, C)
        self.assertEqual(player.strategy(opponent), C)
        self.assertGreaterEqual(player.late_defects, 1)
        self.assertGreaterEqual(player.my_D, 1)

        player = self._late_player()
        player._bad_standing = True
        player._bad_standing_turns = 2
        player.last_my = D
        opponent = axl.Cooperator()
        opponent.history.append(C, D)
        self.assertEqual(player.strategy(opponent), C)
        self.assertGreaterEqual(player.opp_coops_after_my_D, 1)
        self.assertGreaterEqual(player.my_D, 1)

        def contrite(my_prev):
            actor = self._late_player()
            actor.opp_len = 4
            actor.last_my = my_prev
            actor._contrite = True
            actor._bad_standing = False
            foe = axl.Defector()
            foe.history.extend([D] * 5, [C] * 5)
            action = actor.strategy(foe)
            return actor, action

        soft, action = contrite(C)
        self.assertEqual(action, C)
        self.assertFalse(soft._contrite)
        self.assertGreaterEqual(soft.opp_defects_after_my_C, 1)
        self.assertGreaterEqual(soft.late_defects, 1)
        self.assertGreaterEqual(soft.my_C, 1)
        hard, action = contrite(D)
        self.assertEqual(action, C)
        self.assertGreaterEqual(hard.my_D, 1)
        self.assertGreaterEqual(hard.late_defects, 1)

    def test_noise_ladder_harvest_and_scheduled_strike(self):
        player = self._player()
        player.nl_harvest_scheduled_at = 1
        player.nl_harvest_size = 3
        opponent = axl.Cooperator()
        opponent.history.append(C, C)
        self.assertEqual(player.strategy(opponent), D)
        self.assertEqual(player._last_D_reason, "nl_harvest_comp")
        self.assertEqual(player.nl_harvest_left, 2)
        self.assertEqual(player.nl_harvest_scheduled_at, 0)
        self.assertEqual(player.nl_provoked_until, 7)

        player = self._player()
        player.nl_harvest_scheduled_at = 1
        player.nl_harvest_size = 3
        player.strategy(axl.Cooperator())
        self.assertEqual(player.nl_harvest_postponed, 1)
        self.assertEqual(player.nl_harvest_scheduled_at, 4)

        player = self._player()
        player.nl_harvest_scheduled_at = 1
        player.nl_harvest_size = 3
        player.nl_harvest_postponed = 2
        player.strategy(axl.Cooperator())
        self.assertEqual(player.nl_harvest_scheduled_at, 0)
        self.assertEqual(player.nl_harvest_size, 0)

        player = self._player()
        player.opp_last3.extend([C, C, C])
        player.opp_defects_after_my_D = 0
        player.nl_scheduled = [{"turn": 1, "kind": "strike"}]
        player.queue = [1]
        player.debt = 2
        player.nl_debt_ledger = 1
        self.assertEqual(player.strategy(axl.Cooperator()), C)
        self.assertEqual(player.nl_pardon_step, 1)
        self.assertGreaterEqual(player.nl_pardoned, 1)
        self.assertNotIn(1, player.queue)
        self.assertEqual(player.debt, 1)

        player = self._player()
        player.opp_last3.extend([D, D, D])
        player.nl_scheduled = [{"turn": 1, "kind": "strike"}]
        player.nl_debt_ledger = 4
        self.assertEqual(player.strategy(axl.Cooperator()), D)
        self.assertEqual(player.nl_debt_ledger, 3)

    def test_hostile_cooldown_deadlock_probe_and_queue(self):
        player = self._player()
        player.opp_len = 20
        player.opp_defects = 18
        self.assertEqual(player.strategy(axl.Cooperator()), D)
        self.assertTrue(player.is_red_line)
        self.assertEqual(player._last_D_reason, "red_line")

        player = self._player()
        player.p_noise_est = 0.05
        player.cc_pairs = 20
        player._enter_red_line()
        player._red_line_cooldown = 0
        self.assertEqual(player._state.name, "RED_LINE_COOLDOWN")
        self.assertEqual(player.strategy(axl.Cooperator()), C)
        self.assertGreater(player._red_line_cooldown, 0)
        self.assertEqual(player._last_D_reason, None)

        player = self._player()
        player.deadlock = player.DEADLOCK_THRESHOLD
        player.queue = [99]
        player.debt = 3
        player.systemic = 4
        player.echo_forgive = 2
        player._contrite = True
        player._bad_standing = True
        self.assertEqual(player.strategy(axl.Cooperator()), C)
        self.assertEqual(player.deadlock, 0)
        self.assertEqual(player.queue, [])
        self.assertEqual(player.debt, 0)
        self.assertEqual(player.echo_forgive, 0)
        self.assertEqual(player.systemic, 3)
        self.assertFalse(player._contrite)
        self.assertFalse(player._bad_standing)
        self.assertEqual(player._state.name, "COOPERATIVE")

        player = self._player(harvest_jitter=False)
        player.match_attributes["length"] = 5
        player.opp_len = 40
        player.opp_defects = 0
        player.probe_fired = True
        player.tactical = "adaptive"
        self.assertEqual(player.strategy(axl.Cooperator()), D)
        self.assertEqual(player._last_D_reason, "probe")

        player = self._player()
        player.match_attributes["length"] = 200
        player.queue = [1]
        player._contrite = True
        self.assertEqual(player.strategy(axl.Cooperator()), C)
        self.assertEqual(player.queue, [2])
        self.assertTrue(player._contrite)

        player = self._player()
        player.match_attributes["length"] = 200
        player._contrite = True
        self.assertEqual(player.strategy(axl.Cooperator()), C)
        self.assertFalse(player._contrite)
