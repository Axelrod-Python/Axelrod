from axelrod.action import Action
from axelrod.player import Player

C, D = Action.C, Action.D


class SimpleFSM(object):
    """Simple implementation of a finite state machine that transitions
    between states based on the last round of play.

    https://en.wikipedia.org/wiki/Finite-state_machine
    """

    def __init__(self, transitions: tuple, initial_state: int) -> None:
        """
        transitions is a list of the form
        ((state, last_opponent_action, next_state, next_action), ...)

        TitForTat would be represented with the following table:
        ((1, C, 1, C), (1, D, 1, D))
        with initial play C and initial state 1.

        """
        self._state = initial_state
        self._state_transitions = {(current_state, input_action): (next_state, output_action) for
                                   current_state, input_action, next_state, output_action in transitions}  # type: dict

        self._raise_error_for_bad_input()

    def _raise_error_for_bad_input(self):
        callable_states = set(pair[0] for pair in self._state_transitions.values())
        callable_states.add(self._state)
        for state in callable_states:
            self._raise_error_for_bad_state(state)

    def _raise_error_for_bad_state(self, state: int):
        if (state, C) not in self._state_transitions or (state, D) not in self._state_transitions:
            raise ValueError('state: {} does not have values for both C and D'.format(state))

    @property
    def state(self) -> int:
        return self._state

    @state.setter
    def state(self, new_state: int):
        self._raise_error_for_bad_state(new_state)
        self._state = new_state

    @property
    def state_transitions(self) -> dict:
        return self._state_transitions.copy()

    def move(self, opponent_action: Action) -> Action:
        """Computes the response move and changes state."""
        next_state, next_action = self._state_transitions[(self._state, opponent_action)]
        self._state = next_state
        return next_action

    def __eq__(self, other) -> bool:
        """Equality of two FSMs"""
        if not isinstance(other, SimpleFSM):
            return False
        return (self._state, self._state_transitions) == (other.state, other.state_transitions)


class FSMPlayer(Player):
    """Abstract base class for finite state machine players."""

    name = "FSM Player"

    classifier = {
        'memory_depth': 1,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, transitions: tuple = ((1, C, 1, C), (1, D, 1, D)),
                 initial_state: int = 1,
                 initial_action: Action = C) -> None:

        super().__init__()
        self.initial_state = initial_state
        self.initial_action = initial_action
        self.fsm = SimpleFSM(transitions, initial_state)

    def strategy(self, opponent: Player) -> Action:
        if len(self.history) == 0:
            return self.initial_action
        else:
            action = self.fsm.move(opponent.history[-1])
            return action


