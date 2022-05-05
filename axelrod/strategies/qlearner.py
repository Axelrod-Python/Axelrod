from collections import OrderedDict
from typing import Dict, Union

from axelrod.action import Action, actions_to_str
from axelrod.player import Player

import csv
from csv import reader

Score = Union[int, float]

C, D = Action.C, Action.D


class RiskyQLearner(Player):
    """A player who learns the best strategies through the q-learning
    algorithm.

    This Q learner is quick to come to conclusions and doesn't care about the
    future.

    Names:

    - Risky Q Learner: Original name by Geraint Palmer
    """

    name = "Risky QLearner"
    classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }
    learning_rate = 0.9
    discount_rate = 0.33
    action_selection_parameter = 0.1 # was 0.1
    memory_length = 12 #reduce to 6

    def __init__(self) -> None:
        """Initialises the player by picking a random strategy."""

        super().__init__()

        # Set this explicitly, since the constructor of super will not pick it up
        # for any subclasses that do not override methods using random calls.
        self.classifier["stochastic"] = True

        self.prev_action = None  # type: Action
        self.original_prev_action = None  # type: Action
        self.score = 0
        self.Qs = OrderedDict({"": OrderedDict(zip([C, D], [0, 0]))})
        self.Vs = OrderedDict({"": 0})
        self.prev_state = ""

    def receive_match_attributes(self):
        (R, P, S, T) = self.match_attributes["game"].RPST()
        self.payoff_matrix = {C: {C: R, D: S}, D: {C: T, D: P}}

    def strategy(self, opponent: Player) -> Action:
        """Runs a qlearn algorithm while the tournament is running."""
        self.receive_match_attributes()
        if len(self.history) == 0:
            self.prev_action = self._random.random_choice()
            self.original_prev_action = self.prev_action
        state = self.find_state(opponent)
        reward = self.find_reward(opponent)
        if state not in self.Qs:
            self.Qs[state] = OrderedDict(zip([C, D], [0, 0])) #change
            self.Vs[state] = 0
        self.perform_q_learning(
            self.prev_state, state, self.prev_action, reward
        )
        action = self.select_action(state)
        self.prev_state = state
        self.prev_action = action
        return action

    def select_action(self, state: str) -> Action:
        """
        Selects the action based on the epsilon-soft policy
        """
        rnd_num = self._random.random()
        p = 1.0 - self.action_selection_parameter
        if rnd_num < p:
            return max(self.Qs[state], key=lambda x: self.Qs[state][x]) #change
        return self._random.random_choice()

    def find_state(self, opponent: Player) -> str: 
        """
        Finds the my_state (the opponents last n moves +
        its previous proportion of playing C) as a hashable state
        """
        prob = "{:.1f}".format(opponent.cooperations)
        action_str = actions_to_str(opponent.history[-self.memory_length :])
        change_prob = str(self.match_attributes["change_prob"])
        exp_coop_reward = str(self.match_attributes["exp_coop_reward"])
        return action_str + prob + exp_coop_reward #CHANGED STATE

    def perform_q_learning( #glue state to action
        self, prev_state: str, state: str, action: Action, reward
    ):
        """
        Performs the qlearning algorithm
        """
        self.Qs[prev_state][action] = (1.0 - self.learning_rate) * self.Qs[
            prev_state
        ][action] + self.learning_rate * (
            reward + self.discount_rate * self.Vs[state]
        )
        self.Vs[prev_state] = max(self.Qs[prev_state].values())

    def find_reward(
        self, opponent: Player
    ) -> Dict[Action, Dict[Action, Score]]:
        """
        Finds the reward gained on the last iteration
        """

        if len(opponent.history) == 0:
            opp_prev_action = self._random.random_choice()
        else:
            opp_prev_action = opponent.history[-1]
        return self.payoff_matrix[self.prev_action][opp_prev_action]

    def load_state(self):
        # open file in read mode
        values = []
        keys = []
        with open('Qtable_values.csv', 'r') as read_obj:
            csv_reader = reader(read_obj)
            for row in csv_reader:
                values += row
        dict = self.dictify(values)
        with open('Qtable_keys.csv', 'r') as read_obj:
            csv_reader = reader(read_obj)
            for row in csv_reader:
                keys += row
        if len(values) > 0:
            self.Qs = OrderedDict([(k,v) for k,v in zip(keys, dict)])
        
        values = []
        keys = []
        with open('Vtable_values.csv', 'r') as read_obj:
            csv_reader = reader(read_obj)
            for row in csv_reader:
                values += [float(i) for i in row]
        with open('Vtable_keys.csv', 'r') as read_obj:
            csv_reader = reader(read_obj)
            for row in csv_reader:
                keys += row
        
        if len(values) > 1:
            self.Vs = OrderedDict([(k, v) for k, v in zip(keys, values)])

    def dictify(self, list):
        #convert the list of stringed C and D values to ordered dict
        dicts = []
        previous = -1
        for element in list:
            value = float(element)
            if previous == -1:
                previous = value
            else:
                dicts.append(OrderedDict(zip([C, D], [previous, float(element)])))
                previous = -1
        return dicts

    def save_state(self):
        keys, values = [], []

        for key, value in self.Qs.items():
            keys.append(key)
            for k, v in value.items():
                values.append(v)

        with open("Qtable_keys.csv", "w") as outfile:
            csvwriter = csv.writer(outfile)
            csvwriter.writerow(keys)
        
        with open("Qtable_values.csv", "w") as outfile:
            csvwriter = csv.writer(outfile)
            csvwriter.writerow(values)

        keys, values = [], []

        for key, value in self.Vs.items():
            keys.append(key)
            values.append(value)       

        with open("Vtable_keys.csv", "w") as outfile:
            csvwriter = csv.writer(outfile)
            csvwriter.writerow(keys)

        with open("Vtable_values.csv", "w") as outfile:
            csvwriter = csv.writer(outfile)
            csvwriter.writerow(values)

