"""Memory One strategies. Note that there are Memory One strategies in other
files, including titfortat.py and zero_determinant.py"""

import warnings

from axelrod.action import Action
from axelrod.player import Player
from axelrod.random_ import random_choice

from typing import Tuple


C, D = Action.C, Action.D


class MemoryOnePlayer(Player):
    """
    Uses a four-vector for strategies based on the last round of play,
    (P(C|CC), P(C|CD), P(C|DC), P(C|DD)). Win-Stay Lose-Shift is set as
    the default player if four_vector is not given.
    Intended to be used as an abstract base class or to at least be supplied
    with a initializing four_vector.

    Names

    - Memory One: [Nowak1990]_
    """

    name = 'Generic Memory One Player'
    classifier = {
        'memory_depth': 1,  # Memory-one Four-Vector
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, four_vector: Tuple[float, float, float, float] = None,
                 initial: Action = C) -> None:
        """
        Parameters
        ----------

        fourvector: list or tuple of floats of length 4
            The response probabilities to the preceding round of play
            ( P(C|CC), P(C|CD), P(C|DC), P(C|DD) )
        initial: C or D
            The initial move

        Special Cases
        -------------

        Alternator is equivalent to MemoryOnePlayer((0, 0, 1, 1), C)
        Cooperator is equivalent to MemoryOnePlayer((1, 1, 1, 1), C)
        Defector   is equivalent to MemoryOnePlayer((0, 0, 0, 0), C)
        Random     is equivalent to MemoryOnePlayer((0.5, 0.5, 0.5, 0.5))
        (with a random choice for the initial state)
        TitForTat  is equivalent to MemoryOnePlayer((1, 0, 1, 0), C)
        WinStayLoseShift is equivalent to MemoryOnePlayer((1, 0, 0, 1), C)

        See also: The remaining strategies in this file
                  Multiple strategies in titfortat.py
                  Grofman, Joss in axelrod_tournaments.py
        """
        super().__init__()
        self._initial = initial
        self.set_initial_four_vector(four_vector)

    def set_initial_four_vector(self, four_vector):
        if four_vector is None:
            four_vector = (1, 0, 0, 1)
            warnings.warn("Memory one player is set to default (1, 0, 0, 1).")

        self.set_four_vector(four_vector)
        if self.name == 'Generic Memory One Player':
            self.name = "%s: %s" % (self.name, four_vector)

    def set_four_vector(self, four_vector: Tuple[float, float, float, float]):
        if not all(0 <= p <= 1 for p in four_vector):
            raise ValueError("An element in the probability vector, {}, is not "
                             "between 0 and 1.".format(str(four_vector)))

        self._four_vector = dict(zip([(C, C), (C, D), (D, C), (D, D)], four_vector))
        self.classifier['stochastic'] = any(0 < x < 1 for x in set(four_vector))

    def strategy(self, opponent: Player) -> Action:
        if len(opponent.history) == 0:
            return self._initial
        # Determine which probability to use
        p = self._four_vector[(self.history[-1], opponent.history[-1])]
        # Draw a random number in [0, 1] to decide
        return random_choice(p)


class WinStayLoseShift(MemoryOnePlayer):
    """
    Win-Stay Lose-Shift, also called Pavlov.

    Names:

    - Win Stay Lose Shift: [Nowak1993]_
    - WSLS: [Stewart2012]_
    - Pavlov: [Kraines1989]_
    """

    name = 'Win-Stay Lose-Shift'
    classifier = {
        'memory_depth': 1,  # Memory-one Four-Vector
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, initial: Action = C) -> None:
        four_vector = (1, 0, 0, 1)
        super().__init__(four_vector)
        self._initial = initial


class WinShiftLoseStay(MemoryOnePlayer):
    """Win-Shift Lose-Stay, also called Reverse Pavlov.

    Names:

    - WSLS: [Li2011]_
    """

    name = 'Win-Shift Lose-Stay'
    classifier = {
        'memory_depth': 1,  # Memory-one Four-Vector
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, initial: Action = D) -> None:
        four_vector = (0, 1, 1, 0)
        super().__init__(four_vector)
        self._initial = initial


