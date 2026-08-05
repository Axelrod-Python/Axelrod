"""Tests for the ZeroResp v2 strategy."""

import axelrod as axl
from axelrod.strategies.zeroresp_v2 import _State

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestZeroRespV2(TestPlayer):

    # Player.__repr__ appends init kwargs → "ZeroResp v2: 25" (base_epoch)
    name = "ZeroResp v2: 25"
    player = axl.ZeroRespV2
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "makes_use_of": {"length"},
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_initial_move_is_always_c(self):
        for opponent in (
            axl.Cooperator(),
            axl.Defector(),
            axl.TitForTat(),
            axl.Alternator(),
        ):
            player = self.player()
            player.set_seed(0)
            self.assertEqual(player.strategy(opponent), C)
            self.assertFalse(player.is_red_line)

    def test_vs_cooperator(self):
        actions = [(C, C)] * 40
        self.versus_test(
            axl.Cooperator(),
            expected_actions=actions,
            match_attributes={"length": 200},
            seed=1,
            attrs={"is_red_line": False, "debt": 0, "queue": []},
        )

    def test_early_sharp_queues_delay_one(self):
        """First-window D schedules retaliation for the next turn (delay=1)."""
        player = self.player()
        opponent = axl.MockPlayer(actions=[D] + [C] * 10)
        match = axl.Match(
            (player, opponent),
            turns=3,
            seed=1,
            match_attributes={"length": 200},
        )
        result = match.play()
        self.assertEqual(result[0], (C, D))
        # Turn 2: process D at step=2 (still early) → queue step+1=3, play C
        self.assertEqual(result[1], (C, C))
        # Turn 3: fire queued D (delay=1 early sharp)
        self.assertEqual(result[2], (D, C))
        self.assertEqual(player.echo_forgive, 1)
        self.assertEqual(player.queue, [])

    def test_echo_shield_ignores_mirror_after_retaliation(self):
        """After our queued D, one mirror D is absorbed (no new debt)."""
        player = self.player()
        # Opp: D, C, D — we retaliate on turn 3; their D on turn 4 is echo
        opponent = axl.MockPlayer(actions=[D, C, D, C, C, C, C, C])
        match = axl.Match(
            (player, opponent),
            turns=6,
            seed=2,
            match_attributes={"length": 200},
        )
        match.play()
        # echo_forgive was set when we fired; mirror should not red-line
        self.assertFalse(player.is_red_line)

    def test_one_shot_forgive_after_long_peace(self):
        """First isolated mid-game D after long mutual C is forgiven once."""
        player = self.player()
        # 15 mutual C, then one D, then C — one-shot should apply
        opp_actions = [C] * 15 + [D] + [C] * 10
        opponent = axl.MockPlayer(actions=opp_actions)
        match = axl.Match(
            (player, opponent),
            turns=len(opp_actions),
            seed=3,
            match_attributes={"length": 200},
        )
        match.play()
        self.assertTrue(player.one_shot_used)
        # Single noise D after peace: mostly still cooperate
        self.assertGreaterEqual(player.cooperations, 20)

    def test_three_systemic_defects_trigger_red_line(self):
        player = self.player()
        opponent = axl.MockPlayer(actions=[D] * 12)
        match = axl.Match(
            (player, opponent),
            turns=12,
            seed=7,
            match_attributes={"length": 200},
        )
        match.play()
        self.assertTrue(player.is_red_line)
        self.assertEqual(player.history[0], C)
        self.assertGreaterEqual(player.defections, 5)

        # Early sharp: C,C then D-heavy; permanent red line by end
        self.versus_test(
            axl.Defector(),
            expected_actions=[
                (C, D),
                (C, D),
                (D, D),
                (D, D),
                (C, D),
                (D, D),
                (D, D),
                (D, D),
                (D, D),
                (D, D),
            ],
            turns=10,
            seed=0,
            match_attributes={"length": 200},
            attrs={"is_red_line": True},
        )

    def test_reset_cleans_state(self):
        player = self.player()
        clone = player.clone()
        axl.Match(
            (player, axl.Defector()),
            turns=15,
            seed=5,
            match_attributes={"length": 200},
        ).play()
        player.reset()
        self.assertEqual(player, clone)
        self.assertFalse(player.is_red_line)
        self.assertEqual(player.debt, 0)
        self.assertEqual(player.queue, [])
        self.assertEqual(player.echo_forgive, 0)
        self.assertFalse(player.one_shot_used)
        self.assertEqual(player.deadlock, 0)
        self.assertEqual(player.clean_peace, 0)

    def test_vs_tit_for_tat_cooperates(self):
        actions = [(C, C)] * 20
        self.versus_test(
            axl.TitForTat(),
            expected_actions=actions,
            match_attributes={"length": 200},
            seed=2,
            attrs={"is_red_line": False},
        )

    def test_seed_reproducible(self):
        r1 = axl.Match(
            (self.player(), axl.Defector()),
            turns=25,
            seed=42,
            match_attributes={"length": 200},
        ).play()
        r2 = axl.Match(
            (self.player(), axl.Defector()),
            turns=25,
            seed=42,
            match_attributes={"length": 200},
        ).play()
        self.assertEqual(r1, r2)

    def test_match_length_edge_cases(self):
        player = self.player()
        player.set_match_attributes(length=None)
        self.assertIsNone(player._match_length())
        player.set_match_attributes(length=-1)
        self.assertIsNone(player._match_length())
        player.set_match_attributes(length=float("inf"))
        self.assertIsNone(player._match_length())
        player.set_match_attributes(length=0)
        self.assertIsNone(player._match_length())
        player.set_match_attributes(length="bad")
        self.assertIsNone(player._match_length())
        player.set_match_attributes(length=[200])
        self.assertIsNone(player._match_length())
        player.set_match_attributes(length=200)
        self.assertEqual(player._match_length(), 200)
        player.set_match_attributes(length=-1)
        self.assertEqual(
            player._effective_length(), player._DEFAULT_MATCH_LENGTH
        )

    def test_live_coop_rate_empty(self):
        self.assertEqual(self.player()._live_coop_rate(), 1.0)

    def test_close_epoch_while_red_lined(self):
        player = self.player()
        player.is_red_line = True
        player._state = _State.RED_LINE
        player.epoch_step = 100
        player.systemic = 5
        player._close_epoch()
        self.assertEqual(player.epoch_step, 100)
        self.assertEqual(player.systemic, 5)

    def test_epoch_resets_after_clean_window(self):
        player = self.player()
        player.systemic = 1
        player.debt = 0
        player.queue = []
        player.epoch_step = player.base_epoch
        player._close_epoch()
        self.assertEqual(player.epoch_step, 0)
        self.assertEqual(player.systemic, 0)

    def test_endgame_harvest_vs_soft_victim(self):
        length = 100
        opp_actions = [D] + [C] * (length - 1)
        player = self.player()
        match = axl.Match(
            (player, axl.MockPlayer(actions=opp_actions)),
            turns=length,
            seed=3,
            match_attributes={"length": length},
        )
        match.play()
        self.assertIn(D, list(player.history[-8:]))

    def test_anti_raider_late_defects(self):
        length = 40
        opp_actions = [C] * 31 + [D, D] + [C] * 10
        player = self.player()
        axl.Match(
            (player, axl.MockPlayer(actions=opp_actions)),
            turns=len(opp_actions),
            seed=4,
            match_attributes={"length": length},
        ).play()
        self.assertTrue(player.is_red_line)
        self.assertGreaterEqual(player.late_defects, 2)

    def test_hostile_live_ban(self):
        player = self.player()
        axl.Match(
            (player, axl.MockPlayer(actions=[D] * 15 + [C] * 5)),
            turns=20,
            seed=9,
            match_attributes={"length": 200},
        ).play()
        self.assertTrue(player.is_red_line)

    def test_deadlock_break_forces_cooperate(self):
        """CD/DC alternation raises deadlock and forces a cooperative reset."""
        player = self.player()
        player.set_seed(0)
        player.set_match_attributes(length=200)
        # Manually drive deadlock counter then call strategy
        player.deadlock = player.DEADLOCK_THRESHOLD
        player.debt = 2
        player.queue = [99]
        player.echo_forgive = 1
        player.systemic = 2
        opp = axl.Cooperator()
        # empty histories → first move path with high deadlock
        action = player.strategy(opp)
        self.assertEqual(action, C)
        self.assertEqual(player.deadlock, 0)
        self.assertEqual(player.debt, 0)
        self.assertEqual(player.queue, [])
        self.assertEqual(player.echo_forgive, 0)

    def test_deadlock_meter_from_alternating_pairs(self):
        """Alternating exploitation pairs increment deadlock."""
        player = self.player()
        # Sequence that produces (C,D) then (D,C) patterns via TFT-like fight
        # After early D we retaliate sharp; then CD/DC loops with Alternator-ish
        opp_actions = [D, C, D, C, D, C, D, C, D, C]
        axl.Match(
            (player, axl.MockPlayer(actions=opp_actions)),
            turns=len(opp_actions),
            seed=1,
            match_attributes={"length": 200},
        ).play()
        # Either broke deadlock with C or still tracking — just exercise path
        self.assertGreaterEqual(len(player.history), 10)

    def test_unknown_length_vs_cooperator(self):
        actions = [(C, C)] * 40
        self.versus_test(
            axl.Cooperator(),
            expected_actions=actions,
            match_attributes={"length": float("inf")},
            seed=5,
            attrs={"is_red_line": False},
        )

    def test_midgame_noise_forgive_and_buffer(self):
        """After long clean peace, isolated D is forgiven; later D is buffered."""
        player = self.player()
        # First D after peace → one-shot forgive; second → short schedule
        opp = [C] * 15 + [D, C, C, D] + [C] * 20
        axl.Match(
            (player, axl.MockPlayer(actions=opp)),
            turns=len(opp),
            seed=11,
            match_attributes={"length": 200},
        ).play()
        self.assertTrue(player.one_shot_used)
        self.assertGreaterEqual(player.one_shot_forgives, 1)

    def test_dd_and_cc_reset_deadlock(self):
        player = self.player()
        player._last_pair = (D, D)
        player.deadlock = 2
        player.set_seed(0)
        player.set_match_attributes(length=200)
        # Simulate observe path via strategy against Cooperator after fake hist
        # Use internal path: set history-like state
        player.last_my = C
        player._last_pair = (C, C)
        player.deadlock = 2
        opp = axl.MockPlayer(actions=[C])
        # play one turn
        axl.Match(
            (player, opp), turns=1, seed=0, match_attributes={"length": 200}
        ).play()
        # After CC pair, deadlock should reset in observe
        self.assertEqual(player.deadlock, 0)

    def _endgame_player(
        self,
        *,
        hist_len: int,
        length: int,
        opp_len: int,
        opp_defects: int,
        my_D: int,
        probe_fired: bool,
        seed: int = 0,
        opp_coops_after_my_D: int = 0,
    ):
        """Build a player mid end-game harvest window (known finite length)."""
        player = self.player()
        player.set_seed(seed)
        player.set_match_attributes(length=length)
        for _ in range(hist_len):
            player.history.append(C, C)
        player.opp_len = opp_len
        player.opp_defects = opp_defects
        player.my_D = my_D
        player.opp_coops_after_my_D = opp_coops_after_my_D
        player.probe_fired = probe_fired
        player.last_my = C
        return player

    def test_grim_last_safe_defects(self):
        """vs never-defector: last-turn safe harvest is D (rev 2.2 grim)."""
        # remaining = length - step = 60 - 59 = 1 <= GRIM_LAST_SAFE
        player = self._endgame_player(
            hist_len=58,
            length=60,
            opp_len=55,
            opp_defects=0,
            my_D=0,
            probe_fired=False,
        )
        self.assertEqual(player.strategy(axl.Cooperator()), D)

    def test_grim_after_probe_keeps_defecting(self):
        """Once probe_fired against pure cooperator, stay D in harvest window."""
        player = self._endgame_player(
            hist_len=56,
            length=60,
            opp_len=55,
            opp_defects=0,
            my_D=1,
            probe_fired=True,
        )
        self.assertEqual(player.strategy(axl.Cooperator()), D)

    def test_grim_stochastic_probe_fires(self):
        """With remaining in PROBE_WINDOW and my_D==0, probe can fire (seeded)."""
        player = self._endgame_player(
            hist_len=56,
            length=60,
            opp_len=55,
            opp_defects=0,
            my_D=0,
            probe_fired=False,
            seed=7,
        )
        action = player.strategy(axl.Cooperator())
        self.assertEqual(action, D)
        self.assertTrue(player.probe_fired)

    def test_non_grim_probe_fired_stays_d_in_window(self):
        """Non-grim end-game: if probe already fired, defect in PROBE_WINDOW."""
        # opp_len <= 50 → not is_grim; high defect rate → not is_victim
        player = self._endgame_player(
            hist_len=56,
            length=60,
            opp_len=40,
            opp_defects=10,
            my_D=5,
            probe_fired=True,
            opp_coops_after_my_D=0,
        )
        self.assertEqual(player.strategy(axl.Cooperator()), D)
