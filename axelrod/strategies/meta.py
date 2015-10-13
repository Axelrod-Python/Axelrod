from axelrod import Player, obey_axelrod
from ._strategies import strategies
from .hunter import DefectorHunter, AlternatorHunter, RandomHunter, MathConstantHunter, CycleHunter, EventualCycleHunter
from .cooperator import Cooperator

# Needs to be computed manually to prevent circular dependency
ordinary_strategies = [s for s in strategies if obey_axelrod(s)]


class MetaPlayer(Player):
    """A generic player that has its own team of players."""

    name = "Meta Player"

    team = [Cooperator]
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

        # This player inherits the classifiers of its team.
        for key in ['stochastic', 'inspects_source', 'manipulates_source',
                    'manipulates_state']:
            self.classifier[key] = (any([t.classifier[key] for t in self.team]))
        self.classifier['memory_depth'] = max([t.classifier['memory_depth'] for
                                               t in self.team])

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

    def reset(self):
        Player.reset(self)
        # Reset each player as well
        for player in self.team:
            player.reset()


class MetaMajority(MetaPlayer):
    """A player who goes by the majority vote of all other non-meta players."""

    name = "Meta Majority"

    def __init__(self, team=None):
        if team:
            self.team = team
        else:
            # Needs to be computed manually to prevent circular dependency
            self.team = ordinary_strategies
        super(MetaMajority, self).__init__()

    def meta_strategy(self, results, opponent):
        if results.count('D') > results.count('C'):
            return 'D'
        return 'C'


class MetaMinority(MetaPlayer):
    """A player who goes by the minority vote of all other non-meta players."""

    name = "Meta Minority"

    def __init__(self, team=None):
        if team:
            self.team = team
        else:
            # Needs to be computed manually to prevent circular dependency
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

        # For each player, we will keep the history of proposed moves and
        # a running score since the beginning of the game.
        for t in self.team:
            t.proposed_history = []
            t.score = 0

    def strategy(self, opponent):

        # Update the running score for each player, before determining the next move.
        if len(self.history):
            for player in self.team:
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

        if opponent.defections == 0:
            # Don't poke the bear
            return 'C'

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
        self.team = [DefectorHunter, AlternatorHunter, RandomHunter, MathConstantHunter, CycleHunter, EventualCycleHunter]

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


class MetaMajorityMemoryOne(MetaMajority):
    """MetaMajority with the team of Memory One players"""

    name = "Meta Majority Memory One"

    def __init__(self):
        team = [s for s in ordinary_strategies if s().classifier['memory_depth'] <= 1]
        super(MetaMajorityMemoryOne, self).__init__(team=team)


class MetaWinnerMemoryOne(MetaWinner):
    """MetaWinner with the team of Memory One players"""

    name = "Meta Winner Memory One"

    def __init__(self):
        team = [s for s in ordinary_strategies if s().classifier['memory_depth'] <= 1]
        super(MetaWinnerMemoryOne, self).__init__(team=team)


class MetaMajorityFiniteMemory(MetaMajority):
    """MetaMajority with the team of Finite Memory Players"""

    name = "Meta Majority Finite Memory"
    def __init__(self):
        team = [s for s in ordinary_strategies if s().classifier['memory_depth']
                < float('inf')]
        super(MetaMajorityFiniteMemory, self).__init__(team=team)


class MetaWinnerFiniteMemory(MetaWinner):
    """MetaWinner with the team of Finite Memory Players"""

    name = "Meta Winner Finite Memory"
    def __init__(self):
        team = [s for s in ordinary_strategies if s().classifier['memory_depth']
                < float('inf')]
        super(MetaWinnerFiniteMemory, self).__init__(team=team)


class MetaMajorityLongMemory(MetaMajority):
    """MetaMajority with the team of Long (infinite) Memory Players"""

    name = "Meta Majority Long Memory"
    def __init__(self):
        team = [s for s in ordinary_strategies if s().classifier['memory_depth']
                == float('inf')]
        super(MetaMajorityLongMemory, self).__init__(team=team)


class MetaWinnerLongMemory(MetaWinner):
    """MetaWinner with the team of Long (infinite) Memory Players"""

    name = "Meta Winner Long Memory"
    def __init__(self):
        team = [s for s in ordinary_strategies if s().classifier['memory_depth']
                == float('inf')]
        super(MetaWinnerLongMemory, self).__init__(team=team)
