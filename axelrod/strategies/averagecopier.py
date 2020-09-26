from axelrod.action import Action
from axelrod.player import Player

C, D = Action.C, Action.D


def calculate_cooperation_ratio(player: Player) -> float:
    """ Calculates the cooperation ratio of the player given."""
    return player.cooperations / len(player.history)


class AverageCopier(Player):
    """
    The player will cooperate with probability p where the opponent's cooperation
    ratio is p. Starts with random decision.

    Names:

    - Average Copier: Original name by Geraint Palmer
    """

    name = "Average Copier"
    classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def strategy(self, opponent: Player) -> Action:
        """Actual strategy definition that determines player's action."""
        if len(opponent.history) == 0:
            # Randomly picks a strategy (not affected by history).
            return self._random.random_choice(0.5)
        return self._random.random_choice(calculate_cooperation_ratio(opponent))


class NiceAverageCopier(Player):
    """
    Same as Average Copier, but always starts by cooperating.

    Names:

    - Average Copier: Original name by Owen Campbell
    """

    name = "Nice Average Copier"
    classifier = {
        "memory_depth": float("inf"),  # Long memory
        "stochastic": True,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def strategy(self, opponent: Player) -> Action:
        """Actual strategy definition that determines player's action."""
        if len(opponent.history) == 0:
            return C
        return self._random.random_choice(calculate_cooperation_ratio(opponent))
