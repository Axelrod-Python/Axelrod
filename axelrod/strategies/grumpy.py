from axelrod import Player

class Grumpy(Player):
    """A player that defects after a ceratin level of grumpiness. Grumpiness increases when the opponent defects and decreases when the opponent co-operates."""

    name = 'Grumpy'

    def __init__(self, starting_state = 'Nice', grumpy_threshold = 10, nice_threshold = -10):
        """Player starts of nice be default with set thresholds"""
        super(Grumpy, self).__init__()
        self.history = []
        self.score = 0
        self.state = starting_state
        self.starting_state = starting_state
        self.grumpy_threshold = grumpy_threshold
        self.nice_threshold = nice_threshold

    def strategy(self, opponent):
        """A player that gets grumpier the more the opposition defects, and nicer the more they cooperate.

        Starts off Nice, but becomes grumpy once the grumpiness threshold is hit.
        Won't become nice once that grumpy threshold is hit, but must reach a much lower threshold before it becomes nice again.
        """

        self.grumpiness = sum(play=='D' for play in opponent.history) - sum(play=='C' for play in opponent.history)

        if self.state == 'Nice':
            if self.grumpiness > self.grumpy_threshold:
                self.state = 'Grumpy'
                return 'D'
            return 'C'

        if self.state == 'Grumpy':
            if self.grumpiness < self.nice_threshold:
                self.state = 'Nice'
                return 'C'
            return 'D'

    def reset(self):
        """Resets score, history and state for the next round of the tournement."""

        self.history = []
        self.state = self.starting_state
