from axelrod.action import Action
from axelrod.player import Player

C, D = Action.C, Action.D


class Grudger(Player):
    """
    A player starts by cooperating however will defect if at any point the
    opponent has defected.

    This strategy came 7th in Axelrod's original tournament.

    Names:

    - Friedman's strategy: [Axelrod1980]_
    - Grudger: [Li2011]_
    - Grim: [Berg2015]_
    - Grim Trigger: [Banks1990]_
    - Spite: [Beaufils1997]_
    - Spiteful: [Mathieu2015]_
    - Vengeful: [Ashlock2009]_
    """

    name = "Grudger"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    @staticmethod
    def strategy(opponent: Player) -> Action:
        """Begins by playing C, then plays D for the remaining rounds if the
        opponent ever plays D."""
        if opponent.defections:
            return D
        return C


class ForgetfulGrudger(Player):
    """
    A player starts by cooperating however will defect if at any point the
    opponent has defected, but forgets after mem_length matches.

    Names:

    - Forgetful Grudger: Original name by Geraint Palmer
    """

    name = "Forgetful Grudger"
    classifier = {
        "memory_depth": 10,
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self) -> None:
        """Initialised the player."""
        super().__init__()
        self.mem_length = 10
        self.grudged = False
        self.grudge_memory = 0

    def strategy(self, opponent: Player) -> Action:
        """Begins by playing C, then plays D for mem_length rounds if the
        opponent ever plays D."""
        if self.grudge_memory == self.mem_length:
            self.grudge_memory = 0
            self.grudged = False

        if D in opponent.history[-1:]:
            self.grudged = True

        if self.grudged:
            self.grudge_memory += 1
            return D
        return C


class OppositeGrudger(Player):
    """
    A player starts by defecting however will cooperate if at any point the
    opponent has cooperated.

    Names:

    - Opposite Grudger: Original name by Geraint Palmer
    """

    name = "Opposite Grudger"
    classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    @staticmethod
    def strategy(opponent: Player) -> Action:
        """Begins by playing D, then plays C for the remaining rounds if the
        opponent ever plays C."""
        if opponent.cooperations:
            return C
        return D


class Aggravater(Player):
    """
    Grudger, except that it defects on the first 3 turns

    Names

    - Aggravater: Original name by Thomas Campbell
    """

    name = "Aggravater"
    classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    @staticmethod
    def strategy(opponent: Player) -> Action:
        """Actual strategy definition that determines player's action."""
        if len(opponent.history) < 3:
            return D
        elif opponent.defections:
            return D
        return C


class SoftGrudger(Player):
    """
    A modification of the Grudger strategy. Instead of punishing by always
    defecting: punishes by playing: D, D, D, D, C, C. (Will continue to
    cooperate afterwards).

    - Soft Grudger (SGRIM): [Li2011]_
    """

    name = "Soft Grudger"
    classifier = {
        "memory_depth": 6,
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self) -> None:
        """Initialised the player."""
        super().__init__()
        self.grudged = False
        self.grudge_memory = 0

    def strategy(self, opponent: Player) -> Action:
        """Begins by playing C, then plays D, D, D, D, C, C against a defection"""
        if self.grudged:
            strategy = [D, D, D, C, C][self.grudge_memory]
            self.grudge_memory += 1
            if self.grudge_memory == 5:
                self.grudge_memory = 0
                self.grudged = False
            return strategy
        elif D in opponent.history[-1:]:
            self.grudged = True
            return D
        return C


class GrudgerAlternator(Player):
    """
    A player starts by cooperating until the first opponents defection,
    then alternates D-C.

    Names:

    - c_then_per_dc: [Prison1998]_
    - Grudger Alternator: Original name by Geraint Palmer
    """

    name = "GrudgerAlternator"
    classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def strategy(self, opponent: Player) -> Action:
        """Begins by playing C, then plays Alternator for the remaining rounds
        if the opponent ever plays D."""
        if opponent.defections:
            if self.history[-1] == C:
                return D
        return C


class EasyGo(Player):
    """
    A player starts by defecting however will cooperate if at any point the
    opponent has defected.

    Names:

    - Easy Go: [Prison1998]_
    - Reverse Grudger (RGRIM): [Li2011]_
    - Fool Me Forever: [Harper2017]_
    """

    name = "EasyGo"
    classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    @staticmethod
    def strategy(opponent: Player) -> Action:
        """Begins by playing D, then plays C for the remaining rounds if the
        opponent ever plays D."""
        if opponent.defections:
            return C
        return D


