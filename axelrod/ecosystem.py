
import random


class Ecosystem(object):
    """Create an ecosystem based on the payoff matrix from an Axelrod tournament."""

    def __init__(self, results, fitness=None):

        results.finalise()
        self.results = results
        self.nplayers = self.results.nplayers
        self.payoff_matrix = self.results.payoff_matrix
        self.payoff_stddevs = self.results.payoff_stddevs

        # Population sizes will be recorded in this nested list, with each internal
        # list containing strategy populations for a given turn. The first list,
        # representing the starting populations, should have all equal values,
        # and all population lists should be normalized to one.
        self.population_sizes = [[1.0 / self.nplayers for i in range(self.nplayers)]]

        # This function is quite arbitrary and probably only influences the kinetics
        # for the current code.
        if fitness:
            self.fitness = fitness
        else:
            self.fitness = lambda p: 5.0 / (5.0 + p)

    def reproduce(self, turns):

        for iturn in range(turns):

            plist = list(range(self.nplayers))
            pops = self.population_sizes[-1]

            # The unit payoff for each player in this turn is the sum of the payoffs
            # obtained from playing with all other players, scaled by the size of the
            # opponent's population. Note that we sample the normal distribution
            # based on the payoff matrix and its standard deviations obtained from
            # the iterated PD tournament run previously.
            payoffs = [0 for ip in plist]
            for ip in plist:
                for jp in plist:
                    avg = self.payoff_matrix[ip][jp]
                    dev = self.payoff_stddevs[ip][jp]
                    p = random.normalvariate(avg, dev)
                    payoffs[ip] += p * pops[jp]

            # The fitness should determine how well a strategy reproduces. The new populations
            # should be multiplied by something that is proportional to the fitness, but we are
            # normalizing anyway so just multiply times fitness.
            fitness = [self.fitness(p) for p in payoffs]
            newpops = [p * f for p, f in zip(pops, fitness)]

            # Make sure the new populations are normalized to one.
            norm = sum(newpops)
            newpops = [p / norm for p in newpops]

            self.population_sizes.append(newpops)
