from axelrod import Player
import random

class RiskyQLearner(Player):
    """
    A player who learns the best strategies through the q-learning algorithm

    This qlearner is quick to come to conclusions and doesn't care about the future
    """
    learning_rate = 0.9
    discount_rate = 0.9
    action_selection_parameter = 0.1
    memory_length = 12
    def __init__(self):
        """
        Initialises the player by picking a random strategy
        """
        super(RiskyQLearner, self).__init__()
        self.prev_action = random.choice(['C', 'D'])
        self.history = []
        self.score = 0
        self.Qs = {'':{'C':0, 'D':0}}
        self.Vs = {'':0}
        self.prev_state = ''


    def strategy(self, opponent):
        """
        Runs a qlearn algorithm while the tournament is running
        """
        state = self.find_state(opponent)
        reward = self.find_reward(opponent)
        if state not in self.Qs:
            self.Qs[state] = {'C':0, 'D':0}
            self.Vs[state] = 0
        self.perform_q_learning(self.prev_state, state, self.prev_action, reward)
        if state not in self.Qs:
            action =  random.choice(['C', 'D'])
        else:
            action = self.select_action(state)
        self.prev_state = state
        self.prev_action = action
        return action


    def select_action(self, state):
        """
        Selects the action based on the epsilon-soft policy
        """
        rnd_num = random.random()
        if rnd_num < (1-self.action_selection_parameter):
            return max(self.Qs[state], key=lambda x: self.Qs[state][x])
        return random.choice(['C', 'D'])


    def find_state(self, opponent):
        """
        Finds the my_state (the opponents last n moves +  its previous proportion of playing 'C') as a hashable state
        """
        prob = round(sum([i=='C' for i in opponent.history]), 1)
        return ''.join(opponent.history[-self.memory_length:]) + str(prob)


    def perform_q_learning(self, prev_state, state, action, reward):
        """
        Performs the qlearning algorithm
        """
        self.Qs[prev_state][action] = (1-self.learning_rate)*self.Qs[prev_state][action] + self.learning_rate*(reward + self.discount_rate*self.Vs[state])
        self.Vs[prev_state] = max(self.Qs[prev_state].values())

    def find_reward(self, opponent):
        """
        Finds the reward gained on the last iteration
        """
        payoff_matrix = {'C':{'C':1, 'D':-2}, 'D':{'C':3, 'D':-1}}
        if len(opponent.history) == 0:
            opp_prev_action = random.choice(['C', 'D'])
        else:
            opp_prev_action = opponent.history[-1]
        return payoff_matrix[self.prev_action][opp_prev_action]

    def reset(self):
        """
        Resets scores and history
        """
        self.history = []

        self.Qs = {'':{'C':0, 'D':0}}
        self.Vs = {'':0}
        self.prev_state = ''
        self.prev_action = random.choice(['C', 'D'])

    def __repr__(self):
        """
        The string method for the strategy:
        """
        return 'Risky QLearner'


class ArrogantQLearner(RiskyQLearner):
    """
    A player who learns the best strategies through the q-learning algorithm

    This Q learner jumps to quick conclusions and care about the future
    """
    learning_rate = 0.9
    discount_rate = 0.1

    def __init__(self):
        """
        Initialises the player by picking a random strategy
        """
        super(RiskyQLearner, self).__init__()
        self.prev_action = random.choice(['C', 'D'])
        self.history = []
        self.score = 0
        self.Qs = {'':{'C':0, 'D':0}}
        self.Vs = {'':0}
        self.prev_state = ''

    def __repr__(self):
        """
        The string method for the strategy:
        """
        return 'Arrogant QLearner'


class HesitantQLearner(RiskyQLearner):
    """
    A player who learns the best strategies through the q-learning algorithm

    This Q learner is slower to come to conclusions and does not look ahead much
    """
    learning_rate = 0.1
    discount_rate = 0.9

    def __init__(self):
        """
        Initialises the player by picking a random strategy
        """
        super(RiskyQLearner, self).__init__()
        self.prev_action = random.choice(['C', 'D'])
        self.history = []
        self.score = 0
        self.Qs = {'':{'C':0, 'D':0}}
        self.Vs = {'':0}
        self.prev_state = ''


    def __repr__(self):
        """
        The string method for the strategy:
        """
        return 'Hesitant QLearner'

class CautiousQLearner(RiskyQLearner):
    """
    A player who learns the best strategies through the q-learning algorithm

    This Q learner is slower to come to conclusions and wants to look ahead more
    """
    learning_rate = 0.1
    discount_rate = 0.1

    def __init__(self):
        """
        Initialises the player by picking a random strategy
        """
        super(RiskyQLearner, self).__init__()
        self.prev_action = random.choice(['C', 'D'])
        self.history = []
        self.score = 0
        self.Qs = {'':{'C':0, 'D':0}}
        self.Vs = {'':0}
        self.prev_state = ''

    def __repr__(self):
        """
        The string method for the strategy:
        """
        return 'Cautious QLearner'
