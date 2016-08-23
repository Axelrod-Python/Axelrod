from axelrod import Actions, Player, init_args

C, D = Actions.C, Actions.D


class Grumpy(Player):
    """A player that defects after a certain level of grumpiness.
    Grumpiness increases when the opponent defects and decreases
    when the opponent co-operates."""

    name = 'Grumpy'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @init_args
    def __init__(self, starting_state='Nice', grumpy_threshold=10,
                 nice_threshold=-10):
        """
        Parameters
        ----------
        starting_state, str: 'Nice' or 'Grumpy'
        grumpy_threshold, int
            The threshold of opponent defections - cooperations to become
            grumpy
        nice_threshold, int
            The threshold of opponent defections - cooperations to become
            nice
        """
        super(Grumpy, self).__init__()
        self.history = []
        self.state = starting_state
        self.starting_state = starting_state
        self.grumpy_threshold = grumpy_threshold
        self.nice_threshold = nice_threshold

    def strategy(self, opponent):
        """A player that gets grumpier the more the opposition defects,
        and nicer the more they cooperate.

        Starts off Nice, but becomes grumpy once the grumpiness threshold is hit.
        Won't become nice once that grumpy threshold is hit, but must reach a much lower threshold before it becomes nice again.
        """

        self.grumpiness = opponent.defections - opponent.cooperations

        if self.state == 'Nice':
            if self.grumpiness > self.grumpy_threshold:
                self.state = 'Grumpy'
                return D
            return C

        if self.state == 'Grumpy':
            if self.grumpiness < self.nice_threshold:
                self.state = 'Nice'
                return C
            return D

    def reset(self):
        """Resets score, history and state for the next round of the tournement."""
        Player.reset(self)
        self.state = self.starting_state
