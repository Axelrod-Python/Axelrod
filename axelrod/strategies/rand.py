from axelrod import Player, init_args, random_choice


class Random(Player):
    """A player who randomly chooses between cooperating and defecting.

    Names:

    - Random: [Axelrod1980]_
    """

    name = 'Random'
    classifier = {
        'memory_depth': 0,  # Memory-one Four-Vector = (p, p, p, p)
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @init_args
    def __init__(self, p=0.5):
        """
        Parameters
        ----------
        p, float
            The probability to cooperate

        Special Cases
        -------------
        Random(0) is equivalent to Defector
        Random(1) is equivalent to Cooperator
        """
        Player.__init__(self)
        self.p = p

    def strategy(self, opponent):
        return random_choice(self.p)

    def __repr__(self):
        return "%s: %s" % (self.name, round(self.p, 2))