class GTFT(MemoryOnePlayer):
    """Generous Tit For Tat Strategy.

    Names:

    - Generous Tit For Tat: [Nowak1993]_
    - Naive peace maker: [Gaudesi2016]_
    - Soft Joss: [Gaudesi2016]_
    """

    name = 'GTFT'
    classifier = {
        'memory_depth': 1,  # Memory-one Four-Vector
        'stochastic': True,
        'makes_use_of': set(["game"]),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, p: float = None) -> None:
        """
        Parameters

        p, float
            A parameter used to compute the four-vector

        Special Cases

        TitForTat is equivalent to GTFT(0)
        """
        self.p = p
        super().__init__()

    def set_initial_four_vector(self, four_vector):
        pass

    def receive_match_attributes(self):
        (R, P, S, T) = self.match_attributes["game"].RPST()
        if self.p is None:
            self.p = min(1 - (T - R) / (R - S), (R - P) / (T - P))
        four_vector = [1, self.p, 1, self.p]
        self.set_four_vector(four_vector)

    def __repr__(self) -> str:
        assert self.p is not None
        return "%s: %s" % (self.name, round(self.p, 2))


class FirmButFair(MemoryOnePlayer):
    """A strategy that cooperates on the first move, and cooperates except after
    receiving a sucker payoff.

    Names:

    - Firm But Fair: [Frean1994]_"""

    name = 'Firm But Fair'

    def __init__(self) -> None:
        four_vector = (1, 0, 1, 2/3)
        super().__init__(four_vector)
        self.set_four_vector(four_vector)


class StochasticCooperator(MemoryOnePlayer):
    """Stochastic Cooperator.

    Names:

    - Stochastic Cooperator: [Adami2013]_
    """

    name = 'Stochastic Cooperator'

    def __init__(self) -> None:
        four_vector = (0.935, 0.229, 0.266, 0.42)
        super().__init__(four_vector)
        self.set_four_vector(four_vector)


class StochasticWSLS(MemoryOnePlayer):
    """
    Stochastic WSLS, similar to Generous TFT. Note that this is not the same as
    Stochastic WSLS described in [Amaral2016]_, that strategy is a modification
    of WSLS that learns from the performance of other strategies.

    Names:

    - Stochastic WSLS: Original name by Marc Harper
    """

    name = 'Stochastic WSLS'

    def __init__(self, ep: float = 0.05) -> None:
        """
        Parameters

        ep, float
            A parameter used to compute the four-vector -- the probability of
            cooperating when the previous round was CD or DC

        Special Cases

        WinStayLoseShift is equivalent to StochasticWSLS(0)
        """

        self.ep = ep
        four_vector = (1. - ep, ep, ep, 1. - ep)
        super().__init__(four_vector)
        self.set_four_vector(four_vector)


class SoftJoss(MemoryOnePlayer):
    """
    Defects with probability 0.9 when the opponent defects, otherwise
    emulates Tit-For-Tat.

    Names:

    - Soft Joss: [Prison1998]_
    """

    name = "Soft Joss"

    def __init__(self, q: float = 0.9) -> None:
        """
        Parameters

        q, float
            A parameter used to compute the four-vector

        Special Cases

        Cooperator is equivalent to SoftJoss(0)
        TitForTat  is equivalent to SoftJoss(1)
        """
        self.q = q
        four_vector = (1., 1 - q, 1, 1 - q)
        super().__init__(four_vector)

    def __repr__(self) -> str:
        return "%s: %s" % (self.name, round(self.q, 2))


class ALLCorALLD(Player):
    """This strategy is at the parameter extreme of the ZD strategies (phi = 0).
    It simply repeats its last move, and so mimics ALLC or ALLD after round one.
    If the tournament is noisy, there will be long runs of C and D.

    For now starting choice is random of 0.6, but that was an arbitrary choice
    at implementation time.

    Names:

    - ALLC or ALLD: Original name by Marc Harper
    - Repeat: [Akin2015]_
    """

    name = "ALLCorALLD"
    classifier = {
        'memory_depth': 1,  # Memory-one Four-Vector (1, 1, 0, 0)
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent: Player) -> Action:
        if len(self.history) == 0:
            return random_choice(0.6)
        return self.history[-1]


class ReactivePlayer(MemoryOnePlayer):
    """
    A generic reactive player. Defined by 2 probabilities conditional on the
    opponent's last move: P(C|C), P(C|D).

    Names:

    - Reactive: [Nowak1989]_
    """
    name = "Reactive Player"

    def __init__(self, probabilities: Tuple[float, float]) -> None:
        four_vector = (*probabilities, *probabilities)
        super().__init__(four_vector)
        self.name = "%s: %s" % (self.name, probabilities)