class ArrogantQLearner(RiskyQLearner):
    """A player who learns the best strategies through the q-learning
    algorithm.

    This Q learner jumps to quick conclusions and cares about the future.

    Names:

    - Arrogant Q Learner: Original name by Geraint Palmer
    """

    name = "Arrogant QLearner"
    learning_rate = 0.9
    discount_rate = 0.1

class StochasticQLearner(RiskyQLearner):
    """An algorithm choosing the probability to cooperate, p, instead of 
    choosing a definite action
    
    This Q Learner should be more flexible and create more mixed strategies
    """
    name = "Stochastic QLearner"
    learning_rate = 0.9
    discount_rate = 0.33

    def __init__(self) -> None:
        """Initialises the player by picking a random strategy."""

        super().__init__()

        # Set this explicitly, since the constructor of super will not pick it up
        # for any subclasses that do not override methods using random calls.
        self.classifier["stochastic"] = True

        self.prev_action = None  # type: Action
        self.prev_prob = None #type: Action
        self.original_prev_action = None  # type: Action
        self.score = 0
        self.Qs = OrderedDict({"": OrderedDict(zip([Action.One, Action.Two, Action.Three, Action.Four, Action.Five, Action.Six, Action.Seven, Action.Eight, Action.Nine, Action.Ten], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))})
        self.Vs = OrderedDict({"": 0})
        self.prev_state = ""

    def strategy(self, opponent: Player) -> Action:
        """Runs a qlearn algorithm while the tournament is running."""
        self.receive_match_attributes()
        if len(self.history) == 0:
            self.prev_prob = self._random.random_prob()
            self.prev_action = self._random.random_choice()
            self.original_prev_action = self.prev_action
        state = self.find_state(opponent)
        reward = self.find_reward(opponent)
        if state not in self.Qs:
            self.Qs[state] = OrderedDict(zip([Action.One, Action.Two, Action.Three, Action.Four, Action.Five, Action.Six, Action.Seven, Action.Eight, Action.Nine, Action.Ten], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])) #change
            self.Vs[state] = 0
        self.perform_q_learning(
            self.prev_state, state, self.prev_prob, reward
        )
        action, prob = self.select_action(state)
        self.prev_state = state
        self.prev_action = action
        self.prev_prob = prob
        return action
    
    def select_action(self, state: str) -> Action:
        """
        Selects the action based on the epsilon-soft policy
        """
        rnd_num = self._random.random()
        p = 1.0 - self.action_selection_parameter
        if rnd_num < p:
            values = OrderedDict(zip([Action.One, Action.Two, Action.Three, Action.Four, Action.Five, Action.Six, Action.Seven, Action.Eight, Action.Nine, Action.Ten], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]))
            rng = self._random.random()
            if rng < values[max(self.Qs[state], key=lambda x: self.Qs[state][x])]: #change
                return C, max(self.Qs[state], key=lambda x: self.Qs[state][x])
            else:
                return D, max(self.Qs[state], key=lambda x: self.Qs[state][x])
        return self._random.random_choice(), self._random.random_prob()

    def perform_q_learning( #glue state to action
        self, prev_state: str, state: str, action: Action, reward
    ):
        """
        Performs the qlearning algorithm
        """
        self.Qs[prev_state][action] = (1.0 - self.learning_rate) * self.Qs[
            prev_state
        ][action] + self.learning_rate * (
            reward + self.discount_rate * self.Vs[state]
        )
        self.Vs[prev_state] = max(self.Qs[prev_state].values())

    def dictify(self, list):
        #convert the list of stringed C and D values to ordered dict
        dicts = []
        gather_ten_values = []
        for element in list:
            value = float(element)
            if len(gather_ten_values) < 10:
                gather_ten_values.append(value)
            else:
                dicts.append(OrderedDict(zip([Action.One, Action.Two, Action.Three, Action.Four, Action.Five, Action.Six, Action.Seven, Action.Eight, Action.Nine, Action.Ten], gather_ten_values)))
                gather_ten_values = []
                gather_ten_values.append(value)
        return dicts
  
class HesitantQLearner(RiskyQLearner):
    """A player who learns the best strategies through the q-learning algorithm.

    This Q learner is slower to come to conclusions and does not look ahead much.

    Names:

    - Hesitant Q Learner: Original name by Geraint Palmer
    """

    name = "Hesitant QLearner"
    learning_rate = 0.1
    discount_rate = 0.9


class CautiousQLearner(RiskyQLearner):
    """A player who learns the best strategies through the q-learning algorithm.

    This Q learner is slower to come to conclusions and wants to look ahead
    more.

    Names:

    - Cautious Q Learner: Original name by Geraint Palmer
    """

    name = "Cautious QLearner"
    learning_rate = 0.1
    discount_rate = 0.1
