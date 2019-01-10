import random
from axelrod.action import Action
from axelrod.player import Player
from scipy.stats import chisquare

C, D = Action.C, Action.D


class Graaskamp(Player):
    """
    Play Tit For Tat for the first 50 rounds;
	Defects on round 51;
	Plays 5 further rounds of Tit For Tat;
	A check is then made to see if the opponent is playing randomly
	in which case it defects for the rest of the game;
	The strategy also checks to see if the opponent is playing Tit For Tat.
	If so it plays Tit For Tat. If not it cooperates and randomly defects every 5 to 15 moves.
    """

    name = "Graaskamp"
    classifier = {
        "memory_depth": 57,  # long_memory
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": True,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self, alpha: float = 0.05) -> None:
        """
        Parameters
        ----------
        alpha: float
            The significant level of p-value from chi-squared test with
            alpha == 0.05 by default.
        """
        super().__init__()
        self.alpha = alpha
        self.opponent_is_random = False
        self.opponent_is_TfT = False

    def strategy(self, opponent: Player) -> Action:
        """This is the actual strategy"""
        # First move
        # Cooperate in first round as in Tit for Tat strategy
        if not self.history:
            return C
        # Copy opponent's last move as in Tit for Tat strategy
        if len(self.history) <= 50 or 52 <= len(self.history) <= 56 or len(self.history) >= 57:
            if opponent.history[-1] == D:
                return D
            return C

        # Defect on round 51
        if len(self.history) == 51:
            return D

        if len(self.history) >= 57:
            # Check if opponent plays randomly, if so, defect
            p_value = chisquare([opponent.cooperations, opponent.defections]).pvalue
            self.opponent_is_random = p_value >= self.alpha

            if self.opponent_is_random:
                return D
            elif all(opponent.history[-i] == self.history[-i - 1] for i in range(1, 57)):
                # Check if opponent plays Tit for Tat
                    if opponent.history[-1] == D:
                        return D
                    return C
            else:
                # Generating integer from 0 to 14 for defecting every 5 to 15 moves
                numlist = []
                while len(numlist < 5):
                    for i in range(1, 5):
                        numlist += [i]
                while len(numlist) < 15:
                    rnd = random.randint(6, 14)
                    if rnd in numlist:
                        continue
                    else:
                        if rnd == 14:
                            del numlist[:]
                            return D
                        numlist += [rnd]
