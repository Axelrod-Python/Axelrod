"""ZeroResp v5.4.4 — long-memory IPD player with a noise ladder.

Built on the v5.3 noise-ladder basis: epoch debt, delayed retaliation,
noise-aware forgiveness, opening disambiguation, and finite-horizon harvest.
v5.4.x adds responsiveness-gated apology and a cycler contour (periods 2–6,
noise-tolerant, mirror-guarded). Feature flags default on; disable via
``Features`` for ablation.

Compatible with ``axelrod.Match``. Class-level opponent profiles set
``manipulates_state`` to True.
"""

from __future__ import annotations

from collections import deque
from enum import Enum, auto
from typing import Dict, List, Optional

from axelrod.action import Action
from axelrod.player import Player

C, D = Action.C, Action.D

# Standard PD payoffs (fallback for nl_balance).
PAYOFF = {(C, C): 3, (C, D): 0, (D, C): 5, (D, D): 1}


class _State(Enum):
    COOPERATIVE = auto()
    EQUALIZING = auto()
    RED_LINE = auto()
    RED_LINE_COOLDOWN = auto()


class Features:
    __slots__ = (
        "profiles",
        "apology",
        "harvest_jitter",
        "noise_extra",
        "estimated_endgame",
        "opening_d_retort",
        "noise_adaptive",
        "contrite_full",
        "generous",
        "red_line_cooldown",
        "noise_ladder",
        "adaptive_harvest",
        "balance_apology",
        "tactical_prefilter",
        "profile_memory",
        "cycler_contour",
    )

    def __init__(
        self,
        profiles: bool = True,
        apology: bool = True,
        harvest_jitter: bool = True,
        noise_extra: bool = False,
        estimated_endgame: bool = True,
        opening_d_retort: bool = True,
        noise_adaptive: bool = True,
        contrite_full: bool = True,
        generous: bool = True,
        red_line_cooldown: bool = True,
        noise_ladder: bool = True,
        adaptive_harvest: bool = True,
        balance_apology: bool = True,
        tactical_prefilter: bool = True,
        profile_memory: bool = True,
        cycler_contour: bool = True,
    ):
        self.profiles = profiles
        self.apology = apology
        self.harvest_jitter = harvest_jitter
        self.noise_extra = noise_extra
        self.estimated_endgame = estimated_endgame
        self.opening_d_retort = opening_d_retort
        self.noise_adaptive = noise_adaptive
        self.contrite_full = contrite_full
        self.generous = generous
        self.red_line_cooldown = red_line_cooldown
        self.noise_ladder = noise_ladder
        self.adaptive_harvest = adaptive_harvest
        self.balance_apology = balance_apology
        self.tactical_prefilter = tactical_prefilter
        self.profile_memory = profile_memory
        self.cycler_contour = cycler_contour

    def asdict(self):
        return {k: getattr(self, k) for k in self.__slots__}

    def replace(self, **kw):
        d = self.asdict()
        d.update(kw)
        return Features(**d)


