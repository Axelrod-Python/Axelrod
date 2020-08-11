import numpy as np
from axelrod.action import Action
from axelrod.classifier import Classifiers
from axelrod.player import Player
from axelrod.strategies import TitForTat
from axelrod.strategy_transformers import NiceTransformer

from ._strategies import all_strategies
from .hunter import (
    AlternatorHunter,
    CooperatorHunter,
    CycleHunter,
    DefectorHunter,
    EventualCycleHunter,
    MathConstantHunter,
    RandomHunter,
)

# Needs to be computed manually to prevent circular dependency
ordinary_strategies = [
    s for s in all_strategies if Classifiers.obey_axelrod(s())
]

C, D = Action.C, Action.D


class MetaPlayer(Player):
    """
    A generic player that has its own team of players.

    Names:

    - Meta Player: Original name by Karol Langner
    """

    name = "Meta Player"
    classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "long_run_time": True,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self, team=None):
        # The default is to use all strategies available, but we need to import
        # the list at runtime, since _strategies import also _this_ module
        # before defining the list.
        if team:
            self.team = team
        else:
            self.team = ordinary_strategies
        # Make sure we don't use any meta players to avoid infinite recursion.
        self.team = [t for t in self.team if not issubclass(t, MetaPlayer)]
        # Initiate all the players in our team.
        self.team = [t() for t in self.team]
        self._last_results = None
        super().__init__()

    def _post_init(self):
        # The player's classification characteristics are derived from the team.
        # Note that memory_depth is not simply the max memory_depth of the team.
        for key in [
            "stochastic",
            "inspects_source",
            "manipulates_source",
            "manipulates_state",
        ]:
            self.classifier[key] = any(map(Classifiers[key], self.team))

        self.classifier["makes_use_of"] = set()
        for t in self.team:
            new_uses = Classifiers["makes_use_of"](t)
            if new_uses:
                self.classifier["makes_use_of"].update(new_uses)

    def set_seed(self, seed=None):
        super().set_seed(seed=seed)
        # Seed the team as well
        for t in self.team:
            t.set_seed(self._random.random_seed_int())

    def receive_match_attributes(self):
        for t in self.team:
            t.set_match_attributes(**self.match_attributes)

    def __repr__(self):
        team_size = len(self.team)
        return "{}: {} player{}".format(
            self.name, team_size, "s" if team_size > 1 else ""
        )

    def update_histories(self, coplay):
        # Update team histories.
        try:
            for player, play in zip(self.team, self._last_results):
                player.update_history(play, coplay)
        except TypeError:
            # If the Meta class is decorated by the Joss-Ann transformer,
            # such that the decorated class is now deterministic, the underlying
            # strategy isn't called. In that case, updating the history of all the
            # team members doesn't matter.
            # As a sanity check, look for at least one reclassifier, otherwise
            # this try-except clause could hide a bug.
            if len(self._reclassifiers) == 0:
                raise TypeError("MetaClass update_histories issue, expected a reclassifier.")
            # Otherwise just update with C always, so at least the histories have the
            # expected length.
            for player in self.team:
                player.update_history(C, coplay)

    def update_history(self, play, coplay):
        super().update_history(play, coplay)
        self.update_histories(coplay)

    def strategy(self, opponent):
        # Get the results of all our players.
        results = []
        for player in self.team:
            play = player.strategy(opponent)
            results.append(play)
        self._last_results = results
        # A subclass should just define a way to choose the result based on
        # team results.
        return self.meta_strategy(results, opponent)

    def meta_strategy(self, results, opponent):
        """Determine the meta result based on results of all players.
        Override this function in child classes."""
        return C


class MetaMajority(MetaPlayer):
    """A player who goes by the majority vote of all other non-meta players.

    Names:

    - Meta Majority: Original name by Karol Langner
    """

    name = "Meta Majority"

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
        self.scores = np.zeros(len(self.team))
        self.classifier["long_run_time"] = True

    def _update_scores(self, coplay):
        # Update the running score for each player, before determining the
        # next move.
        game = self.match_attributes["game"]
        scores = []
        for player in self.team:
            last_round = (player.history[-1], coplay)
            s = game.scores[last_round][0]
            scores.append(s)
        self.scores += np.array(scores)

    def update_histories(self, coplay):
        super().update_histories(coplay)
        self._update_scores(coplay)

    def meta_strategy(self, results, opponent):
        # Choose an action based on the collection of scores
        bestscore = max(self.scores)
        beststrategies = [
            i for (i, score) in enumerate(self.scores) if score == bestscore
        ]
        bestproposals = [results[i] for i in beststrategies]
        bestresult = C if C in bestproposals else D
        return bestresult


