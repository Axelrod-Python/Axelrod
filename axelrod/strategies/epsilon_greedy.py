from axelrod.action import Action
from axelrod.player import Player

C, D = Action.C, Action.D


class EpsilonGreedy(Player):
    """
    Behaves greedily (chooses the optimal action) with a probability of 1 - epsilon,
    and chooses randomly between the actions with a probability of epsilon.

    The optimal action is determined from the average payoff of each action in previous turns.

    Names:

    # TODO: reference Sutton & Barto's Reinforcement Learning: an Introduction 2nd Ed.
    """

    name = "$\varepsilon$-greedy"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(
        self,
        epsilon: float = 0.1,
        init_c_reward: float = 0.0,
        init_d_reward: float = 0.0,
    ) -> None:
        """
        Parameters
        ----------
        epsilon
            0.0 <= epsilon <= 1.0
            the probability that the player will "explore" (act uniformly random); defaults to 0.1
        init_c_reward
            initial expected utility from action C; defaults to 0.0.
        init_d_reward
            initial expected utility from action D; defaults to 0.0

        Special cases
        ----------
            epsilon = 0 is equal to Random(0.5)
        """
        super().__init__()
        self.epsilon = epsilon

        # treat out of range values as extremes
        if epsilon <= 0:
            self.epsilon = 0.0
        if epsilon >= 1:
            self.epsilon = 1.0

        self._rewards = {C: init_c_reward, D: init_d_reward}

    def _post_init(self):
        super()._post_init()
        if self.epsilon == 0:
            self.classifier["stochastic"] = False

    def update_rewards(self, opponent: Player):
        game = self.match_attributes["game"]
        last_round = (self.history[-1], opponent.history[-1])
        last_play = self.history[-1]
        last_score = game.score(last_round)[0]

        # update the expected rewards based on previous play
        if last_play == C:
            num_plays = self.history.cooperations
        else:
            num_plays = self.history.defections

        self._rewards[last_play] = self._rewards[last_play] + (
            1 / num_plays
        ) * (last_score - self._rewards[last_play])

    def strategy(self, opponent: Player) -> Action:
        """Actual strategy definition that determines player's action."""
        # if not the first turn
        if len(self.history) != 0:
            self.update_rewards(opponent)

        # explore
        if self.epsilon > 0 and self._random.uniform(0.0, 1.0) <= self.epsilon:
            return self._random.random_choice()
        # exploit
        else:
            return max(self._rewards, key=self._rewards.get)
