from typing import Any, Dict

from axelrod.action import Action
from axelrod.evolvable_player import (
    EvolvablePlayer,
    InsufficientParametersError,
    copy_lists,
    crossover_lists,
)
from axelrod.player import Player

C, D = Action.C, Action.D


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


def normalize_vector(vec):
    s = sum(vec)
    vec = [v / s for v in vec]
    return vec


def mutate_row(row, mutation_probability, rng):
    """, crossover_lists_of_lists
    Given a row of probabilities, randomly change each entry with probability
    `mutation_probability` (a value between 0 and 1).  If changing, then change
    by a value randomly (uniformly) chosen from [-0.25, 0.25] bounded by 0 and
    100%.
    """
    randoms = rng.random(len(row))
    for i in range(len(row)):
        if randoms[i] < mutation_probability:
            ep = rng.uniform(-1, 1) / 4
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
        self._cache_C = dict()  # type: Dict[int, int]
        self._cache_D = dict()  # type: Dict[int, int]
        self._cache_deterministic_transitions()
        # Random generator will be set by parent strategy
        self._random = None  # type: Any

    def _cache_deterministic_transitions(self):
        """Cache deterministic transitions to avoid unnecessary random draws."""
        # If 1 is in the transition vector, it's deterministic. Just pick it out.
        # By caching we avoid repeated searches.
        for state in range(len(self.transitions_C)):
            if 1 in self.transitions_C[state]:
                self._cache_C[state] = self.transitions_C[state].index(1)
        for state in range(len(self.transitions_D)):
            if 1 in self.transitions_D[state]:
                self._cache_D[state] = self.transitions_D[state].index(1)

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
        # Choose next state.
        if opponent_action == C:
            try:
                next_state = self._cache_C[self.state]
            except KeyError:
                num_states = len(self.emission_probabilities)
                next_state = self._random.choice(num_states, 1, p=self.transitions_C[self.state])[0]
        else:
            try:
                next_state = self._cache_D[self.state]
            except KeyError:
                num_states = len(self.emission_probabilities)
                next_state = self._random.choice(num_states, 1, p=self.transitions_D[self.state])[0]

        self.state = next_state
        # Choose action to emit.
        p = self.emission_probabilities[self.state]
        if p == 0:
            return D
        if p == 1:
            return C
        action = self._random.random_choice(p)
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
        Player.__init__(self)
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

    def set_seed(self, seed=None):
        super().set_seed(seed=seed)
        # Share RNG with HMM
        # The evolvable version of the class needs to manually share the rng with the HMM
        # after initialization.
        try:
            self.hmm._random = self._random
        except AttributeError:
            pass


class EvolvableHMMPlayer(HMMPlayer, EvolvablePlayer):
    """Evolvable version of HMMPlayer."""
    name = "EvolvableHMMPlayer"

    def __init__(
        self,
        transitions_C=None,
        transitions_D=None,
        emission_probabilities=None,
        initial_state=0,
        initial_action=C,
        num_states=None,
        mutation_probability=None,
        seed: int = None
    ) -> None:
        EvolvablePlayer.__init__(self, seed=seed)
        transitions_C, transitions_D, emission_probabilities, initial_state, initial_action, num_states, mutation_probability = self._normalize_parameters(
            transitions_C, transitions_D, emission_probabilities, initial_state, initial_action, num_states, mutation_probability)
        self.mutation_probability = mutation_probability
        HMMPlayer.__init__(self,
                           transitions_C=transitions_C,
                           transitions_D=transitions_D,
                           emission_probabilities=emission_probabilities,
                           initial_state=initial_state,
                           initial_action=initial_action)
        self.hmm._random = self._random
        self.overwrite_init_kwargs(
            transitions_C=transitions_C,
            transitions_D=transitions_D,
            emission_probabilities=emission_probabilities,
            initial_state=initial_state,
            initial_action=initial_action,
            num_states=num_states,
            mutation_probability=mutation_probability
        )

    def _normalize_parameters(self, transitions_C=None, transitions_D=None, emission_probabilities=None,
                              initial_state=None, initial_action=None, num_states=None, mutation_probability=None):
        if not ((transitions_C and transitions_D and emission_probabilities) and (initial_state is not None) and (initial_action is not None)):
            if not num_states:
                raise InsufficientParametersError("Insufficient Parameters to instantiate EvolvableHMMPlayer")
            transitions_C, transitions_D, emission_probabilities, initial_state, initial_action = self.random_params(
                num_states)
        # Normalize types of various matrices
        for m in [transitions_C, transitions_D]:
            for i in range(len(m)):
                m[i] = list(map(float, m[i]))
        emission_probabilities = list(map(float, emission_probabilities))
        num_states = len(emission_probabilities)
        if mutation_probability is None:
            mutation_probability = 10 / (num_states ** 2)
        else:
            mutation_probability = mutation_probability
        return transitions_C, transitions_D, emission_probabilities, initial_state, initial_action, num_states, mutation_probability

    def random_params(self, num_states):
        transitions_C = []
        transitions_D = []
        emission_probabilities = []
        for _ in range(num_states):
            transitions_C.append(self._random.random_vector(num_states))
            transitions_D.append(self._random.random_vector(num_states))
            emission_probabilities.append(self._random.random())
        initial_state = self._random.randint(0, num_states)
        initial_action = C
        return transitions_C, transitions_D, emission_probabilities, initial_state, initial_action

    @property
    def num_states(self):
        return len(self.hmm.emission_probabilities)

    def mutate_rows(self, rows, mutation_probability):
        for i, row in enumerate(rows):
            row = mutate_row(row, mutation_probability, self._random)
            rows[i] = normalize_vector(row)
        return rows

    def mutate(self):
        transitions_C = self.mutate_rows(
            self.hmm.transitions_C, self.mutation_probability)
        transitions_D = self.mutate_rows(
            self.hmm.transitions_D, self.mutation_probability)
        emission_probabilities = mutate_row(
            self.hmm.emission_probabilities, self.mutation_probability, self._random)
        initial_action = self.initial_action
        if self._random.random() < self.mutation_probability / 10:
            initial_action = self.initial_action.flip()
        initial_state = self.initial_state
        if self._random.random() < self.mutation_probability / (10 * self.num_states):
            initial_state = self._random.randint(0, self.num_states)
        return self.create_new(
            transitions_C=transitions_C,
            transitions_D=transitions_D,
            emission_probabilities=emission_probabilities,
            initial_state=initial_state,
            initial_action=initial_action,
        )

    def crossover(self, other):
        if other.__class__ != self.__class__:
            raise TypeError("Crossover must be between the same player classes.")
        transitions_C = crossover_lists(self.hmm.transitions_C, other.hmm.transitions_C, self._random)
        transitions_D = crossover_lists(self.hmm.transitions_D, other.hmm.transitions_D, self._random)
        emission_probabilities = crossover_lists(
            self.hmm.emission_probabilities, other.hmm.emission_probabilities, self._random)
        return self.create_new(
            transitions_C=transitions_C,
            transitions_D=transitions_D,
            emission_probabilities=emission_probabilities
        )

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
