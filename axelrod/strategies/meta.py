import random

from axelrod import Player


class MetaPlayer(Player):
    """A generic player that has its own team of players."""

    team = []

    def __init__(self):

        Player.__init__(self)

        # Make sure we don't use any meta players to avoid infinite recursion.
        self.team = [t for t in self.team if not issubclass(t, MetaPlayer)]
        self.nteam = len(self.team)

        # Initiate all the player in out team.
        self.team = [t() for t in self.team]

        # If the team will have stochastic players, this meta is also stochastic.
        self.stochastic = any([t.stochastic for t in self.team])

    def strategy(self, opponent):

        # Make sure the history of all hunters is current.
        for ih in range(len(self.team)):
            self.team[ih].history = self.history

        # Get the results of all our players.
        results = [player.strategy(opponent) for player in self.team]

        # A subclass should just define a way to choose the result based on team results.
        return self.meta_strategy(results)

    def meta_strategy(self, results):
        """Determine the meta result based on results of all players."""
        pass


class MetaMajority(MetaPlayer):
    """A player who goes by the majority vote of all other non-meta players."""

    name = "Meta Majority"

    def __init__(self):

        # We need to import the list of strategies at runtime, since
        # _strategies import also _this_ module before defining the list.
        from _strategies import ordinary_strategies
        self.team = ordinary_strategies

        MetaPlayer.__init__(self)

    def meta_strategy(self, results):
        if results.count('D') > results.count('C'):
            return 'D'
        return 'C'


class MetaMinority(MetaPlayer):
    """A player who goes by the minority vote of all other non-meta players."""

    name = "Meta Minority"

    def __init__(self):

        # We need to import the list of strategies at runtime, since
        # _strategies import also _this_ module before defining the list.
        from _strategies import ordinary_strategies
        self.team = ordinary_strategies

        MetaPlayer.__init__(self)

    def meta_strategy(self, results):
        if results.count('D') < results.count('C'):
            return 'D'
        return 'C'


class MetaWinner(MetaPlayer):
    """A player who goes by the strategy of the current winner."""

    name = "Meta Winner"

    def __init__(self, team=None):

        # The default is to used all strategies available, but we need to import the list
        # at runtime, since _strategies import also _this_ module before defining the list.
        if team:
            self.team = team
        else:
            from _strategies import ordinary_strategies
            self.team = ordinary_strategies

        MetaPlayer.__init__(self)

        # For each player, we will keep the history of proposed moves and
        # a running score since the beginning of the game.
        for t in self.team:
            t.proposed_history = []
            t.score = 0

    def strategy(self, opponent):

        # Update the running score for each player, before determining the next move.
        if len(self.history):
            for player in self.team:
                pl_C = player.proposed_history[-1] == "C"
                opp_C = opponent.history[-1] == "C"
                s = 2 * (pl_C and opp_C) or 5 * (pl_C and not opp_C) or 4 * (not pl_C and not opp_C) or 0
                player.score += s

        return MetaPlayer.strategy(self, opponent)

    def meta_strategy(self, results):

        scores = [pl.score for pl in self.team]
        bestscore = min(scores)
        beststrategies = [i for i, pl in enumerate(self.team) if pl.score == bestscore]
        bestproposals = [results[i] for i in beststrategies]
        bestresult = "C" if "C" in bestproposals else "D"

        # Update each player's proposed history with his proposed result, but always after
        # the new result has been settled based on scores accumulated until now.
        for r, t in zip(results, self.team):
            t.proposed_history.append(r)

        return bestresult