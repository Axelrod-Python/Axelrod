class Ecosystem(object):
    """Create an ecosystem based on the payoff matrix from an Axelrod tournament."""

    def __init__(self, pmatrix):

        self.pmatrix = pmatrix
        self.nplayers = len(self.pmatrix)

        # Population histories will be recorded in a nested list,
        # with each internal list containing a list of populations
        # for all strategies. The first list, representing the
        # starting populations, should have all equal values.
        self.populations = [[1.0 / self.nplayers for i in range(self.nplayers)]]

    def reproduce(self, turns):

        for iturn in range(turns):

            plist = list(range(self.nplayers))
            pops = self.populations[-1]

            # The unit payoff for each player in this turn is a sum of the payoffs
            # obtained from all other players scaled by the size of the opponent population.
            payoffs = [sum([self.pmatrix[ip][jp] * pops[jp] for jp in plist]) for ip in plist]

            # In our case lower payoffs are better, so fitness should increase when
            # the payoff descreases. This is a simple linear function that fulfills
            # this and still behaves nicely, but we could chooise more complicated forms.
            pmax = 5 * self.nplayers
            fitness = [pmax - p + 1 for p in payoffs]

            # The new populations should be multiplied by something that is proportional
            # to the fitness, but we are normalizing anyway so just multiply times fitness.
            newpops = [p * f for p, f in zip(pops, fitness)]
            norm = sum(newpops)
            newpops = [p / norm for p in newpops]

            self.populations.append(newpops)