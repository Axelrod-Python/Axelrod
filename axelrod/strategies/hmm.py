from numpy.random import choice

from axelrod.actions import Actions , Action
from axelrod.player import Player
from axelrod.random_ import random_choice

C, D = Actions.C, Actions.D

#Type Hinting has not finished yet
#Lines 9 and 10 will be deleted

def is_stochastic_matrix(m, ep=1e-8) -> bool:
    """Checks that the matrix m (a list of lists) is a stochastic matrix."""
    for i in range(len(m)):
        for j in range(len(m[i])):
            if (m[i][j] < 0) or (m[i][j] > 1):
                return False
        s = sum(m[i])
        if abs(1. - s) > ep:
            return False
    return True


class SimpleHMM(object):
    """Implementation of a basic Hidden Markov Model. We assume that the
    transition matrix is conditioned on the opponent's last action, so there
    are two transition matrices. Emission distributions are stored as Bernoulli
    probabilities for each state. This is essentially a stochastic FSM.

    https://en.wikipedia.org/wiki/Hidden_Markov_model
    """

    def __init__(self, transitions_C, transitions_D, emission_probabilities,
                 initial_state) -> None:
        """
        Params
        ------
        transitions_C and transitions_D are square stochastic matrices:
            lists of lists with all values in [0, 1] and rows that sum to 1.
        emission_probabilities is a vector of values in [0, 1]
        initial_state is an element of range(0, len(emission_probabilities))
        """
        self.transitions_C = transitions_C
        self.transitions_D = transitions_D
        self.emission_probabilities = emission_probabilities
        self.state = initial_state

    def is_well_formed(self) -> bool:
        """
        Determines if the HMM parameters are well-formed:
            - Both matrices are stochastic
            - Emissions probabilities are in [0, 1]
            - The initial state is valid.
        """
        if not is_stochastic_matrix(self.transitions_C):
            return False
        if not is_stochastic_matrix(self.transitions_D):
            return False
        for p in self.emission_probabilities:
            if (p < 0) or (p > 1):
                return False
        if self.state not in range(0, len(self.emission_probabilities)):
            return False
        return True

    def __eq__(self, other: Player) -> bool:
        """Equality of two HMMs"""
        check = True
        for attr in ["transitions_C", "transitions_D",
                     "emission_probabilities", "state"]:
            check = check and getattr(self, attr) == getattr(other, attr)
        return check


    def move(self, opponent_action: Action) -> Action:
        """Changes state and computes the response action.

        Parameters
            opponent_action: Axelrod.Action
                The opponent's last action.
        """
        num_states = len(self.emission_probabilities)
        if opponent_action == C:
            next_state = choice(num_states, 1, p=self.transitions_C[self.state])
        else:
            next_state = choice(num_states, 1, p=self.transitions_D[self.state])
        self.state = next_state[0]
        p = self.emission_probabilities[self.state]
        action = random_choice(p)
        return action


class HMMPlayer(Player):
    """
    Abstract base class for Hidden Markov Model players.

    Names

        - HMM Player: Original name by Marc Harper
    """

    name = "HMM Player"

    classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, transitions_C=None, transitions_D=None,
                 emission_probabilities=None, initial_state=0,
                 initial_action=C) -> None:
        super().__init__()
        if not transitions_C:
            transitions_C = [[1]]
            transitions_D = [[1]]
            emission_probabilities = [0.5]  # Not stochastic
            initial_state = 0
        self.initial_state = initial_state
        self.initial_action = initial_action
        self.hmm = SimpleHMM(transitions_C, transitions_D,
                             emission_probabilities, initial_state)
        assert self.hmm.is_well_formed()
        self.state = self.hmm.state
        self.classifier['stochastic'] = self.is_stochastic()

    def is_stochastic(self) -> bool:
        """Determines if the player is stochastic."""
        # If the transitions matrices and emission_probabilities are all 0 or 1
        # Then the player is stochastic
        values = set(self.hmm.emission_probabilities)
        for m in [self.hmm.transitions_C, self.hmm.transitions_D]:
            for row in m:
                values.update(row)
        if not values.issubset({0, 1}):
            return True
        return False

    def strategy(self, opponent: Player) -> Action:
        if len(self.history) == 0:
            return self.initial_action
        else:
            action = self.hmm.move(opponent.history[-1])
            # Record the state for testing purposes, this isn't necessary
            # for the strategy to function
            self.state = self.hmm.state
            return action

    def reset(self) -> None:
        super().reset()
        self.hmm.state = self.initial_state
        self.state = self.hmm.state


class EvolvedHMM5(HMMPlayer):
    """
    An HMM-based player with five hidden states trained with an evolutionary
    algorithm.

    Names:

        - Evolved HMM 5: Original name by Marc Harper
    """
    name = "Evolved HMM 5"

    classifier = {
        'memory_depth': 5,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        initial_state = 3
        initial_action = C
        t_C = [[1, 0, 0, 0, 0],
               [0, 1, 0, 0, 0],
               [0, 1, 0, 0, 0],
               [0.631, 0, 0, 0.369, 0],
               [0.143, 0.018, 0.118, 0, 0.721]]

        t_D = [[0, 1, 0, 0, 0],
               [0, 0.487, 0.513, 0, 0],
               [0, 0, 0, 0.590, 0.410],
               [1, 0, 0, 0, 0],
               [0, 0.287, 0.456, 0.146, 0.111]]

        emissions = [1, 0, 0, 1, 0.111]
        super().__init__(t_C, t_D, emissions, initial_state,
                           initial_action)
