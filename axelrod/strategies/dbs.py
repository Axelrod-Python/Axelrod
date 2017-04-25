from axelrod.actions import Actions, Action
from axelrod.player import Player


C, D = Actions.C, Actions.D


class DBS(Player):
    """
    Desired Belief Strategy as described in [Au2006]_
    http://www.cs.utexas.edu/%7Echiu/papers/Au06NoisyIPD.pdf

    A strategy that learns the opponent's strategy, and uses symbolic 
    noise detection for detecting whether anomalies in player’s behavior
    are deliberate or accidental, hence increasing performance in noisy 
    tournaments.  

    From the learned opponent's strategy, a tree search is used to
    choose the best move

    Default values for the parameters are the suggested values in the
    article. When noise increases you can try to diminish 
    violation_threshold and rejection_threshold

    Parameters:

    discount_factor: (float, between 0 and 1) discount factor used when
            computing discounted frequencies to learn opponent's strategy
            defaults = .75

    promotion_threshold: (int) number of observations needed to promote
            a change in opponent's strategy
            defaults = 3

    violation_threshold: (int) number of observation needed to 
            considerate opponent's strategy has changed. Seems good to
            lower it when noise increases
            defaults = 4

    reject_threshold: (int) number of observations before forgetting
            opponents old strategy. Seems good to lower it when noise
            increases
            default = 3

    tree_depth: (int) depth of the tree for the tree-search algorithm. 
            default is 5.
            Higher depth means more time to coompute the move.

    """

    # These are various properties for the strategy
    name = 'DBS'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, discount_factor=.75, promotion_threshold=3, 
                 violation_threshold=4, reject_threshold=3, tree_depth=5): 
        super().__init__()

        # default opponent's policy is TitForTat
        self.Rd = create_policy(1, 1, 0, 0)
        self.Rc = {}
        self.Pi = self.Rd   # policy used by MoveGen
        self.violation_counts = {}
        self.reject_threshold = reject_threshold
        self.violation_threshold = violation_threshold
        self.promotion_threshold = promotion_threshold
        self.tree_depth = tree_depth
        self.v = 0
        self.alpha = discount_factor
        self.history_by_cond = {}
        # to compute the discount frequencies, we need to keep
        # up to date an history of what has been played for each
        # condition:
        # We save it as a dict history_by_cond; keys are conditions 
        # (ex (C,C)) and values are a tuple of 2 lists (G,F)
        # for a condition j: 
        # G[i] = 1 if cond j was True at turn i-1 and C has been played
        # by the opponent; else G[i]=0
        # F[i] = 1 if cond j was True at turn i-1; else G[i]=0
        # initial hypothesized policy is TitForTat
        self.history_by_cond[(C, C)] = ([1], [1])
        self.history_by_cond[(C, D)] = ([1], [1])
        self.history_by_cond[(D, C)] = ([0], [1])
        self.history_by_cond[(D, D)] = ([0], [1])

    def reset(self):
        super().reset()
        self.Rd = create_policy(1, 1, 0, 0)
        self.Rc = {}
        self.Pi = self.Rd   # policy used by MoveGen
        self.violation_counts = {}
        self.v = 0
        self.history_by_cond = {}
        self.history_by_cond[(C, C)] = ([1], [1])
        self.history_by_cond[(C, D)] = ([1], [1])
        self.history_by_cond[(D, C)] = ([0], [1])
        self.history_by_cond[(D, D)] = ([0], [1])

    def should_promote(self, r_plus, promotion_threshold=3):
        if r_plus[1] == C:
            opposite_action = 0
        elif r_plus[1] == D:
            opposite_action = 1
        k = 1
        count = 0
        # We iterate on the history, while we do not encounter
        # counter-examples of r_plus, i.e. while we do not encounter
        # r_minus
        while(
            k < len(self.history_by_cond[r_plus[0]][0])
            and not (self.history_by_cond[r_plus[0]][0][1:][-k] 
                        == opposite_action
                    and self.history_by_cond[r_plus[0]][1][1:][-k] == 1)
            ):
            # We count every occurence of r_plus in history
            if (self.history_by_cond[r_plus[0]][1][1:][-k] == 1):
                count += 1
            k += 1
        if(count >= promotion_threshold):
            return True
        return False

    def should_demote(self, r_minus, violation_threshold=4):
        return (self.violation_counts[r_minus[0]] >= violation_threshold)

    def update_history_by_cond(self, opponent_history):
        two_moves_ago = (self.history[-2], opponent_history[-2])
        for outcome,GF in self.history_by_cond.items():
            G,F = GF
            if outcome == two_moves_ago:
                if opponent_history[-1] == C:
                    G.append(1)
                else:
                    G.append(0)
                F.append(1)
            else:
                G.append(0)
                F.append(0)

    def compute_prob_rule(self, outcome, alpha):
        G = self.history_by_cond[outcome][0]
        F = self.history_by_cond[outcome][1]
        discounted_g = 0
        discounted_f = 0
        alpha_k = 1
        for g,f in zip(G[::-1], F[::-1]):
            discounted_g += alpha_k*g
            discounted_f += alpha_k*f
            alpha_k = alpha*alpha_k
        p_cond = discounted_g/discounted_f
        return p_cond

    def strategy(self, opponent: Player) -> Action:
        """This is the actual strategy"""

        # First move
        if not self.history:
            return C
        
        if(len(opponent.history) >= 2):

            # update history_by_cond
            # (i.e. update Rp)
            self.update_history_by_cond(opponent.history)
     
            two_moves_ago = (self.history[-2], opponent.history[-2])
            r_plus = (two_moves_ago, opponent.history[-1])
            r_minus = (two_moves_ago, ({C, D} - {opponent.history[-1]}).pop())

            if r_plus[0] not in self.Rc.keys(): 
                if self.should_promote(r_plus, self.promotion_threshold):
                    self.Rc[r_plus[0]] = action_to_int(r_plus[1])
                    self.violation_counts[r_plus[0]] = 0
                    self.violation_counts[r_plus[0]] = 0

            # (if r+ or r- in Rc)
            if r_plus[0] in self.Rc.keys():
                to_check = (C if self.Rc[r_plus[0]] == 1 else D)
                # (if r+ in Rc)
                if r_plus[1] == to_check:
                    # set the violation count of r+ to 0
                    self.violation_counts[r_plus[0]] = 0
                # (if r- in Rc)
                elif r_minus[1] == to_check:
                    # increment violation count of r-
                    self.violation_counts[r_plus[0]] += 1
                    if self.should_demote(r_minus,self.violation_threshold):
                        self.Rd.update(self.Rc)
                        self.Rc.clear()
                        self.violation_counts.clear()
                        self.v = 0

            # r+ in Rc
            r_plus_in_Rc = (
                    r_plus[0] in self.Rc.keys() 
                    and self.Rc[r_plus[0]] == action_to_int(r_plus[1])
                    )
            # r- in Rd
            r_minus_in_Rd = (
                    r_minus[0] in self.Rd.keys()
                    and self.Rd[r_minus[0]] == action_to_int(r_minus[1])
                    )

            if r_minus_in_Rd:
                self.v += 1

            if (self.v > self.reject_threshold 
                    or (r_plus_in_Rc and r_minus_in_Rd)):
                self.Rd.clear()
                self.v = 0

            # compute Rp for conditions that are neither in Rc or Rd
            Rp = {}
            all_cond = [(C, C), (C, D), (D, C), (D, D)]
            for outcome in all_cond:
                if ((outcome not in self.Rc.keys()) 
                        and (outcome not in self.Rd.keys())):
                    # then we need to compute opponent's C answer probability
                    Rp[outcome] = self.compute_prob_rule(outcome, self.alpha)

            self.Pi = {}
            # algorithm ensure no duplicate keys -> no key overwriting
            self.Pi.update(self.Rc)
            self.Pi.update(self.Rd)
            self.Pi.update(Rp)

        # React to the opponent's last move
        return MoveGen((self.history[-1], opponent.history[-1]), self.Pi,
                depth_search_tree=self.tree_depth)


