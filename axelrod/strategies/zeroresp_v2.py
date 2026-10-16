"""
ZeroResp v2 (revision 2.2): adaptive IPD strategy.

Tournament-tuned state machine with short adaptive retaliation, noise-aware
forgiveness, deadlock recovery, red-line ban, and smart end-game logic.
"""

from __future__ import annotations

from enum import Enum, auto
from typing import List, Optional, Tuple

from axelrod.action import Action
from axelrod.player import Player

C, D = Action.C, Action.D


class _State(Enum):
    """Internal finite-state labels."""

    COOPERATIVE = auto()
    EQUALIZING = auto()
    RED_LINE = auto()


class ZeroRespV2(Player):
    """
    ZeroResp v2 — tournament-tuned adaptive state machine (revision 2.2).

    Keeps the ZeroResp backbone (dynamic epochs, systemic red line, anti-raider)
    and adds:

    1. **Early sharp** — in the first few turns, retaliate with delay 1 so
       probers that check early punishment are answered.
    2. **Short adaptive buffer** — mid-game delay is 1–2 turns (not a long
       6–16 window), collapsing to 1 under hostility or late pressure.
    3. **Contrition / echo-shield** — after a queued retaliatory D, ignore one
       mirror D to avoid cascade wars with Suspicious TFT-style reciprocators.
    4. **Noise-aware one-shot forgive** — isolated mid-game D after a long clean
       mutual-cooperation stretch is treated as noise (up to twice per match).
    5. **Deadlock break** — CD/DC alternating loops force a cooperative reset
       (Omega-TFT inspired) without permanent softness.
    6. **Smart end-game harvest / grim probe** — only with known finite length
       and a short remaining horizon; cautious against never-defectors.

    Names:

    - ZeroResp v2: Library display name
    - ZeroResp v2.2: Implementation revision (this module)
    - ZeroRespV2: Class identifier
    """

    name = "ZeroResp v2"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    _DEFAULT_MATCH_LENGTH = 200
    _LATE_FRACTION = 0.75
    _LIVE_INTEL_MIN_SAMPLES = 10
    _HOSTILE_COOP_THRESHOLD = 0.4
    _SOFT_HOSTILE_COOP = 0.7

    EARLY_WINDOW = 5
    ONE_SHOT_PEACE = 12
    DEADLOCK_THRESHOLD = 3

    # revision 2.2 tuning
    HARVEST_WINDOW = 5
    HARVEST_FORGIVENESS = 0.8
    ONE_SHOT_MAX = 2
    GRIM_LAST_SAFE = 1
    PROBE_WINDOW = 4
    PROBE_PROB = 0.15

    def __init__(self, base_epoch: int = 25) -> None:
        """Initialise epoch, red-line, and v2 counters."""
        super().__init__()
        self.base_epoch = int(base_epoch)
        self._init_state()

    def _init_state(self) -> None:
        self._state = _State.COOPERATIVE
        self.is_red_line = False
        self.epoch_step = 0
        self.debt = 0
        self.systemic = 0
        self.queue: List[int] = []

        self.opp_len = 0
        self.opp_defects = 0
        self.opp_coops_after_my_D = 0
        self.my_D = 0
        self.last_my: Action = C
        self.late_defects = 0

        self.echo_forgive = 0
        self.one_shot_forgives = 0
        self.one_shot_used = False
        self.clean_peace = 0
        self.deadlock = 0
        self._last_pair: Optional[Tuple[Action, Action]] = None
        self.probe_fired = False

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _match_length(self) -> Optional[int]:
        """Return known finite match length, else ``None``."""
        length = self.match_attributes["length"]
        if length is None or length in (-1, float("inf")):
            return None
        try:
            length_int = int(length)
        except (TypeError, ValueError):
            return None
        return length_int if length_int > 0 else None

    def _effective_length(self) -> int:
        return self._match_length() or self._DEFAULT_MATCH_LENGTH

    def _late_threshold(self) -> int:
        return int(self._effective_length() * self._LATE_FRACTION)

    def _live_coop_rate(self) -> float:
        if self.opp_len == 0:
            return 1.0
        return 1.0 - (self.opp_defects / self.opp_len)

    def _is_hostile(self) -> bool:
        return (
            self.opp_len >= self._LIVE_INTEL_MIN_SAMPLES
            and self._live_coop_rate() < self._HOSTILE_COOP_THRESHOLD
        )

    def _is_soft_hostile(self) -> bool:
        return (
            self.opp_len >= self._LIVE_INTEL_MIN_SAMPLES
            and self._live_coop_rate() < self._SOFT_HOSTILE_COOP
        )

    def _enter_red_line(self) -> None:
        self._state = _State.RED_LINE
        self.is_red_line = True
        self.queue.clear()
        self.debt = 0
        self.echo_forgive = 0

    # ------------------------------------------------------------------
    # Core strategy
    # ------------------------------------------------------------------

    def strategy(self, opponent: Player) -> Action:
        """Select C or D for the current turn."""
        step = len(self.history) + 1

        if opponent.history:
            opp_last = opponent.history[-1]
            my_prev = self.last_my
            self.opp_len += 1

            if opp_last == D:
                self.opp_defects += 1
                if step > self._late_threshold():
                    self.late_defects += 1
                self._on_defect(step)
                self.clean_peace = 0
            else:
                if my_prev == D:
                    self.opp_coops_after_my_D += 1
                if my_prev == C:
                    self.clean_peace += 1
                else:
                    self.clean_peace = 0

            pair = (my_prev, opp_last)
            if self._last_pair is not None:
                a0, b0 = self._last_pair
                if (a0, b0) == (C, D) and pair == (D, C):
                    self.deadlock += 1
                elif (a0, b0) == (D, C) and pair == (C, D):
                    self.deadlock += 1
                elif a0 == b0 == C:
                    self.deadlock = 0
                elif a0 == D and b0 == D:
                    self.deadlock = 0
            self._last_pair = pair

        if self._is_hostile():
            self._enter_red_line()

        if self.late_defects >= 2:
            self._enter_red_line()
            return self._play(D)

        if self.is_red_line or self._state == _State.RED_LINE:
            return self._play(D)

        # Deadlock break: force C and soft-reset equalizing
        if self.deadlock >= self.DEADLOCK_THRESHOLD and not self.is_red_line:
            self.deadlock = 0
            self.queue.clear()
            self.debt = 0
            self.echo_forgive = 0
            self._state = _State.COOPERATIVE
            self.systemic = max(0, self.systemic - 1)
            self.epoch_step += 1
            self._close_epoch()
            return self._play(C)

        # Smart harvest + grim probe (known finite horizon only)
        known_len = self._match_length()
        if known_len is not None and self.opp_len > 30:
            remaining = known_len - step
            if remaining < self.HARVEST_WINDOW:
                forgiveness = self.opp_coops_after_my_D / max(1, self.my_D)
                low_defect = (self.opp_defects / max(1, self.opp_len)) < 0.02
                high_forgive = forgiveness > self.HARVEST_FORGIVENESS
                is_victim = high_forgive or low_defect
                is_grim = self.opp_len > 50 and self.opp_defects == 0

                if is_grim:
                    if remaining <= self.GRIM_LAST_SAFE:
                        return self._play(D)
                    if self.probe_fired:
                        return self._play(D)
                    if remaining <= self.PROBE_WINDOW and self.my_D == 0:
                        if self._random.random() < self.PROBE_PROB:
                            self.probe_fired = True
                            return self._play(D)
                else:
                    if self.probe_fired and remaining <= self.PROBE_WINDOW:
                        return self._play(D)
                    if is_victim:
                        return self._play(D)

        # Queued delayed retaliation
        if step in self.queue:
            self.queue.remove(step)
            self.debt = max(0, self.debt - 1)
            self.echo_forgive = max(self.echo_forgive, 1)
            self._close_epoch()
            return self._play(D)

        self.epoch_step += 1
        self._close_epoch()
        return self._play(C)

    def _play(self, action: Action) -> Action:
        self.last_my = action
        if action == D:
            self.my_D += 1
        return action

    def _on_defect(self, step: int) -> None:
        """Record opponent defection; apply v2 shields then schedule / ban."""
        # Contrition: ignore mirror D after our retaliatory fire
        if self.echo_forgive > 0:
            self.echo_forgive -= 1
            return

        # Noise-aware forgive after long clean peace
        if (
            self.one_shot_forgives < self.ONE_SHOT_MAX
            and self.opp_defects <= 3
            and step > self.EARLY_WINDOW
            and self.clean_peace >= self.ONE_SHOT_PEACE
            and self.debt <= 0
            and not self.queue
            and self._state == _State.COOPERATIVE
            and self.late_defects == 0
            and not self._is_soft_hostile()
        ):
            self.one_shot_forgives += 1
            self.one_shot_used = True
            return

        if self.debt > 0 or self.queue or self._state == _State.EQUALIZING:
            self.systemic += 1

        self.debt += 1
        self._state = _State.EQUALIZING

        threshold = 3
        if (
            self.systemic >= 1
            or self._is_soft_hostile()
            or self.late_defects > 0
        ):
            threshold = 2

        if self.systemic >= threshold:
            self._enter_red_line()
            return

        # Early sharp / hostile: delay 1; else short stochastic delay 1–2
        if self._is_hostile() or self.late_defects > 0:
            delay = 1
        elif step <= self.EARLY_WINDOW or self.opp_len <= 3:
            delay = 1
        else:
            delay = 1 + int(self._random.randint(0, 1))

        self.queue.append(step + delay)

    def _close_epoch(self) -> None:
        """Reset systemic counters when a clean epoch completes."""
        if self.is_red_line or self._state == _State.RED_LINE:
            return
        if (
            self.epoch_step >= self.base_epoch
            and self.debt <= 0
            and not self.queue
        ):
            self.epoch_step = 0
            self.systemic = 0
            self._state = _State.COOPERATIVE
