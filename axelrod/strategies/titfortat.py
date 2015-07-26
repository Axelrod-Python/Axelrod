from axelrod import Player

flip_dict = {'C': 'D', 'D': 'C'}


class TitForTat(Player):
    """A player starts by cooperating and then mimics previous move by opponent."""

    name = 'Tit For Tat'
    memory_depth = 1  # Four-Vector = (1.,0.,1.,0.)

    @staticmethod
    def strategy(opponent):
        return 'D' if opponent.history[-1:] == ['D'] else 'C'


class TitFor2Tats(Player):
    """A player starts by cooperating and then defects only after two defects by opponent."""

    name = "Tit For 2 Tats"
    memory_depth = 2  # Long memory, memory-2

    @staticmethod
    def strategy(opponent):
        return 'D' if opponent.history[-2:] == ['D', 'D'] else 'C'


class TwoTitsForTat(Player):
    """A player starts by cooperating and replies to each defect by two defections."""

    name = "Two Tits For Tat"
    memory_depth = 2  # Long memory, memory-2

    @staticmethod
    def strategy(opponent):
        return 'D' if 'D' in opponent.history[-2:] else 'C'


class Bully(Player):
    """A player that behaves opposite to Tit For Tat, including first move.

    Starts by defecting and then does the opposite of opponent's previous move.
    This the complete opposite of TIT FOR TAT, also called BULLY in literature.
    """

    name = "Bully"
    memory_depth = 1  # Four-Vector = (0.,1.,0.,1.)

    @staticmethod
    def strategy(opponent):
        return 'C' if opponent.history[-1:] == ['D'] else 'D'


class SneakyTitForTat(Player):
    """Tries defecting once and repents if punished."""

    name = "Sneaky Tit For Tat"
    memory_depth = float('inf')  # Long memory

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
    memory_depth = 1  # Four-Vector = (1.,0.,1.,0.)

    @staticmethod
    def strategy(opponent):
        return 'C' if opponent.history[-1:] == ['C'] else 'D'


class AntiTitForTat(Player):
    """A strategy that plays the opposite of the opponents previous move.
    This is similar to BULLY above, except that the first move is cooperation."""

    name = 'Anti Tit For Tat'
    memory_depth = 1  # Four-Vector = (0.,1.,0.,1.)

    @staticmethod
    def strategy(opponent):
        return 'D' if opponent.history[-1:] == ['C'] else 'C'


class Shubik(Player):
    """
    Plays like Tit-For-Tat with the following modification. After
    each retaliation, the number of rounds that Shubik retaliates
    increases by 1.
    """

    name = 'Shubik'
    memory_depth = float('inf')

    def __init__(self):
        Player.__init__(self)
        self.is_retaliating = False
        self.retaliation_length = 0
        self.retaliation_remaining = 0

    def _refresh_retaliation(self, opponent):
        """Reset the retaliation counter based on the history"""
        self.retaliation_length = 0
        for i in range(len(self.history)):
            if self.history[i] == 'C':
                if opponent.history[i] == 'D':
                    self.retaliation_length += 1
        self.retaliation_remaining = self.retaliation_length

    def _decrease_retaliation_counter(self):
        """Lower the remaining owed retaliation count and flip to non-retaliate
        if the count drops to zero."""
        if self.is_retaliating:
            self.retaliation_remaining -= 1
            if self.retaliation_remaining == 0:
                self.is_retaliating = False

    def strategy(self, opponent):
        if not opponent.history:
            return 'C'
        if opponent.history[-1] == 'D':
            # Retaliate against defections
            if self.history[-1] == 'C': # it's on now!
                # Lengthen the retaliation period
                self.is_retaliating = True
                self._refresh_retaliation(opponent)
                self._decrease_retaliation_counter()
                return 'D'
            else:
                # Just retaliate
                if self.is_retaliating:
                    self._decrease_retaliation_counter()
                return 'D'
        if self.is_retaliating:
            # Are we retaliating still?
            self._decrease_retaliation_counter()
            return 'D'
        return 'C'


class HardTitForTat(Player):
    """A variant of Tit For Tat that uses a longer history for retaliation."""

    name = 'Hard Tit For Tat'
    memory_depth = 3  # memory-three

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
    memory_depth = 3  # memory-three

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

class Tester(Player):
    """
    Submitted to Axelrod's second tournament by David Gladstein.

    Defects on the first move and plays TFT if the opponent ever defects (after
    one apology cooperation round). Otherwise alternate cooperation and defection.
    """

    name = "Tester"
    memory_depth = float('inf')

    def __init__(self):
        Player.__init__(self)
        self.is_TFT = False

    def strategy(self, opponent):
        # Defect on the first move
        if not opponent.history:
            return 'D'
        # Am I TFT?
        if self.is_TFT:
            return 'D' if opponent.history[-1:] == ['D'] else 'C'
        else:
            # Did opponent defect?
            if opponent.history[-1] == 'D':
                self.is_TFT = True
                return 'C'
            if len(self.history) in [1, 2]:
                return 'C'
            # Alternate C and D
            return flip_dict[self.history[-1]]