class Node(object):
    """
    Nodes used to build a tree for the tree-search procedure
    The tree has Determinist ans Stochastic nodes, as the opponent's
    strategy is learned as a probability distribution
    """

    # abstract method
    def get_siblings(self):
        raise NotImplementedError('subclasses must override get_siblings()!')

    # abstract method
    def is_stochastic(self):
        raise NotImplementedError('subclasses must override is_stochastic()!')


class StochasticNode(Node):
    """
    Node that have a probability pC to get to each sibling
    A StochasticNode can be written (C, X) or (D, X), with X = C with
    a probability pC, else X = D
    """

    def __init__(self, own_action, pC, depth):
        self.pC = pC
        self.depth = depth
        self.own_action = own_action

    def get_siblings(self):
        # siblings of a stochastic node get depth += 1 
        opponent_c_choice = DeterministNode(self.own_action, C, self.depth+1)
        opponent_d_choice = DeterministNode(self.own_action, D, self.depth+1)
        return (opponent_c_choice, opponent_d_choice)

    def is_stochastic(self):
        return True


class DeterministNode(Node):
    """
    Nodes (C, C), (C, D), (D, C), or (D, D) with determinist choice 
    for siblings
    """

    def __init__(self, action1, action2, depth):
        self.action1 = action1
        self.action2 = action2
        self.depth = depth

    def get_siblings(self, policy):
        """
        build 2 siblings (C, X) and (D, X)
        siblings of a DeterministicNode are Stochastic, and are of the
        same depth
        """
        c_choice = StochasticNode(
                C, policy[(self.action1, self.action2)], self.depth
                )
        d_choice = StochasticNode(
                D, policy[(self.action1, self.action2)], self.depth
                )
        return (c_choice, d_choice)

    def is_stochastic(self):
        return False

    def get_value(self):
        values = {
            (C, C): 3,
            (C, D): 0,
            (D, C): 5,
            (D, D): 1
        }
        return values[(self.action1, self.action2)]


