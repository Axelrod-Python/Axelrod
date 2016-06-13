from axelrod import Actions, Player, init_args, random_choice

C, D = Actions.C, Actions.D


class NaiveProber(Player):
    """
    Like tit-for-tat, but it occasionally defects with a small probability.
    """

    name = 'Naive Prober'
    classifier = {
        'memory_depth': 1,  # Four-Vector = (1.,0.,1.,0.)
        'stochastic': True,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @init_args
    def __init__(self, p=0.1):
        """
        Parameters
        ----------
        p, float
            The probability to defect randomly
        """
        Player.__init__(self)
        self.p = p
        if (self.p == 0) or (self.p == 1):
            self.classifier['stochastic'] = False

    def strategy(self, opponent):
        # First move
        if len(self.history) == 0:
            return C
        # React to the opponent's last move
        if opponent.history[-1] == D:
            return D
        # Otherwise cooperate, defect with a small probability
        choice = random_choice(1 - self.p)
        return choice

    def __repr__(self):
        return "%s: %s" % (self.name, round(self.p, 2))