NiceMetaWinner = NiceTransformer()(MetaWinner)


class MetaWinnerEnsemble(MetaWinner):
    """A variant of MetaWinner that chooses one of the top scoring strategies
    at random against each opponent. Note this strategy is always stochastic
    regardless of the team, if team larger than 1, and the players are distinct.

    Names:

    - Meta Winner Ensemble: Original name by Marc Harper
    """

    name = "Meta Winner Ensemble"

    def _post_init(self):
        super()._post_init()
        team = list(t.__class__ for t in self.team)
        if len(team) > 1:
            self.classifier["stochastic"] = True
            self.singular = False
        else:
            self.singular = True
        # If the team has repeated identical members, then it reduces to a singular team
        # and it may not actually be stochastic.
        if team and len(set(team)) == 1:
            self.classifier["stochastic"] = Classifiers["stochastic"](self.team[0])
            self.singular = True

    def meta_strategy(self, results, opponent):
        # If the team consists of identical players, just take the first result.
        # This prevents an unnecessary call to _random below.
        if self.singular:
            return results[0]
        # Sort by score
        scores = [(score, i) for (i, score) in enumerate(self.scores)]
        # Choose one of the best scorers at random
        scores.sort(reverse=True)
        prop = max(1, int(len(scores) * 0.08))
        best_scorers = [i for (s, i) in scores[:prop]]
        index = self._random.choice(best_scorers)
        return results[index]


NiceMetaWinnerEnsemble = NiceTransformer()(MetaWinnerEnsemble)


class MetaHunter(MetaPlayer):
    """A player who uses a selection of hunters.

    Names

    - Meta Hunter: Original name by Karol Langner
    """

    name = "Meta Hunter"
    classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self):
        # Notice that we don't include the cooperator hunter, because it leads
        # to excessive defection and therefore bad performance against
        # unforgiving strategies. We will stick to hunters that use defections
        # as cues. However, a really tangible benefit comes from combining
        # Random Hunter and Math Constant Hunter, since together they catch
        # strategies that are lightly randomized but still quite constant
        # (the tricky/suspicious ones).
        team = [
            DefectorHunter,
            AlternatorHunter,
            RandomHunter,
            MathConstantHunter,
            CycleHunter,
            EventualCycleHunter,
        ]

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
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self, team=None):
        # This version uses CooperatorHunter
        if team is None:
            team = [
                DefectorHunter,
                AlternatorHunter,
                RandomHunter,
                MathConstantHunter,
                CycleHunter,
                EventualCycleHunter,
                CooperatorHunter,
            ]

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
        team = [
            s
            for s in ordinary_strategies
            if Classifiers["memory_depth"](s()) <= 1
        ]
        super().__init__(team=team)
        self.classifier["long_run_time"] = False


class MetaMajorityFiniteMemory(MetaMajority):
    """MetaMajority with the team of Finite Memory Players

    Names

    - Meta Majority Finite Memory: Original name by Marc Harper
    """

    name = "Meta Majority Finite Memory"

    def __init__(self):
        team = [
            s
            for s in ordinary_strategies
            if Classifiers["memory_depth"](s()) < float("inf")
        ]
        super().__init__(team=team)


class MetaMajorityLongMemory(MetaMajority):
    """MetaMajority with the team of Long (infinite) Memory Players

    Names

    - Meta Majority Long Memory: Original name by Marc Harper
    """

    name = "Meta Majority Long Memory"

    def __init__(self):
        team = [
            s
            for s in ordinary_strategies
            if Classifiers["memory_depth"](s()) == float("inf")
        ]
        super().__init__(team=team)


class MetaWinnerMemoryOne(MetaWinner):
    """MetaWinner with the team of Memory One players

    Names

    - Meta Winner Memory Memory One: Original name by Marc Harper
    """

    name = "Meta Winner Memory One"

    def __init__(self):
        team = [
            s
            for s in ordinary_strategies
            if Classifiers["memory_depth"](s()) <= 1
        ]
        super().__init__(team=team)
        self.classifier["long_run_time"] = False


