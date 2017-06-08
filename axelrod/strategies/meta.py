from numpy.random import choice

from axelrod.actions import Actions
from axelrod.player import Player, obey_axelrod
from axelrod.strategy_transformers import NiceTransformer
from ._strategies import all_strategies
from .hunter import (
    AlternatorHunter, CooperatorHunter, CycleHunter, DefectorHunter,
    EventualCycleHunter, MathConstantHunter, RandomHunter,)


# Needs to be computed manually to prevent circular dependency
ordinary_strategies = [s for s in all_strategies if obey_axelrod(s)]
C, D = Actions.C, Actions.D


class MetaPlayer(Player):
    """
    A generic player that has its own team of players.

    Names:

    - Meta Player: Original name by Karol Langner
    """

    name = "Meta Player"
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'makes_use_of': {'game', 'length'},
        'long_run_time': True,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, team=None):
        super().__init__()
        # The default is to use all strategies available, but we need to import
        # the list at runtime, since _strategies import also _this_ module
        # before defining the list.
        if team:
            self.team = team
        else:
            # Needs to be computed manually to prevent circular dependency
            self.team = ordinary_strategies

        # Make sure we don't use any meta players to avoid infinite recursion.
        self.team = [t for t in self.team if not issubclass(t, MetaPlayer)]
        self.nteam = len(self.team)

        # Initiate all the player in out team.
        self.team = [t() for t in self.team]

        # This player inherits the classifiers of its team.
        # Note that memory_depth is not simply the max memory_depth of the team.
        for key in ['stochastic',
                    'inspects_source',
                    'manipulates_source',
                    'manipulates_state']:
            self.classifier[key] = any(t.classifier[key] for t in self.team)

        for t in self.team:
            self.classifier['makes_use_of'].update(t.classifier['makes_use_of'])

    def __repr__(self):
        team_size = len(self.team)
        return '{}: {} player{}'.format(self.name, team_size, 's' if team_size > 1 else '')

    def strategy(self, opponent):
        # Get the results of all our players.
        results = []
        for player in self.team:
            play = player.strategy(opponent)
            player.history.append(play)
            results.append(play)

        # A subclass should just define a way to choose the result based on
        # team results.
        return self.meta_strategy(results, opponent)

    def meta_strategy(self, results, opponent):
        """Determine the meta result based on results of all players.
        Override this function in child classes."""
        return 'C'

    def reset(self):
        super().reset()
        # Reset each player as well
        for player in self.team:
            player.reset()


class MetaMajority(MetaPlayer):
    """A player who goes by the majority vote of all other non-meta players.

    Names:

    - Meta Marjority: Original name by Karol Langner
    """

    name = "Meta Majority"

    def __init__(self, team=None):
        super().__init__(team=team)

    @staticmethod
    def meta_strategy(results, opponent):
        if results.count(D) > results.count(C):
            return D
        return C


class MetaMinority(MetaPlayer):
    """A player who goes by the minority vote of all other non-meta players.

    Names:

    - Meta Minority: Original name by Karol Langner
    """

    name = "Meta Minority"

    def __init__(self, team=None):
        super().__init__(team=team)

    @staticmethod
    def meta_strategy(results, opponent):
        if results.count(D) < results.count(C):
            return D
        return C


class MetaWinner(MetaPlayer):
    """A player who goes by the strategy of the current winner.

    Names:

    - Meta Winner: Original name by Karol Langner
    """

    name = "Meta Winner"

    def __init__(self, team=None):
        super().__init__(team=team)
        # For each player, we will keep the history of proposed moves and
        # a running score since the beginning of the game.
        self.scores = [0] * len(self.team)
        self.classifier['long_run_time'] = True

    def _update_scores(self, opponent):
        # Update the running score for each player, before determining the
        # next move.
        game = self.match_attributes["game"]
        if len(self.history):
            for i, player in enumerate(self.team):
                last_round = (player.history[-1], opponent.history[-1])
                s = game.scores[last_round][0]
                self.scores[i] += s

    def meta_strategy(self, results, opponent):
        self._update_scores(opponent)
        # Choice an action based on the collection of scores
        bestscore = max(self.scores)
        beststrategies = [i for (i, score) in enumerate(self.scores)
                          if score == bestscore]
        bestproposals = [results[i] for i in beststrategies]
        bestresult = C if C in bestproposals else D
        return bestresult

    def reset(self):
        super().reset()
        self.scores = [0] * len(self.team)


