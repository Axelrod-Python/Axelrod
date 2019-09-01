import random
from random import randrange
import numpy as np
from numpy.random import choice

from axelrod.action import Action
from axelrod.player import EvolvablePlayer, Player
from axelrod.random_ import random_choice

C, D = Action.C, Action.D

# Type Hinting has not finished yet
# Lines 9 and 10 will be deleted


def is_stochastic_matrix(m, ep=1e-8) -> bool:
    """Checks that the matrix m (a list of lists) is a stochastic matrix."""
    for i in range(len(m)):
        for j in range(len(m[i])):
            if (m[i][j] < 0) or (m[i][j] > 1):
                return False
        s = sum(m[i])
        if abs(1.0 - s) > ep:
            return False
    return True


def copy_lists(rows):
    new_rows = list(map(list, rows))
    return new_rows


def random_vector(size):
    """Create a random vector of values in [0, 1] that sums to 1."""
    vector = []
    s = 1
    for _ in range(size - 1):
        r = s * random.random()
        vector.append(r)
        s -= r
    vector.append(s)
    return vector


def normalize_vector(vec):
    s = sum(vec)
    if s == 0.0:
        n = len(vec)
        return [1 / n for v in vec]
    vec = [v / s for v in vec]
    return vec


def mutate_row(row, mutation_probability):
    """
    Given a row of probabilities, randomly change each entry with probability
    `mutation_probability` (a value between 0 and 1).  If changing, then change
    by a value randomly (uniformly) chosen from [-0.25, 0.25] bounded by 0 and
    100%.
    """
    randoms = np.random.random(len(row))
    for i in range(len(row)):
        if randoms[i] < mutation_probability:
            ep = random.uniform(-1, 1) / 4
            row[i] += ep
            if row[i] < 0:
                row[i] = 0
            if row[i] > 1:
                row[i] = 1
    return row


class SimpleHMM(object):
    """Implementation of a basic Hidden Markov Model. We assume that the
    transition matrix is conditioned on the opponent's last action, so there
    are two transition matrices. Emission distributions are stored as Bernoulli
    probabilities for each state. This is essentially a stochastic FSM.

    https://en.wikipedia.org/wiki/Hidden_Markov_model
    """

    def __init__(
        self, transitions_C, transitions_D, emission_probabilities, initial_state
    ) -> None:
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
        for attr in [
            "transitions_C",
            "transitions_D",
            "emission_probabilities",
            "state",
        ]:
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
        "memory_depth": 1,
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(
        self,
        transitions_C=None,
        transitions_D=None,
        emission_probabilities=None,
        initial_state=0,
        initial_action=C
    ) -> None:
        super().__init__()
        if not transitions_C:
            transitions_C = [[1]]
            transitions_D = [[1]]
            emission_probabilities = [0.5]  # Not stochastic
            initial_state = 0
        self.initial_state = initial_state
        self.initial_action = initial_action
        self.hmm = SimpleHMM(
            copy_lists(transitions_C), copy_lists(transitions_D), list(emission_probabilities), initial_state
        )
        assert self.hmm.is_well_formed()
        self.state = self.hmm.state
        self.classifier["stochastic"] = self.is_stochastic()

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


