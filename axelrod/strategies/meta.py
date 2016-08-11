from axelrod import Actions, Player, obey_axelrod
from ._strategies import all_strategies
from .hunter import (
    DefectorHunter, AlternatorHunter, RandomHunter, MathConstantHunter,
    CycleHunter, EventualCycleHunter)
from .cooperator import Cooperator
from numpy.random import choice

# Needs to be computed manually to prevent circular dependency
ordinary_strategies = [s for s in all_strategies if obey_axelrod(s)]
C, D = Actions.C, Actions.D


class MetaPlayer(Player):
    """A generic player that has its own team of players."""

    name = "Meta Player"
    team = [Cooperator]
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': True,
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
        for key in ['stochastic',
                    'inspects_source',
                    'manipulates_source',
                    'manipulates_state']:
            self.classifier[key] = (any(t.classifier[key] for t in self.team))

        for t in self.team:
            self.classifier['makes_use_of'].update(t.classifier['makes_use_of'])

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
        self.init_args = (team,)
        self.classifier['memory_depth'] = float('inf')

    @staticmethod
    def meta_strategy(results, opponent):
        if results.count(D) > results.count(C):
            return D
        return C


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
        self.init_args = (team,)
        self.classifier['memory_depth'] = float('inf')

    @staticmethod
    def meta_strategy(results, opponent):
        if results.count(D) < results.count(C):
            return D
        return C


class MetaWinner(MetaPlayer):
    """A player who goes by the strategy of the current winner."""

    name = "Meta Winner"

    def __init__(self, team=None):
        # The default is to use all strategies available, but we need to import
        # the list at runtime, since _strategies import also _this_ module
        # before defining the list.
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
                game = self.match_attributes["game"]
                last_round = (player.proposed_history[-1], opponent.history[-1])
                s = game.scores[last_round][0]
                player.score += s
        return super(MetaWinner, self).strategy(opponent)

    def meta_strategy(self, results, opponent):
        scores = [pl.score for pl in self.team]
        bestscore = max(scores)
        beststrategies = [i for i, pl in enumerate(self.team) if pl.score == bestscore]
        bestproposals = [results[i] for i in beststrategies]
        bestresult = C if C in bestproposals else D

        # Update each player's proposed history with his proposed result, but
        # always after the new result has been settled based on scores
        # accumulated until now.
        for r, t in zip(results, self.team):
            t.proposed_history.append(r)

        if opponent.defections == 0:
            # Don't poke the bear
            return C

        return bestresult


class MetaHunter(MetaPlayer):
    """A player who uses a selection of hunters."""

    name = "Meta Hunter"
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self):
        # Notice that we don't include the cooperator hunter, because it leads
        # to excessive defection and therefore bad performance against
        # unforgiving strategies. We will stick to hunters that use defections
        # as cues. However, a really tangible benefit comes from combining
        # Random Hunter and Math Constant Hunter, since together they catch
        # strategies that are lightly randomized but still quite constant
        # (the tricky/suspicious ones).
        self.team = [DefectorHunter, AlternatorHunter, RandomHunter, MathConstantHunter, CycleHunter, EventualCycleHunter]

        super(MetaHunter, self).__init__()

    @staticmethod
    def meta_strategy(results, opponent):
        # If any of the hunters smells prey, then defect!
        if D in results:
            return D

        # Tit-for-tat might seem like a better default choice, but in many
        # cases it complicates the heuristics of hunting and creates
        # false-positives. So go ahead and use it, but only for longer
        # histories.
        if len(opponent.history) > 100:
            return D if opponent.history[-1:] == [D] else C
        else:
            return C


class MetaMajorityMemoryOne(MetaMajority):
    """MetaMajority with the team of Memory One players"""

    name = "Meta Majority Memory One"

    def __init__(self):
        team = [s for s in ordinary_strategies if s().classifier['memory_depth'] <= 1]
        super(MetaMajorityMemoryOne, self).__init__(team=team)
        self.init_args = ()


class MetaWinnerMemoryOne(MetaWinner):
    """MetaWinner with the team of Memory One players"""

    name = "Meta Winner Memory One"

    def __init__(self):
        team = [s for s in ordinary_strategies if s().classifier['memory_depth'] <= 1]
        super(MetaWinnerMemoryOne, self).__init__(team=team)
        self.init_args = ()


class MetaMajorityFiniteMemory(MetaMajority):
    """MetaMajority with the team of Finite Memory Players"""

    name = "Meta Majority Finite Memory"

    def __init__(self):
        team = [s for s in ordinary_strategies if s().classifier['memory_depth']
                < float('inf')]
        super(MetaMajorityFiniteMemory, self).__init__(team=team)
        self.init_args = ()


class MetaWinnerFiniteMemory(MetaWinner):
    """MetaWinner with the team of Finite Memory Players"""

    name = "Meta Winner Finite Memory"

    def __init__(self):
        team = [s for s in ordinary_strategies if s().classifier['memory_depth']
                < float('inf')]
        super(MetaWinnerFiniteMemory, self).__init__(team=team)
        self.init_args = ()


class MetaMajorityLongMemory(MetaMajority):
    """MetaMajority with the team of Long (infinite) Memory Players"""

    name = "Meta Majority Long Memory"

    def __init__(self):
        team = [s for s in ordinary_strategies if s().classifier['memory_depth']
                == float('inf')]
        super(MetaMajorityLongMemory, self).__init__(team=team)
        self.init_args = ()


class MetaWinnerLongMemory(MetaWinner):
    """MetaWinner with the team of Long (infinite) Memory Players"""

    name = "Meta Winner Long Memory"

    def __init__(self):
        team = [s for s in ordinary_strategies if s().classifier['memory_depth']
                == float('inf')]
        super(MetaWinnerLongMemory, self).__init__(team=team)
        self.init_args = ()


class MetaMixer(MetaPlayer):
    """A player who randomly switches between a team of players.
    If no distribution is passed then the player will uniformly choose between
    sub players.

    In essence this is creating a Mixed strategy.

    Parameters

    team : list of strategy classes, optional
        Team of strategies that are to be randomly played
        If none is passed will select the ordinary strategies.
    distribution : list representing a probability distribution, optional
        This gives the distribution from which to select the players.
        If none is passed will select uniformly.
    """

    name = "Meta Mixer"
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': True,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, team=None, distribution=None):
        # The default is to use all strategies available, but we need to import
        # the list at runtime, since _strategies import also _this_ module
        # before defining the list.
        if team:
            self.team = team
        else:
            # Needs to be computed manually to prevent circular dependency
            self.team = ordinary_strategies

        self.distribution = distribution

        super(MetaMixer, self).__init__()
        self.init_args = (team, distribution)

    def meta_strategy(self, results, opponent):
        """Using the numpy.random choice function to sample with weights"""
        return choice(results, p=self.distribution)
