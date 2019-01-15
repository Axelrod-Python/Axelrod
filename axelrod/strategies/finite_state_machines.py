from axelrod.action import Action
from axelrod.player import Player
from typing import DefaultDict, Iterator, Dict, Tuple, Set, List
from collections import defaultdict, namedtuple

C, D = Action.C, Action.D
ALL_ACTIONS = [C, D]


"""
Memit = unit of memory.

This represents the amount of memory that we gain with each new piece of
history.  It includes a state, our_response that we make on our way into that
state (in_act), and the opponent's action that makes us move out of that state
(out_act).

For example for this FSM:
(0, C, 0, C),
(0, D, 1, C),
(1, C, 0, D),
(1, D, 0, D)

Has the memits:
(C, 0, C),
(C, 0, D),
(D, 0, C),
(D, 0, D),
(C, 1, C),
(C, 1, D)
"""
Memit = namedtuple("Memit", ["in_act", "state", "out_act"])

def memits_match(x: Memit, y: Memit):
    """In action and out actions are the same."""
    return x.in_act == y.in_act and x.out_act == y.out_act

def memit_sort(x: Memit, y: Memit):
    """Returns a tuple of x in y, sorted so that (x, y) are viewed as the
    same as (y, x).
    """
    if repr(x) <= repr(y):
        return (x, y)
    else:
        return (y, x)


Transition = namedtuple("Transition", ["state", "last_opponent_action",
                                       "next_state", "next_action"])
TransitionDict = Dict[Tuple[int, Action], Tuple[int, Action]]

def transition_iterator(transitions: TransitionDict) -> Iterator[Transition]:
    """Changes the transition dictionary into a iterator on namedtuples, because
    we use repeatedly.
    """
    for k, v in transitions.items():
        yield Transition(k[0], k[1], v[0], v[1])


def get_accessible_transitions(transitions: TransitionDict,
                               initial_state: int) -> TransitionDict:
    """Gets all transitions from the list that can be reached from the
    initial_state.
    """
    # Initial dict of edges between states and a dict of visited status for each
    # of the states.
    edge_dict = defaultdict(list)  # type: DefaultDict[int, List[int]]
    visited = dict()
    for trans in transition_iterator(transitions):
        visited[trans.state] = False
        edge_dict[trans.state].append(trans.next_state)
    # Keep track of states that can be accessed.
    accessible_states = [initial_state]

    state_queue = [initial_state]
    visited[initial_state] = True
    # While there are states in the queue, visit all its children, adding each
    # to the accesible_states.  [A basic BFS.]
    while len(state_queue) > 0:
        state = state_queue.pop()
        for successor in edge_dict[state]:
            # Don't process the same state twice.
            if not visited[successor]:
                visited[successor] = True
                state_queue.append(successor)
                accessible_states.append(successor)

    # Now for each transition in the passed TransitionDict, copy the transition
    # to accessible_transitions if and only if the starting state is accessible,
    # as determined above.
    accessible_transitions = dict()
    for trans in transition_iterator(transitions):
        if trans.state in accessible_states:
            accessible_transitions[(
                trans.state, trans.last_opponent_action)] = (trans.next_state,
                                                             trans.next_action)

    return accessible_transitions


MemitPair = Tuple[Memit, Memit]

def longest_path(edges: DefaultDict[MemitPair, Set[MemitPair]],
                 starting_at: MemitPair) -> int:
    """Returns the number of nodes in the longest path that starts at the given
    node.  Returns infinity if a loop is encountered.
    """
    visited = dict()
    for source, destinations in edges.items():
        visited[source] = False
        for destination in destinations:
            visited[destination] = False

    # This is what we'll recurse on.  visited dict is shared between calls.
    def recurse(at_node):
        visited[at_node] = True
        record = 1  # Count the nodes, not the edges.
        for successor in edges[at_node]:
            if visited[successor]:
                return float("inf")
            successor_length = recurse(successor)
            if successor_length == float("inf"):
                return float("inf")
            if record < successor_length + 1:
                record = successor_length + 1
        return record

    return recurse(starting_at)