NiceMetaWinner = NiceTransformer()(MetaWinner)


class MetaWinnerEnsemble(MetaWinner):
    """A variant of MetaWinner that chooses one of the top scoring strategies
    at random against each opponent. Note this strategy is always stochastic
    regardless of the team.

    Names:

    - Meta Winner Ensemble: Original name by Marc Harper
    """

    name = "Meta Winner Ensemble"

    def meta_strategy(self, results, opponent):
        self._update_scores(opponent)
        # Sort by score
        scores = [(score, i) for (i, score) in enumerate(self.scores)]
        # Choose one of the best scorers at random
        scores.sort(reverse=True)
        prop = max(1, int(len(scores) * 0.08))
        index = choice([i for (s, i) in scores[:prop]])
        return results[index]


NiceMetaWinnerEnsemble = NiceTransformer()(MetaWinnerEnsemble)


class MetaHunter(MetaPlayer):
    """A player who uses a selection of hunters.

    Names

    - Meta Hunter: Original name by Karol Langner
    """

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
        team = [DefectorHunter, AlternatorHunter, RandomHunter,
                MathConstantHunter, CycleHunter, EventualCycleHunter]

        super().__init__(team=team)

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


class MetaHunterAggressive(MetaPlayer):
    """A player who uses a selection of hunters.

    Names

    - Meta Hunter Aggressive: Original name by Marc Harper
    """

    name = "Meta Hunter Aggressive"
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, team=None):
        # This version uses CooperatorHunter
        if team is None:
            team = [DefectorHunter, AlternatorHunter, RandomHunter,
                    MathConstantHunter, CycleHunter, EventualCycleHunter,
                    CooperatorHunter]

        super().__init__(team=team)

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
    """MetaMajority with the team of Memory One players

    Names

    - Meta Majority Memory One: Original name by Marc Harper
    """

    name = "Meta Majority Memory One"

    def __init__(self):
        team = [s for s in ordinary_strategies if s().classifier['memory_depth'] <= 1]
        super().__init__(team=team)
        self.classifier["long_run_time"] = False


class MetaMajorityFiniteMemory(MetaMajority):
    """MetaMajority with the team of Finite Memory Players

    Names

    - Meta Majority Finite Memory: Original name by Marc Harper
    """

    name = "Meta Majority Finite Memory"

    def __init__(self):
        team = [s for s in ordinary_strategies if s().classifier['memory_depth']
                < float('inf')]
        super().__init__(team=team)


class MetaMajorityLongMemory(MetaMajority):
    """MetaMajority with the team of Long (infinite) Memory Players

    Names

    - Meta Majority Long Memory: Original name by Marc Harper
    """

    name = "Meta Majority Long Memory"

    def __init__(self):
        team = [s for s in ordinary_strategies if s().classifier['memory_depth']
                == float('inf')]
        super().__init__(team=team)


class MetaWinnerMemoryOne(MetaWinner):
    """MetaWinner with the team of Memory One players

    Names

    - Meta Winner Memory Memory One: Original name by Marc Harper
    """

    name = "Meta Winner Memory One"

    def __init__(self):
        team = [s for s in ordinary_strategies if s().classifier['memory_depth'] <= 1]
        super().__init__(team=team)
        self.classifier["long_run_time"] = False


