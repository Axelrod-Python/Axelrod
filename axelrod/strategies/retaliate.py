from collections import defaultdict

from axelrod import Player


class Retaliate(Player):
    """
    A player starts by cooperating but will retaliate once the opponent
    has won more than 10 percent times the number of defections the player has.
    """
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, retaliation_threshold=0.1):
        """
        Uses the basic init from the Player class, but also set the name to
        include the retaliation setting.
        """
        Player.__init__(self)
        self.retaliation_threshold = retaliation_threshold
        self.name = (
            'Retaliate (' +
            str(self.retaliation_threshold) + ')')
        self.play_counts = defaultdict(int)
        self.init_args = (retaliation_threshold,)

    def strategy(self, opponent):
        """
        If the opponent has played D to my C more often than x% of the time
        that I've done the same to him, play D. Otherwise, play C.
        """

        if len(self.history):
            last_round = (self.history[-1], opponent.history[-1])
            self.play_counts[last_round] += 1
        CD_count = self.play_counts[('C', 'D')]
        DC_count = self.play_counts[('D', 'C')]
        if CD_count > DC_count * self.retaliation_threshold:
                return 'D'
        return 'C'

    def reset(self):
        Player.reset(self)
        self.play_counts = defaultdict(int)

class Retaliate2(Retaliate):
    """
    Retaliate player with a threshold of 8 percent.
    """

    def __init__(self, retaliation_threshold=0.08):
        super(self.__class__, self).__init__(
            retaliation_threshold=retaliation_threshold)


class Retaliate3(Retaliate):
    """
    Retaliate player with a threshold of 5 percent.
    """

    def __init__(self, retaliation_threshold=0.05):
        super(self.__class__, self).__init__(
            retaliation_threshold=retaliation_threshold)


class LimitedRetaliate(Player):
    """
    A player that co-operates unless the opponent defects and wins.
    It will then retaliate by defecting. It stops when either, it has beaten
    the opponent 10 times more often that it has lost or it reaches the
    retaliation limit (20 defections).
    """

    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, retaliation_threshold = 0.1, retaliation_limit = 20,):
        """
        Uses the basic init from the Player class, but also set the name to
        include the retaliation setting.
        """
        Player.__init__(self)
        self.retaliating = False
        self.retaliation_count = 0
        self.retaliation_threshold = retaliation_threshold
        self.retaliation_limit = retaliation_limit
        self.play_counts = defaultdict(int)
        self.init_args = (retaliation_threshold, retaliation_limit)

        self.name = (
            'Limited Retaliate (' +
            str(self.retaliation_threshold) +
            '/' + str(self.retaliation_limit) + ')')

    def strategy(self, opponent):
        """
        If the opponent has played D to my C more often than x% of the time
        that I've done the same to him, retaliate by playing D but stop doing
        so once I've hit the retaliation limit.
        """

        if len(self.history):
            last_round = (self.history[-1], opponent.history[-1])
            self.play_counts[last_round] += 1
        CD_count = self.play_counts[('C', 'D')]
        DC_count = self.play_counts[('D', 'C')]
        if CD_count > DC_count * self.retaliation_threshold:
            self.retaliating = True
        else:
            self.retaliating = False
            self.retaliation_count = 0

        #history = list(zip(self.history, opponent.history))

        #if history.count(('C', 'D')) > (
           #history.count(('D', 'C')) * self.retaliation_threshold):
            #self.retaliating = True
        #else:
            #self.retaliating = False
            #self.retaliation_count = 0

        if self.retaliating:
            if self.retaliation_count < self.retaliation_limit:
                self.retaliation_count += 1
                return 'D'
            else:
                self.retaliation_count = 0
                self.retaliating = False

        return 'C'

    def reset(self):
        Player.reset(self)
        self.play_counts = defaultdict(int)
        self.retaliating = False
        self.retaliation_count = 0


class LimitedRetaliate2(LimitedRetaliate):
    """
    LimitedRetaliate player with a threshold of 8 percent and a
    retaliation limit of 15.
    """

    def __init__(self, retaliation_threshold=0.08, retaliation_limit=15):
        super(self.__class__, self).__init__(
            retaliation_threshold=retaliation_threshold,
            retaliation_limit=retaliation_limit)


class LimitedRetaliate3(LimitedRetaliate):
    """
    LimitedRetaliate player with a threshold of 5 percent and a
    retaliation limit of 20.
    """

    def __init__(self, retaliation_threshold=0.05, retaliation_limit=20):
        super(self.__class__, self).__init__(
            retaliation_threshold=retaliation_threshold,
            retaliation_limit=retaliation_limit)
