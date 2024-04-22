import numpy as np

from axelrod.action import Action
from axelrod.player import Player

C, D = Action.C, Action.D


class Greedy(Player):
    """
    A player that always chooses the optimal action based on the average reward of each action from previous turns.

    If initial rewards for each action are equivalent (true by default),
    then the optimal action for the first turn is cooperate.

    Names:

    - Greedy: [Sutton2018]_
    """

    name = "greedy"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    UNIFORM = -1.0  # constant that replaces weight when rewards aren't weighted

    def __init__(
        self,
        init_c_reward: float = 0.0,
        init_d_reward: float = 0.0,
        recency_weight: float = UNIFORM,
    ) -> None:
        """
        Parameters
        ----------
        init_c_reward
            Initial expected utility from action C; defaults to 0.0.
        init_d_reward
            Initial expected utility from action D; defaults to 0.0
        recency_weight
            0.0 <= recency_weight <= 1.0
            The exponential recency weight used in calculating the average reward.
            If this argument is equal to -1 or is not provided, the player will not weigh rewards based on recency.
        """
        super().__init__()
        self._rewards = {C: init_c_reward, D: init_d_reward}
        self.weight = recency_weight

        # limit parameter value range
        if (self.weight != self.UNIFORM) and self.weight <= 0:
            self.weight = 0.0
        if self.weight >= 1:
            self.weight = 1.0

    def update_rewards(self, opponent: Player):
        """Updates the expected reward associated with the last action."""
        game = self.match_attributes["game"]
        last_round = (self.history[-1], opponent.history[-1])
        last_play = self.history[-1]
        last_score = game.score(last_round)[0]

        # if UNIFORM, use 1 / total number of times the updated action was taken previously
        if self.weight == self.UNIFORM:
            weight = 1 / (
                self.history.cooperations if last_play == C else self.history.defections
            )
        else:
            weight = self.weight

        self._rewards[last_play] = self._rewards[last_play] + weight * (
            last_score - self._rewards[last_play]
        )

    def strategy(self, opponent: Player) -> Action:
        # if not the first turn
        if len(self.history) != 0:
            self.update_rewards(opponent)

        # select the optimal play
        return max(self._rewards, key=self._rewards.get)


class EpsilonGreedy(Greedy):
    """
    Has a 1 - epsilon probability of behaving like Greedy; otherwise, randomly choose to cooperate or defect.

    Names:

    - Epsilon-greedy: [Sutton2018]_
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
        recency_weight: float = Greedy.UNIFORM,
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
            When epsilon <= 0, this player behaves like Random(0.5)
            When epsilon >= 1, this player behaves like Greedy()
        """
        super().__init__(init_c_reward, init_d_reward, recency_weight)
        self.epsilon = epsilon

        # treat out of range values as extremes
        if epsilon <= 0:
            self.epsilon = 0.0
        if epsilon >= 1:
            self.epsilon = 1.0

    def _post_init(self):
        super()._post_init()
        if self.epsilon == 0:
            self.classifier["stochastic"] = False

    def strategy(self, opponent: Player) -> Action:
        # this will also update the reward appropriately
        greedy_action = super().strategy(opponent)

        # explore
        if self.epsilon > 0 and self._random.uniform() <= self.epsilon:
            return self._random.random_choice()
        # exploit
        else:
            return greedy_action
