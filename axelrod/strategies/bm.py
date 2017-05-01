import random
from axelrod.actions import Actions, Action
from axelrod.player import Player

C, D = Actions.C, Actions.D


class BM(Player):
    """
    A player that is based on Bush Mosteller reinforced learning algorithm, he decides what he'll
    play only depending on his own previous payoffs.

    The probability of playing C or D will be updated using a stimulus which represents
    a win or a loss of value based on his previous play's payoff in the specified probability.
    The more a play will be rewarded through rounds , the more the player will be tempted to use it.
    
    Names:

    - Bush Mosteller: [Luis2008]_
    """

    name = 'Bush Mosteller'
    classifier = {
        'memory_depth': 1,  # Updates stimulus using last round
        'stochastic': True,
        'makes_use_of': set(["game"]),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    
    def __init__(self, c_probability: float = 0.5, d_probability: float = 0.5, aspiration_level_divider: float = 3.0, learning_rate: float = 0.5) -> None:
        """
        Parameters
        ----------
        c_probability: float, 0.5
           Probability to play C
        d_probability: float, 0.5
           Probability to play D 
        aspiration_level: float
            Value that impacts the stimulus changes, isn't modified during match
        aspiration_level_divider: float, 3.0
            Value that regulates the aspiration level, isn't modified during match
        stimulus
            Value that impacts the changes of action probability
        """
        super().__init__()
        self._c_probability , self._d_probability = c_probability , d_probability
        self._aspiration_level = abs((max(self.match_attributes["game"].RPST()) / aspiration_level_divider))
        self._stimulus = 0.0
        self._learning_rate = learning_rate

    
    def stimulus_update(self, opponent: Player):
        
        game = self.match_attributes["game"]

        last_round = (self.history[-1], opponent.history[-1])

        scores = game.score(last_round)
        
        previous_play = scores[0]

        self._stimulus = ((previous_play - self._aspiration_level) / abs((max(self.match_attributes["game"].RPST()) - self._aspiration_level)))
        
        if self._stimulus > 1:
            self._stimulus = 1
        elif self._stimulus < -1:
            self._stimulus = -1

        # Updates probability following previous choice C
        if self.history[-1] == C:
           
            if self._stimulus >= 0:
                self._c_probability = self._c_probability + self._learning_rate * self._stimulus * (1 - self._c_probability)
           
            elif self._stimulus < 0:
                self._c_probability = self._c_probability + self._learning_rate * self._stimulus * self._c_probability

        # Updates probability following previous choice D
        if self.history[-1] == D:
           
            if self._stimulus >= 0:
                self._d_probability = self._d_probability + self._learning_rate * self._stimulus * (1 - self._d_probability)
           
            elif self._stimulus < 0:
                self._d_probability = self._d_probability + self._learning_rate * self._stimulus * self._d_probability
    

    def BM_random_choice(self) -> Action:
        # Variable defining next choice probability 
        next_choice = random.uniform(0 , (self._c_probability + self._d_probability))

        # Return C if next choice is within c_probability range , returns D otherwise
        if next_choice < self._c_probability:
            return C
        return D

    def reset(self):
        """ Reset instance properties. """
        super().reset()
        self._c_probability = 0.5
        self._d_probability = 0.5
        self._stimulus = 0.0


    def strategy(self, opponent: Player) -> Action:

        # First turn
        if len(self.history) == 0:
            return self.BM_random_choice()
        
        # Updating stimulus depending on his own latest choice
        self.stimulus_update(opponent)

        return self.BM_random_choice()