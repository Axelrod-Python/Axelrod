from collections import Counter
import random

import numpy as np

from .deterministic_cache import DeterministicCache
from .match import Match
from .random_ import randrange


def fitness_proportionate_selection(scores):
    """Randomly selects an individual proportionally to score.

    Parameters
    ----------
    scores: Any sequence of real numbers

    Returns
    -------
    An index of the above list selected at random proportionally to the list
    element divided by the total.
    """
    csums = np.cumsum(scores)
    total = csums[-1]
    r = random.random() * total

    for i, x in enumerate(csums):
        if x >= r:
            return i


class MoranProcess(object):
    def __init__(self, players, turns=100, noise=0, deterministic_cache=None,
                 mutation_rate=0., mode='bd', match_class=Match):
        """
        An agent based Moran process class. In each round, each player plays a
        Match with each other player. Players are assigned a fitness score by
        their total score from all matches in the round. A player is chosen to
        reproduce proportionally to fitness, possibly mutated, and is cloned.
        The clone replaces a randomly chosen player.

        If the mutation_rate is 0, the population will eventually fixate on
        exactly one player type. In this case a StopIteration exception is
        raised and the play stops. If the mutation_rate is not zero, then the
        process will iterate indefinitely, so mp.play() will never exit, and
        you should use the class as an iterator instead.

        When a player mutates it chooses a random player type from the initial
        population. This is not the only method yet emulates the common method
        in the literature.

        Parameters
        ----------
        players, iterable of axelrod.Player subclasses
        turns: int, 100
            The number of turns in each pairwise interaction
        noise: float, 0
            The background noise, if any. Randomly flips plays with probability
            `noise`.
        deterministic_cache: axelrod.DeterministicCache, None
            A optional prebuilt deterministic cache
        mutation_rate: float, 0
            The rate of mutation. Replicating players are mutated with
            probability `mutation_rate`
        mode: string, bd
            Birth-Death (bd) or Death-Birth (db)
        match_class: subclass of Match
            The match type to use for scoring
        """
        self.match_class = match_class
        self.turns = turns
        self.noise = noise
        self.initial_players = players  # save initial population
        self.players = []
        self.populations = []
        self.set_players()
        self.score_history = []
        self.winning_strategy_name = None
        self.mutation_rate = mutation_rate
        assert (mutation_rate >= 0) and (mutation_rate <= 1)
        assert (noise >= 0) and (noise <= 1)
        mode = mode.lower()
        assert mode in ['bd', 'db']
        self.mode = mode
        if deterministic_cache is not None:
            self.deterministic_cache = deterministic_cache
        else:
            self.deterministic_cache = DeterministicCache()
        # Build the set of mutation targets
        # Determine the number of unique types (players)
        keys = set([str(p) for p in players])
        # Create a dictionary mapping each type to a set of representatives
        # of the other types
        d = dict()
        for p in players:
            d[str(p)] = p
        mutation_targets = dict()
        for key in sorted(keys):
            mutation_targets[key] = [v for (k, v) in sorted(d.items()) if k != key]
        self.mutation_targets = mutation_targets

    def set_players(self):
        """Copy the initial players into the first population."""
        self.players = []
        for player in self.initial_players:
            player.reset()
            self.players.append(player)
        self.populations = [self.population_distribution()]

    def mutate(self, index):
        """Mutate the player at index."""
        # Choose another strategy at random from the initial population
        r = random.random()
        if r < self.mutation_rate:
            s = str(self.players[index])
            j = randrange(0, len(self.mutation_targets[s]))
            p = self.mutation_targets[s][j]
            new_player = p.clone()
        else:
            # Just clone the player
            new_player = self.players[index].clone()
        return new_player

    def death(self, index=None):
        """Selects the player to be removed. Note that the in the birth-death
        case, the player that is reproducing may also be replaced. However in
        the death-birth case, this player will be excluded from the choices.

        `index` is unused here but is needed in the graph case.
        """
        i = randrange(0, len(self.players))
        return i

    def birth(self, index=None):
        """The birth event."""
        # Compute necessary fitnesses.
        scores = self.score_all()
        if self.mode == "db":
            # Death has already occurred, so remove the dead player from the
            # possible choices
            scores.pop(index)
            # Make sure to get the correct index post-pop
            j = fitness_proportionate_selection(scores)
            if j >= index:
                j += 1
        else:
            j = fitness_proportionate_selection(scores)
        return j

    def fixation_check(self):
        """Is the population of a single type?"""
        if self.mutation_rate > 0:
            return False
        classes = set(str(p) for p in self.players)
        if len(classes) == 1:
            # Set the winning strategy name variable
            self.winning_strategy_name = str(self.players[0])
            return True
        return False

    def __next__(self):
        """Iterate the population:
        - play the round's matches
        - chooses a player proportionally to fitness (total score) to reproduce
        - mutate, if appropriate
        - choose a player to be replaced
        - update the population
        """
        # Check the exit condition, that all players are of the same type.
        if self.fixation_check():
            raise StopIteration
        if self.mode == "bd":
            # Birth then death
            j = self.birth()
            i = self.death(j)
        elif self.mode == "db":
            # Death then birth
            i = self.death()
            self.players[i] = None
            j = self.birth(i)
        # Mutate
        if self.mutation_rate:
            new_player = self.mutate(j)
        else:
            new_player = self.players[j].clone()
        # Replace player i with clone of player j
        self.players[i] = new_player
        self.populations.append(self.population_distribution())
        # Check again for fixation
        self.fixation_check()
        return self

    def _matchup_indices(self):
        """Generate the matchup pairs."""
        indices = []
        N = len(self.players)
        for i in range(N):
            for j in range(i + 1, N):
                # For the death-birth mode the dead player is marked None
                # so skip those
                if (self.players[i] is None) or (self.players[j] is None):
                    continue
                indices.append((i, j))
        return indices

    def score_all(self):
        """Plays the next round of the process. Every player is paired up
        against every other player and the total scores are recorded."""
        N = len(self.players)
        scores = [0] * N
        for i, j in self._matchup_indices():
            player1 = self.players[i]
            player2 = self.players[j]
            match = self.match_class(
                (player1, player2), turns=self.turns, noise=self.noise,
                deterministic_cache=self.deterministic_cache)
            match.play()
            match_scores = match.final_score_per_turn()
            scores[i] += match_scores[0]
            scores[j] += match_scores[1]
        self.score_history.append(scores)
        return scores

    def population_distribution(self):
        """Returns the population distribution of the last iteration."""
        player_names = [str(player) for player in self.players]
        counter = Counter(player_names)
        return counter

    def __iter__(self):
        return self

    def reset(self):
        """Reset the process to replay."""
        self.winning_strategy_name = None
        self.score_history = []
        # Reset all the players
        self.set_players()

    def play(self):
        """Play the process out to completion."""
        if self.mutation_rate != 0:
            raise ValueError("MoranProcess.play() will never exit if mutation_rate is nonzero")
        while True:
            try:
                self.__next__()
            except StopIteration:
                break
        return self.populations

    def __len__(self):
        return len(self.populations)


