"""Tests for the ZeroResp strategy."""

import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestZeroResp(TestPlayer):

    name = "ZeroResp"
    player = axl.ZeroResp
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
        """Initial move is always C against any opponent."""
        for opponent in (
            axl.Cooperator(),
            axl.Defector(),
            axl.TitForTat(),
            axl.Alternator(),
            axl.Random(),
        ):
            player = self.player()
            player.set_seed(0)
            self.assertEqual(player.strategy(opponent), C)
            self.assertFalse(player.is_red_line)
            self.assertEqual(player.queue, [])

    def test_vs_cooperator(self):
        """Never-defectors are grim-safe: full cooperation on known length."""
        actions = [(C, C)] * 50
        self.versus_test(
            axl.Cooperator(),
            expected_actions=actions,
            match_attributes={"length": 200},
            seed=1,
            attrs={"is_red_line": False, "debt": 0, "queue": []},
        )

    def test_single_defect_queues_buffer_retaliation(self):
        """
        A single D does not trigger immediate retaliation; a delayed D is
        queued (buffer = 5 + U{1..10}) and fires later.
        """
        # seed=1 → first delay draw yields a known schedule:
        # turn 1: (C, D); turn 2 processes D and queues step 2 + delay.
        # Under non-hostile samples delay ∈ [6, 15], so turn 2 is still C.
        player = self.player()
        opponent = axl.MockPlayer(actions=[D] + [C] * 30)
        match = axl.Match(
            (player, opponent),
            turns=2,
            seed=1,
            match_attributes={"length": 200},
        )
        result = match.play()
        self.assertEqual(result[0], (C, D))
        self.assertEqual(result[1], (C, C))  # buffered — not immediate D
        self.assertFalse(player.is_red_line)
        self.assertEqual(player.debt, 1)
        self.assertEqual(len(player.queue), 1)
        scheduled = player.queue[0]
        self.assertGreaterEqual(scheduled, 2 + 6)  # 5 + min U{1..10}
        self.assertLessEqual(scheduled, 2 + 15)  # 5 + max U{1..10}

        # Continue until the queued strike fires: exactly one delayed D.
        player2 = self.player()
        opponent2 = axl.MockPlayer(actions=[D] + [C] * 40)
        match2 = axl.Match(
            (player2, opponent2),
            turns=30,
            seed=1,
            match_attributes={"length": 200},
        )
        match2.play()
        self.assertEqual(player2.history[0], C)
        self.assertEqual(player2.defections, 1)
        self.assertFalse(player2.is_red_line)
        # After the single strike clears debt/queue, no permanent ban.
        self.assertEqual(player2.queue, [])

    def test_three_systemic_defects_trigger_red_line(self):
        """
        Three opponent defections while debt/queue is open raise the
        systemic counter and set is_red_line permanently True.
        """
        # Consecutive D keeps debt open between events:
        # 1st D opens debt (not yet systemic), 2nd → systemic=1,
        # 3rd → systemic=2 ≥ threshold 2 → RED_LINE.
        player = self.player()
        opponent = axl.MockPlayer(actions=[D] * 10)
        match = axl.Match(
            (player, opponent),
            turns=10,
            seed=7,
            match_attributes={"length": 200},
        )
        match.play()
        self.assertTrue(player.is_red_line)
        # After red line, remaining replies are unconditional D.
        # First move C; after third processed D (around turn 4) permanent D.
        self.assertEqual(player.history[0], C)
        self.assertGreaterEqual(player.defections, 5)
        # Permanent: still red-lined at end of match.
        self.assertTrue(player.is_red_line)
        self.assertEqual(player.queue, [])

        # versus_test form with attrs check at end of match.
        # Turns 1–3: C while debt accumulates; turn 4+: permanent D (red line).
        self.versus_test(
            axl.Defector(),
            expected_actions=[(C, D)] * 3 + [(D, D)] * 7,
            turns=10,
            seed=0,
            match_attributes={"length": 200},
            attrs={"is_red_line": True},
        )

    def test_reset_cleans_state_for_multi_rep_tournaments(self):
        """reset() restores a clean match state (multi-rep tournaments)."""
        player = self.player()
        clone = player.clone()
        opponent = axl.Defector()
        match = axl.Match(
            (player, opponent),
            turns=20,
            seed=11,
            match_attributes={"length": 200},
        )
        match.play()
        self.assertGreater(len(player.history), 0)
        self.assertTrue(
            player.is_red_line or player.debt > 0 or player.defections > 0
        )

        player.reset()
        self.assertEqual(player, clone)
        self.assertEqual(len(player.history), 0)
        self.assertFalse(player.is_red_line)
        self.assertEqual(player.debt, 0)
        self.assertEqual(player.systemic, 0)
        self.assertEqual(player.queue, [])
        self.assertEqual(player.epoch_step, 0)
        self.assertEqual(player.opp_len, 0)
        self.assertEqual(player.opp_defects, 0)
        self.assertEqual(player.my_D, 0)
        self.assertEqual(player.late_defects, 0)
        self.assertEqual(player.last_my, C)

        # Second match after reset still starts with C
        match2 = axl.Match(
            (player, axl.Cooperator()),
            turns=5,
            seed=3,
            match_attributes={"length": 200},
        )
        result = match2.play()
        self.assertEqual(result[0], (C, C))
        self.assertFalse(player.is_red_line)

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
        actions = None
        for _ in range(2):
            player = self.player()
            opponent = axl.Defector()
            match = axl.Match(
                (player, opponent),
                turns=25,
                seed=42,
                match_attributes={"length": 200},
            )
            result = match.play()
            if actions is None:
                actions = result
            else:
                self.assertEqual(result, actions)

    def test_unknown_length_vs_cooperator(self):
        """Unknown / infinite length: no end-game harvest of pure C."""
        actions = [(C, C)] * 40
        self.versus_test(
            axl.Cooperator(),
            expected_actions=actions,
            match_attributes={"length": float("inf")},
            seed=5,
            attrs={"is_red_line": False},
        )

    def test_match_length_edge_cases(self):
        """Cover _match_length branches: invalid, non-positive, None."""
        player = self.player()
        player.set_match_attributes(length=None)
        self.assertIsNone(player._match_length())

        player.set_match_attributes(length=-1)
        self.assertIsNone(player._match_length())

        player.set_match_attributes(length=float("inf"))
        self.assertIsNone(player._match_length())

        player.set_match_attributes(length=0)
        self.assertIsNone(player._match_length())

        player.set_match_attributes(length="not-a-number")
        self.assertIsNone(player._match_length())

        player.set_match_attributes(length=[200])  # TypeError on int()
        self.assertIsNone(player._match_length())

        player.set_match_attributes(length=200)
        self.assertEqual(player._match_length(), 200)
        self.assertEqual(player._effective_length(), 200)

        # Fallback when length unknown
        player.set_match_attributes(length=-1)
        self.assertEqual(
            player._effective_length(), player._DEFAULT_MATCH_LENGTH
        )

    def test_live_coop_rate_empty_history(self):
        """With no observations, live coop rate defaults to 1.0."""
        player = self.player()
        self.assertEqual(player.opp_len, 0)
        self.assertEqual(player._live_coop_rate(), 1.0)

    def test_close_epoch_while_red_lined(self):
        """_close_epoch is a no-op once is_red_line is set."""
        from axelrod.strategies.zeroresp import _State

        player = self.player()
        player.is_red_line = True
        player._state = _State.RED_LINE
        player.epoch_step = 100
        player.systemic = 5
        player._close_epoch()
        # Counters must not reset under red line
        self.assertEqual(player.epoch_step, 100)
        self.assertEqual(player.systemic, 5)
        self.assertTrue(player.is_red_line)

    def test_epoch_resets_after_clean_window(self):
        """After base_epoch clean turns, systemic counter resets."""
        player = self.player()
        player.set_seed(0)
        # Force equalising history then clear debt/queue and advance epoch
        player.systemic = 1
        player.debt = 0
        player.queue = []
        player.epoch_step = player.base_epoch
        player._close_epoch()
        self.assertEqual(player.epoch_step, 0)
        self.assertEqual(player.systemic, 0)

    def test_endgame_harvest_vs_soft_victim(self):
        """
        Near a known match end, defect against a near-pure cooperator that
        defected once early (victim, not grim).
        """
        length = 100
        # One early D, then all C — low defect rate, not grim.
        opp_actions = [D] + [C] * (length - 1)
        player = self.player()
        opponent = axl.MockPlayer(actions=opp_actions)
        match = axl.Match(
            (player, opponent),
            turns=length,
            seed=3,
            match_attributes={"length": length},
        )
        match.play()
        # Late turns should include harvest D (p_end high, opp_len > 50)
        late = list(player.history[-8:])
        self.assertIn(D, late)

    def test_anti_raider_late_defects(self):
        """Two late-game opponent defects trigger immediate red line."""
        length = 40
        # All C until late phase, then two Ds past 75% mark (threshold=30)
        opp_actions = [C] * 31 + [D, D] + [C] * 10
        player = self.player()
        opponent = axl.MockPlayer(actions=opp_actions)
        match = axl.Match(
            (player, opponent),
            turns=len(opp_actions),
            seed=4,
            match_attributes={"length": length},
        )
        match.play()
        self.assertTrue(player.is_red_line)
        self.assertGreaterEqual(player.late_defects, 2)

    def test_hostile_short_delay_and_live_ban(self):
        """High defect rate → hostile path (delay=1 / red line)."""
        player = self.player()
        # 10+ samples with coop_rate < 0.4 → _is_hostile
        opponent = axl.MockPlayer(actions=[D] * 15 + [C] * 5)
        match = axl.Match(
            (player, opponent),
            turns=20,
            seed=9,
            match_attributes={"length": 200},
        )
        match.play()
        self.assertTrue(player.is_red_line)

    def test_forgiveness_cadastre_after_our_defect(self):
        """Opponent C after our D increments opp_coops_after_my_D."""
        player = self.player()
        # One early D from them → we queue strike; then they C while we may D
        opponent = axl.MockPlayer(actions=[D] + [C] * 40)
        match = axl.Match(
            (player, opponent),
            turns=30,
            seed=1,
            match_attributes={"length": 200},
        )
        match.play()
        # After our delayed D, further opponent C should raise forgiveness count
        self.assertGreaterEqual(player.opp_coops_after_my_D, 0)
        self.assertGreaterEqual(player.my_D, 1)