class ZeroResp(Player):
    name = "ZeroResp v5.4.4"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": True,
    }

    _DEFAULT_MATCH_LENGTH = 200
    _LATE_FRACTION = 0.75
    _LIVE_INTEL_MIN_SAMPLES = 10
    _HOSTILE_COOP_THRESHOLD = 0.40
    _SOFT_HOSTILE_COOP = 0.65

    EARLY_WINDOW = 5
    ONE_SHOT_PEACE = 12
    DEADLOCK_THRESHOLD = 3
    HARVEST_FORGIVENESS = 0.80
    HARVEST_WINDOW = 5
    ONE_SHOT_MAX = 2
    GRIM_LAST_SAFE = 1
    PROBE_WINDOW = 3
    FORGIVENESS_BASE = 3

    NL_WINDOW_TURNS = 12
    NL_DELAY_MIN = 8
    NL_DELAY_MAX = 20
    NL_PARDON_STREAK = 3
    NL_HARVEST_MIN = 3
    NL_HARVEST_MAX = 4

    NL_BALANCE_FLOOR = -4
    NL_SOFTNESS_FLOOR = 0.30

    _global_profiles: Dict[str, Dict] = {}
    _global_lengths: List[int] = []

    def __init__(
        self,
        base_epoch: int = 25,
        use_profiles: bool = True,
        features: Features | None = None,
    ):
        super().__init__()
        if not hasattr(self, "_random"):
            self.set_seed(None)
        self.base_epoch = int(base_epoch)
        self.features = features if features is not None else Features()
        self.use_profiles = bool(use_profiles) and self.features.profiles
        self._init_state()

    def _init_state(self):
        self._state = _State.COOPERATIVE
        self.is_red_line = False
        self.epoch_step = 0
        self.debt = 0
        self.systemic = 0
        self.queue: List[int] = []
        self.opp_len = 0
        self.opp_defects = 0
        self.my_D = 0
        self.my_C = 0
        self.opp_coops_after_my_D = 0
        self.opp_defects_after_my_C = 0
        self.opp_coops_after_my_C = 0
        self.opp_defects_after_my_D = 0
        self.last_my = C
        self.late_defects = 0
        self.opp_last3 = deque(maxlen=4)
        self.echo_forgive = 0
        self.one_shot_forgives = 0
        self.clean_peace = 0
        self.deadlock = 0
        self.probe_fired = False
        self.warmth = self._random.uniform(0.40, 0.60)
        self.target_warmth = 0.50
        self.intent = "normal"
        self.tactical = "adaptive"
        self._contrite = False
        self._last_D_reason = None
        self._consecutive_forgiven = 0
        self._apology_mode = False
        self._apology_steps = 0
        self._apology_tries = 0
        self._apology_max_tries = 2
        self._first_D_was_noise = False
        self._apology_opp_moves: List[Action] = []
        self._my_hist = deque(maxlen=3)
        self._opp_hist = deque(maxlen=3)
        self._forgiveness_exploiter = 0
        self._opening_d = False
        self._known_soft_opponent = False
        self._profile_checked = False

        self.cc_pairs = 0
        self.unprovoked_d = 0
        self.p_noise_est = 0.0
        self._fixed_period_latch = False
        self._intended_prev = C
        self._realized_prev = C
        self._bad_standing = False
        self._bad_standing_turns = 0
        self._red_line_cooldown = 0

        self.nl_evidence = 0
        self.nl_window = deque(maxlen=24)
        self.nl_scheduled: List[Dict] = []
        self.nl_debt_ledger = 0
        self.nl_pardoned = 0
        self.nl_balance = 0
        self.nl_harvest_left = 0
        self.nl_harvest_size = 0
        self.nl_harvest_postponed = 0
        self.nl_harvest_scheduled_at = 0
        self.nl_my_flips = 0
        self.nl_my_obs = 0
        self.nl_provoked_until = 0
        self.nl_pardon_step = 0
        self._pending_reason: Optional[str] = None

        if self.features.harvest_jitter:
            self._harvest_window = int(self._random.randint(3, 6))
        else:
            self._harvest_window = self.HARVEST_WINDOW

    def reset(self):
        if self.history:
            try:
                self.__class__._global_lengths.append(len(self.history))
                if len(self.__class__._global_lengths) > 200:
                    self.__class__._global_lengths = (
                        self.__class__._global_lengths[-200:]
                    )
            except Exception:
                pass
        old_p = self.__class__._global_profiles
        old_l = self.__class__._global_lengths
        feats = self.features
        use_p = self.use_profiles
        epoch = self.base_epoch
        super().reset()
        self.features = feats
        self.use_profiles = use_p
        self.base_epoch = epoch
        self._init_state()
        if self.use_profiles or self.features.estimated_endgame:
            self.__class__._global_profiles = old_p
            self.__class__._global_lengths = old_l

    # ---- helpers v5.1 ----
    def _match_length(self) -> Optional[int]:
        length = self.match_attributes.get("length")
        if length is None or length in (-1, float("inf")):
            return None
        try:
            val = int(length)
            return val if val > 0 else None
        except Exception:
            return None

    def _effective_length(self) -> int:
        known = self._match_length()
        if known is not None:
            return known
        obs = self.__class__._global_lengths
        if self.features.estimated_endgame and obs:
            return int(sorted(obs)[len(obs) // 2])
        return self._DEFAULT_MATCH_LENGTH

    def _late_threshold(self) -> int:
        return int(self._effective_length() * self._LATE_FRACTION)

    def _live_coop_rate(self) -> float:
        return (
            1.0
            if self.opp_len == 0
            else 1.0 - (self.opp_defects / self.opp_len)
        )

    def _estimate_remaining(self, step: int) -> Optional[int]:
        known = self._match_length()
        if known is not None:
            return max(0, known - step + 1)
        if not self.features.estimated_endgame:
            return None
        obs = self.__class__._global_lengths
        if len(obs) < 3:
            return None
        greater = [l for l in obs if l >= step]
        if not greater:
            return 1
        greater.sort()
        return max(0, greater[len(greater) // 2] - step + 1)

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

    def _get_adaptive_epoch(self) -> int:
        if self.warmth < 0.3:
            return 10
        if self.warmth > 0.7:
            return 40
        return self.base_epoch

    def _detect_intent(self) -> str:
        if self.my_C == 0 or self.opp_len < 15:
            return "normal"
        r = self.opp_defects_after_my_C / max(1, self.my_C)
        if r > 0.40:
            return "exploitation"
        if r < 0.25 and 0.02 < (self.opp_defects / max(1, self.opp_len)) < 0.25:
            return "noise"
        return "normal"

    def _classify_tactical(self) -> str:
        if self.opp_len < 15:
            return "adaptive"
        cr = self._live_coop_rate()
        if cr > 0.95:
            return "cooperator"
        if cr < 0.35:
            return "aggressor"
        eff = self._effective_length()
        if self.opp_len > eff * 0.65:
            early = self.opp_defects - self.late_defects
            if early <= 3 and self.late_defects >= 1:
                return "backstabber"
        if (
            self.my_D > 0
            and self.opp_coops_after_my_D == 0
            and self.opp_defects > 5
        ):
            return "grudger"
        if self.deadlock >= 2 or (self.opp_len > 20 and 0.40 < cr < 0.60):
            return "oscillator"
        return "adaptive"

    def _detect_fixed_period(self, opponent) -> bool:
        """Detect a fixed opponent period (cycler contour).

        Periods 2-6 over the last up to 18 opponent moves (min 12),
        mismatch tolerance ~15% for channel noise. Period 1 is
        excluded (looks like Grudger). Once latched, stays for the
        rest of the match.
        """
        if self._fixed_period_latch:
            return True
        hist = list(opponent.history)
        if len(hist) < 12:
            return False
        window = hist[-18:]
        n = len(window)
        my_hist = list(self.history)
        if len(my_hist) > n:
            my_window = my_hist[-(n + 1) : -1]
            agree = sum(1 for i in range(n) if window[i] == my_window[i])
            if agree >= int(n * 0.80):
                return False
        for p in range(2, 7):
            cmp_pairs = n - p
            if cmp_pairs < 8:
                continue
            mism = sum(1 for i in range(p, n) if window[i] != window[i - p])
            if mism <= max(1, int(cmp_pairs * 0.15)):
                self._fixed_period_latch = True
                return True
        return False

    def _update_target_warmth(self):
        if self.opp_len < 10:
            return
        ca = self.opp_coops_after_my_C / max(1, self.my_C)
        od = self.opp_defects / max(1, self.opp_len)
        md = self.my_D / max(1, self.opp_len)
        t = (
            0.5
            + 0.3 * (ca - 0.5)
            - 0.4 * max(0.0, od - 0.02)
            - 0.2 * max(0.0, md - od)
        )
        if self.tactical == "cooperator":
            t += 0.20
        elif self.tactical == "aggressor":
            t -= 0.30
        elif self.tactical == "oscillator":
            t -= 0.15
        elif (
            self.tactical == "backstabber"
            and self.opp_len > self._effective_length() * 0.65
        ):
            t -= 0.25
        if self._forgiveness_exploiter >= 2:
            t -= 0.20
        self.target_warmth = max(0.10, min(0.90, t))

    def _align_warmth(self, step: int):
        if step % 5 == 0 and step <= 25:
            self.warmth += (self.target_warmth - self.warmth) * 0.10
        elif step > 25 and step % self._get_adaptive_epoch() == 0:
            self.warmth = max(
                0.10,
                min(
                    0.90,
                    self.warmth + (self.target_warmth - self.warmth) * 0.25,
                ),
            )

    # ---- v5.2 noise ----
    def _is_noisy_regime(self) -> bool:
        if not self.features.noise_adaptive:
            return False
        if self._nl_active():
            return (
                self.p_noise_est > 0.015
                and (self.cc_pairs + self.nl_my_obs) > 10
            )
        return self.p_noise_est > 0.015 and self.cc_pairs > 10

    # ---- Noise ladder ----
    def _nl_noise_proven(self) -> bool:
        return self.nl_my_flips > 0

    def _nl_active(self) -> bool:
        return (
            self.features.noise_ladder
            and self._nl_noise_proven()
            and self.nl_balance >= 0
        )

    def _nl_is_unexplained(self) -> bool:
        if self._bad_standing or self._contrite:
            return False
        if not self.history:
            return True
        if (
            self.nl_provoked_until
            and self._nl_step_hint <= self.nl_provoked_until
        ):
            return False
        return self.history[-1] == C

    def _nl_ladder(self, step: int) -> bool:
        """Noise-ladder step on unexplained D. True means play C this turn."""
        if (
            self.nl_window
            and (step - self.nl_window[-1]) > self.NL_WINDOW_TURNS
        ):
            self.nl_evidence = 0
            self.nl_window.clear()
        self.nl_evidence += 1
        self.nl_window.append(step)

        if self.nl_pardon_step and (step - self.nl_pardon_step) <= 6:
            self._forgiveness_exploiter += 1
            self.nl_pardon_step = 0

        if self.nl_evidence == 1:
            self.nl_pardoned += 1
            self.nl_debt_ledger += 1
            self._pending_reason = "nl_deferred"
            return True

        if self.nl_evidence == 2:
            self.nl_pardoned += 1
            self.nl_debt_ledger += 1
            self._pending_reason = "nl_deferred"
            if not any(r.get("kind") == "strike" for r in self.nl_scheduled):
                self.nl_scheduled.append(
                    {
                        "turn": step
                        + self._random.randint(
                            self.NL_DELAY_MIN, self.NL_DELAY_MAX
                        ),
                        "kind": "strike",
                    }
                )
            forg = self.opp_coops_after_my_D / max(1, self.my_D)
            min_d = self.my_D >= 3
            if self.features.profile_memory and self._known_soft_opponent:
                min_d = self.my_D >= 1
            blocked_tactical = (
                self.features.tactical_prefilter
                and self.tactical in ("aggressor", "grudger")
            )
            if self.features.adaptive_harvest:
                softness = (forg - self.NL_SOFTNESS_FLOOR) / (
                    1.0 - self.NL_SOFTNESS_FLOOR
                )
                softness = max(0.0, min(1.0, softness))
                if (
                    softness > 0
                    and min_d
                    and not blocked_tactical
                    and self.nl_balance >= 0
                    and not self._is_noisy_regime()
                    and self._random.random() < softness
                ):
                    size = int(
                        round(
                            self.NL_HARVEST_MIN
                            + softness
                            * (self.NL_HARVEST_MAX - self.NL_HARVEST_MIN)
                        )
                    )
                    self.nl_harvest_size = max(self.NL_HARVEST_MIN, size)
                    self.nl_harvest_left = 0
                    self.nl_harvest_postponed = 0
                    self.nl_harvest_scheduled_at = step + self._random.randint(
                        6, 10
                    )
            else:
                if (
                    forg > 0.6
                    and min_d
                    and not blocked_tactical
                    and self.nl_balance >= 0
                    and not self._is_noisy_regime()
                ):
                    self.nl_harvest_size = self._random.randint(
                        self.NL_HARVEST_MIN, self.NL_HARVEST_MAX
                    )
                    self.nl_harvest_left = 0
                    self.nl_harvest_postponed = 0
                    self.nl_harvest_scheduled_at = step + self._random.randint(
                        6, 10
                    )
            return True

        if self.nl_evidence >= 3:
            if self._live_coop_rate() < self._HOSTILE_COOP_THRESHOLD and (
                not self._is_noisy_regime() or self.nl_evidence >= 8
            ):
                self._enter_red_line()
                return False
        return None

    def _enter_red_line(self):
        if self.features.red_line_cooldown and self._is_noisy_regime():
            self._state = _State.RED_LINE_COOLDOWN
            self.is_red_line = True
            self._red_line_cooldown = int(
                12 + 20 * (1 - min(self.p_noise_est * 10, 0.9))
            )
            self.warmth = 0.15
            self.queue.clear()
            self.debt = 0
            return
        self._state = _State.RED_LINE
        self.is_red_line = True
        self.warmth = 0.0
        self.target_warmth = 0.0
        self.queue.clear()
        self.debt = 0
        self.echo_forgive = 0
        self._apology_mode = False

    def _get_forgiveness_budget(self) -> int:
        base = self.FORGIVENESS_BASE
        jitter = self._random.randint(0, 2)
        if self.warmth > 0.7:
            jitter += 1
        if self.warmth < 0.4:
            jitter -= 1
        if self.features.noise_extra and self.intent == "noise":
            jitter += 4
        if self.tactical == "aggressor":
            jitter = max(jitter - 2, 0)
        if self._is_noisy_regime():
            jitter += int(self.p_noise_est * 40)
        return max(2, min(12, base + jitter))

    def _harvest_action(
        self, remaining: int, opponent: Player
    ) -> Optional[Action]:
        if self._is_noisy_regime() and self.features.noise_adaptive:
            if remaining > 2:
                return None
        forg = self.opp_coops_after_my_D / max(1, self.my_D)
        low = (self.opp_defects / max(1, self.opp_len)) < 0.02
        high = forg > self.HARVEST_FORGIVENESS
        is_victim = high or low
        is_grim = self.opp_len > 50 and self.opp_defects == 0

        if is_grim:
            if remaining <= self.GRIM_LAST_SAFE:
                return D
            if self.probe_fired:
                return D
            return None
        if self.probe_fired and remaining <= self.PROBE_WINDOW:
            return D
        if is_victim and self.tactical in ("cooperator", "adaptive"):
            return D
        return None

    def _opening_action(self, step: int, opponent: Player) -> Optional[Action]:
        if not self.features.opening_d_retort or not opponent.history:
            return None
        if step == 2 and opponent.history[0] == D:
            self._opening_d = True
            self.queue.clear()
            self.debt = 0
            self.systemic = 0
            self._state = _State.COOPERATIVE
            return self._play(D, "opening_retort", intended=D)
        if step == 3 and self._opening_d:
            if opponent.history[1] == C:
                self.queue.clear()
                self.debt = 0
                self.systemic = 0
                self._state = _State.COOPERATIVE
                self.echo_forgive = max(self.echo_forgive, 1)
                return self._play(C, "opening_resync", intended=C)
            self.queue.clear()
            self.debt = max(self.debt, 1)
            self._state = _State.EQUALIZING
            return self._play(D, "opening_dd", intended=D)
        return None

    # ---- core play ----
    def _play(
        self,
        action: Action,
        reason: str = "normal",
        intended: Optional[Action] = None,
    ) -> Action:
        if intended is None:
            intended = action
        self._intended_prev = intended
        self._realized_prev = action
        self.last_my = action
        self._last_D_reason = reason if action == D else None
        return action

    def _on_defect(self, step: int, opp_action: Action) -> bool:
        """Strategy helper (see module docstring)."""
        self._nl_step_hint = step

        # === v5.2 CONTRITE FULL ===
        if self.features.contrite_full:
            if self._bad_standing:
                self._bad_standing_turns -= 1
                if self._bad_standing_turns <= 0:
                    self._bad_standing = False
                self._contrite = False
                return True

        if (
            self._last_D_reason in ("harvest", "probe")
            and self.tactical == "cooperator"
        ):
            self._last_D_reason = None
            return True

        if self.echo_forgive > 0:
            if not (self._nl_active() and self._nl_is_unexplained()):
                self.echo_forgive -= 1
                return True

        # === v5.2 GENEROUS FORGIVENESS ===
        if self.features.generous and self._is_noisy_regime():
            if self._live_coop_rate() > 0.90 and self.opp_len > 20:
                return True

            p_forgive = min(
                0.6, self.p_noise_est * 7 + 0.05 + (self.warmth - 0.5) * 0.2
            )
            if len(self.opp_last3) >= 3 and list(self.opp_last3)[-2:] == [D, D]:
                p_forgive *= 0.3
            if self._random.random() < p_forgive:
                return True

        maxf = self.ONE_SHOT_MAX + (1 if self.warmth > 0.60 else 0)
        if self.features.noise_extra and self.intent == "noise":
            maxf += 4
        if self._is_noisy_regime():
            maxf += 2

        if (
            self.one_shot_forgives < maxf
            and self.opp_defects <= 5
            and step > self.EARLY_WINDOW
            and self.clean_peace >= self.ONE_SHOT_PEACE
            and self.debt <= 0
            and not self.queue
            and self._state == _State.COOPERATIVE
            and self.late_defects == 0
            and not self._is_soft_hostile()
            and self.warmth > 0.35
        ):
            self.one_shot_forgives += 1
            if self.features.noise_ladder:
                self.nl_pardon_step = step
            return True

        if self._nl_active() and self._nl_is_unexplained():
            handled = self._nl_ladder(step)
            if handled is not None:
                return handled

        if self.intent != "noise":
            if self.debt > 0 or self.queue or self._state == _State.EQUALIZING:
                self.systemic += 1
        self.debt += 1
        self._state = _State.EQUALIZING

        thr = 3
        if (
            self.warmth < 0.40
            or self._is_soft_hostile()
            or self.late_defects > 0
        ):
            thr = 2
        if self.intent == "exploitation":
            thr = 2
        if self.features.noise_extra and self.intent == "noise":
            thr = 12
        if self._is_noisy_regime():
            thr = 8
        if self.systemic >= thr:
            self._enter_red_line()
            return False

        delay = 1
        known = self._match_length()
        if known and step + delay > known:
            self.debt = max(0, self.debt - 1)
            self.echo_forgive = max(self.echo_forgive, 1)
            return False
        self.queue.append(step + delay)
        return False

    def _close_epoch(self):
        if self.is_red_line and self._state == _State.RED_LINE:
            return
        if (
            self.epoch_step >= self._get_adaptive_epoch()
            and self.debt <= 0
            and not self.queue
        ):
            self.epoch_step = 0
            self.systemic = 0
            if self._state != _State.RED_LINE_COOLDOWN:
                self._state = _State.COOPERATIVE

    def _save_profile(self, opp_name: str):
        if not self.use_profiles or not opp_name:
            return
        forgiveness = self.opp_coops_after_my_D / max(1, self.my_D)
        self.__class__._global_profiles[opp_name] = {
            "warmth": float(self.target_warmth),
            "coop_rate": self._live_coop_rate(),
            "tactical": self.tactical,
            "defects": self.opp_defects,
            "len": self.opp_len,
            "p_noise": self.p_noise_est,
            "forgiveness": forgiveness if self.my_D >= 3 else None,
        }

    def strategy(self, opponent: Player) -> Action:
        self._last_opponent_name = getattr(opponent, "name", "Opponent")
        step = len(self.history) + 1
        remaining = self._estimate_remaining(step)
        self._pending_reason = None
        self._nl_step_hint = 0

        if self.features.profile_memory and not self._profile_checked:
            self._profile_checked = True
            if self.use_profiles:
                prof = self.__class__._global_profiles.get(
                    self._last_opponent_name
                )
                if (
                    prof
                    and prof.get("forgiveness") is not None
                    and prof["forgiveness"] > 0.6
                ):
                    self._known_soft_opponent = True

        if (
            self.features.balance_apology
            and self.nl_balance <= self.NL_BALANCE_FLOOR
        ):
            # 1. 0% noise protection: never trigger balance_apology in deterministic matches
            # 2. Overall coop rate floor: live_coop_rate >= 0.60 when history >= 15
            # 3. Responsiveness condition: P(C|our C) - P(C|our D) >= 0.35 when our D >= 2
            noise_attr = self.match_attributes.get("noise")
            if self.features.cycler_contour and self._detect_fixed_period(
                opponent
            ):
                can_apologize = False
            elif noise_attr == 0.0:
                can_apologize = False
            elif self.opp_len >= 15 and self._live_coop_rate() < 0.60:
                can_apologize = False
            else:
                my_hist = self.history
                opp_hist = opponent.history
                n_c = sum(1 for i in range(len(my_hist) - 1) if my_hist[i] == C)
                n_d = sum(1 for i in range(len(my_hist) - 1) if my_hist[i] == D)
                if n_d >= 2:
                    c_after_c = sum(
                        1
                        for i in range(len(my_hist) - 1)
                        if my_hist[i] == C and opp_hist[i + 1] == C
                    )
                    c_after_d = sum(
                        1
                        for i in range(len(my_hist) - 1)
                        if my_hist[i] == D and opp_hist[i + 1] == C
                    )
                    p_c_c = c_after_c / max(1, n_c)
                    p_c_d = c_after_d / max(1, n_d)
                    delta_p = p_c_c - p_c_d
                    can_apologize = delta_p >= 0.35
                else:
                    can_apologize = True

            if can_apologize:
                self.nl_scheduled = []
                self.nl_harvest_left = 0
                self.nl_harvest_scheduled_at = 0
                self.nl_harvest_postponed = 0
                self.nl_harvest_size = 0
                self.nl_evidence = 0
                self.nl_window.clear()
                self.echo_forgive = max(self.echo_forgive, 2)
                self.warmth = max(self.warmth, 0.6)
                self.target_warmth = max(self.target_warmth, 0.6)

        if self.history:
            last_realized = self.history[-1]
            # intended vs realized
            if (
                last_realized != self._intended_prev
                and last_realized == D
                and self._intended_prev == C
            ):
                self._contrite = True
                self._first_D_was_noise = self.my_D <= 1
                self._bad_standing = True
                self._bad_standing_turns = 1
                if self.features.noise_ladder:
                    self.nl_my_flips += 1
            if self.features.noise_ladder and self._intended_prev == C:
                self.nl_my_obs += 1
            if self.features.noise_ladder and opponent.history:
                opp_last_move = opponent.history[-1]
                game = self.match_attributes.get("game")
                my_s = opp_s = None
                if game is not None:
                    try:
                        my_s, opp_s = game.score((last_realized, opp_last_move))
                    except Exception:
                        my_s = opp_s = None
                if my_s is None:
                    my_s = PAYOFF[(last_realized, opp_last_move)]
                    opp_s = PAYOFF[(opp_last_move, last_realized)]
                self.nl_balance += my_s - opp_s
            if len(self.history) >= 2 and len(opponent.history) >= 2:
                my_prev = self.history[-2]
                opp_prev = opponent.history[-2]
                if my_prev == C and opp_prev == C:
                    self.cc_pairs += 1
                    if opponent.history[-1] == D:
                        self.unprovoked_d += 1
                    if self.cc_pairs % 5 == 0 and self.cc_pairs > 10:
                        if self._nl_active():
                            total = self.cc_pairs + self.nl_my_obs
                            est_n = self.unprovoked_d + self.nl_my_flips
                        else:
                            total, est_n = self.cc_pairs, self.unprovoked_d
                        self.p_noise_est = est_n / max(1, total)

        if self.features.apology and self._apology_mode:
            if opponent.history:
                opp_last = opponent.history[-1]
                my_prev = self.last_my
                self._apology_opp_moves.append(opp_last)
                self.opp_len += 1
                self.opp_last3.append(opp_last)
                if opp_last == D:
                    self.opp_defects += 1
                    if my_prev == C:
                        self.opp_defects_after_my_C += 1
                    if step > self._late_threshold():
                        self.late_defects += 1
                    self.clean_peace = 0
                else:
                    if my_prev == D:
                        self.opp_coops_after_my_D += 1
                    if my_prev == C:
                        self.opp_coops_after_my_C += 1
                        self.clean_peace += 1
                    else:
                        self.clean_peace = 0
                if my_prev == D:
                    self.my_D += 1
                else:
                    self.my_C += 1

            self._apology_steps -= 1
            if self._apology_steps <= 0:
                if any(m == C for m in self._apology_opp_moves):
                    self._apology_mode = False
                    self._apology_tries = 0
                    self._first_D_was_noise = False
                    self._contrite = False
                    self._apology_opp_moves = []
                    self.debt = 0
                    self.systemic = 0
                    self.queue.clear()
                    self.echo_forgive = 1
                    self._state = _State.COOPERATIVE
                    self.epoch_step = 0
                    self.warmth = 0.60
                    self.target_warmth = 0.60
                    self.tactical = "adaptive"
                    self._close_epoch()
                    self._save_profile(self._last_opponent_name)
                    return self._play(C, "apology_success", intended=C)
                self._apology_tries += 1
                self._apology_opp_moves = []
                if self._apology_tries >= self._apology_max_tries:
                    self._enter_red_line()
                    self._save_profile(self._last_opponent_name)
                    return self._play(D, "red_line", intended=D)
                self._apology_mode = False
            else:
                self.epoch_step += 1
                self._close_epoch()
                self._save_profile(self._last_opponent_name)
                return self._play(C, "apology", intended=C)

        if self.features.apology:
            apology_max = self._apology_max_tries
            if self.use_profiles:
                prof = self.__class__._global_profiles.get(
                    self._last_opponent_name
                )
                if prof and prof.get("tactical") == "grudger":
                    apology_max = 4
            if (
                not self.is_red_line
                and not self._apology_mode
                and self._first_D_was_noise
                and len(self.opp_last3) >= 2
                and list(self.opp_last3)[-2:] == [D, D]
                and self._apology_tries < apology_max
                and self.opp_len < 300
            ):
                self._apology_mode = True
                self._apology_steps = self._get_forgiveness_budget()
                self._apology_opp_moves = []
                self.epoch_step += 1
                self._close_epoch()
                self._save_profile(self._last_opponent_name)
                return self._play(C, "apology", intended=C)

        if opponent.history and self.opp_len < len(opponent.history):
            opp_last = opponent.history[-1]
            my_prev = self.last_my

            if self._bad_standing and self.features.contrite_full:
                self.opp_len += 1
                self.opp_last3.append(opp_last)
                if opp_last == D:
                    self.opp_defects += 1
                    if step > self._late_threshold():
                        self.late_defects += 1
                    self.clean_peace = 0
                else:
                    self.clean_peace += 1 if my_prev == C else 0
                    if my_prev == D:
                        self.opp_coops_after_my_D += 1
                if my_prev == D:
                    self.my_D += 1
                else:
                    self.my_C += 1
                self._bad_standing_turns -= 1
                if self._bad_standing_turns <= 0:
                    self._bad_standing = False
                self._contrite = False
                if self.opp_len % 5 == 0:
                    self.intent = self._detect_intent()
                    self.tactical = self._classify_tactical()
                    self._update_target_warmth()
                self._align_warmth(step)
                self.epoch_step += 1
                self._close_epoch()
                self._save_profile(self._last_opponent_name)
                return self._play(C, "contrite_full", intended=C)

            if opp_last == D and self._contrite:
                self.opp_len += 1
                self.opp_last3.append(opp_last)
                self.opp_defects += 1
                if my_prev == C:
                    self.opp_defects_after_my_C += 1
                if step > self._late_threshold():
                    self.late_defects += 1
                self.clean_peace = 0
                if my_prev == D:
                    self.my_D += 1
                else:
                    self.my_C += 1
                self._contrite = False
                self._consecutive_forgiven += 1
                if self.opp_len % 5 == 0:
                    self.intent = self._detect_intent()
                    self.tactical = self._classify_tactical()
                    self._update_target_warmth()
                self._align_warmth(step)
                self.epoch_step += 1
                self._close_epoch()
                self._save_profile(self._last_opponent_name)
                return self._play(C, "contrite", intended=C)

            self.opp_len += 1
            self.opp_last3.append(opp_last)
            if opp_last == D:
                self.opp_defects += 1
                if my_prev == C:
                    self.opp_defects_after_my_C += 1
                if step > self._late_threshold():
                    self.late_defects += 1
                if my_prev == D:
                    self.opp_defects_after_my_D += 1
                self._on_defect(step, opp_last)
                self.clean_peace = 0
            else:
                if my_prev == D:
                    self.opp_coops_after_my_D += 1
                if my_prev == C:
                    self.opp_coops_after_my_C += 1
                    self.clean_peace += 1
                else:
                    self.clean_peace = 0
            if my_prev == D:
                self.my_D += 1
            else:
                self.my_C += 1

        # --- opening ---
        opened = self._opening_action(step, opponent)
        if opened is not None:
            self._save_profile(self._last_opponent_name)
            return opened

        if self.features.noise_ladder:
            if (
                self.nl_harvest_scheduled_at != 0
                and step >= self.nl_harvest_scheduled_at
            ):
                if opponent.history and opponent.history[-1] == C:
                    self.nl_harvest_left = self.nl_harvest_size
                    self.nl_harvest_scheduled_at = 0
                    self.nl_provoked_until = step + self.nl_harvest_size + 3
                elif self.nl_harvest_postponed < 2:
                    self.nl_harvest_postponed += 1
                    self.nl_harvest_scheduled_at = step + 3
                else:
                    self.nl_harvest_scheduled_at = 0
                    self.nl_harvest_size = 0
            if self.nl_harvest_left > 0:
                self.nl_harvest_left -= 1
                return self._play(D, "nl_harvest_comp", intended=D)

        self.nl_scheduled = [r for r in self.nl_scheduled if r["turn"] >= step]
        due = next((r for r in self.nl_scheduled if r["turn"] == step), None)
        if due is not None:
            self.nl_scheduled.remove(due)
            last3 = list(self.opp_last3)[-self.NL_PARDON_STREAK :]
            if (
                len(last3) >= self.NL_PARDON_STREAK
                and all(mv == C for mv in last3)
                and self.opp_defects_after_my_D == 0
            ):
                self.nl_debt_ledger += 1
                self.nl_pardoned += 1
                self.nl_pardon_step = step
                if step in self.queue:
                    self.queue.remove(step)
                    self.debt = max(0, self.debt - 1)
                self._pending_reason = "nl_pardon"
            else:
                self.queue.append(step)
                self.nl_debt_ledger = max(0, self.nl_debt_ledger - 1)

        if self.opp_len % 5 == 0:
            self.intent = self._detect_intent()
            self.tactical = self._classify_tactical()
            self._update_target_warmth()
        self._align_warmth(step)

        # --- red_line checks ---
        if self.intent != "noise" and not self._is_noisy_regime():
            if len(self.opp_last3) >= 3 and list(self.opp_last3)[-3:] == [
                D,
                D,
                D,
            ]:
                nl_governs = self._nl_active() and all(
                    m == C for m in list(self.history)[-4:-1]
                )
                if (
                    not nl_governs
                    and not self._contrite
                    and not self._bad_standing
                    and self._consecutive_forgiven < 2
                    and not self._apology_mode
                ):
                    self._enter_red_line()
                    if self._state == _State.RED_LINE:
                        return self._play(D, "red_line", intended=D)

        if (
            self._is_hostile()
            and not self._contrite
            and not self._bad_standing
            and not self._apology_mode
        ):
            if not self._is_noisy_regime():
                self._enter_red_line()

        if self.is_red_line:
            if self._state == _State.RED_LINE_COOLDOWN:
                if self._red_line_cooldown <= 0:
                    self._red_line_cooldown = int(
                        15 + 10 * (1 - min(self.p_noise_est * 5, 0.8))
                    )
                    self.epoch_step += 1
                    self._close_epoch()
                    self._save_profile(self._last_opponent_name)
                    return self._play(C, "red_line_probe", intended=C)
                self._red_line_cooldown -= 1
                self._save_profile(self._last_opponent_name)
                return self._play(D, "red_line_cooldown", intended=D)
            return self._play(D, "red_line", intended=D)

        if self.deadlock >= self.DEADLOCK_THRESHOLD:
            self.deadlock = 0
            self.queue.clear()
            self.debt = 0
            self.echo_forgive = 0
            self._state = _State.COOPERATIVE
            self.systemic = max(0, self.systemic - 1)
            self.epoch_step += 1
            self._close_epoch()
            self._contrite = False
            self._bad_standing = False
            return self._play(C, "normal", intended=C)

        if (
            remaining is not None
            and self.opp_len > 30
            and remaining <= self._harvest_window
        ):
            harvested = self._harvest_action(remaining, opponent)
            if harvested is not None:
                reason = "harvest" if harvested == D else "harvest_keep_C"
                if self.probe_fired and harvested == D:
                    reason = "probe"
                return self._play(harvested, reason, intended=harvested)

        if step in self.queue:
            if self._contrite or self._bad_standing or self._apology_mode:
                self.queue.remove(step)
                self.queue.append(step + 1)
                self.epoch_step += 1
                self._close_epoch()
                self._save_profile(self._last_opponent_name)
                return self._play(
                    C, "contrite" if self._contrite else "apology", intended=C
                )
            self.queue.remove(step)
            self.debt = max(0, self.debt - 1)
            echo_val = (
                2
                if (self.features.noise_extra and self.intent == "noise")
                else 1
            )
            if self._is_noisy_regime():
                echo_val = 2
            self.echo_forgive = max(self.echo_forgive, echo_val)
            self._close_epoch()
            self._save_profile(self._last_opponent_name)
            return self._play(D, "retaliation", intended=D)

        self.epoch_step += 1
        self._close_epoch()
        self._save_profile(self._last_opponent_name)
        if self._contrite:
            self._contrite = False
        self._bad_standing = False
        reason = (
            self._pending_reason
            if self._pending_reason is not None
            else "normal"
        )
        self._pending_reason = None
        return self._play(C, reason, intended=C)
