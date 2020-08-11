"""Memory Two strategies."""

import itertools
import warnings
from typing import Dict, Optional, Tuple

from axelrod.action import Action
from axelrod.player import Player

from .defector import Defector
from .titfortat import TitFor2Tats, TitForTat

C, D = Action.C, Action.D


class MemoryTwoPlayer(Player):
    """
    Uses a sixteen-vector for strategies based on the 16 conditional probabilities
    P(X | I,J,K,L) where X, I, J, K, L in [C, D] and I, J are the players last
    two moves and K, L are the opponents last two moves. These conditional
    probabilities are the following:
    1.  P(C|CC, CC)
    2.  P(C|CC, CD)
    3.  P(C|CC, DC)
    4.  P(C|CC, DD)
    5.  P(C|CD, CC)
    6.  P(C|CD, CD)
    7.  P(C|CD, DC)
    8.  P(C|CD, DD)
    9.  P(C|DC, CC)
    10. P(C|DC, CD)
    11. P(C|DC, DC)
    12. P(C|DC, DD)
    13. P(C|DD, CC)
    14. P(C|DD, CD)
    15. P(C|DD, DC)
    16. P(C|DD, DD)
    Cooperator is set as the default player if sixteen_vector is not given.

    Names

    - Memory Two: [Hilbe2017]_
    """

    name = "Generic Memory Two Player"
    classifier = {
        "memory_depth": 2,
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(
        self, sixteen_vector: Optional[Tuple[float, ...]] = None, initial: Optional[Tuple[Action, Action]] = None
    ) -> None:
        """
        Parameters
        ----------
        sixteen_vector: list or tuple of floats of length 16
            The response probabilities to the preceding round of play
        initial: (Action, Action)
            The initial 2 moves
        """
        super().__init__()
        if initial is None:
            initial = (C, C)
        self._initial = initial
        self.set_initial_sixteen_vector(sixteen_vector)

    def set_initial_sixteen_vector(self, sixteen_vector: Optional[Tuple[float, ...]]):
        if sixteen_vector is None:
            sixteen_vector = tuple([1] * 16)
            warnings.warn("Memory two player is set to default, Cooperator.")

        self.set_sixteen_vector(sixteen_vector)

    def set_sixteen_vector(self, sixteen_vector: Tuple[float, ...]):
        if not all(0 <= p <= 1 for p in sixteen_vector):
            raise ValueError(
                "An element in the probability vector, {}, is not "
                "between 0 and 1.".format(str(sixteen_vector))
            )

        states = [
            (hist[:2], hist[2:]) for hist in list(itertools.product((C, D), repeat=4))
        ]

        self._sixteen_vector = dict(
            zip(states, sixteen_vector)
        )  # type: Dict[tuple, float]

    @staticmethod
    def compute_memory_depth(sixteen_vector: Dict[Tuple[Action, Action], float]) -> int:
        values = set(list(sixteen_vector.values()))

        # Memory-depth 0
        if all(x == 0 for x in values) or all(x == 1 for x in values):
            return 0

        is_memory_one = True
        d = sixteen_vector
        contexts = [(C, C), (C, D), (D, C), (D, D)]

        for c1 in contexts:
            values = set()
            i, j = c1
            for c2 in contexts:
                x, y = c2
                values.add(d[((x, i), (y, j))])
            if len(values) > 1:
                is_memory_one = False
                break
        if is_memory_one:
            return 1
        return 2

    def _post_init(self):
        values = set(self._sixteen_vector.values())
        self.classifier["stochastic"] = any(0 < x < 1 for x in values)
        self.classifier["memory_depth"] = self.compute_memory_depth(self._sixteen_vector)

    def strategy(self, opponent: Player) -> Action:
        turn = len(self.history)
        if turn <= 1:
            return self._initial[turn]
        # Determine which probability to use
        p = self._sixteen_vector[
            (tuple(self.history[-2:]), tuple(opponent.history[-2:]))
        ]
        # Draw a random number in [0, 1] to decide
        try:
            return self._random.random_choice(p)
        except AttributeError:
            return C if p == 1 else D


class AON2(MemoryTwoPlayer):
    """
    AON2 a memory two strategy introduced in [Hilbe2017]_. It belongs to the
    AONk (all-or-none) family of strategies. These strategies were designed to
    satisfy the three following properties:

    1. Mutually Cooperative. A strategy is mutually cooperative if there are
    histories for which the strategy prescribes to cooperate, and if it continues
    to cooperate after rounds with mutual cooperation (provided the last k actions
    of the focal player were actually consistent).

    2. Error correcting. A strategy is error correcting after at most k rounds if,
    after any history, it generally takes a group of players at most k + 1 rounds
    to re-establish mutual cooperation.

    3. Retaliating. A strategy is retaliating for at least k rounds if, after
    rounds in which the focal player cooperated while the coplayer defected,
    the strategy responds by defecting the following k rounds.

    In [Hilbe2017]_ the following vectors are reported as "equivalent" to AON2
    with their respective self-cooperation rate (note that these are not the same):

    1. [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], self-cooperation
    rate: 0.952
    2. [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], self-cooperation
    rate: 0.951
    3. [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], self-cooperation
    rate:  0.951
    4. [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1], self-cooperation
    rate: 0.952

    AON2 is implemented using vector 1 due its self-cooperation rate.

    In essence it is a strategy that starts off by cooperating and will cooperate
    again only after the states (CC, CC), (CD, CD), (DC, DC), (DD, DD).

    Names:

    - AON2: [Hilbe2017]_
    """

    name = "AON2"
    classifier = {
        "memory_depth": 2,
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self) -> None:
        sixteen_vector = (1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1)
        super().__init__(sixteen_vector)


class DelayedAON1(MemoryTwoPlayer):
    """
    Delayed AON1 a memory two strategy also introduced in [Hilbe2017]_ and belongs
    to the AONk family. Note that AON1 is equivalent to Win Stay Lose Shift.

    In [Hilbe2017]_ the following vectors are reported as "equivalent" to Delayed
    AON1 with their respective self-cooperation rate (note that these are not the
    same):

    1. [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1], self-cooperation
    rate: 0.952
    2. [1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1], self-cooperation
    rate: 0.970
    3. [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1], self-cooperation
    rate: 0.971

    Delayed AON1 is implemented using vector 3 due its self-cooperation rate.

    In essence it is a strategy that starts off by cooperating and will cooperate
    again only after the states (CC, CC), (CD, CD), (CD, DD), (DD, CD),
    (DC, DC) and (DD, DD).

    Names:

    - Delayed AON1: [Hilbe2017]_
    """

    name = "Delayed AON1"
    classifier = {
        "memory_depth": 2,
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self) -> None:
        sixteen_vector = (1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1)
        super().__init__(sixteen_vector)


class MEM2(Player):
    """A memory-two player that switches between TFT, TFTT, and ALLD.

    Note that the reference claims that this is a memory two strategy but in
    fact it is infinite memory. This is because the player plays as ALLD if
    ALLD has ever been selected twice, which can only be known if the entire
    history of play is accessible.

    Names:

    - MEM2: [Li2014]_
    """

    name = "MEM2"
    classifier = {
        "memory_depth": float("inf"),
        "long_run_time": False,
        "stochastic": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self) -> None:
        super().__init__()
        self.players = {"TFT": TitForTat(), "TFTT": TitFor2Tats(), "ALLD": Defector()}
        self.play_as = "TFT"
        self.shift_counter = 3
        self.alld_counter = 0

    def strategy(self, opponent: Player) -> Action:
        # Update Histories
        # Note that this assumes that TFT and TFTT do not use internal counters,
        # Rather that they examine the actual history of play
        if len(self.history) > 0:
            for v in self.players.values():
                v.history.append(self.history[-1], opponent.history[-1])
        self.shift_counter -= 1
        if (self.shift_counter == 0) and (self.alld_counter < 2):
            self.shift_counter = 2
            # Depending on the last two moves, play as TFT, TFTT, or ALLD
            last_two = list(zip(self.history[-2:], opponent.history[-2:]))
            if set(last_two) == set([(C, C)]):
                self.play_as = "TFT"
            elif set(last_two) == set([(C, D), (D, C)]):
                self.play_as = "TFTT"
            else:
                self.play_as = "ALLD"
                self.alld_counter += 1
        return self.players[self.play_as].strategy(opponent)