def get_memory_from_transitions(transitions: TransitionDict,
                                initial_state: int = None) -> int:
    """This function calculates the memory of an FSM from the transitions.

    Assume that transitions are a dict with entries like
    (state, last_opponent_action): (next_state, next_action)

    We first break down the transitions into memits (see above).  We also create
    a graph of memits, where the successor to a given memit are all possible
    memits that could occur in the memory immediately before the given memit.

    Then we pair up memits with different states, but same in and out actions.
    These represent points in time that we can't determine which state we're in.
    We also create a graph of memit-pairs, where memit-pair, Y, succedes a
    memit-pair, X, if the two memits in X are succeded by the two memits in Y.
    These edges reperesent consecutive points in time that we can't determine
    which state we're in.

    Then for all memit-pairs that disagree, in the sense that they imply
    different next_action, we find the longest chain starting at that
    memit-pair.  [If a loop is encountered then this will be infinite.]  We take
    the maximum over all such memit-pairs.  This represents the longest possible
    chain of memory for which we wouldn't know what to do next.  We return this.
    """
    # If initial_state is set, use this to determine which transitions are
    # reachable from the initial_state and restrict to those.
    if initial_state is not None:
        transitions = get_accessible_transitions(transitions, initial_state)

    # Get the incoming actions for each state.
    incoming_action_by_state = defaultdict(set)  # type: DefaultDict[int, Set[Action]]
    for trans in transition_iterator(transitions):
        incoming_action_by_state[trans.next_state].add(trans.next_action)

    # Keys are starting memit, and values are all possible terminal memit.
    # Will walk backwards through the graph.
    memit_edges = defaultdict(set)  # type: DefaultDict[Memit, Set[Memit]]
    for trans in transition_iterator(transitions):
        # Since all actions are out-paths for each state, add all of these.
        # That is to say that your opponent could do anything
        for out_action in ALL_ACTIONS:
            # More recent in action history
            starting_node = Memit(trans.next_action, trans.next_state,
                                  out_action)
            # All incoming paths to current state
            for in_action in incoming_action_by_state[trans.state]:
                # Less recent in action history
                ending_node = Memit(in_action, trans.state,
                                    trans.last_opponent_action)
                memit_edges[starting_node].add(ending_node)

    all_memits = [x for x in memit_edges.keys()]

    pair_nodes = set()
    pair_edges = defaultdict(set)  # type: DefaultDict[MemitPair, Set[MemitPair]]
    # Loop through all pairs of memits.
    for x, y in [(x, y) for x in all_memits for y in all_memits]:
        if x == y:
            continue
        if not memits_match(x, y):
            continue

        # If the memits match, then the strategy can't tell the difference
        # between the states.  We call this a pair of matched memits (or just a
        # pair).
        pair_nodes.add(memit_sort(x, y))
        # When two memits in matched pair have successors that are also matched,
        # then we draw an edge.  This represents consecutive historical times
        # that we can't tell which state we're in.
        for x_successor in memit_edges[x]:
            for y_successor in memit_edges[y]:
                if memits_match(x_successor, y_successor):
                    pair_edges[memit_sort(x, y)].add(memit_sort(x_successor,
                                                                y_successor))

    if len(pair_nodes) == 0:
        # If there are no pair of tied memits, then either no memits are needed
        # to break a tie (i.e. all next_actions are the same) or the first memit
        # breaks a tie (i.e. memory 1)
        next_action_set = set()
        for trans in transition_iterator(transitions):
            next_action_set.add(trans.next_action)
        if len(next_action_set) == 1:
            return 0
        return 1

    # Get next_action for each memit.  Used to decide if they are in conflict,
    # because we only have undecidability if next_action doesn't match.
    next_action_by_memit = dict()
    for trans in transition_iterator(transitions):
        for in_action in incoming_action_by_state[trans.state]:
            memit_key = Memit(in_action, trans.state,
                              trans.last_opponent_action)
            next_action_by_memit[memit_key] = trans.next_action

    # Calculate the longest path.
    record = 0
    for pair in pair_nodes:
        if next_action_by_memit[pair[0]] != next_action_by_memit[pair[1]]:
            # longest_path is the longest chain of tied states.  We add one to
            # get the memory length needed to break all ties.
            path_length = longest_path(pair_edges, pair) + 1
            if record < path_length:
                record = path_length
    return record


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
        self._state_transitions = {
            (current_state, input_action): (next_state, output_action)
            for current_state, input_action, next_state, output_action in transitions
        }  # type: dict

        self._raise_error_for_bad_input()

    def _raise_error_for_bad_input(self):
        callable_states = set(pair[0] for pair in self._state_transitions.values())
        callable_states.add(self._state)
        for state in callable_states:
            self._raise_error_for_bad_state(state)

    def _raise_error_for_bad_state(self, state: int):
        if (state, C) not in self._state_transitions or (
            state,
            D,
        ) not in self._state_transitions:
            raise ValueError(
                "state: {} does not have values for both C and D".format(state)
            )

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
        next_state, next_action = self._state_transitions[
            (self._state, opponent_action)
        ]
        self._state = next_state
        return next_action

    def __eq__(self, other) -> bool:
        """Equality of two FSMs"""
        if not isinstance(other, SimpleFSM):
            return False
        return (self._state, self._state_transitions) == (
            other.state,
            other.state_transitions,
        )


