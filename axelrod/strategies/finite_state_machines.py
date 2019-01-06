from axelrod.action import Action
from axelrod.player import Player
from collections import defaultdict, namedtuple

C, D = Action.C, Action.D


def get_accessible_transitions(transitions, initial_state):
  """Gets all transitions from the list that can be reached from the
  initial_state.
  """
  edge_dict = defaultdict(list)
  visited = dict()
  for trans in transitions:
      visited[trans[0]] = False
      edge_dict[trans[0]].append(trans[2])
  accessible_edges = [initial_state]

  edge_queue = [initial_state]
  visited[initial_state] = True
  while len(edge_queue) > 0:
      edge = edge_queue.pop()
      for next_edge in edge_dict[edge]:
          if not visited[next_edge]:
              visited[next_edge] = True
              edge_queue.append(next_edge)
              accessible_edges.append(next_edge)

  accessible_transitions = list()
  for trans in transitions:
      if trans[0] in accessible_edges:
          accessible_transitions.append(trans)

  return accessible_transitions


def get_memory_from_transitions(transitions, initial_state=None,
                                print_trace=False):
    """
    This function calculates the memory of an FSM from the transitions.

    Assume that transitions are a list with entries like
     ((state, last_opponent_action, next_state, next_action), ...)

    We look at all the next_actions for all the transitions.  If these aren't
    all the same, then we attach 1 turn worth of memory (this strategy's
    previous action and the opponent's previous action).  We can get the
    opponent's previous strategy from the transition, but to get this strategy's
    previous action, we need to consider all incoming transitions into the
    current state.  [We call this walking backwards through the graph along the
    path given by the incoming transition.]  There may be zero or one or
    multiple incoming transitions into each state, creating multiple paths we
    could walk along.  We call these branches, and keep track of all branches.

    Along each branch there is a chain of actions.  After 1 step, it may be CC,
    CD, DC, or DD.  [However we write "CC" like "_/C, C/_" though to establish
    that letters to the left of the "/" are the opponent's moves, while the
    letters to the right are this strategy's moves.]  For each chain of actions,
    we gather the branches that match that chain.  If all these branches have
    the same next_action, then we know what to do following that chain of
    actions.  In that case we call these branches decided.  With undecided
    branches, we continue to walk back.  We repeat until all branches are
    decided.  The number of steps that this takes is the memory of the FSM.

    If however, there are still undecided branches after E*(E-1) steps (where E
    is the number of transitions), then the memory must be infinite.  This is
    shown elsewhere.


    As an example, we show how the Fortress3 (defined below) strategy would
    work.

    Fortress3 is given by the transitions:
    transitions = (
        (1, C, 1, D),
        (1, D, 2, D),
        (2, C, 1, D),
        (2, D, 3, C),
        (3, C, 3, C),
        (3, D, 1, D),
    )

    In the first step, we just check transitions' next-actions.
    We list transtions as state:prev_opponent_action;next_action:
    1:C;D | Back-trace: _ | On-state: 1
    1:D;D | Back-trace: _ | On-state: 1
    2:C;D | Back-trace: _ | On-state: 2
    2:D;C | Back-trace: _ | On-state: 2
    3:C;C | Back-trace: _ | On-state: 3
    3:D;D | Back-trace: _ | On-state: 3

    In the second step, we walk backwards along incoming transitions.
    We continue to label each branch by its ending
    state:previous_opponent_action;next_action, but we list the state that
    we're on at this point in time:
    1:C;D | Back-trace: _/D, C/_ | On-state: 1
    1:C;D | Back-trace: _/D, C/_ | On-state: 2
    1:C;D | Back-trace: _/D, C/_ | On-state: 3
    2:C;D | Back-trace: _/D, C/_ | On-state: 1
    1:D;D | Back-trace: _/D, D/_ | On-state: 1
    1:D;D | Back-trace: _/D, D/_ | On-state: 2
    1:D;D | Back-trace: _/D, D/_ | On-state: 3
    2:D;C | Back-trace: _/D, D/_ | On-state: 1
    3:C;C | Back-trace: _/C, C/_ | On-state: 2
    3:C;C | Back-trace: _/C, C/_ | On-state: 3
    3:D;D | Back-trace: _/C, D/_ | On-state: 2
    3:D;D | Back-trace: _/C, D/_ | On-state: 3

    From here we can conclude that:
    If _/D, C/_, then D
    If _/C, C/_, then C
    If _/C, D/_, then D

    We remove the branches that correspond to those action chains.  But we
    continue to walk back the _/D, D/_ branches:
    1:D;D | Back-trace: _/D, C/D, D/_ | On-state: 1
    1:D;D | Back-trace: _/D, C/D, D/_ | On-state: 2
    1:D;D | Back-trace: _/D, C/D, D/_ | On-state: 3
    1:D;D | Back-trace: _/D, C/D, D/_ | On-state: 1
    1:D;D | Back-trace: _/C, D/D, D/_ | On-state: 2
    1:D;D | Back-trace: _/C, D/D, D/_ | On-state: 3
    2:D;C | Back-trace: _/D, D/D, D/_ | On-state: 1
    2:D;C | Back-trace: _/D, D/D, D/_ | On-state: 2
    2:D;C | Back-trace: _/D, D/D, D/_ | On-state: 3

    From here we conclude that:
    If _/D, C/D, D/_, then D
    If _/C, D/D, D/_, then D
    If _/D, D/D, D/_, then C

    There are no more undecided branches, so we stop and say that the memory
    is 2.
    """
    # If initial_state is set, use this to determine which transitions are
    # reachable from the initial_state and restrict to those.
    if initial_state is not None:
        transitions = get_accessible_transitions(transitions, initial_state)

    # First make a back_transitions dict from transitions.  This is keyed on
    # states, and a list of "BackTrans" (one for each transition incoming to
    # that state) as values.
    back_transitions = defaultdict(list)
    # A "BackTrans" has the previous state and previous action/reaction pair.
    BackTrans = namedtuple("BackTrans", ["prev_state", "prev_reaction",
                                         "prev_opp_action"])
    for trans in transitions:
        state = trans[0]
        last_opponent_action = trans[1]
        next_state = trans[2]
        next_action = trans[3]

        back_transitions[next_state].append(BackTrans(state,
                                                      next_action,
                                                      last_opponent_action))

    class ActionChain(object):
        """A list of actions.  Made a class so that we can hash."""
        def __init__(self, initial_list=None):
            if initial_list is None:
                initial_list = list()
            self.actions = initial_list[:]

        def __eq__(self, other):
            return self.actions == other.actions

        def __repr__(self):
            """
            This is a way to represent a memory of a certain length.  We
            represent history as a opponent_action/this_player_reaction
            seperated by commas, with the most recent pair listed last.

            Because knowing the left half of the _/_ action-reaction requires
            more memory than knowing the right half, we will have a blank on the
            oldest pair.
            """
            if len(self.actions) == 0:
                return "_"

            # The first action on the list will be the opponent's previous
            # action.  We don't know yet how we will respond, so we leave a
            # blank (_).
            action_str = "{}/_".format(self.actions[0])
            # Then we go backwards.  The next actions on the list are the
            # opponent's previous actions, our previous actions, alternatively.
            i = 1
            while i < len(self.actions)-2:
                action_str = "{}/{}, {}".format(self.actions[i+1],
                                                self.actions[i], action_str)
                i += 2
            # The oldest action we'll have will be our response to an unknown
            # opponent action.
            action_str = "_/{}, {}".format(self.actions[-1], action_str)

            return action_str

        def __hash__(self):
            return hash(repr(self))

        def append(self, action):
            self.actions.append(action)

    class Branch(object):
        """A chain of previous actions.  With other information captured, like
        state, so that we can continue to walk backwards.
        """
        def __init__(self, trans=None):
            if trans is None:
                return

            state = trans[0]
            last_opponent_action = trans[1]
            next_state = trans[2]
            next_action = trans[3]

            self.num_moves_recorded = 0
            self.action_chain = ActionChain([])
            self.next_action = next_action
            self.on_state = state
            # The information that we have available at any step will be half of
            # next step's history.  So we keep this in a buffer.
            self.buffer = last_opponent_action

            # For debugging
            self.initial_trans = "{}:{}".format(state, last_opponent_action)

        def step(self, backtrans):
            """Continues to walk (or branch) backwards from where the branch
            leaves off, given a path (backtrans) to walk backwards along.  This
            will return a Branch instance.
            """
            new_branch = Branch()
            new_branch.num_moves_recorded = self.num_moves_recorded + 1
            new_branch.action_chain = ActionChain(self.action_chain.actions)
            new_branch.action_chain.append(self.buffer)
            new_branch.action_chain.append(backtrans.prev_reaction)
            new_branch.next_action = self.next_action
            new_branch.on_state = backtrans.prev_state
            # This needs one more memory to know.
            new_branch.buffer = backtrans.prev_opp_action

            new_branch.initial_trans = self.initial_trans

            return new_branch

        def debug_str(self):
            return "{};{} | Back-trace: {} | On-state: {}".format(
                    self.initial_trans, self.next_action,
                    repr(self.action_chain), self.on_state)

    BranchList = namedtuple("BranchList", ("branch_list", "next_actions"))

    class BranchPool(object):
        """We keep branches in the branch_pool, grouped by common-end
        ActionChains.  A common-end ActionChain is a chain of N actions
        occurring most-recently that is common to all branches in the group.
        Specifically branch_pool is a dict with keys given by common-end
        ActionChains, and with dict-values given by a list of branches and the
        set of possible next_actions for these branches.

        The set of possible next_actions is the set of actions that this FSM may
        choose to do following the chain of actions given in the key.  When
        there is a single action, we know that the strategy will make that
        action; we call the branches with that chain of actions "decided" at
        this point.
        """
        def __init__(self):
            self.clear()

        def push(self, branch):
            """Just adds a branch to the branch_pool."""
            common_branches = self.branch_pool[branch.action_chain]
            common_branches.next_actions.add(branch.next_action)
            common_branches.branch_list.append(branch)

        def branches(self):
            """An iterator that loops through all the branches in the
            branch_pool.
            """
            for k, v in self.branch_pool.items():
                for branch in v.branch_list:
                    yield branch

        def clear(self):
            """Empty the branch_pool."""
            self.branch_pool = defaultdict(lambda: BranchList(list(), set()))

        def remove_decided_branches(self):
            """We call a branch "decided" if all branches with that common-end
            (end of ActionChain) give the same next_action.  This function
            removes those from the branch_pool, and returns these as a dict
            keyed by common-end ActionChain, and with dict-values given by the
            common next_action.
            """
            decided_branches = dict()
            for k, v in self.branch_pool.items():
                if len(v.next_actions) == 1:
                  decided_branches[k] = list(v.next_actions)[0]
            for k in decided_branches.keys():
                del self.branch_pool[k]
            return decided_branches

        def __bool__(self):
            return len(self.branch_pool) > 0

    # Set up variables
    num_edges = len(transitions)
    waiting, processed = BranchPool(), BranchPool()
    if print_trace:
        print("STEP 0")
        print("===============")
    for trans in transitions:
        trans_branch = Branch(trans)
        processed.push(trans_branch)
        if print_trace:
            print(trans_branch.debug_str())
    processed.remove_decided_branches()

    steps = 0
    while processed:
        steps += 1
        if print_trace:
            print("STEP {}".format(steps))
            print("===============")
        if steps > num_edges*(num_edges-1):
            return float("inf")
        # Move processed to waiting
        for branch in processed.branches():
            waiting.push(branch)
        processed.clear()
        # Now process the waiting list.
        for branch in waiting.branches():
            for backtrans in back_transitions[branch.on_state]:
                processed.push(branch.step(backtrans))
        if print_trace:
          for branch in processed.branches():
                print(branch.debug_str())
        waiting.clear()
        # And remove decided branches.
        decided_branches = processed.remove_decided_branches()
        for k, v in decided_branches.items():
            print("If {}, then {}".format(k, v))
    return steps


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
        "memory_depth": 4,
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
        "memory_depth": 9,
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
        "memory_depth": 2,
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
        "memory_depth": 5,
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
        "memory_depth": 2,
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
        "memory_depth": 4,
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
        "memory_depth": 16,  # At most
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
        "memory_depth": 16,  # At most
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
