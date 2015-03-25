class RoundRobin(object):
    """A class to define play a round robin game of players"""

    def __init__(self, players, game, turns, deterministic_cache={},
                 cache_mutable=True):
        """Initialise the players, game and deterministic cache"""
        self.players = players
        self.nplayers = len(players)
        self.game = game
        self.turns = turns
        self.deterministic_cache = deterministic_cache
        self.cache_mutable = cache_mutable

    def calculate_scores(self, p1, p2):
        """Calculates the score for two players based their history"""
        s1, s2 = 0, 0
        for pair in zip(p1.history, p2.history):
            score = self.game.score(pair)
            s1 += score[0]
            s2 += score[1]
        return s1, s2

    def play(self):
        """Plays a round robin where each match lasts turns.

        We cache scores for pairs of deterministic strategies, since the outcome will
        always be the same.

        Notice also that we need to handle self-interactions with some special exceptions
        due to the way gameplay is coded within Player.

        Returns the total payoff matrix.
        """

        payoffs = [[0 for j in range(self.nplayers)] for i in range(self.nplayers)]

        for ip1 in range(self.nplayers):

            p1 = self.players[ip1]
            cl1 = p1.__class__

            for ip2 in range(ip1, self.nplayers):

                # For self-interactions we need to create an additional object. otherwise
                # the play method in Player will write twice to the same history, effectively
                # doubling the score and causing historic schizophrenia.
                if ip1 == ip2:
                    p2 = cl1()
                    cl2 = cl1
                else:
                    p2 = self.players[ip2]
                    cl2 = p2.__class__

                # There are many possible keys to cache by, but perhaps the
                # most versatile is a tuple with the classes of both players.
                key = (cl1, cl2)
                if (p1.stochastic or p2.stochastic or key not in self.deterministic_cache):
                    turn = 0
                    p1.reset()
                    p2.reset()
                    while turn < self.turns:
                        turn += 1
                        p1.play(p2)
                    scores = self.calculate_scores(p1, p2)
                    if self.cache_mutable and not (p1.stochastic or p2.stochastic):
                        self.deterministic_cache[key] = scores
                else:
                    scores = self.deterministic_cache[key]

                # For self-interactions we can take the average of the two sides, which
                # should improve the averaging a bit.
                if ip1 == ip2:
                    payoffs[ip1][ip2] = 0.5 * (scores[0] + scores[1])
                else:
                    payoffs[ip1][ip2] = scores[0]
                    payoffs[ip2][ip1] = scores[1]

        return payoffs
