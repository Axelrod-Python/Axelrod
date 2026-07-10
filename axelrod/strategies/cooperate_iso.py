import numpy as np

import torch
from torch import optim

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
        "stochastic": True,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self):
        super().__init__()
        self.n_tft_would_c = 0
        self.n_d_when_tft_would_c = 0
        self.z = 0.
        # Estimate of the opponent's rate of playing D after C, taking noise
        # into account.
        self.opp_pr_d_after_c = 0.

    def receive_match_attributes(self):
        self.noise = self.match_attributes["noise"]

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
            std_expected_ds = np.sqrt(self.noise * (1-self.noise) * self.n_tft_would_c)
            # This becomes n_d_when_tft_would_c for noise->0
            self.z = (self.n_d_when_tft_would_c - n_expected_ds) / max(1., std_expected_ds)
        if self.n_tft_would_c < 5 and self.n_d_when_tft_would_c < 3:
            # TfT
            return opponent.history[-1]
        elif self.z < 2:
            return C
        else:
            # TfT
            return opponent.history[-1]

def are_same_binomial(p1: float, n1: int, p2: float, n2: int, min_abs_z: float = 2.0) -> bool:
    p = (n1 * p1 + n2 * p2) / (n1 + n2)
    z = (p1 - p2) / np.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    return abs(z) < min_abs_z

def has_greater_mean(ary1: np.ndarray, ary2: np.ndarray, min_z: float = 2.0) -> bool:
    """Tests if ary1 has a greater mean than ary2"""
    se1 = np.std(ary1) / np.sqrt(len(ary1))
    se2 = np.std(ary2) / np.sqrt(len(ary2))
    if se1 == 0 and se2 == 0:
        return ary1.mean() > ary2.mean()
    return (ary1.mean() - ary2.mean()) / np.sqrt(se1**2 + se2**2) > min_z

def find_recent_average(ary, discount_factor: float = 0.99) -> float:
    assert len(ary) > 0
    assert 0 < discount_factor <= 1
    ary = np.array(ary)
    N = len(ary)
    weights = np.array([discount_factor**((N-1)-i) for i in range(N)])
    return (weights * ary).sum() / weights.sum()

def optimize_constrained(loss_fn,
                         starting_points=[[0.5, 0.5, 0.5, 0.5]],
                         lr=0.1,
                         n_steps=100):
    # Constrains all params to [0, 1].
    min_loss_so_far = None
    best_params_so_far = None
    for point in starting_points:
        params = torch.Tensor(point)
        params.requires_grad_()
        opt = optim.Adam([params], lr=lr)
        for i in range(n_steps):
            loss = loss_fn(params)
            loss_value = loss.detach().numpy().sum()
            if min_loss_so_far is None or loss_value < min_loss_so_far:
                min_loss_so_far = loss_value
                best_params_so_far = params.detach().numpy()
            opt.zero_grad()
            loss.backward()
            opt.step()
            with torch.no_grad():
                for param in params:
                    param.clamp_(0, 1)
    return min_loss_so_far, best_params_so_far

# opp_strategy already includes the effect of noise.
def get_reward(my_strategy: torch.Tensor,
               opp_strategy: torch.Tensor,
               init_state: torch.Tensor,
               p_end: float,
               p_noise: float = 0.,
               RSTP=(3, 0, 5, 1)):
    # Apply p_noise only to own strategy, not to opponent.
    own = my_strategy + p_noise * (1 - 2 * my_strategy)
    # Flip CD/DC for opponent
    opp = torch.Tensor(
        [opp_strategy[0], opp_strategy[2], opp_strategy[1], opp_strategy[3]])
    T = torch.stack([own * opp,
                     own * (1 - opp),
                     (1 - own) * opp,
                     (1 - own) * (1 - opp)])
    T = torch.transpose(T, 0, 1)
    TT = torch.inverse(torch.eye(4) - (1 - p_end) * T)
    rewards = torch.tensor(RSTP, dtype=torch.float)
    # Don't include init state in summed rewards.
    reward = torch.dot(init_state, torch.matmul(TT, rewards) - rewards)
    # Avg. reward per step
    return p_end * reward / (1 - p_end)

# The opponent model is assumed to already include the effect of noise.
# init_state_idx in [0, 1, 2, 3]
def optimize_against(opponent: np.ndarray, init_state_idx: int,
                     p_end: float = 1e-2, p_noise: float = 0) -> np.ndarray:
    opp = torch.Tensor(opponent)
    assert p_noise < 0.5
    opp.clamp_(min=p_noise, max=1-p_noise)
    init_state = [0] * 4
    init_state[init_state_idx] = 1
    init_state = torch.Tensor(init_state)
    def loss_fn(strategy: torch.Tensor):
        return -1 * get_reward(strategy, opp, init_state, p_end=p_end, p_noise=p_noise)
    # Only 50 steps to save time
    loss, strat = optimize_constrained(loss_fn, n_steps=50)
    return -1 * loss, strat

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
        "long_run_time": True,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self):
        super().__init__()
        # Opponent's action in certain situations. 1 is C, 0 is D.
        # Start by assuming the opponent played in accordance with TfT once.
        self.opp_after_CC = [1]
        self.opp_after_CD = [1]
        self.opp_after_DC = [0]
        self.opp_after_DD = [0]
        # Recent averages of cooperation rates
        self.opp_pr_c_after_CC = np.mean(self.opp_after_CC)
        self.opp_pr_c_after_CD = np.mean(self.opp_after_CD)
        self.opp_pr_c_after_DC = np.mean(self.opp_after_DC)
        self.opp_pr_c_after_DD = np.mean(self.opp_after_DD)
        self.opp_model = [1., 0., 1., 0.]
        self.my_policy = [1., 0., 1., 0.]

    def receive_match_attributes(self):
        self.noise = self.match_attributes["noise"]

    def _update_opponent_model(self, opponent):
        if len(self.history) < 2:
            return
        prev = (self.history[-2], opponent.history[-2])
        opp_act = 1 if opponent.history[-1] == C else 0
        if prev == (C, C):
            self.opp_after_CC.append(opp_act)
            self.opp_pr_c_after_CC = find_recent_average(self.opp_after_CC)
        elif prev == (C, D):
            self.opp_after_CD.append(opp_act)
            self.opp_pr_c_after_CD = find_recent_average(self.opp_after_CD)
        elif prev == (D, C):
            self.opp_after_DC.append(opp_act)
            self.opp_pr_c_after_DC = find_recent_average(self.opp_after_DC)
        elif prev == (D, D):
            self.opp_after_DD.append(opp_act)
            self.opp_pr_c_after_DD = find_recent_average(self.opp_after_DD)
        self.opp_model = [self.opp_pr_c_after_CC, self.opp_pr_c_after_DC, self.opp_pr_c_after_CD, self.opp_pr_c_after_DD]

    def _get_state_idx(self, opponent) -> int:
        if not self.history:
            # Pretend we started with CC
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
        self._update_opponent_model(opponent)
        state_idx = self._get_state_idx(opponent)
        expected, my_policy = optimize_against(self.opp_model,
                                               init_state_idx=state_idx,
                                               p_noise=self.noise)
        self.my_policy = my_policy
        return expected

    def act(self, opponent) -> Action:
        state_idx = self._get_state_idx(opponent)
        pr_c = self.my_policy[state_idx]
        return C if np.random.uniform() < pr_c else D

    def strategy(self, opponent: Player) -> Action:
        _ = self.update(opponent)
        return self.act(opponent)
