import numpy as np
from scipy.optimize import minimize

from axelrod.action import Action
from axelrod.player import Player

C, D = Action.C, Action.D


class LongtermTfT(Player):
    """Noise-tolerant Tit-for-Tat.

    Cooperates by default and mirrors the opponent, but distinguishes
    noise-corrupted cooperation from genuine defection using a statistical
    test: it compares the opponent's observed defection count against the
    binomial null expected from the noise rate (via a z-statistic) and
    forgives defections that are consistent with noise. The number of
    forgiven defections grows like O(sqrt(N_C)), so the forgiven *rate*
    tends to zero — tolerating noise while staying unexploitable in the
    long run. Retaliates only when the defection rate is significantly
    above what noise alone would explain.

    Names:
    - Longterm TFT: [Hutter2023]_
    """

    name = "LongtermTfT"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": {"noise"},
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self):
        super().__init__()
        self.n_tft_would_c = 0
        self.n_d_when_tft_would_c = 0
        self.z = 0.0

    def receive_match_attributes(self):
        self.noise = self.match_attributes.get("noise", 0.0)

    def strategy(self, opponent: Player) -> Action:
        if not self.history:
            return C
        if len(self.history) == 1:
            return opponent.history[-1]
        if self.history[-2] == C:
            self.n_tft_would_c += 1
            if opponent.history[-1] == D:
                self.n_d_when_tft_would_c += 1
            n_expected_ds = self.n_tft_would_c * self.noise
            std_expected_ds = np.sqrt(
                self.noise * (1 - self.noise) * self.n_tft_would_c
            )
            self.z = (self.n_d_when_tft_would_c - n_expected_ds) / max(
                1.0, std_expected_ds
            )
        if self.n_tft_would_c >= 5 and self.z < 2:
            return C
        else:
            return opponent.history[-1]


def get_reward(
    my_strategy: np.ndarray,
    opp_strategy: np.ndarray,
    init_state: np.ndarray,
    p_end: float,
    p_noise: float,
    RPST: tuple[float, float, float, float],
) -> float:
    """Calculates the expected average reward per step for a given policy
    against a specific opponent strategy (including the effect of noise),
    utilizing Markov transition matrices.

    Memory-1 strategies are described as length-4 arrays, quantifying the probability
    of cooperation in the states [CC, CD, DC, DD].

    Applies p_noise only to own strategy (the opponent strategy already includes
    noise effects) and flips CD/DC indices for the opponent.
    """
    own = my_strategy + p_noise * (1.0 - 2.0 * my_strategy)
    opp = opp_strategy[[0, 2, 1, 3]]

    trans_mat = np.array(
        [
            own * opp,
            own * (1.0 - opp),
            (1.0 - own) * opp,
            (1.0 - own) * (1.0 - opp),
        ]
    ).T

    R, P, S, T = RPST
    rewards = np.array([R, S, T, P], dtype=float)
    inv = np.linalg.inv(np.eye(4) - (1.0 - p_end) * trans_mat)
    reward = init_state @ (inv @ rewards - rewards)
    return p_end * float(reward) / (1.0 - p_end)


def optimize_against(
    opponent: np.ndarray,
    init_state_idx: int,
    p_end: float,
    p_noise: float,
    RPST: tuple[float, float, float, float],
) -> tuple[float, np.ndarray]:
    """
    Discovers the optimal response strategy (policy) against a fixed opponent
    model by maximizing the expected reward from a given starting state.
    """
    assert p_noise < 0.5

    opp = np.clip(opponent, p_noise, 1.0 - p_noise)

    init_state = np.zeros(4, dtype=np.float32)
    init_state[init_state_idx] = 1.0

    def objective(params: np.ndarray) -> float:
        return -get_reward(params, opp, init_state, p_end, p_noise, RPST)

    x0 = np.array([0.5, 0.5, 0.5, 0.5])
    bounds = [(0.0, 1.0), (0.0, 1.0), (0.0, 1.0), (0.0, 1.0)]
    result = minimize(
        objective, x0, method="L-BFGS-B", bounds=bounds, options={"maxiter": 50}
    )

    return -result.fun, result.x


