"""
ZeroResp: adaptive state-machine strategy for the Iterated Prisoner's Dilemma.

Designed to resist both heuristic exploiters and simple RL / tabular Q-learners
via delayed stochastic retaliation, epoch-based debt accounting, and a permanent
red-line ban after systemic abuse.
"""

from __future__ import annotations

import math
from enum import Enum, auto
from typing import List, Optional

from axelrod.action import Action
from axelrod.player import Player

C, D = Action.C, Action.D


class _State(Enum):
    """Internal finite-state labels."""

    COOPERATIVE = auto()
    EQUALIZING = auto()
    RED_LINE = auto()


class ZeroResp(Player):
    """
    An adaptive state machine that balances cooperation with delayed,
    randomised retaliation and a permanent ban against systemic defectors.

    Architecture
    ------------
    1. **Dynamic epochs** — interaction is partitioned into epochs of length
       ``base_epoch`` (default 25). While a retaliation debt or queued strike
       is outstanding the epoch is extended; once cleared the systemic-abuse
       counter resets and the bot returns to cooperative mode.

    2. **Stochastic retaliation buffer** — a defection does not trigger an
       immediate mirror response. Instead a retaliatory ``D`` is scheduled
       ``5 + U{1..10}`` turns later. The random delay breaks short-horizon
       Markov estimates used by tabular Q-learners and reduces cascade wars
       against tit-for-tat family strategies.

    3. **Red line (ban list)** — systemic defections (defects that arrive while
       debt/queue is still open, or while already equalising) raise a counter.
       After a dynamic threshold (2 or 3 depending on observed hostility) the
       strategy enters permanent red line (``is_red_line = True``) and defects
       unconditionally for the rest of the match.

    4. **Anti-raider** — two or more late-game defections (past ~75% of the
       known match length) are treated as end-game harvest and trigger red
       line immediately.

    5. **End-game harvest** — against highly forgiving / near-pure cooperators
       (and never against grim-trigger types that never defected), ZeroResp may
       defect near the known end of a finite match. This is disabled when
       match length is unknown.

    Names:

    - ZeroResp: Original name by EpochRedLine / SovereignStabilizer authors
    - EpochRedLine: Earlier development name
    - SmartTitForTat: Legacy sandbox name
    """

    name = "ZeroResp"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    # Fallback when match length is unknown / infinite.
    _DEFAULT_MATCH_LENGTH = 200
    _LATE_FRACTION = 0.75
    _LIVE_INTEL_MIN_SAMPLES = 10
    _HOSTILE_COOP_THRESHOLD = 0.4
    _SOFT_HOSTILE_COOP = 0.7

    def __init__(self) -> None:
        """Initialise epoch accounting and red-line state."""
        super().__init__()
        self.base_epoch = 25

        self._state = _State.COOPERATIVE
        self.is_red_line = False
        self.epoch_step = 0
        self.debt = 0
        self.systemic = 0
        self.queue: List[int] = []

        # Opponent cadastre (loyalty / exploitability estimates)
        self.opp_len = 0
        self.opp_defects = 0
        self.opp_coops_after_my_D = 0
        self.my_D = 0
        self.last_my: Action = C
        self.late_defects = 0

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _match_length(self) -> Optional[int]:
        """Return known finite match length, else ``None``."""
        # Bracket access so Axelrod's makes_use_of scanner detects "length".
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
        """Enough evidence of a low-cooperation opponent."""
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

    # ------------------------------------------------------------------
    # Core strategy
    # ------------------------------------------------------------------

    def strategy(self, opponent: Player) -> Action:
        """Select C or D for the current turn."""
        step = len(self.history) + 1  # 1-based turn index

        # --- Cadastre update from opponent's previous action -------------
        if opponent.history:
            opp_last = opponent.history[-1]
            self.opp_len += 1
            if opp_last == D:
                self.opp_defects += 1
                if step > self._late_threshold():
                    self.late_defects += 1
                self._on_defect(step)
            else:
                if self.last_my == D:
                    self.opp_coops_after_my_D += 1

        # Live zero-turn defence: permanent ban against proven predators
        if self._is_hostile():
            self._enter_red_line()

        # --- Anti-raider (late harvest interception) ---------------------
        if self.late_defects >= 2:
            self._enter_red_line()
            return self._play(D)

        if self.is_red_line or self._state == _State.RED_LINE:
            return self._play(D)

        # --- End-game harvest vs forgiving victims (known finite length) -
        known_len = self._match_length()
        if known_len is not None and self.opp_len > 50:
            p_end = 1.0 / (1.0 + math.exp(-10.0 * (step / known_len - 0.85)))
            forgiveness = self.opp_coops_after_my_D / max(1, self.my_D)
            is_grim = self.opp_len > 50 and self.opp_defects == 0
            is_victim = forgiveness > 0.6 or (
                self.opp_defects / max(1, self.opp_len) < 0.03
            )
            if p_end > 0.75 and is_victim and not is_grim:
                return self._play(D)

        # --- Queued delayed retaliation ----------------------------------
        if step in self.queue:
            self.queue.remove(step)
            self.debt = max(0, self.debt - 1)
            self._close_epoch()
            return self._play(D)

        # --- Default: cooperate & advance epoch --------------------------
        self.epoch_step += 1
        self._close_epoch()
        return self._play(C)

    def _play(self, action: Action) -> Action:
        self.last_my = action
        if action == D:
            self.my_D += 1
        return action

    def _on_defect(self, step: int) -> None:
        """Record an opponent defection and schedule / escalate response."""
        if self.debt > 0 or self.queue or self._state == _State.EQUALIZING:
            self.systemic += 1

        self.debt += 1
        self._state = _State.EQUALIZING

        # Dynamic red-line threshold (tighter under hostility).
        # Default: 3 systemic defects; after the first systemic event (or
        # soft hostility / late defects) the threshold tightens to 2.
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

        # Adaptive buffer: near-immediate under pressure, else stochastic
        if self._is_hostile() or self.late_defects > 0:
            delay = 1
        else:
            # numpy RandomState.randint is high-exclusive → use (1, 11)
            delay = 5 + int(self._random.randint(1, 11))

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