class MetaWinnerFiniteMemory(MetaWinner):
    """MetaWinner with the team of Finite Memory Players

    Names

    - Meta Winner Finite Memory: Original name by Marc Harper
    """

    name = "Meta Winner Finite Memory"

    def __init__(self):
        team = [s for s in ordinary_strategies if s().classifier['memory_depth']
                < float('inf')]
        super().__init__(team=team)


class MetaWinnerLongMemory(MetaWinner):
    """MetaWinner with the team of Long (infinite) Memory Players

    Names

    - Meta Winner Long Memory: Original name by Marc Harper
    """
    name = "Meta Winner Long Memory"

    def __init__(self):
        team = [s for s in ordinary_strategies if s().classifier['memory_depth']
                == float('inf')]
        super().__init__(team=team)


class MetaWinnerDeterministic(MetaWinner):
    """Meta Winner with the team of Deterministic Players.

    Names

    - Meta Winner Deterministic: Original name by Marc Harper
    """

    name = "Meta Winner Deterministic"

    def __init__(self):
        team = [s for s in ordinary_strategies if
                not s().classifier['stochastic']]
        super().__init__(team=team)
        self.classifier['stochastic'] = False


class MetaWinnerStochastic(MetaWinner):
    """Meta Winner with the team of Stochastic Players.

    Names

    - Meta Winner Stochastic: Original name by Marc Harper
    """

    name = "Meta Winner Stochastic"

    def __init__(self):
        team = [s for s in ordinary_strategies if
                s().classifier['stochastic']]
        super().__init__(team=team)


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

    Names

    - Meta Mixer: Original name by Vince Knight
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
        self.distribution = distribution
        super().__init__(team=team)

    def meta_strategy(self, results, opponent):
        """Using the numpy.random choice function to sample with weights"""
        return choice(results, p=self.distribution)


class NMWEDeterministic(NiceMetaWinnerEnsemble):
    """Nice Meta Winner Ensemble with the team of Deterministic Players.

    Names

    - Nice Meta Winner Ensemble Deterministic: Original name by Marc Harper
    """

    name = "NMWE Deterministic"

    def __init__(self):
        team = [s for s in ordinary_strategies if
                not s().classifier['stochastic']]
        super().__init__(team=team)
        self.classifier["stochastic"] = True


class NMWEStochastic(NiceMetaWinnerEnsemble):
    """Nice Meta Winner Ensemble with the team of Stochastic Players.

    Names

    - Nice Meta Winner Ensemble Stochastic: Original name by Marc Harper
    """

    name = "NMWE Stochastic"

    def __init__(self):
        team = [s for s in ordinary_strategies if
                s().classifier['stochastic']]
        super().__init__(team=team)


class NMWEFiniteMemory(NiceMetaWinnerEnsemble):
    """Nice Meta Winner Ensemble with the team of Finite Memory Players.

    Names

    - Nice Meta Winner Ensemble Finite Memory: Original name by Marc Harper
    """

    name = "NMWE Finite Memory"

    def __init__(self):
        team = [s for s in ordinary_strategies if s().classifier['memory_depth']
                < float('inf')]
        super().__init__(team=team)


class NMWELongMemory(NiceMetaWinnerEnsemble):
    """Nice Meta Winner Ensemble with the team of Long Memory Players.

    Names

    - Nice Meta Winner Ensemble Long Memory: Original name by Marc Harper
    """

    name = "NMWE Long Memory"

    def __init__(self):
        team = [s for s in ordinary_strategies if s().classifier['memory_depth']
                == float('inf')]
        super().__init__(team=team)


class NMWEMemoryOne(NiceMetaWinnerEnsemble):
    """Nice Meta Winner Ensemble with the team of Memory One Players.

    Names

    - Nice Meta Winner Ensemble Memory One: Original name by Marc Harper
    """

    name = "NMWE Memory One"

    def __init__(self):
        team = [s for s in ordinary_strategies if s().classifier['memory_depth']
                <= 1]
        super().__init__(team=team)
        self.classifier["long_run_time"] = False