class MoranProcessGraph(MoranProcess):
    def __init__(self, players, interaction_graph, reproduction_graph=None,
                 turns=100, noise=0, deterministic_cache=None,
                 mutation_rate=0., mode='bd', match_class=Match):
        """
        An agent based Moran process class. In each round, each player plays a
        Match with each neighboring player according to the interaction graph.
        Players are assigned a fitness score by their total score from all
        matches in the round. A player is chosen to reproduce proportionally to
        fitness, possibly mutated, and is cloned. The clone replaces a randomly
        chosen neighboring player according to the reproduction graph.

        If the mutation_rate is 0, the population will eventually fixate on
        exactly one player type. In this case a StopIteration exception is
        raised and the play stops. If mutation_rate is not zero, then the
        process will iterate indefinitely, so mp.play() will never exit, and
        you should use the class as an iterator instead.

        When a player mutates it chooses a random player type from the initial
        population. This is not the only method yet emulates the common method
        in the literature.

        Note: the weighted graph case is not yet implemented, nor is birth-bias,
        death-bias, or Link Dynamics updating; however the most common use cases
        are implemented.

        See [Shakarian2013]_ for more detail on the process and different
        updating modes.

        Parameters
        ----------
        players, iterable of axelrod.Player subclasses
        interaction_graph: Axelrod.graph.Graph
            The graph in which the replicators are arranged
        reproduction_graph: Axelrod.graph.Graph
            The reproduction graph, set equal to the interaction graph if not
            given
        turns: int, 100
            The number of turns in each pairwise interaction
        noise: float, 0
            The background noise, if any. Randomly flips plays with probability
            `noise`.
        deterministic_cache: axelrod.DeterministicCache, None
            A optional prebuilt deterministic cache
        mutation_rate: float, 0
            The rate of mutation. Replicating players are mutated with
            probability `mutation_rate`
        mode: string, bd
            Birth-Death (bd) or Death-Birth (db)
        match_class: subclass of Match
            The match type to use for scoring
        """
        super().__init__(players, turns=turns, noise=noise,
                              deterministic_cache=deterministic_cache,
                              mutation_rate=mutation_rate, mode=mode)
        if not reproduction_graph:
            reproduction_graph = interaction_graph
        # Check equal vertices
        v1 = interaction_graph.vertices()
        v2 = reproduction_graph.vertices()
        assert list(v1) == list(v2)
        self.interaction_graph = interaction_graph
        self.reproduction_graph = reproduction_graph
        # Map players to graph vertices
        self.locations = list(interaction_graph.vertices())
        self.index = dict(zip(interaction_graph.vertices(),
                              range(len(players))))

    def birth(self, index=None):
        """Compute the birth index."""
        scores = self.score_all()
        if index:
            # Death-birth case
            scores.pop(index)
            # Make sure to get the correct index post-pop
            j = fitness_proportionate_selection(scores)
            if j >= index:
                j += 1
        else:
            j = fitness_proportionate_selection(scores)
        return j

    def death(self, index=None):
        """Selects the player to be removed."""
        if self.mode == "db":
            # Select a player to be replaced globally
            i = randrange(0, len(self.players))
            # Record internally for use in _matchup_indices
            self.dead = i
        else:
            # Select locally
            # index is not None in this case
            vertex = random.choice(
                self.reproduction_graph.out_vertices(self.locations[index]))
            i = self.index[vertex]
        return i

    def _matchup_indices(self):
        """Generate the matchup pairs"""
        indices = set()
        # For death-birth we only want the neighbors of the dead node
        # The other calculations are unnecessary
        if self.mode == "db":
            source = self.index[self.dead]
            self.dead = None
            sources = self.interaction_graph.out_vertices(source)
        else:
            # birth-death is global
            sources = self.locations
        for i, source in enumerate(sources):
            for target in self.interaction_graph.out_vertices(source):
                j = self.index[target]
                if (self.players[i] is None) or (self.players[j] is None):
                    continue
                # Don't duplicate matches
                if ((i, j) in indices) or ((j, i) in indices):
                    continue
                indices.add((i, j))
        return indices

    def population_distribution(self):
        """Returns the population distribution of the last iteration."""
        player_names = [str(player) for player in self.players]
        counter = Counter(player_names)
        return counter


