from axelrod.actions import Actions
from axelrod.player import Player

import copy

C, D = Actions.C, Actions.D


class GoByMajority(Player):
    """A player examines the history of the opponent: if the opponent has more
    defections than cooperations then the player defects.

    In case of equal
    number of defections and cooperations this player will Cooperate. Passing
    the `soft=False` keyword argument when initialising will create a
    HardGoByMajority which Defects in case of equality.

    An optional memory attribute will limit the number of turns remembered (by
    default this is 0)
    """

    name = 'Go By Marjority'
    classifier = {
        'stochastic': False,
        'inspects_source': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'manipulates_source': False,
        'manipulates_state': False,
        'memory_depth': float('inf')  # memory_depth may be altered by __init__
    }

    def __init__(self, memory_depth=float('inf'), soft=True):
        """
        Parameters
        ----------
        memory_depth, int >= 0
            The number of rounds to use for the calculation of the cooperation
            and defection probabilities of the opponent.
        soft, bool
            Indicates whether to cooperate or not in the case that the
            cooperation and defection probabilities are equal.
        """

        super().__init__()
        self.soft = soft
        self.classifier['memory_depth'] = memory_depth
        if self.classifier['memory_depth'] < float('inf'):
            self.memory = self.classifier['memory_depth']
        else:
            self.memory = 0

        self.name = (
            'Go By Majority' + (self.memory > 0) * (": %i" % self.memory))
        if self.soft:
            self.name = "Soft " + self.name
        else:
            self.name = "Hard " + self.name

    def strategy(self, opponent):
        """This is affected by the history of the opponent.

        As long as the opponent cooperates at least as often as they defect then
        the player will cooperate.  If at any point the opponent has more
        defections than cooperations in memory the player defects.
        """

        history = opponent.history[-self.memory:]
        defections = sum([s == D for s in history])
        cooperations = sum([s == C for s in history])
        if defections > cooperations:
            return D
        if defections == cooperations:
            if self.soft:
                return C
            else:
                return D
        return C


class GoByMajority40(GoByMajority):
    """
    GoByMajority player with a memory of 40.
    """
    name = 'Go By Majority 40'
    classifier = copy.copy(GoByMajority.classifier)
    classifier['memory_depth'] = 40

    def __init__(self, memory_depth=40, soft=True):
        super().__init__(memory_depth=memory_depth, soft=soft)


class GoByMajority20(GoByMajority):
    """
    GoByMajority player with a memory of 20.
    """
    name = 'Go By Majority 20'
    classifier = copy.copy(GoByMajority.classifier)
    classifier['memory_depth'] = 20

    def __init__(self, memory_depth=20, soft=True):
        super().__init__(memory_depth=memory_depth, soft=soft)


class GoByMajority10(GoByMajority):
    """
    GoByMajority player with a memory of 10.
    """
    name = 'Go By Majority 10'
    classifier = copy.copy(GoByMajority.classifier)
    classifier['memory_depth'] = 10

    def __init__(self, memory_depth=10, soft=True):
        super().__init__(memory_depth=memory_depth, soft=soft)


class GoByMajority5(GoByMajority):
    """
    GoByMajority player with a memory of 5.
    """
    name = 'Go By Majority 5'
    classifier = copy.copy(GoByMajority.classifier)
    classifier['memory_depth'] = 5

    def __init__(self, memory_depth=5, soft=True):
        super().__init__(memory_depth=memory_depth, soft=soft)


class HardGoByMajority(GoByMajority):
    """A player examines the history of the opponent: if the opponent has more
    defections than cooperations then the player defects. In case of equal
    number of defections and cooperations this player will Defect.

    An optional memory attribute will limit the number of turns remembered (by
    default this is 0)
    """
    name = 'Hard Go By Majority'

    def __init__(self, memory_depth=float('inf'), soft=False):
        super().__init__(memory_depth=memory_depth, soft=soft)


class HardGoByMajority40(HardGoByMajority):
    """
    HardGoByMajority player with a memory of 40.
    """
    name = 'Hard Go By Majority 40'
    classifier = copy.copy(GoByMajority.classifier)
    classifier['memory_depth'] = 40

    def __init__(self, memory_depth=40, soft=False):
        super().__init__(memory_depth=memory_depth, soft=soft)


class HardGoByMajority20(HardGoByMajority):
    """
    HardGoByMajority player with a memory of 20.
    """
    name = 'Hard Go By Majority 20'
    classifier = copy.copy(GoByMajority.classifier)
    classifier['memory_depth'] = 20

    def __init__(self, memory_depth=20, soft=False):
        super().__init__(memory_depth=memory_depth, soft=soft)


class HardGoByMajority10(HardGoByMajority):
    """
    HardGoByMajority player with a memory of 10.
    """
    name = 'Hard Go By Majority 10'
    classifier = copy.copy(GoByMajority.classifier)
    classifier['memory_depth'] = 10

    def __init__(self, memory_depth=10, soft=False):
        super().__init__(memory_depth=memory_depth, soft=soft)


class HardGoByMajority5(HardGoByMajority):
    """
    HardGoByMajority player with a memory of 5.
    """
    name = 'Hard Go By Majority 5'
    classifier = copy.copy(GoByMajority.classifier)
    classifier['memory_depth'] = 5

    def __init__(self, memory_depth=5, soft=False):
        super().__init__(memory_depth=memory_depth, soft=soft)
