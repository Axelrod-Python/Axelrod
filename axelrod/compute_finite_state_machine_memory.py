from collections import defaultdict, namedtuple
from typing import DefaultDict, Dict, Iterator, List, Set, Tuple

from axelrod.action import Action

C, D = Action.C, Action.D

Transition = namedtuple(
    "Transition", ["state", "last_opponent_action", "next_state", "next_action"]
)
TransitionDict = Dict[Tuple[int, Action], Tuple[int, Action]]


class Memit(object):
    """
    Memit = unit of memory.

    This represents the amount of memory that we gain with each new piece of
    history.  It includes a state, our_response that we make on our way into that
    state (in_act), and the opponent's action that makes us move out of that state
    (out_act).

    For example, for this finite state machine:
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

    def __init__(self, in_act: Action, state: int, out_act: Action):
        self.in_act = in_act
        self.state = state
        self.out_act = out_act

    def __repr__(self) -> str:
        return "{}, {}, {}".format(self.in_act, self.state, self.out_act)

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other_memit) -> bool:
        """In action and out actions are the same."""
        return (
            self.in_act == other_memit.in_act
            and self.out_act == other_memit.out_act
        )

    def __lt__(self, other_memit) -> bool:
        return repr(self) < repr(other_memit)


MemitPair = Tuple[Memit, Memit]


def ordered_memit_tuple(x: Memit, y: Memit) -> tuple:
    """Returns a tuple of x in y, sorted so that (x, y) are viewed as the
    same as (y, x).
    """
    if x < y:
        return (x, y)
    else:
        return (y, x)


def transition_iterator(transitions: TransitionDict) -> Iterator[Transition]:
    """Changes the transition dictionary into a iterator on namedtuples."""
    for k, v in transitions.items():
        yield Transition(k[0], k[1], v[0], v[1])


def get_accessible_transitions(
    transitions: TransitionDict, initial_state: int
) -> TransitionDict:
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
    # to the accesible_states.  [A basic breadth-first search.]
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
            accessible_transitions[
                (trans.state, trans.last_opponent_action)
            ] = (trans.next_state, trans.next_action)

    return accessible_transitions


def longest_path(
    edges: DefaultDict[MemitPair, Set[MemitPair]], starting_at: MemitPair
) -> int:
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


def get_memory_from_transitions(
    transitions: TransitionDict,
    initial_state: int = None,
    all_actions: Tuple[Action, Action] = (C, D),
) -> int:
    """This function calculates the memory of an FSM from the transitions.

    Assume that transitions are a dict with entries like
    (state, last_opponent_action): (next_state, next_action)

    We first break down the transitions into memits (see above).  We also create
    a graph of memits, where the successor to a given memit are all possible
    memits that could occur in the memory immediately before the given memit.

    Then we pair up memits with different states, but same in and out actions.
    These represent points in time that we can't determine which state we're in.
    We also create a graph of memit-pairs, where memit-pair, Y, succeeds a
    memit-pair, X, if the two memits in X are succeeded by the two memits in Y.
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
    incoming_action_by_state = defaultdict(
        set
    )  # type: DefaultDict[int, Set[Action]]
    for trans in transition_iterator(transitions):
        incoming_action_by_state[trans.next_state].add(trans.next_action)

    # Keys are starting memit, and values are all possible terminal memit.
    # Will walk backwards through the graph.
    memit_edges = defaultdict(set)  # type: DefaultDict[Memit, Set[Memit]]
    for trans in transition_iterator(transitions):
        # Since all actions are out-paths for each state, add all of these.
        # That is to say that the opponent could do anything
        for out_action in all_actions:
            # More recent in action history
            starting_node = Memit(
                trans.next_action, trans.next_state, out_action
            )
            # All incoming paths to current state
            for in_action in incoming_action_by_state[trans.state]:
                # Less recent in action history
                ending_node = Memit(
                    in_action, trans.state, trans.last_opponent_action
                )
                memit_edges[starting_node].add(ending_node)

    all_memits = list(memit_edges.keys())

    pair_nodes = set()
    pair_edges = defaultdict(
        set
    )  # type: DefaultDict[MemitPair, Set[MemitPair]]
    # Loop through all pairs of memits.
    for x, y in [(x, y) for x in all_memits for y in all_memits]:
        if x == y and x.state == y.state:
            continue
        if x != y:
            continue

        # If the memits match, then the strategy can't tell the difference
        # between the states.  We call this a pair of matched memits (or just a
        # pair).
        pair_nodes.add(ordered_memit_tuple(x, y))
        # When two memits in matched pair have successors that are also matched,
        # then we draw an edge.  This represents consecutive historical times
        # that we can't tell which state we're in.
        for x_successor in memit_edges[x]:
            for y_successor in memit_edges[y]:
                if x_successor == y_successor:
                    pair_edges[ordered_memit_tuple(x, y)].add(
                        ordered_memit_tuple(x_successor, y_successor)
                    )

    # Get next_action for each memit.  Used to decide if they are in conflict,
    # because we only have undecidability if next_action doesn't match.
    next_action_by_memit = dict()
    for trans in transition_iterator(transitions):
        for in_action in incoming_action_by_state[trans.state]:
            memit_key = Memit(
                in_action, trans.state, trans.last_opponent_action
            )
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

    if record > 0:
        return record

    # If there are no pair of tied memits (for which the next action are
    # distinct), then either no memits are needed to break a tie (i.e. all
    # next_actions are the same) or the first memit breaks a tie (i.e. memory 1)
    next_action_set = set()
    for trans in transition_iterator(transitions):
        next_action_set.add(trans.next_action)
    if len(next_action_set) == 1:
        return 0
    return 1
