import copy
import itertools
import random

from axelrod.action import Action, actions_to_str, str_to_actions
from axelrod.player import EvolvablePlayer, Player

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

    # def get_new_itertools_cycle(self):
    #     return

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
        mutation_probability: float = 0.5,
        mutation_potency: int = 1
    ) -> None:
        # Normalize parameters
        if not cycle:
            if not cycle_length:
                raise Exception("Insufficient Parameters to instantiate EvolvableCycler")
            cycle = self.generate_random_cycle(cycle_length)
        self.cycle_length = len(cycle)
        self.mutation_probability = mutation_probability
        self.mutation_potency = mutation_potency

        Cycler.__init__(self, cycle=cycle)
        EvolvablePlayer.__init__(self)
        self.overwrite_init_kwargs(
            cycle=cycle,
            cycle_length=len(cycle))

    @staticmethod
    def generate_random_cycle(cycle_length):
        """
        Generate a sequence of random moves

        Parameters
        ----------
        sequence_length - length of random moves to generate

        Returns
        -------
        list - a list of C & D actions: list[Action]
        """
        return actions_to_str(random.choice(actions) for _ in range(cycle_length))

    def crossover(self, other_cycler):
        """
        Creates and returns a new Player instance with a single crossover point.
        """
        seq1 = self.cycle
        seq2 = other_cycler.cycle
        crosspoint = random.randint(0, len(seq1))
        new_cycle = seq1[:crosspoint] + seq2[crosspoint:]
        return self.__class__(
            cycle=new_cycle,
            mutation_probability=self.mutation_probability,
            mutation_potency=self.mutation_potency)

    def mutate(self):
        """
        Basic mutation which may change any random gene(s) in the sequence.
        """
        if random.random() <= self.mutation_probability:
            mutated_sequence = list(str_to_actions(self.cycle))
            for _ in range(self.mutation_potency):
                index_to_change = random.randint(0, len(mutated_sequence) - 1)
                mutated_sequence[index_to_change] = mutated_sequence[index_to_change].flip()
            cycle = actions_to_str(mutated_sequence)
        else:
            cycle = self.cycle
        return self.__class__(
            cycle=cycle,
            mutation_probability=self.mutation_probability,
            mutation_potency=self.mutation_potency
        )

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
