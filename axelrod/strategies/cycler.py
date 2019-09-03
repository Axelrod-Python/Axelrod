import copy
import itertools
import random

from axelrod.action import Action, actions_to_str, str_to_actions
from axelrod.evolvable_player import EvolvablePlayer, InsufficientParametersError, crossover_lists
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
        "makes_use_of": set(),
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
    def _get_first_three():
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
        "makes_use_of": set(),
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
        super().__init__()
        self.cycle = cycle
        self.cycle_iter = None
        self.set_cycle(cycle=cycle)

    def strategy(self, opponent: Player) -> Action:
        return next(self.cycle_iter)

    def set_cycle(self, cycle):
        """Set or change the cycle."""
        self.cycle = cycle
        self.cycle_iter = itertools.cycle(str_to_actions(self.cycle))
        self.classifier["memory_depth"] = len(cycle) - 1


class EvolvableCycler(Cycler, EvolvablePlayer):
    """Evolvable version of Cycler."""

    def __init__(
        self,
        cycle: str = None,
        cycle_length: int = None,
        mutation_probability: float = 0.2,
        mutation_potency: int = 1
    ) -> None:
        cycle, cycle_length = self._normalize_parameters(cycle, cycle_length)
        # The following __init__ sets self.cycle = cycle
        Cycler.__init__(self, cycle=cycle)
        EvolvablePlayer.__init__(self)
        # Overwrite init_kwargs in the case that we generated a new cycle from cycle_length
        self.overwrite_init_kwargs(
            cycle=cycle,
            cycle_length=cycle_length)
        self.mutation_probability = mutation_probability
        self.mutation_potency = mutation_potency

    @classmethod
    def _normalize_parameters(cls, cycle=None, cycle_length=None):
        """Compute other parameters from those that may be missing, to ensure proper cloning."""
        if not cycle:
            if not cycle_length:
                raise InsufficientParametersError("Insufficient Parameters to instantiate EvolvableCycler")
            cycle = cls._generate_random_cycle(cycle_length)
        cycle_length = len(cycle)
        return cycle, cycle_length

    @classmethod
    def _generate_random_cycle(cls, cycle_length):
        """
        Generate a sequence of random moves
        """
        return actions_to_str(random.choice(actions) for _ in range(cycle_length))

    def mutate(self):
        """
        Basic mutation which may change any random actions in the sequence.
        """
        if random.random() <= self.mutation_probability:
            mutated_sequence = list(str_to_actions(self.cycle))
            for _ in range(self.mutation_potency):
                index_to_change = random.randint(0, len(mutated_sequence) - 1)
                mutated_sequence[index_to_change] = mutated_sequence[index_to_change].flip()
            cycle = actions_to_str(mutated_sequence)
        else:
            cycle = self.cycle
        cycle, _ = self._normalize_parameters(cycle)
        return self.create_new(cycle=cycle)

    def crossover(self, other):
        """
        Creates and returns a new Player instance with a single crossover point.
        """
        if not isinstance(other, self.__class__):
            raise TypeError("Crossover must be between the same player classes.")
        cycle_list = crossover_lists(self.cycle, other.cycle)
        cycle = "".join(cycle_list)
        cycle, _ = self._normalize_parameters(cycle)
        return self.create_new(cycle=cycle)

    def serialize_parameters(self):
        return "{}:{}:{}".format(
                actions_to_str(self.cycle),
                str(self.mutation_probability),
                str(self.mutation_potency)
        )

    @classmethod
    def deserialize_parameters(cls, serialized):
        cycle, mutation_probability, mutation_potency = list(serialized.split(':'))
        return cls(
            cycle=cycle,
            mutation_probability=float(mutation_probability),
            mutation_potency=int(mutation_potency)
        )


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