def create_policy(pCC, pCD, pDC, pDD):
    """
    Creates a dict that represents a Policy.
    As defined in the reference, a Policy is a set of (prev_move, p) 
    where p is the probability to cooperate after prev_move,
    where prev_move can be (C, C), (C, D), (D, C) or (D, D)
    """
    pol = {}
    pol[(C, C)] = pCC
    pol[(C, D)] = pCD
    pol[(D, C)] = pDC
    pol[(D, D)] = pDD
    return pol


def action_to_int(action):
    if action == C:
        return 1
    return 0


def minimax_tree_search(begin_node, policy, max_depth):
    """
    tree search function (minimax search procedure)
    build by recursion the tree corresponding to a game against 
    opponent's policy, and solve it
    """
    if begin_node.is_stochastic():
        # a stochastic node cannot has the same depth than its parent
        # node hence there is no need to check that his 
        # depth is < max_depth
        siblings = begin_node.get_siblings()
        # The stochastic node value is the expected values of siblings
        node_value = (
            begin_node.pC * minimax_tree_search(
                                            siblings[0], 
                                            policy, 
                                            max_depth) 
            + (1 - begin_node.pC) * minimax_tree_search(
                                            siblings[1], 
                                            policy, 
                                            max_depth)
            )
        return node_value
    else:   # determinist node
        if begin_node.depth == max_depth:
            # this is an end node, we just return its outcome value
            return begin_node.get_value()
        elif begin_node.depth == 0:
            siblings = begin_node.get_siblings(policy)
            # this returns the two max expected values, for choice C or D,
            # as a tuple
            return (
                minimax_tree_search(siblings[0], policy, max_depth) 
                    + begin_node.get_value(),
                minimax_tree_search(siblings[1], policy, max_depth) 
                    + begin_node.get_value()
                )
        elif begin_node.depth < max_depth:
            siblings = begin_node.get_siblings(policy)
            # the determinist node value is the max of both siblings values
            # + the score of the outcome of the node
            a = minimax_tree_search(siblings[0], policy, max_depth)
            b = minimax_tree_search(siblings[1], policy, max_depth)
            node_value = max(a, b) + begin_node.get_value()
            return node_value
    

def MoveGen(outcome, policy, depth_search_tree=5):
    """
    returns the best move considering opponent's policy and last move,
    using tree-search procedure
    """
    current_node = DeterministNode(outcome[0], outcome[1], depth=0)
    values_of_choices = minimax_tree_search(
            current_node, policy, depth_search_tree)
    # returns the Action which correspond to the best choice in terms of 
    # expected value. In case value(C) == value(D), returns C
    actions_tuple = (C, D)
    return actions_tuple[values_of_choices.index(max(values_of_choices))]