class MetaWinnerFiniteMemory(MetaWinner):
    """MetaWinner with the team of Finite Memory Players

    Names

    - Meta Winner Finite Memory: Original name by Marc Harper
    """

    name = "Meta Winner Finite Memory"

    def __init__(self):
        team = [
            s
            for s in ordinary_strategies
            if Classifiers["memory_depth"](s()) < float("inf")
        ]
        super().__init__(team=team)


class MetaWinnerLongMemory(MetaWinner):
    """MetaWinner with the team of Long (infinite) Memory Players

    Names

    - Meta Winner Long Memory: Original name by Marc Harper
    """

    name = "Meta Winner Long Memory"

    def __init__(self):
        team = [
            s
            for s in ordinary_strategies
            if Classifiers["memory_depth"](s()) == float("inf")
        ]
        super().__init__(team=team)


class MetaWinnerDeterministic(MetaWinner):
    """Meta Winner with the team of Deterministic Players.

    Names

    - Meta Winner Deterministic: Original name by Marc Harper
    """

    name = "Meta Winner Deterministic"

    def __init__(self):
        team = [
            s for s in ordinary_strategies if not Classifiers["stochastic"](s())
        ]
        super().__init__(team=team)
        self.classifier["stochastic"] = False


class MetaWinnerStochastic(MetaWinner):
    """Meta Winner with the team of Stochastic Players.

    Names

    - Meta Winner Stochastic: Original name by Marc Harper
    """

    name = "Meta Winner Stochastic"

    def __init__(self):
        team = [
            s for s in ordinary_strategies if Classifiers["stochastic"](s())
        ]
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
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "long_run_time": True,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self, team=None, distribution=None):
        super().__init__(team=team)
        # Check that distribution is not all zeros, which will make numpy unhappy.
        if distribution and all(x == 0 for x in distribution):
            distribution = None
        self.distribution = distribution

    def _post_init(self):
        distribution = self.distribution
        if distribution and len(set(distribution)) > 1:
            self.classifier["stochastic"] = True
        if len(self.team) == 1:
            self.classifier["stochastic"] = Classifiers["stochastic"](self.team[0])
            # Overwrite strategy to avoid use of _random. This will ignore self.meta_strategy.
            self.index = 0
            self.strategy = self.index_strategy
            return
        # Check if the distribution has only one non-zero value. If so, the strategy may be
        # deterministic, and we can avoid _random.
        if distribution:
            total = sum(distribution)
            distribution = np.array(distribution) / total
            if 1 in distribution:
                self.index = list(distribution).index(1)
                # It's potentially deterministic.
                self.classifier["stochastic"] = Classifiers["stochastic"](self.team[self.index])
                # Overwrite strategy to avoid use of _random. This will ignore self.meta_strategy.
                self.strategy = self.index_strategy

    def index_strategy(self, opponent):
        """When the team effectively has a single player, only use that strategy."""
        results = [C] * len(self.team)
        player = self.team[self.index]
        action = player.strategy(opponent)
        results[self.index] = action
        self._last_results = results
        return action

    def meta_strategy(self, results, opponent):
        """Using the _random.choice function to sample with weights."""
        return self._random.choice(results, p=self.distribution)


class NMWEDeterministic(NiceMetaWinnerEnsemble):
    """Nice Meta Winner Ensemble with the team of Deterministic Players.

    Names

    - Nice Meta Winner Ensemble Deterministic: Original name by Marc Harper
    """

    name = "NMWE Deterministic"

    def __init__(self):
        team = [
            s for s in ordinary_strategies if not Classifiers["stochastic"](s())
        ]
        super().__init__(team=team)
        self.classifier["stochastic"] = True


class NMWEStochastic(NiceMetaWinnerEnsemble):
    """Nice Meta Winner Ensemble with the team of Stochastic Players.

    Names

    - Nice Meta Winner Ensemble Stochastic: Original name by Marc Harper
    """

    name = "NMWE Stochastic"

    def __init__(self):
        team = [
            s for s in ordinary_strategies if Classifiers["stochastic"](s())
        ]
        super().__init__(team=team)