class GeneralSoftGrudger(Player):
    """
    A generalization of the SoftGrudger strategy. SoftGrudger punishes by
    playing: D, D, D, D, C, C. after a defection by the opponent.
    GeneralSoftGrudger only punishes after its opponent defects a specified
    amount of times consecutively. The punishment is in the form of a series of
    defections followed by a 'penance' of a series of consecutive cooperations.

    Names:

    - General Soft Grudger: Original Name by J. Taylor Smith
    """

    name = "General Soft Grudger"
    classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self, n: int = 1, d: int = 4, c: int = 2) -> None:
        """
        Parameters
        ----------
        n: int
            The number of defections by the opponent to trigger punishment
        d: int
            The number of defections to punish the opponent
        c: int
            The number of cooperations in the 'penance' stage

        Special Cases
        -------------
        GeneralSoftGrudger(1,4,2) is equivalent to SoftGrudger
        """
        super().__init__()
        self.n = n
        self.d = d
        self.c = c
        self.grudge = [D] * (d - 1) + [C] * c
        self.grudged = False
        self.grudge_memory = 0

    def strategy(self, opponent: Player) -> Action:
        """
        Punishes after its opponent defects 'n' times consecutively.
        The punishment is in the form of 'd' defections followed by a penance of
        'c' consecutive cooperations.
        """
        if self.grudged:
            strategy = self.grudge[self.grudge_memory]
            self.grudge_memory += 1
            if self.grudge_memory == len(self.grudge):
                self.grudged = False
                self.grudge_memory = 0
            return strategy
        elif [D] * self.n == opponent.history[-self.n :]:
            self.grudged = True
            return D

        return C

    def __repr__(self) -> str:
        return "%s: n=%s,d=%s,c=%s" % (self.name, self.n, self.d, self.c)


class SpitefulCC(Player):
    """
    Behaves like Grudger after cooperating for 2 turns

    Names:

    - spiteful_cc: [Mathieu2015]_
    """

    name = "SpitefulCC"
    classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    @staticmethod
    def strategy(opponent: Player) -> Action:
        """
        Cooperates until the opponent defects. Then defects forever.
        Always cooperates twice at the start.
        """
        if len(opponent.history) < 2:
            return C
        elif opponent.defections:
            return D
        return C


class Capri(Player):
    """
    CAPRI is a memory-3 strategy proposed in [Murase2020]_. Its behavior is
    defined by the following five rules applied to the last 3 moves of the
    player and the opponent:

    - C: Cooperate at mutual cooperation.  This rule prescribes c at (ccc, ccc).
    - A: Accept punishment when you mistakenly defected from mutual cooperation.
      This rule prescribes c at (ccd, ccc), (cdc, ccd), (dcc, cdc), and (ccc,
      dcc).
    - P: Punish your co-player by defecting once when he defected from mutual
      cooperation.  This rule prescribes d at (ccc, ccd), and then c at (ccd,
      cdc), (cdc, dcc), and (dcc, ccc).
    - R: Recover cooperation when you or your co-player cooperated at mutual
      defection.  This rule prescribes c at (ddd, ddc), (ddc, dcc), (dcc, ccc),
      (ddc, ddd), (dcc, ddc), (ccc, dcc), (ddc, ddc), and (dcc, dcc).
    - I: In all the other cases, defect.

    The original implementation used in [Murase2020]_ is available at
    https://github.com/yohm/sim_exhaustive_m3_PDgame

    Names:

    - CAPRI: Original Name by Y. Murase et al. [Murase2020]_
    """

    name = "CAPRI"
    classifier = {
        "memory_depth": 3,
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def strategy(self, opponent: Player) -> Action:
        # initial history profile is full cooperation
        hist = list(zip(self.history[-3:], opponent.history[-3:]))
        while len(hist) < 3:
            hist.insert(0, (C, C))

        if hist == [(C, C), (C, C), (C, C)]:  # Rule: C
            return C
        if hist == [(C, C), (C, C), (D, C)]:  # Rule: A
            return C
        if hist == [(C, C), (D, C), (C, D)]:
            return C
        if hist == [(D, C), (C, D), (C, C)]:
            return C
        if hist == [(C, D), (C, C), (C, C)]:  # Rule: A & R2
            return C
        if hist == [(C, C), (C, C), (C, D)]:  # Rule: P
            return D
        if hist == [(C, C), (C, D), (D, C)]:
            return C
        if hist == [(C, D), (D, C), (C, C)]:
            return C
        if hist == [(D, C), (C, C), (C, C)]:  # Rule: P & R1
            return C
        if hist == [(D, D), (D, D), (D, C)]:  # Rule: R1
            return C
        if hist == [(D, D), (D, C), (C, C)]:
            return C
        if hist == [(D, D), (D, D), (C, D)]:  # Rule: R2
            return C
        if hist == [(D, D), (C, D), (C, C)]:
            return C
        if hist == [(D, D), (D, D), (C, C)]:  # Rule: R3
            return C
        if hist == [(D, D), (C, C), (C, C)]:
            return C
        return D
