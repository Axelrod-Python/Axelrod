import copy
import itertools
from typing import List, Tuple

from axelrod.action import Action, actions_to_str, str_to_actions
from axelrod.evolvable_player import (
    EvolvablePlayer,
    InsufficientParametersError,
    crossover_lists,
)
from axelrod.player import Player

C, D = Action.C, Action.D
actions = (C, D)


class AntiCycler(Player):
    """
    A player that follows a sequence of plays that contains no cycles:
    CDD  CD  CCD CCCD CCCCD ...

    Names:

    - Anti Cycler: Original name by Marc Harper
    """

    name = "AntiCycler"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self) -> None:
        super().__init__()
        self.cycle_length = 1
        self.cycle_counter = 0
        self.first_three = self._get_first_three()

    @staticmethod
    def _get_first_three() -> List[Action]:
        return [C, D, D]

    def strategy(self, opponent: Player) -> Action:
        while self.first_three:
            return self.first_three.pop(0)
        if self.cycle_counter < self.cycle_length:
            self.cycle_counter += 1
            return C
        else:
            self.cycle_length += 1
            self.cycle_counter = 0
            return D


class Cycler(Player):
    """
    A player that repeats a given sequence indefinitely.

    Names:

    - Cycler: Original name by Marc Harper
    """

    name = "Cycler"
    classifier = {
        "memory_depth": 2,
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self, cycle: str = "CCD") -> None:
        """This strategy will repeat the parameter `cycle` endlessly,
        e.g. C C D C C D C C D ...

        Special Cases
        -------------
        Cooperator is equivalent to Cycler("C")
        Defector   is equivalent to Cycler("D")
        Alternator is equivalent to Cycler("CD")

        """
        Player.__init__(self)
        self.cycle = cycle
        self.set_cycle(cycle=cycle)

    def strategy(self, opponent: Player) -> Action:
        return next(self.cycle_iter)

    def set_cycle(self, cycle: str):
        """Set or change the cycle."""
        self.cycle = cycle
        self.cycle_iter = itertools.cycle(str_to_actions(self.cycle))
        self.classifier["memory_depth"] = len(cycle) - 1


class EvolvableCycler(Cycler, EvolvablePlayer):
    """Evolvable version of Cycler."""

    name = "EvolvableCycler"

    def __init__(
        self,
        cycle: str = None,
        cycle_length: int = None,
        mutation_probability: float = 0.2,
        mutation_potency: int = 1,
        seed: int = None
    ) -> None:
        EvolvablePlayer.__init__(self, seed=seed)
        cycle, cycle_length = self._normalize_parameters(cycle, cycle_length)
        Cycler.__init__(self, cycle=cycle)
        # Overwrite init_kwargs in the case that we generated a new cycle from cycle_length
        self.overwrite_init_kwargs(
            cycle=cycle,
            cycle_length=cycle_length)
        self.mutation_probability = mutation_probability
        self.mutation_potency = mutation_potency

    def _normalize_parameters(self, cycle=None, cycle_length=None) -> Tuple[str, int]:
        """Compute other parameters from those that may be missing, to ensure proper cloning."""
        if not cycle:
            if not cycle_length:
                raise InsufficientParametersError("Insufficient Parameters to instantiate EvolvableCycler")
            cycle = self._generate_random_cycle(cycle_length)
        cycle_length = len(cycle)
        return cycle, cycle_length

    def _generate_random_cycle(self, cycle_length: int) -> str:
        """
        Generate a sequence of random moves
        """
        return actions_to_str(self._random.choice(actions) for _ in range(cycle_length))

    def mutate(self) -> EvolvablePlayer:
        """
        Basic mutation which may change any random actions in the sequence.
        """
        if self._random.random() <= self.mutation_probability:
            mutated_sequence = list(str_to_actions(self.cycle))
            for _ in range(self.mutation_potency):
                index_to_change = self._random.randint(0, len(mutated_sequence) - 1)
                mutated_sequence[index_to_change] = mutated_sequence[index_to_change].flip()
            cycle = actions_to_str(mutated_sequence)
        else:
            cycle = self.cycle
        cycle, _ = self._normalize_parameters(cycle)
        return self.create_new(cycle=cycle)

    def crossover(self, other) -> EvolvablePlayer:
        """
        Creates and returns a new Player instance with a single crossover point.
        """
        if other.__class__ != self.__class__:
            raise TypeError("Crossover must be between the same player classes.")
        cycle_list = crossover_lists(self.cycle, other.cycle, self._random)
        cycle = "".join(cycle_list)
        cycle, _ = self._normalize_parameters(cycle)
        return self.create_new(cycle=cycle, seed=self._random.random_seed_int())


class CyclerDC(Cycler):
    """
    Cycles D, C

    Names:

    - Cycler DC: Original name by Marc Harper
    """

    name = "Cycler DC"
    classifier = copy.copy(Cycler.classifier)
    classifier["memory_depth"] = 1

    def __init__(self) -> None:
        super().__init__(cycle="DC")


class CyclerCCD(Cycler):
    """
    Cycles C, C, D

    Names:

    - Cycler CCD: Original name by Marc Harper
    - Periodic player CCD: [Mittal2009]_
    """

    name = "Cycler CCD"
    classifier = copy.copy(Cycler.classifier)
    classifier["memory_depth"] = 2

    def __init__(self) -> None:
        super().__init__(cycle="CCD")


class CyclerDDC(Cycler):
    """
    Cycles D, D, C

    Names:

    - Cycler DDC: Original name by Marc Harper
    - Periodic player DDC: [Mittal2009]_
    """

    name = "Cycler DDC"
    classifier = copy.copy(Cycler.classifier)
    classifier["memory_depth"] = 2

    def __init__(self) -> None:
        super().__init__(cycle="DDC")


class CyclerCCCD(Cycler):
    """
    Cycles C, C, C, D

    Names:

    - Cycler CCCD: Original name by Marc Harper
    """

    name = "Cycler CCCD"
    classifier = copy.copy(Cycler.classifier)
    classifier["memory_depth"] = 3

    def __init__(self) -> None:
        super().__init__(cycle="CCCD")


class CyclerCCCCCD(Cycler):
    """
    Cycles C, C, C, C, C, D

    Names:

    - Cycler CCCD: Original name by Marc Harper
    """

    name = "Cycler CCCCCD"
    classifier = copy.copy(Cycler.classifier)
    classifier["memory_depth"] = 5

    def __init__(self) -> None:
        super().__init__(cycle="CCCCCD")


class CyclerCCCDCD(Cycler):
    """
    Cycles C, C, C, D, C, D

    Names:

    - Cycler CCCDCD: Original name by Marc Harper
    """

    name = "Cycler CCCDCD"
    classifier = copy.copy(Cycler.classifier)
    classifier["memory_depth"] = 5

    def __init__(self) -> None:
        super().__init__(cycle="CCCDCD")