class ApproximateMoranProcess(MoranProcess):
    """
    A class to approximate a Moran process based
    on a distribution of potential Match outcomes.

    Instead of playing the matches, the result is sampled
    from a dictionary of player tuples to distribution of match outcomes
    """
    def __init__(self, players, cached_outcomes, mutation_rate=0.):
        """
        Parameters
        ----------
        players: iterable of axelrod.Player subclasses
        cached_outcomes: dictionary
            Mapping tuples of players to instances of the moran.Pdf class.
        mutation_rate: float, 0
            The rate of mutation. Replicating players are mutated with
            probability `mutation_rate`
        """
        super(ApproximateMoranProcess, self).__init__(
            players, turns=0, noise=0, deterministic_cache=None,
            mutation_rate=mutation_rate)
        self.cached_outcomes = cached_outcomes

    def score_all(self):
        """
        Plays the next round of the process. Every player is paired up
        against every other player and the total scores are obtained from the
        cached_outcomes.
        """
        N = len(self.players)
        scores = [0] * N
        for i in range(N):
            for j in range(i + 1, N):
                player_names = tuple([str(self.players[i]), str(self.players[j])])

                cached_score = self._get_scores_from_cache(player_names)
                scores[i] += cached_score[0]
                scores[j] += cached_score[1]
        self.score_history.append(scores)
        return scores

    def _get_scores_from_cache(self, player_names):
        try:
            match_scores = self.cached_outcomes[player_names].sample()
            return match_scores
        except KeyError:  # If players are stored in opposite order
            match_scores = self.cached_outcomes[player_names[::-1]].sample()
            return match_scores[::-1]