class NMWEFiniteMemory(NiceMetaWinnerEnsemble):
    """Nice Meta Winner Ensemble with the team of Finite Memory Players.

    Names

    - Nice Meta Winner Ensemble Finite Memory: Original name by Marc Harper
    """

    name = "NMWE Finite Memory"

    def __init__(self):
        team = [
            s
            for s in ordinary_strategies
            if Classifiers["memory_depth"](s()) < float("inf")
        ]
        super().__init__(team=team)


class NMWELongMemory(NiceMetaWinnerEnsemble):
    """Nice Meta Winner Ensemble with the team of Long Memory Players.

    Names

    - Nice Meta Winner Ensemble Long Memory: Original name by Marc Harper
    """

    name = "NMWE Long Memory"

    def __init__(self):
        team = [
            s
            for s in ordinary_strategies
            if Classifiers["memory_depth"](s()) == float("inf")
        ]
        super().__init__(team=team)


class NMWEMemoryOne(NiceMetaWinnerEnsemble):
    """Nice Meta Winner Ensemble with the team of Memory One Players.

    Names

    - Nice Meta Winner Ensemble Memory One: Original name by Marc Harper
    """

    name = "NMWE Memory One"

    def __init__(self):
        team = [
            s
            for s in ordinary_strategies
            if Classifiers["memory_depth"](s()) <= 1
        ]
        super().__init__(team=team)
        self.classifier["long_run_time"] = False


class MemoryDecay(MetaPlayer):
    """
    A player utilizes the (default) Tit for Tat strategy for the first (default) 15 turns,
    at the same time memorizing the opponent's decisions. After the 15 turns have
    passed, the player calculates a 'net cooperation score' (NCS) for their opponent,
    weighing decisions to Cooperate as (default) 1, and to Defect as (default)
    -2. If the opponent's NCS is below 0, the player defects; otherwise,
    they cooperate.

    The player's memories of the opponent's decisions have a random chance to be
    altered (i.e., a C decision becomes D or vice versa; default probability
    is 0.03) or deleted (default probability is 0.1).

    It is possible to pass a different axelrod player class to change the initial
    player behavior.

    Name: Memory Decay
    """

    name = "Memory Decay"
    classifier = {
        "memory_depth": float("inf"),
        "long_run_time": False,
        "stochastic": True,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(
        self,
        p_memory_delete: float = 0.1,
        p_memory_alter: float = 0.03,
        loss_value: float = -2,
        gain_value: float = 1,
        memory: list = None,
        start_strategy: Player = TitForTat,
        start_strategy_duration: int = 15,
    ):
        super().__init__(team=[start_strategy])
        self.p_memory_delete = p_memory_delete
        self.p_memory_alter = p_memory_alter
        self.loss_value = loss_value
        self.gain_value = gain_value
        self.memory = [] if not memory else memory
        self.start_strategy_duration = start_strategy_duration
        self.gloss_values = None

    def _post_init(self):
        super()._post_init()
        # This strategy is stochastic even if none of the team is.  The
        # MetaPlayer initializer will set stochastic to be False in that case.
        self.classifier["stochastic"] = True

    def __repr__(self):
        return Player.__repr__(self)

    def gain_loss_translate(self):
        """
        Translates the actions (D and C) to numeric values (loss_value and
        gain_value).
        """
        values = {C: self.gain_value, D: self.loss_value}
        self.gloss_values = [values[action] for action in self.memory]

    def memory_alter(self):
        """
        Alters memory entry, i.e. puts C if there's a D and vice versa.
        """
        alter = self._random.choice(range(0, len(self.memory)))
        self.memory[alter] = self.memory[alter].flip()

    def memory_delete(self):
        """
        Deletes memory entry.
        """
        self.memory.pop(self._random.choice(range(0, len(self.memory))))

    def meta_strategy(self, results, opponent):
        try:
            self.memory.append(opponent.history[-1])
        except IndexError:
            pass
        if len(self.history) < self.start_strategy_duration:
            return results[0]
        else:
            if self._random.random() <= self.p_memory_alter:
                self.memory_alter()
            if self._random.random() <= self.p_memory_delete:
                self.memory_delete()
            self.gain_loss_translate()
            if sum(self.gloss_values) < 0:
                return D
            else:
                return C