class EvolvableHMMPlayer(HMMPlayer, EvolvablePlayer):
    """Evolvable version of HMMPlayer."""
    def __init__(
        self,
        transitions_C=None,
        transitions_D=None,
        emission_probabilities=None,
        initial_state=0,
        initial_action=C,
        num_states=None,
        mutation_probability=None
    ) -> None:
        if not (emission_probabilities and transitions_C and transitions_D and (initial_state is not None) and (initial_action is not None)):
            if not num_states:
                raise Exception("Insufficient Parameters to instantiate EvolvableHMMPlayer")
            self.randomize(num_states)
        HMMPlayer.__init__(self,
                           transitions_C=self.init_kwargs["transitions_C"],
                           transitions_D=self.init_kwargs["transitions_D"],
                           emission_probabilities=self.init_kwargs["emission_probabilities"],
                           initial_state=self.init_kwargs["initial_state"],
                           initial_action=self.init_kwargs["initial_action"])
        EvolvablePlayer.__init__(self)

        if mutation_probability is None:
            self.mutation_probability = 10 / (num_states ** 2)
        else:
            self.mutation_probability = mutation_probability

    @property
    def num_states(self):
        return len(self.hmm.emission_probabilities)

    @staticmethod
    def random_params(num_states):
        t_C = []
        t_D = []
        p = []
        for _ in range(num_states):
            t_C.append(random_vector(num_states))
            t_D.append(random_vector(num_states))
            p.append(random.random())
        initial_state = randrange(num_states)
        initial_action = C
        return p, t_C, t_D, initial_state, initial_action

    def randomize(self, num_states=None):
        if not num_states:
            num_states = self.num_states
        emission_probabilities, transitions_C, transitions_D, initial_state, initial_action = self.random_params(num_states)
        self.initial_state = initial_state
        self.initial_action = initial_action
        self.init_kwargs["transitions_C"] = transitions_C
        self.init_kwargs["transitions_D"] = transitions_D
        self.init_kwargs["emission_probabilities"] = emission_probabilities
        self.init_kwargs["initial_state"] = initial_state
        self.init_kwargs["initial_action"] = initial_action

    @staticmethod
    def mutate_rows(rows, mutation_probability):
        for i, row in enumerate(rows):
            row = mutate_row(row, mutation_probability)
            rows[i] = normalize_vector(row)
        return rows

    def mutate(self):
        self.hmm.transitions_C = self.mutate_rows(
            self.hmm.transitions_C, self.mutation_probability)
        self.hmm.transitions_D = self.mutate_rows(
            self.hmm.transitions_D, self.mutation_probability)
        self.hmm.emission_probabilities = mutate_row(
            self.hmm.emission_probabilities, self.mutation_probability)
        if random.random() < self.mutation_probability / 10:
            self.initial_action = self.initial_action.flip()
        if random.random() < self.mutation_probability / (10 * self.num_states):
            self.initial_state = randrange(self.num_states)
        self.init_kwargs["transitions_C"] = self.hmm.transitions_C
        self.init_kwargs["transitions_D"] = self.hmm.transitions_D
        self.init_kwargs["emission_probabilities"] = self.hmm.emission_probabilities
        self.init_kwargs["initial_state"] = self.initial_state
        self.init_kwargs["initial_action"] = self.initial_action

    @staticmethod
    def crossover_rows(rows1, rows2):
        num_states = len(rows1)
        crosspoint = randrange(num_states)
        new_rows = copy_lists(rows1[:crosspoint])
        new_rows += copy_lists(rows2[crosspoint:])
        return new_rows

    @staticmethod
    def crossover_weights(w1, w2):
        crosspoint = random.randrange(len(w1))
        new_weights = list(w1[:crosspoint]) + list(w2[crosspoint:])
        return new_weights

    def crossover(self, other):
        # Assuming that the number of states is the same
        t_C = self.crossover_rows(self.hmm.transitions_C, other.hmm.transitions_C)
        t_D = self.crossover_rows(self.hmm.transitions_D, other.hmm.transitions_D)
        emissions = self.crossover_weights(
            self.hmm.emission_probabilities, other.hmm.emission_probabilities)
        return EvolvableHMMPlayer(
            transitions_C=t_C,
            transitions_D=t_D,
            emission_probabilities=emissions,
            initial_state=self.initial_state,
            initial_action=self.initial_action,
            num_states=self.num_states,
            mutation_probability=self.mutation_probability)

    def receive_vector(self, vector):
        """
        Read a serialized vector into the set of HMM parameters (less initial
        state).  Then assign those HMM parameters to this class instance.

        Assert that the vector has the right number of elements for an HMMParams
        class with self.num_states.

        Assume the first num_states^2 entries are the transitions_C matrix.  The
        next num_states^2 entries are the transitions_D matrix.  Then the next
        num_states entries are the emission_probabilities vector.  Finally the last
        entry is the initial_action.
        """

        assert(len(vector) == 2 * self.num_states ** 2 + self.num_states + 1)

        def deserialize(vector):
            matrix = []
            for i in range(self.num_states):
                row = vector[self.num_states * i: self.num_states * (i + 1)]
                row = normalize_vector(row)
                matrix.append(row)
            return matrix

        break_tc = self.num_states ** 2
        break_td = 2 * self.num_states ** 2
        break_ep = 2 * self.num_states ** 2 + self.num_states
        initial_state = 0
        self.hmm = SimpleHMM(
            deserialize(vector[0:break_tc]),
            deserialize(vector[break_tc:break_td]),
            normalize_vector(vector[break_td:break_ep]),
            initial_state
        )
        self.initial_action = C if round(vector[-1]) == 0 else D
        self.initial_state = initial_state

    def create_vector_bounds(self):
        """Creates the bounds for the decision variables."""
        vec_len = 2 * self.num_states ** 2 + self.num_states + 1
        lb = [0.0] * vec_len
        ub = [1.0] * vec_len
        return lb, ub

    @classmethod
    def repr_rows(cls, rows):
        ss = []
        for row in rows:
            ss.append("_".join(list(map(str, row))))
        return "|".join(ss)

    def serialize_parameters(self):
        return "{}:{}:{}:{}:{}".format(
            self.initial_state,
            self.initial_action,
            self.repr_rows(self.hmm.transitions_C),
            self.repr_rows(self.hmm.transitions_D),
            self.repr_rows([self.hmm.emission_probabilities])
        )

    @classmethod
    def parse_vector(cls, line):
        row = line.split('_')
        row = list(map(float, row))
        return row

    @classmethod
    def parse_matrix(cls, sm):
        rows = []
        lines = sm.split('|')
        for line in lines:
            rows.append(cls.parse_vector(line))
        return rows

    @classmethod
    def deserialize_parameters(cls, serialized):
        lines = serialized.split(':')
        initial_state = int(lines[0])
        initial_action = Action.from_char(lines[1])
        t_C = cls.parse_matrix(lines[2])
        t_D = cls.parse_matrix(lines[3])
        p = cls.parse_vector(lines[4])
        num_states = len(t_C)

        return cls(num_states=num_states,
                   transitions_C=t_C,
                   transitions_D=t_D,
                   emission_probabilities=p,
                   initial_state=initial_state,
                   initial_action=initial_action)


class EvolvedHMM5(HMMPlayer):
    """
    An HMM-based player with five hidden states trained with an evolutionary
    algorithm.

    Names:

        - Evolved HMM 5: Original name by Marc Harper
    """

    name = "Evolved HMM 5"

    classifier = {
        "memory_depth": 5,
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self) -> None:
        initial_state = 3
        initial_action = C
        t_C = [
            [1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0.631, 0, 0, 0.369, 0],
            [0.143, 0.018, 0.118, 0, 0.721],
        ]

        t_D = [
            [0, 1, 0, 0, 0],
            [0, 0.487, 0.513, 0, 0],
            [0, 0, 0, 0.590, 0.410],
            [1, 0, 0, 0, 0],
            [0, 0.287, 0.456, 0.146, 0.111],
        ]

        emissions = [1, 0, 0, 1, 0.111]
        super().__init__(t_C, t_D, emissions, initial_state, initial_action)
