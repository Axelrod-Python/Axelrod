from axelrod import Player, is_cheater
from ._strategies import strategies
from .hunter import DefectorHunter, AlternatorHunter, RandomHunter, MathConstantHunter


# Needs to be computed manually to prevent circular dependency
ordinary_strategies = [s for s in strategies if not is_cheater(s)]


class MetaPlayer(Player):
    """A generic player that has its own team of players."""

    team = []
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self):

        super(MetaPlayer, self).__init__()

        # Make sure we don't use any meta players to avoid infinite recursion.
        self.team = [t for t in self.team if not issubclass(t, MetaPlayer)]
        self.nteam = len(self.team)

        # Initiate all the player in out team.
        self.team = [t() for t in self.team]

        # If the team will have stochastic players, this meta is also stochastic.
        self.classifier['stochastic'] = (
            any([t.classifier['stochastic'] for t in self.team]))

    def strategy(self, opponent):

        # Make sure the history of all hunters is current.
        for ih in range(len(self.team)):
            self.team[ih].history = self.history

        # Get the results of all our players.
        results = [player.strategy(opponent) for player in self.team]

        # A subclass should just define a way to choose the result based on team results.
        return self.meta_strategy(results, opponent)

    def meta_strategy(self, results, opponent):
        """Determine the meta result based on results of all players."""
        pass


class MetaMajority(MetaPlayer):
    """A player who goes by the majority vote of all other non-meta players."""

    name = "Meta Majority"

    def __init__(self):
        self.team = ordinary_strategies
        super(MetaMajority, self).__init__()

    def meta_strategy(self, results, opponent):
        if results.count('D') > results.count('C'):
            return 'D'
        return 'C'


class MetaMinority(MetaPlayer):
    """A player who goes by the minority vote of all other non-meta players."""

    name = "Meta Minority"

    def __init__(self):
        self.team = ordinary_strategies
        super(MetaMinority, self).__init__()

    def meta_strategy(self, results, opponent):
        if results.count('D') < results.count('C'):
            return 'D'
        return 'C'


class MetaWinner(MetaPlayer):
    """A player who goes by the strategy of the current winner."""

    name = "Meta Winner"

    def __init__(self, team=None):

        # The default is to use all strategies available, but we need to import the list
        # at runtime, since _strategies import also _this_ module before defining the list.
        if team:
            self.team = team
        else:
            # Needs to be computed manually to prevent circular dependency
            self.team = ordinary_strategies

        super(MetaWinner, self).__init__()
        self.init_args = (team,)

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
                game = self.tournament_attributes["game"]
                s = game.scores[(player.proposed_history[-1], opponent.history[-1])][0]
                player.score += s
        return super(MetaWinner, self).strategy(opponent)

    def meta_strategy(self, results, opponent):

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


class MetaHunter(MetaPlayer):
    """A player who uses a selection of hunters."""

    name = "Meta Hunter"
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self):
        # Notice that we don't include the cooperator hunter, because it leads to excessive
        # defection and therefore bad performance against unforgiving strategies. We will stick
        # to hunters that use defections as cues. However, a really tangible benefit comes from
        # combining Random Hunter and Math Constant Hunter, since together they catch strategies
        # that are lightly randomized but still quite constant (the tricky/suspecious ones).
        self.team = [DefectorHunter, AlternatorHunter, RandomHunter, MathConstantHunter]

        super(MetaHunter, self).__init__()

    @staticmethod
    def meta_strategy(results, opponent):

        # If any of the hunters smells prey, then defect!
        if 'D' in results:
            return 'D'

        # Tit-for-tat might seem like a better default choice, but in many cases it complicates
        # the heuristics of hunting and creates fale-positives. So go ahead and use it, but only
        # for longer histories.
        if len(opponent.history) > 100:
            return 'D' if opponent.history[-1:] == ['D'] else 'C'
        else:
            return 'C'
