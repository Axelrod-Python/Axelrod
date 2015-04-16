from axelrod import Player

class TitForTat(Player):
    """A player starts by cooperating and then mimics previous move by opponent."""

    name = 'Tit For Tat'

    def strategy(self, opponent):
        try:
            return opponent.history[-1]
        except IndexError:
            return 'C'

class TitFor2Tats(Player):
    """A player starts by cooperating and then defects only after two defects by opponent."""

    name = "Tit For 2 Tats"

    def strategy(self, opponent):
        if opponent.history[-2:] == ['D', 'D']:
            return 'D'
        return 'C'

class TwoTitsForTat(Player):
    """A player starts by cooperating and replies to each defect by two defections."""

    name = "Two Tits For Tat"

    def strategy(self, opponent):
        if 'D' in opponent.history[-2:]:
            return 'D'
        return 'C'

class SuspiciousTitForTat(Player):
    """A player that behaves opposite to Tit For Tat.

    Starts by defecting and then does the opposite of opponent's previous move.
    This the opposite of TIT FOR TAT, also sometimes called BULLY.
    """

    name = "Suspicious Tit For Tat"

    def strategy(self, opponent):
        return 'C' if opponent.history[-1:] == ['D'] else 'D'


class SneakyTitForTat(Player):
    """Tries defecting once and repents if punished."""

    name = "Sneaky Tit For Tat"

    def strategy(self, opponent):
        if len(self.history) < 2:
            return "C"
        if 'D' not in opponent.history:
            return 'D'
        if opponent.history[-1] == 'D' and self.history[-2] == 'D':
            return "C"
        return opponent.history[-1]