class FSMPlayer(Player):
    """Abstract base class for finite state machine players."""

    name = "FSM Player"

    classifier = {
        "memory_depth": 1,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(
        self,
        transitions: tuple = ((1, C, 1, C), (1, D, 1, D)),
        initial_state: int = 1,
        initial_action: Action = C,
    ) -> None:

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

    name = "Fortress3"
    classifier = {
        "memory_depth": 2,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self) -> None:
        transitions = (
            (1, C, 1, D),
            (1, D, 2, D),
            (2, C, 1, D),
            (2, D, 3, C),
            (3, C, 3, C),
            (3, D, 1, D),
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

    name = "Fortress4"
    classifier = {
        "memory_depth": 3,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
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
            (4, D, 1, D),
        )

        super().__init__(transitions=transitions, initial_state=1, initial_action=D)


class Predator(FSMPlayer):
    """
    Finite state machine player specified in
    http://DOI.org/10.1109/CEC.2006.1688322.

    Names:

    - Predator: [Ashlock2006b]_
    """

    name = "Predator"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
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
            (8, D, 6, D),
        )

        super().__init__(transitions=transitions, initial_state=0, initial_action=C)


class Pun1(FSMPlayer):
    """FSM player described in [Ashlock2006]_.

    Names:

    - Pun1: [Ashlock2006]_
    """

    name = "Pun1"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self) -> None:
        transitions = ((1, C, 2, C), (1, D, 2, C), (2, C, 1, C), (2, D, 1, D))

        super().__init__(transitions=transitions, initial_state=1, initial_action=D)


class Raider(FSMPlayer):
    """
    FSM player described in http://DOI.org/10.1109/FOCI.2014.7007818.


    Names

    - Raider: [Ashlock2014]_
    """

    name = "Raider"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
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
            (3, D, 1, C),
        )

        super().__init__(transitions=transitions, initial_state=0, initial_action=D)


class Ripoff(FSMPlayer):
    """
    FSM player described in http://DOI.org/10.1109/TEVC.2008.920675.

    Names

    - Ripoff: [Ashlock2008]_
    """

    name = "Ripoff"
    classifier = {
        "memory_depth": 3,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self) -> None:
        transitions = (
            (1, C, 2, C),
            (1, D, 3, C),
            (2, C, 1, D),
            (2, D, 3, C),
            (3, C, 3, C),  # Note that it's TFT in state 3
            (3, D, 3, D),
        )

        super().__init__(transitions=transitions, initial_state=1, initial_action=D)


class UsuallyCooperates(FSMPlayer):
    """
    This strategy cooperates except after a C following a D.

    Names:

    - Usually Cooperates (UC): [Ashlock2009]_
    """

    name = "UsuallyCooperates"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self) -> None:
        transitions = (
            (1, C, 1, C),
            (1, D, 2, C),
            (2, C, 1, D),
            (2, D, 1, C),
        )

        super().__init__(transitions=transitions, initial_state=1, initial_action=C)


class UsuallyDefects(FSMPlayer):
    """
    This strategy defects except after a D following a C.

    Names:

    - Usually Defects (UD): [Ashlock2009]_
    """

    name = "UsuallyDefects"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self) -> None:
        transitions = (
            (1, C, 2, D),
            (1, D, 1, D),
            (2, C, 1, D),
            (2, D, 1, C),
        )

        super().__init__(transitions=transitions, initial_state=1, initial_action=D)


class SolutionB1(FSMPlayer):
    """
    FSM player described in http://DOI.org/10.1109/TCIAIG.2014.2326012.

    Names

    - Solution B1: [Ashlock2015]_
    """

    name = "SolutionB1"
    classifier = {
        "memory_depth": 2,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self) -> None:
        transitions = (
            (1, C, 2, D),
            (1, D, 1, D),
            (2, C, 2, C),
            (2, D, 3, C),
            (3, C, 3, C),
            (3, D, 3, C),
        )

        super().__init__(transitions=transitions, initial_state=1, initial_action=D)


