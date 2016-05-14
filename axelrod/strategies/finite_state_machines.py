from axelrod import Actions, Player, Game, init_args

C, D = Actions.C, Actions.D


class SimpleFSM(object):
    """Simple implementation of a finite state machine that transitions
    between states based on the last round of play."""

    def __init__(self, transitions, initial_state):
        """
        transitions is a list of the form
        [(state, last_opponent_action, next_state, next_action), ...]

        TitForTat would be represented with the following table:
        [(1, C, 1, C), (1, D, 1, D)]
        with initial play C and initial state 1.

        """
        self.state = initial_state
        self.state_transitions = dict()
        for (state, opp_action, next_state, next_action) in transitions:
            self.state_transitions[(state, opp_action)] = (next_state, next_action)

    def move(self, opponent_action):
        """Computes the response move and changes state."""
        next_state, next_action = self.state_transitions[(self.state, opponent_action)]
        self.state = next_state
        return next_action


class FSMPlayer(Player):
    """Abstract base class for finite state machine players."""

    name = "FSM Player"

    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, transitions, initial_state, initial_action):
        Player.__init__(self)
        self.initial_action = initial_action
        self.fsm = SimpleFSM(transitions, initial_state)

    def strategy(self, opponent):
        if len(self.history) == 0:
            return self.initial_action
        else:
            action = self.fsm.move(opponent.history[-1])
            # Record the state for testing purposes, this isn't necessary
            # for the strategy to function
            self.state = self.fsm.state
            return action


class Fortress3(FSMPlayer):
    """Finite state machine player specified in DOI:10.1109/CEC.2006.1688322.
    Note that the description in http://www.graham-kendall.com/papers/lhk2011.pdf
    is not correct."""

    name = 'Fortress3'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self):
        transitions = ((1, D, 2, D),
                       (1, C, 1, D),
                       (2, C, 1, D),
                       (2, D, 3, C),
                       (3, C, 3, C),
                       (3, D, 1, D))

        FSMPlayer.__init__(self, transitions, initial_state=1, initial_action=D)


class Fortress4(FSMPlayer):
    """Finite state machine player specified in DOI:10.1109/CEC.2006.1688322.
    Note that the description in http://www.graham-kendall.com/papers/lhk2011.pdf
    is not correct."""

    name = 'Fortress4'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }


    def __init__(self):
        transitions = ((1, C, 1, D),
                       (1, D, 2, D),
                       (2, C, 1, D),
                       (2, D, 3, D),
                       (3, C, 1, D),
                       (3, D, 4, C),
                       (4, C, 4, C),
                       (4, D, 1, D))

        FSMPlayer.__init__(self, transitions, initial_state=1, initial_action=D)


class Predator(FSMPlayer):
    """Finite state machine player specified in DOI:10.1109/CEC.2006.1688322."""

    name = 'Predator'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }


    def __init__(self):
        transitions = ((0, C, 0, D),
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
                       (8, D, 6, D))

        FSMPlayer.__init__(self, transitions, initial_state=1, initial_action=C)


class Raider(FSMPlayer):
    """FSM player described in DOI:10.1109/FOCI.2014.7007818"""

    name = 'Raider'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self):
        transitions = ((0, C, 2, D),
                       (0, D, 2, D),
                       (1, C, 1, C),
                       (1, D, 1, D),
                       (2, C, 0, D),
                       (2, D, 3, C),
                       (3, C, 0, D),
                       (3, D, 1, C))

        FSMPlayer.__init__(self, transitions, initial_state=0, initial_action=D)


class Ripoff(FSMPlayer):
    """FSM player described in DOI:10.1109/TEVC.2008.920675."""

    name = 'Ripoff'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self):
        transitions = ((1, C, 2, C),
                       (1, D, 3, C),
                       (2, C, 1, D),
                       (2, D, 3, C),
                       (3, C, 3, C), # Note that it's TFT in state 3
                       (3, D, 3, D))

        FSMPlayer.__init__(self, transitions, initial_state=1, initial_action=D)


class SolutionB1(FSMPlayer):
    """FSM player described in DOI:10.1109/TCIAIG.2014.2326012."""

    name = 'SolutionB1'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self):
        transitions = ((1, C, 2, D),
                       (1, D, 1, D),
                       (2, C, 2, C),
                       (2, D, 3, C),
                       (3, C, 3, C),
                       (3, D, 3, C))

        FSMPlayer.__init__(self, transitions, initial_state=1, initial_action=D)


class SolutionB5(FSMPlayer):
    """FSM player described in DOI:10.1109/TCIAIG.2014.2326012."""

    name = 'SolutionB5'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self):
        transitions = ((1, C, 2, C),
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
                       (6, D, 5, D))

        FSMPlayer.__init__(self, transitions, initial_state=1, initial_action=D)


class Thumper(FSMPlayer):
    """FSM player described in DOI:10.1109/TEVC.2008.920675."""

    name = 'Thumper'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self):
        transitions = ((1, C, 1, C),
                       (1, D, 2, D),
                       (2, C, 1, D),
                       (2, D, 1, D))

        FSMPlayer.__init__(self, transitions, initial_state=1, initial_action=C)
