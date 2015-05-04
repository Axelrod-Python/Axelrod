from axelrod import Player

flip_dict = {'C': 'D', 'D':'C'}

class TitForTat(Player):
    """A player starts by cooperating and then mimics previous move by opponent."""

    name = 'Tit For Tat'

    def strategy(self, opponent):
        return 'D' if opponent.history[-1:] == ['D'] else 'C'

class TitFor2Tats(Player):
    """A player starts by cooperating and then defects only after two defects by opponent."""

    name = "Tit For 2 Tats"

    def strategy(self, opponent):
        return 'D' if opponent.history[-2:] == ['D', 'D'] else 'C'

class TwoTitsForTat(Player):
    """A player starts by cooperating and replies to each defect by two defections."""

    name = "Two Tits For Tat"

    def strategy(self, opponent):
        return 'D' if 'D' in opponent.history[-2:] else 'C'

class Bully(Player):
    """A player that behaves opposite to Tit For Tat, including first move.

    Starts by defecting and then does the opposite of opponent's previous move.
    This the complete opposite of TIT FOR TAT, also called BULLY in literature.
    """

    name = "Bully"

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

class SuspiciousTitForTat(Player):
    """A TFT that initially defects."""

    name = "Suspicious Tit For Tat"

    def strategy(self, opponent):
        return 'C' if opponent.history[-1:] == ['C'] else 'D'

class AntiTitForTat(Player):
    """A strategy that plays the opposite of the opponents previous move.

    This is similar to BULLY above, except that the first move is cooperation.
    """

    name = 'Anti Tit For Tat'

    def strategy(self, opponent):
        return 'D' if opponent.history[-1:] == ['C'] else 'C'