class SolutionB5(FSMPlayer):
    """

    FSM player described in http://DOI.org/10.1109/TCIAIG.2014.2326012.

    Names

    - Solution B5: [Ashlock2015]_
    """

    name = "SolutionB5"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
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
            (6, D, 5, D),
        )

        super().__init__(transitions=transitions, initial_state=1, initial_action=D)


class Thumper(FSMPlayer):
    """
    FSM player described in http://DOI.org/10.1109/TEVC.2008.920675.

    Names

    - Thumper: [Ashlock2008]_
    """

    name = "Thumper"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self) -> None:
        transitions = ((1, C, 1, C), (1, D, 2, D), (2, C, 1, D), (2, D, 1, D))

        super().__init__(transitions=transitions, initial_state=1, initial_action=C)


class EvolvedFSM4(FSMPlayer):
    """
    A 4 state FSM player trained with an evolutionary algorithm.

    Names:

        - Evolved FSM 4: Original name by Marc Harper
    """

    name = "Evolved FSM 4"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
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
            (3, D, 1, D),
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
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
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
            (15, D, 2, C),
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
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
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
            (15, D, 11, C),
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
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self) -> None:
        transitions = (
            (0, C, 7, C),
            (0, D, 1, C),
            (1, C, 11, D),
            (1, D, 11, D),
            (2, C, 8, D),
            (2, D, 8, C),
            (3, C, 3, C),
            (3, D, 12, D),
            (4, C, 6, C),
            (4, D, 3, C),
            (5, C, 11, C),
            (5, D, 8, D),
            (6, C, 13, D),
            (6, D, 14, C),
            (7, C, 4, D),
            (7, D, 2, D),
            (8, C, 14, D),
            (8, D, 8, D),
            (9, C, 0, C),
            (9, D, 10, D),
            (10, C, 8, C),
            (10, D, 15, C),
            (11, C, 6, D),
            (11, D, 5, D),
            (12, C, 6, D),
            (12, D, 9, D),
            (13, C, 9, D),
            (13, D, 8, D),
            (14, C, 8, D),
            (14, D, 13, D),
            (15, C, 4, C),
            (15, D, 5, C),
        )

        super().__init__(transitions=transitions, initial_state=0, initial_action=C)


class TF2(FSMPlayer):
    """
    A FSM player trained to maximize Moran fixation probabilities.

    Names:

        - TF2: Original name by Marc Harper
    """

    name = "TF2"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self) -> None:
        transitions = (
            (0, C, 13, D),
            (0, D, 12, D),
            (1, C, 3, D),
            (1, D, 4, D),
            (2, C, 14, D),
            (2, D, 9, D),
            (3, C, 0, C),
            (3, D, 1, D),
            (4, C, 1, D),
            (4, D, 2, D),
            (7, C, 12, D),
            (7, D, 2, D),
            (8, C, 7, D),
            (8, D, 9, D),
            (9, C, 8, D),
            (9, D, 0, D),
            (10, C, 2, C),
            (10, D, 15, C),
            (11, C, 7, D),
            (11, D, 13, D),
            (12, C, 3, C),
            (12, D, 8, D),
            (13, C, 7, C),
            (13, D, 10, D),
            (14, C, 10, D),
            (14, D, 7, D),
            (15, C, 15, C),
            (15, D, 11, D),
        )

        super().__init__(transitions=transitions, initial_state=0, initial_action=C)


class TF3(FSMPlayer):
    """
    A FSM player trained to maximize Moran fixation probabilities.

    Names:

        - TF3: Original name by Marc Harper
    """

    name = "TF3"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self) -> None:
        transitions = (
            (0, C, 0, C),
            (0, D, 3, C),
            (1, C, 5, D),
            (1, D, 0, C),
            (2, C, 3, C),
            (2, D, 2, D),
            (3, C, 4, D),
            (3, D, 6, D),
            (4, C, 3, C),
            (4, D, 1, D),
            (5, C, 6, C),
            (5, D, 3, D),
            (6, C, 6, D),
            (6, D, 6, D),
            (7, C, 7, D),
            (7, D, 5, C),
        )

        super().__init__(transitions=transitions, initial_state=0, initial_action=C)
