.. _metastrategies:

Meta-Strategies
===============

Finite State Machines
---------------------

A finite state machine (FSM) is a general computation model.  In the context of Axelrod, it's a set of states and "transitions."  A transition for a given state/previous-opponent-action combination says how the strategy will respond, both in what action it will take and in what state it will transitions to. That is a transition will specify that in state :math:`a`, the strategy will respond to action :math:`X` by taking action :math:`Y` and moving to state :math:`b` (which will tell us which transitions to use in later moves).  We may write this transition :math:`(a, X, b, Y)`.  For Axelrod, a FSM must have a full set of transitions, which specifies a unique response for each
state/previous-opponent-action combination.

See [Harper2017]_ for a more-detailed explanation.

Representing a strategy as a finite state machine has been useful in some research (see [Harper2017]_ or [Ashlock2006b]_).  Though it's theoretically possible to represent all strategies as FSMs, this is impractical for most strategies.  However, some strategies lend themselves naturally to a FSM representation.  For example, for the Iterated Prisoner's Dilemma, we could consider a strategy that cooperates (C) until the opponent defects (D) twice in a row, then defect forever thereafter.  (We'll call this strategy grudger_2 for the example.)  We could call state 1, the state where the opponent hasn't started a defect streak; state 2, the state where the opponent is on a 1-defect streak; and state 3, the state where the opponent has defected twice in a row at some point.  Then the transitions would be::

    >>> from axelrod import Action
    >>> C, D = Action.C, Action.D
    >>> grudger_2_transitions = (
    ...    (1, C, 1, C),
    ...    (1, D, 2, C),
    ...    (2, C, 1, C),
    ...    (2, D, 3, D),
    ...    (3, C, 3, D),
    ...    (3, D, 3, D)
    ... )

The Axelrod library includes a FSM meta-strategy player, which will you let you specify a player's strategy by this transition matrix, along with an initial state and initial action.  The syntax for this is::

    >>> from axelrod.strategies.finite_state_machines import FSMPlayer
    >>> grudger_2 = FSMPlayer(transitions=grudger_2_transitions,
    ...                       initial_state=1, initial_action=C)

The library also includes the functionality to compute the memory from the set of transitions.  In the grudger_2 example, the memory would be 2.  Because either the strategy's own previous move was a defect (in which case, continue to defect) or we just need to check if the last two opponent moves were defects or not.  Though this function takes the transitions in a slightly different format::

    >>> transition_dict = {
    ...    (t[0], t[1]): (t[2], t[3]) for t in grudger_2_transitions
    ... }
    >>> from axelrod.compute_finite_state_machine_memory import *
    >>> get_memory_from_transitions(transitions=transition_dict,
    ...                             initial_state=1)
    2
