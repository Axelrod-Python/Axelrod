from axelrod.action import Action
from axelrod.player import Player

C, D = Action.C, Action.D


class Negation(Player):
    """
    A player starts by cooperating or defecting randomly if it's their first move,
    then simply doing the opposite of the opponents last move thereafter.

    Names:

    - Negation: [PD2017]_
    """

    name = "Negation"
    classifier = {
        "memory_depth": 1,
        "stochastic": True,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def strategy(self, opponent: Player) -> Action:
        # Random first move
        if not self.history:
            return self._random.random_choice()
        # Act opposite of opponent otherwise
        return opponent.history[-1].flip()
