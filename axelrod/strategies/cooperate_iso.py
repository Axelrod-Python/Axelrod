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
