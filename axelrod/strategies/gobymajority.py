from axelrod import Player


class GoByMajority(Player):
    """A player examines the history of the opponent: if the opponent has more
    defections than cooperations then the player defects.

    An optional memory attribute will limit the number of turns remembered (by
    default this is 0)
    """

    # memory_depth is set by __init__

    def __init__(self, memory_depth=0, soft=True):
        Player.__init__(self)
        self.soft = soft
        self.memory_depth = memory_depth
        # Set class var for consistency with other strategies
        self.__class__.memory_depth = memory_depth

    def strategy(self, opponent):
        """This is affected by the history of the opponent.

        As long as the opponent cooperates at least as often as they defect then the player will cooperate.
        If at any point the opponent has more defections than cooperations in memory the player defects.
        """

        memory = self.memory_depth
        history = opponent.history[-memory:]
        defections = sum([s == 'D' for s in history])
        cooperations = sum([s == 'C' for s in history])
        if defections > cooperations:
            return 'D'
        if defections == cooperations:
            if self.soft:
                return 'C'
            else:
                return 'D'
        return 'C'

    def __repr__(self):
        """The string method for the strategy."""
        memory = self.memory_depth
        return 'Go By Majority' + (memory > 0) * ("/%i" % memory)


class GoByMajority40(GoByMajority):
    """ 
    GoByMajority player with a memory of 40.
    """

    def __init__(self, memory_depth=40):
        super(self.__class__, self).__init__(memory_depth=memory_depth)


class GoByMajority20(GoByMajority):
    """
    GoByMajority player with a memory of 20.
    """

    def __init__(self, memory_depth=20):
        super(self.__class__, self).__init__(memory_depth=memory_depth)


class GoByMajority10(GoByMajority):
    """
    GoByMajority player with a memory of 10.
    """

    def __init__(self, memory_depth=10):
        super(self.__class__, self).__init__(memory_depth=memory_depth)


class GoByMajority5(GoByMajority):
    """
    GoByMajority player with a memory of 5.
    """

    def __init__(self, memory_depth=5):
        super(self.__class__, self).__init__(memory_depth=memory_depth)
