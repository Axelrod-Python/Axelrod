import random
from axelrod.action import Action
from axelrod import random_choice
from axelrod.player import Player

C, D = Action.C, Action.D


class BushMosteller(Player):
    """
    A player that is based on Bush Mosteller reinforced learning algorithm, it
    decides what it will
    play only depending on its own previous payoffs.

    The probability of playing C or D will be updated using a stimulus which
    represents a win or a loss of value based on its previous play's payoff in
    the specified probability.  The more a play will be rewarded through rounds,
    the more the player will be tempted to use it.

    Names:

    - Bush Mosteller: [Luis2008]_
    """

    name = 'Bush Mosteller'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(["game"]),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }


    def __init__(self, c_prob: float = 0.5, d_prob: float = 0.5,
                 aspiration_level_divider: float = 3.0,
                 learning_rate: float = 0.5) -> None:
        """
        Parameters

        c_prob: float, 0.5
           Probability to play C , is modified during the match
        d_prob: float, 0.5
           Probability to play D , is modified during the match
        aspiration_level_divider: float, 3.0
            Value that regulates the aspiration level,
            isn't modified during match
		learning rate [0 , 1]
			Percentage of learning speed
        Variables / Constants
		_stimulus (Var: [-1 , 1]): float
            Value that impacts the changes of action probability
        _aspiration_level: float
            Value that impacts the stimulus changes, isn't modified during match
        _init_c_prob , _init_d_prob : float
        	Values used to properly set up reset(),
            set to original probabilities
        """
        super().__init__()
        self._c_prob , self._d_prob = c_prob , d_prob
        self._init_c_prob , self._init_d_prob = c_prob , d_prob
        self._aspiration_level = abs((max(self.match_attributes["game"].RPST())
                                     / aspiration_level_divider))

        self._stimulus = 0.0
        self._learning_rate = learning_rate

    def stimulus_update(self, opponent: Player):
        """
        Updates the stimulus attribute based on the opponent's history. Used by
        the strategy.

        Parameters

        opponent : axelrod.Player
            The current opponent
        """
        game = self.match_attributes["game"]

        last_round = (self.history[-1], opponent.history[-1])

        scores = game.score(last_round)

        previous_play = scores[0]

        self._stimulus = ((previous_play - self._aspiration_level) /
                          abs((max(self.match_attributes["game"].RPST()) -
                                   self._aspiration_level)))
        # Lowest range for stimulus
        # Highest doesn't need to be tested since it is divided by the highest
        # reward possible
        if self._stimulus < -1:
            self._stimulus = -1

        # Updates probability following previous choice C
        if self.history[-1] == C:

            if self._stimulus >= 0:
                self._c_prob += (self._learning_rate * self._stimulus *
                                 (1 - self._c_prob))

            elif self._stimulus < 0:
                self._c_prob += (self._learning_rate * self._stimulus *
                                 self._c_prob)

        # Updates probability following previous choice D
        if self.history[-1] == D:
            if self._stimulus >= 0:
                self._d_prob += (self._learning_rate * self._stimulus *
                                 (1 - self._d_prob))

            elif self._stimulus < 0:
                self._d_prob += (self._learning_rate * self._stimulus *
                                 self._d_prob)


    def strategy(self, opponent: Player) -> Action:

        # First turn
        if len(self.history) == 0:
            return random_choice(self._c_prob / (self._c_prob + self._d_prob))

        # Updating stimulus depending on his own latest choice
        self.stimulus_update(opponent)

        return random_choice(self._c_prob / (self._c_prob + self._d_prob))