class Fortress3(FSMPlayer):
    """Finite state machine player specified in http://DOI.org/10.1109/CEC.2006.1688322.

    Note that the description in http://www.graham-kendall.com/papers/lhk2011.pdf
    is not correct.


    Names:

    - Fortress 3: [Ashlock2006b]_
    """

    name = 'Fortress3'
    classifier = {
        'memory_depth': 3,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        transitions = (
            (1, C, 1, D),
            (1, D, 2, D),
            (2, C, 1, D),
            (2, D, 3, C),
            (3, C, 3, C),
            (3, D, 1, D)
        )

        super().__init__(transitions=transitions, initial_state=1, initial_action=D)


class Fortress4(FSMPlayer):
    """
    Finite state machine player specified in
    http://DOI.org/10.1109/CEC.2006.1688322.

    Note that the description in
    http://www.graham-kendall.com/papers/lhk2011.pdf is not correct.

    Names:

    - Fortress 4: [Ashlock2006b]_
    """

    name = 'Fortress4'
    classifier = {
        'memory_depth': 4,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        transitions = (
            (1, C, 1, D),
            (1, D, 2, D),
            (2, C, 1, D),
            (2, D, 3, D),
            (3, C, 1, D),
            (3, D, 4, C),
            (4, C, 4, C),
            (4, D, 1, D)
        )

        super().__init__(transitions=transitions, initial_state=1, initial_action=D)


class Predator(FSMPlayer):
    """
    Finite state machine player specified in
    http://DOI.org/10.1109/CEC.2006.1688322.

    Names:

    - Predator: [Ashlock2006b]_
    """

    name = 'Predator'
    classifier = {
        'memory_depth': 9,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        transitions = (
            (0, C, 0, D),
            (0, D, 1, D),
            (1, C, 2, D),
            (1, D, 3, D),
            (2, C, 4, C),
            (2, D, 3, D),
            (3, C, 5, D),
            (3, D, 4, C),
            (4, C, 2, C),
            (4, D, 6, D),
            (5, C, 7, D),
            (5, D, 3, D),
            (6, C, 7, C),
            (6, D, 7, D),
            (7, C, 8, D),
            (7, D, 7, D),
            (8, C, 8, D),
            (8, D, 6, D)
        )

        super().__init__(transitions=transitions, initial_state=0, initial_action=C)


class Pun1(FSMPlayer):
    """FSM player described in [Ashlock2006]_.

    Names:

    - Pun1: [Ashlock2006]_
    """

    name = 'Pun1'
    classifier = {
        'memory_depth': 2,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        transitions = (
            (1, C, 2, C),
            (1, D, 2, C),
            (2, C, 1, C),
            (2, D, 1, D)
        )

        super().__init__(transitions=transitions, initial_state=1, initial_action=D)


class Raider(FSMPlayer):
    """
    FSM player described in http://DOI.org/10.1109/FOCI.2014.7007818.


    Names

    - Raider: [Ashlock2014]_
    """

    name = 'Raider'
    classifier = {
        'memory_depth': 3,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        transitions = (
            (0, C, 2, D),
            (0, D, 2, D),
            (1, C, 1, C),
            (1, D, 1, D),
            (2, C, 0, D),
            (2, D, 3, C),
            (3, C, 0, D),
            (3, D, 1, C)
        )

        super().__init__(transitions=transitions, initial_state=0, initial_action=D)


class Ripoff(FSMPlayer):
    """
    FSM player described in http://DOI.org/10.1109/TEVC.2008.920675.

    Names

    - Ripoff: [Ashlock2008]_
    """

    name = 'Ripoff'
    classifier = {
        'memory_depth': 2,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        transitions = (
            (1, C, 2, C),
            (1, D, 3, C),
            (2, C, 1, D),
            (2, D, 3, C),
            (3, C, 3, C),  # Note that it's TFT in state 3
            (3, D, 3, D)
        )

        super().__init__(transitions=transitions, initial_state=1, initial_action=D)


class SolutionB1(FSMPlayer):
    """
    FSM player described in http://DOI.org/10.1109/TCIAIG.2014.2326012.

    Names

    - Solution B1: [Ashlock2015]_
    """

    name = 'SolutionB1'
    classifier = {
        'memory_depth': 3,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        transitions = (
            (1, C, 2, D),
            (1, D, 1, D),
            (2, C, 2, C),
            (2, D, 3, C),
            (3, C, 3, C),
            (3, D, 3, C)
        )

        super().__init__(transitions=transitions, initial_state=1, initial_action=D)


class SolutionB5(FSMPlayer):
    """

    FSM player described in http://DOI.org/10.1109/TCIAIG.2014.2326012.

    Names

    - Solution B5: [Ashlock2015]_
    """

    name = 'SolutionB5'
    classifier = {
        'memory_depth': 5,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        transitions = (
            (1, C, 2, C),
            (1, D, 6, D),
            (2, C, 2, C),
            (2, D, 3, D),
            (3, C, 6, C),
            (3, D, 1, D),
            (4, C, 3, C),
            (4, D, 6, D),
            (5, C, 5, D),
            (5, D, 4, D),
            (6, C, 3, C),
            (6, D, 5, D)
        )

        super().__init__(transitions=transitions, initial_state=1, initial_action=D)


class Thumper(FSMPlayer):
    """
    FSM player described in http://DOI.org/10.1109/TEVC.2008.920675.

    Names

    - Thumper: [Ashlock2008]_
    """

    name = 'Thumper'
    classifier = {
        'memory_depth': 2,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        transitions = (
            (1, C, 1, C),
            (1, D, 2, D),
            (2, C, 1, D),
            (2, D, 1, D)
        )

        super().__init__(transitions=transitions, initial_state=1, initial_action=C)


class EvolvedFSM4(FSMPlayer):
    """
    A 4 state FSM player trained with an evolutionary algorithm.

    Names:

        - Evolved FSM 4: Original name by Marc Harper
    """

    name = "Evolved FSM 4"
    classifier = {
        'memory_depth': 4,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        transitions = (
            (0, C, 0, C),
            (0, D, 2, D),
            (1, C, 3, D),
            (1, D, 0, C),
            (2, C, 2, D),
            (2, D, 1, C),
            (3, C, 3, D),
            (3, D, 1, D)
        )

        super().__init__(transitions=transitions, initial_state=0, initial_action=C)


class EvolvedFSM16(FSMPlayer):
    """
    A 16 state FSM player trained with an evolutionary algorithm.

    Names:

        - Evolved FSM 16: Original name by Marc Harper

    """

    name = "Evolved FSM 16"
    classifier = {
        'memory_depth': 16,  # At most
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        transitions = (
            (0, C, 0, C),
            (0, D, 12, D),
            (1, C, 3, D),
            (1, D, 6, C),
            (2, C, 2, D),
            (2, D, 14, D),
            (3, C, 3, D),
            (3, D, 3, D),

            (5, C, 12, D),
            (5, D, 10, D),
            (6, C, 5, C),
            (6, D, 12, D),
            (7, C, 3, D),
            (7, D, 1, C),
            (8, C, 5, C),
            (8, D, 5, C),

            (10, C, 11, D),
            (10, D, 8, C),
            (11, C, 15, D),
            (11, D, 5, D),
            (12, C, 8, C),
            (12, D, 11, D),
            (13, C, 13, D),
            (13, D, 7, D),
            (14, C, 13, D),
            (14, D, 13, D),
            (15, C, 15, D),
            (15, D, 2, C)
        )

        super().__init__(transitions=transitions, initial_state=0, initial_action=C)


class EvolvedFSM16Noise05(FSMPlayer):
    """
    A 16 state FSM player trained with an evolutionary algorithm with
    noisy matches (noise=0.05).

    Names:

        - Evolved FSM 16 Noise 05: Original name by Marc Harper
    """

    name = "Evolved FSM 16 Noise 05"
    classifier = {
        'memory_depth': 16,  # At most
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        transitions = (
            (0, C, 8, C),
            (0, D, 3, D),
            (1, C, 13, C),
            (1, D, 15, D),
            (2, C, 12, C),
            (2, D, 3, D),
            (3, C, 10, C),
            (3, D, 3, D),
            (4, C, 5, D),
            (4, D, 4, D),
            (5, C, 4, D),
            (5, D, 10, D),
            (6, C, 8, C),
            (6, D, 6, D),

            (8, C, 2, C),
            (8, D, 4, D),

            (10, C, 4, D),
            (10, D, 1, D),
            (11, C, 14, D),
            (11, D, 13, C),
            (12, C, 13, C),
            (12, D, 2, C),
            (13, C, 13, C),
            (13, D, 6, C),
            (14, C, 3, D),
            (14, D, 13, D),
            (15, C, 5, D),
            (15, D, 11, C)
        )

        super().__init__(transitions=transitions, initial_state=0, initial_action=C)


# Strategies trained with Moran process objectives


class TF1(FSMPlayer):
    """
    A FSM player trained to maximize Moran fixation probabilities.

    Names:

        - TF1: Original name by Marc Harper
    """

    name = "TF1"
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        transitions = (
            (0, C, 7, C), (0, D, 1, C),
            (1, C, 11, D), (1, D, 11, D),
            (2, C, 8, D), (2, D, 8, C),
            (3, C, 3, C), (3, D, 12, D),
            (4, C, 6, C), (4, D, 3, C),
            (5, C, 11, C), (5, D, 8, D),
            (6, C, 13, D), (6, D, 14, C),
            (7, C, 4, D), (7, D, 2, D),
            (8, C, 14, D), (8, D, 8, D),
            (9, C, 0, C), (9, D, 10, D),
            (10, C, 8, C), (10, D, 15, C),
            (11, C, 6, D), (11, D, 5, D),
            (12, C, 6, D), (12, D, 9, D),
            (13, C, 9, D), (13, D, 8, D),
            (14, C, 8, D), (14, D, 13, D),
            (15, C, 4, C), (15, D, 5, C)
        )

        super().__init__(transitions=transitions, initial_state=0,
                         initial_action=C)


class TF2(FSMPlayer):
    """
    A FSM player trained to maximize Moran fixation probabilities.

    Names:

        - TF2: Original name by Marc Harper
    """

    name = "TF2"
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        transitions = (
            (0, C, 13, D), (0, D, 12, D),
            (1, C, 3, D), (1, D, 4, D),
            (2, C, 14, D), (2, D, 9, D),
            (3, C, 0, C), (3, D, 1, D),
            (4, C, 1, D), (4, D, 2, D),
            (7, C, 12, D), (7, D, 2, D),
            (8, C, 7, D), (8, D, 9, D),
            (9, C, 8, D), (9, D, 0, D),
            (10, C, 2, C), (10, D, 15, C),
            (11, C, 7, D), (11, D, 13, D),
            (12, C, 3, C), (12, D, 8, D),
            (13, C, 7, C), (13, D, 10, D),
            (14, C, 10, D), (14, D, 7, D),
            (15, C, 15, C), (15, D, 11, D)
        )

        super().__init__(transitions=transitions, initial_state=0,
                         initial_action=C)


class TF3(FSMPlayer):
    """
    A FSM player trained to maximize Moran fixation probabilities.

    Names:

        - TF3: Original name by Marc Harper
    """

    name = "TF3"
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        transitions = (
            (0, C, 0, C), (0, D, 3, C),
            (1, C, 5, D), (1, D, 0, C),
            (2, C, 3, C), (2, D, 2, D),
            (3, C, 4, D), (3, D, 6, D),
            (4, C, 3, C), (4, D, 1, D),
            (5, C, 6, C), (5, D, 3, D),
            (6, C, 6, D), (6, D, 6, D),
            (7, C, 7, D), (7, D, 5, C)
        )

        super().__init__(transitions=transitions, initial_state=0,
                         initial_action=C)
