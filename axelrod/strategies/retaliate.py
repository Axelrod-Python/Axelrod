from collections import defaultdict

from axelrod.actions import Actions, Action
from axelrod.player import Player

C, D = Actions.C, Actions.D


class Retaliate(Player):
    """
    A player starts by cooperating but will retaliate once the opponent
    has won more than 10 percent times the number of defections the player has.

    Names:

    - Retaliate: Original name by Owen Campbell
    """

    name = 'Retaliate'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'inspects_source': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, retaliation_threshold: float = 0.1) -> None:
        """
        Uses the basic init from the Player class, but also set the name to
        include the retaliation setting.
        """
        super().__init__()
        self.retaliation_threshold = retaliation_threshold
        self.play_counts = defaultdict(int) # type: defaultdict

    def strategy(self, opponent: Player) -> Action:
        """
        If the opponent has played D to my C more often than x% of the time
        that I've done the same to him, play D. Otherwise, play C.
        """

        if len(self.history):
            last_round = (self.history[-1], opponent.history[-1])
            self.play_counts[last_round] += 1
        CD_count = self.play_counts[(C, D)]
        DC_count = self.play_counts[(D, C)]
        if CD_count > DC_count * self.retaliation_threshold:
                return D
        return C

    def reset(self):
        super().reset()
        self.play_counts = defaultdict(int)


class Retaliate2(Retaliate):
    """
    Retaliate player with a threshold of 8 percent.

    Names:

    - Retaliate 2: Original name by Owen Campbell
    """

    name = 'Retaliate 2'

    def __init__(self, retaliation_threshold: float = 0.08) -> None:
        super().__init__(retaliation_threshold=retaliation_threshold)


class Retaliate3(Retaliate):
    """
    Retaliate player with a threshold of 5 percent.

    Names:

    - Retaliate 3: Original name by Owen Campbell
    """

    name = 'Retaliate 3'

    def __init__(self, retaliation_threshold: float = 0.05) -> None:
        super().__init__(retaliation_threshold=retaliation_threshold)


class LimitedRetaliate(Player):
    """
    A player that co-operates unless the opponent defects and wins.
    It will then retaliate by defecting. It stops when either, it has beaten
    the opponent 10 times more often that it has lost or it reaches the
    retaliation limit (20 defections).

    Names:

    - Limited Retaliate: Original name by Owen Campbell
    """

    name = 'Limited Retaliate'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, retaliation_threshold: float = 0.1, retaliation_limit: int = 20) -> None:
        """
        Parameters
        ----------
        retaliation_threshold, float
            The threshold of the difference in defections, previous rounds of
            (C, D) versus (D, C)
        retaliation_limit, int
            The maximum number of retaliations until the strategy returns to
            cooperation
        """
        super().__init__()
        self.retaliating = False
        self.retaliation_count = 0
        self.retaliation_threshold = retaliation_threshold
        self.retaliation_limit = retaliation_limit
        self.play_counts = defaultdict(int) # type: defaultdict

    def strategy(self, opponent: Player) -> Action:
        """
        If the opponent has played D to my C more often than x% of the time
        that I've done the same to him, retaliate by playing D but stop doing
        so once I've hit the retaliation limit.
        """

        if len(self.history):
            last_round = (self.history[-1], opponent.history[-1])
            self.play_counts[last_round] += 1
        CD_count = self.play_counts[(C, D)]
        DC_count = self.play_counts[(D, C)]
        if CD_count > DC_count * self.retaliation_threshold:
            self.retaliating = True
        else:
            self.retaliating = False
            self.retaliation_count = 0

        if self.retaliating:
            if self.retaliation_count < self.retaliation_limit:
                self.retaliation_count += 1
                return D
            else:
                self.retaliation_count = 0
                self.retaliating = False

        return C

    def reset(self):
        super().reset()
        self.play_counts = defaultdict(int)
        self.retaliating = False
        self.retaliation_count = 0


class LimitedRetaliate2(LimitedRetaliate):
    """
    LimitedRetaliate player with a threshold of 8 percent and a
    retaliation limit of 15.

    Names:

    - Limited Retaliate 2: Original name by Owen Campbell
    """

    name = 'Limited Retaliate 2'

    def __init__(self, retaliation_threshold: float = 0.08,
                 retaliation_limit: int = 15) -> None:
        super().__init__(
            retaliation_threshold=retaliation_threshold,
            retaliation_limit=retaliation_limit)


class LimitedRetaliate3(LimitedRetaliate):
    """
    LimitedRetaliate player with a threshold of 5 percent and a
    retaliation limit of 20.

    Names:

    - Limited Retaliate 3: Original name by Owen Campbell
    """

    name = 'Limited Retaliate 3'

    def __init__(self, retaliation_threshold: float = 0.05,
                 retaliation_limit: int = 20) -> None:
        super().__init__(
            retaliation_threshold=retaliation_threshold,
            retaliation_limit=retaliation_limit)