class ISO(Player):
    """Optimal response against a memory-1 opponent model.

    Estimates the opponent's memory-1 (order-1) conditional cooperation
    probabilities, which together with its own memory-1 strategy induce a
    Markov chain over outcome pairs. Computes the exact expected discounted
    long-term payoff in closed form via the chain's stationary/resolvent
    solution, then optimizes its own memory-1 policy to maximize it. A
    simplification and refinement of DBS: it replaces bounded-depth tree
    search with the exact infinite-horizon value, yielding stronger play
    against exploitable opponents at lower complexity. Adaptive only w.r.t.
    memory-1 opponents (the model is misspecified for higher-memory play).

    Names:
    - ISO: [Hutter2023]_
    """

    name = "ISO"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "makes_use_of": {"noise", "game"},
        "long_run_time": True,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self):
        """Initializes discount factors, opponent models, and policy state.

        Tracks the opponent's rate of cooperation (numerator, denominator) for each
        state. Assumes having seen the opponent play following TfT once in each state
        to make the opponent-model well-defined from the start.

        Sets initial cooperation probabilities (num / den) for opp_model and my_policy.
        """
        super().__init__()
        self.discount_factor = 0.99

        self.ewma_CC = [1.0, 1.0]
        self.ewma_CD = [1.0, 1.0]
        self.ewma_DC = [0.0, 1.0]
        self.ewma_DD = [0.0, 1.0]

        self.opp_model = [1.0, 0.0, 1.0, 0.0]
        self.my_policy = [1.0, 0.0, 1.0, 0.0]

    def receive_match_attributes(self):
        self.noise = self.match_attributes.get("noise", 0.0)
        self.RPST = self.match_attributes["game"].RPST()

    def _update_single_ewma(
        self, state_ewma: list[float], action_val: float
    ) -> float:
        """Updates the (numerator, denominator) pair in-place and returns the new average."""
        state_ewma[0] = self.discount_factor * state_ewma[0] + action_val
        state_ewma[1] = self.discount_factor * state_ewma[1] + 1.0
        return state_ewma[0] / state_ewma[1]

    def _update_opponent_model(self, opponent: Player):
        if len(self.history) < 2:
            return

        prev_state = (self.history[-2], opponent.history[-2])
        opp_act = 1.0 if opponent.history[-1] == C else 0.0

        if prev_state == (C, C):
            pr_c = self._update_single_ewma(self.ewma_CC, opp_act)
            self.opp_model[0] = pr_c
        elif prev_state == (C, D):
            pr_c = self._update_single_ewma(self.ewma_CD, opp_act)
            self.opp_model[2] = pr_c
        elif prev_state == (D, C):
            pr_c = self._update_single_ewma(self.ewma_DC, opp_act)
            self.opp_model[1] = pr_c
        elif prev_state == (D, D):
            pr_c = self._update_single_ewma(self.ewma_DD, opp_act)
            self.opp_model[3] = pr_c

    def _get_state_idx(self, opponent) -> int:
        if not self.history:
            return 0
        state = (self.history[-1], opponent.history[-1])
        if state == (C, C):
            return 0
        elif state == (C, D):
            return 1
        elif state == (D, C):
            return 2
        elif state == (D, D):
            return 3
        return -1

    def update(self, opponent: Player) -> float:
        """Updates the opponent model and our policy.

        Returns our expected reward per step.
        """
        self._update_opponent_model(opponent)
        state_idx = self._get_state_idx(opponent)
        expected, my_policy = optimize_against(
            self.opp_model,
            init_state_idx=state_idx,
            p_noise=self.noise,
            RPST=self.RPST,
            p_end=1e-2,
        )
        self.my_policy = my_policy
        return expected

    def act(self, opponent: Player) -> Action:
        state_idx = self._get_state_idx(opponent)
        pr_c = self.my_policy[state_idx]
        return self._random.random_choice(pr_c)

    def strategy(self, opponent: Player) -> Action:
        _ = self.update(opponent)
        return self.act(opponent)


class CooperateISO(Player):
    """Forgiving cooperation combined with optimal exploitation.

    Seeks to establish and sustain mutual cooperation using LongtermTFT's
    noise-robust forgiveness, while switching to ISO to respond optimally
    to opponents that can be exploited. In effect: cooperate with
    retaliators, exploit the exploitable. This combination is the paper's
    tournament-strong strategy, outperforming prior champions against the
    Axelrod library across noise levels of 0–10%.

    Names:
    - CooperateISO: [Hutter2023]_
    """

    name = "CooperateISO"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "makes_use_of": {"noise", "game"},
        "long_run_time": True,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self):
        self.iso_instance = ISO()
        super().__init__()
        self.n_tft_would_c = 0
        self.n_d_when_tft_would_c = 0
        self.z = 0.0
        self.playing_iso = False
        self.reward_history = []

    def set_seed(self, seed: int = None):
        super().set_seed(seed)
        self.iso_instance.set_seed(seed)

    def receive_match_attributes(self):
        super().receive_match_attributes()
        self.RPST = self.match_attributes["game"].RPST()
        self.noise = self.match_attributes["noise"]
        self.iso_instance.noise = self.noise

    def _update_reward_history(self, opponent):
        R, P, S, T = self.RPST
        state = (self.history[-1], opponent.history[-1])
        if state == (C, C):
            self.reward_history.append(R)
        elif state == (C, D):
            self.reward_history.append(S)
        elif state == (D, C):
            self.reward_history.append(T)
        elif state == (D, D):
            self.reward_history.append(P)

    def strategy(self, opponent: Player) -> Action:
        if not self.history:
            return C
        self.iso_instance.history.append(self.history[-1], opponent.history[-1])
        if self.playing_iso:
            return self.iso_instance.strategy(opponent)
        self._update_reward_history(opponent)
        expected = self.iso_instance.update(opponent)
        if len(self.history) == 1:
            return opponent.history[-1]
        if self.history[-2] == C:
            self.n_tft_would_c += 1
            if opponent.history[-1] == D:
                self.n_d_when_tft_would_c += 1
            n_expected_ds = self.n_tft_would_c * self.noise
            std_expected_ds = np.sqrt(
                self.noise * (1 - self.noise) * self.n_tft_would_c
            )
            self.z = (self.n_d_when_tft_would_c - n_expected_ds) / max(
                1.0, std_expected_ds
            )
        R, P, _, _ = self.RPST
        expected_gain = expected - np.mean(self.reward_history)
        if (
            len(self.reward_history) >= 10
            and expected_gain
            > 2.0
            * np.std(self.reward_history)
            / np.sqrt(len(self.reward_history))
            and expected_gain > 0.05 * (R - P)
        ):
            self.playing_iso = True
            return self.iso_instance.act(opponent)
        if self.n_tft_would_c >= 5 and self.z < 2:
            return C
        else:
            return opponent.history[-1]
