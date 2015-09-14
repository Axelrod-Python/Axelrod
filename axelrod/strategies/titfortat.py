from axelrod import Player

flip_dict = {'C': 'D', 'D': 'C'}


class TitForTat(Player):
    """A player starts by cooperating and then mimics previous move by opponent."""

    name = 'Tit For Tat'
    classifier = {
        'memory_depth': 1,  # Four-Vector = (1.,0.,1.,0.)
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        return 'D' if opponent.history[-1:] == ['D'] else 'C'


class TitFor2Tats(Player):
    """A player starts by cooperating and then defects only after two defects by opponent."""

    name = "Tit For 2 Tats"
    classifier = {
        'memory_depth': 2,  # Long memory, memory-2
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        return 'D' if opponent.history[-2:] == ['D', 'D'] else 'C'


class TwoTitsForTat(Player):
    """A player starts by cooperating and replies to each defect by two defections."""

    name = "Two Tits For Tat"
    classifier = {
        'memory_depth': 2,  # Long memory, memory-2
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        return 'D' if 'D' in opponent.history[-2:] else 'C'


class Bully(Player):
    """A player that behaves opposite to Tit For Tat, including first move.

    Starts by defecting and then does the opposite of opponent's previous move.
    This the complete opposite of TIT FOR TAT, also called BULLY in literature.
    """

    name = "Bully"
    classifier = {
        'memory_depth': 1,  # Four-Vector = (1.,0.,1.,0.)
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        return 'C' if opponent.history[-1:] == ['D'] else 'D'


class SneakyTitForTat(Player):
    """Tries defecting once and repents if punished."""

    name = "Sneaky Tit For Tat"
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

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
    classifier = {
        'memory_depth': 1, # Four-Vector = (1.,0.,1.,0.)
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        return 'C' if opponent.history[-1:] == ['C'] else 'D'


class AntiTitForTat(Player):
    """A strategy that plays the opposite of the opponents previous move.
    This is similar to BULLY above, except that the first move is cooperation."""

    name = 'Anti Tit For Tat'
    classifier = {
        'memory_depth': 1,  # Four-Vector = (1.,0.,1.,0.)
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        return 'D' if opponent.history[-1:] == ['C'] else 'C'


class HardTitForTat(Player):
    """A variant of Tit For Tat that uses a longer history for retaliation."""

    name = 'Hard Tit For Tat'
    classifier = {
        'memory_depth': 3,  # memory-three
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        # Cooperate on the first move
        if not opponent.history:
            return 'C'
        # Defects if 'D' in the opponent's last three moves
        if 'D' in opponent.history[-3:]:
            return 'D'
        # Otherwise cooperates
        return 'C'


class HardTitFor2Tats(Player):
    """A variant of Tit For Two Tats that uses a longer history for
    retaliation."""

    name = "Hard Tit For 2 Tats"
    classifier = {
        'memory_depth': 3,  # memory-three
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        # Cooperate on the first move
        if not opponent.history:
            return 'C'
        # Defects if two consecutive 'D' in the opponent's last three moves
        history_string = "".join(opponent.history[-3:])
        if 'DD' in history_string:
            return 'D'
        # Otherwise cooperates
        return 'C'
