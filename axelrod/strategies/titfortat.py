from axelrod import Actions, Player, init_args, flip_action

C, D = Actions.C, Actions.D


class TitForTat(Player):
    """
    A player starts by cooperating and then mimics the previous action of the
    opponent.

    Note that the code for this strategy is written in a fairly verbose
    way. This is done so that it can serve as an example strategy for
    those who might be new to Python.
    """

    # These are various properties for the strategy
    name = 'Tit For Tat'
    classifier = {
        'memory_depth': 1,  # Four-Vector = (1.,0.,1.,0.)
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        """This is the actual strategy"""
        # First move
        if len(self.history) == 0:
            return C
        # React to the opponent's last move
        if opponent.history[-1] == D:
            return D
        return C


class TitFor2Tats(Player):
    """A player starts by cooperating and then defects only after two defects by opponent."""

    name = "Tit For 2 Tats"
    classifier = {
        'memory_depth': 2,  # Long memory, memory-2
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        return D if opponent.history[-2:] == [D, D] else C


class TwoTitsForTat(Player):
    """A player starts by cooperating and replies to each defect by two defections."""

    name = "Two Tits For Tat"
    classifier = {
        'memory_depth': 2,  # Long memory, memory-2
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        return D if D in opponent.history[-2:] else C


class Bully(Player):
    """A player that behaves opposite to Tit For Tat, including first move.

    Starts by defecting and then does the opposite of opponent's previous move.
    This is the complete opposite of TIT FOR TAT, also called BULLY in literature.
    """

    name = "Bully"
    classifier = {
        'memory_depth': 1,   # Four-Vector = (0, 1, 0, 1)
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        return C if opponent.history[-1:] == [D] else D


class SneakyTitForTat(Player):
    """Tries defecting once and repents if punished."""

    name = "Sneaky Tit For Tat"
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        if len(self.history) < 2:
            return "C"
        if D not in opponent.history:
            return D
        if opponent.history[-1] == D and self.history[-2] == D:
            return "C"
        return opponent.history[-1]


class SuspiciousTitForTat(Player):
    """A TFT that initially defects."""

    name = "Suspicious Tit For Tat"
    classifier = {
        'memory_depth': 1, # Four-Vector = (1.,0.,1.,0.)
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        return C if opponent.history[-1:] == [C] else D


class AntiTitForTat(Player):
    """A strategy that plays the opposite of the opponents previous move.
    This is similar to BULLY above, except that the first move is cooperation."""

    name = 'Anti Tit For Tat'
    classifier = {
        'memory_depth': 1,  # Four-Vector = (1.,0.,1.,0.)
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        return D if opponent.history[-1:] == [C] else C


class HardTitForTat(Player):
    """A variant of Tit For Tat that uses a longer history for retaliation."""

    name = 'Hard Tit For Tat'
    classifier = {
        'memory_depth': 3,  # memory-three
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        # Cooperate on the first move
        if not opponent.history:
            return C
        # Defects if D in the opponent's last three moves
        if D in opponent.history[-3:]:
            return D
        # Otherwise cooperates
        return C


class HardTitFor2Tats(Player):
    """A variant of Tit For Two Tats that uses a longer history for
    retaliation."""

    name = "Hard Tit For 2 Tats"
    classifier = {
        'memory_depth': 3,  # memory-three
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        # Cooperate on the first move
        if not opponent.history:
            return C
        # Defects if two consecutive D in the opponent's last three moves
        history_string = "".join(opponent.history[-3:])
        if 'DD' in history_string:
            return D
        # Otherwise cooperates
        return C


class OmegaTFT(Player):
    """OmegaTFT modifies TFT in two ways:
       -- checks for deadlock loops of alternating rounds of (C, D) and (D, C),
       and attempting to break them
       -- uses a more sophisticated retaliation mechanism that is noise tolerant.
    """

    name = "Omega TFT"
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @init_args
    def __init__(self, deadlock_threshold=3, randomness_threshold=8):
        Player.__init__(self)
        self.deadlock_threshold = deadlock_threshold
        self.randomness_threshold = randomness_threshold
        self.randomness_counter = 0
        self.deadlock_counter = 0

    def strategy(self, opponent):
        # Cooperate on the first move
        if len(self.history) == 0:
            return C
        # TFT on round 2
        if len(self.history) == 1:
            return D if opponent.history[-1:] == [D] else C

        # Are we deadlocked? (in a CD -> DC loop)
        if (self.deadlock_counter >= self.deadlock_threshold):
            self.move = C
            if self.deadlock_counter == self.deadlock_threshold:
                self.deadlock_counter = self.deadlock_threshold + 1
            else:
                self.deadlock_counter = 0
        else:
            # Update counters
            if opponent.history[-2:] == [C, C]:
                self.randomness_counter -= 1
            # If the opponent's move changed, increase the counter
            if opponent.history[-2] != opponent.history[-1]:
                self.randomness_counter += 1
            # If the opponent's last move differed from mine, increase the counter
            if self.history[-1] == opponent.history[-1]:
                self.randomness_counter+= 1
            # Compare counts to thresholds
            # If randomness_counter exceeds Y, Defect for the remainder
            if self.randomness_counter >= 8:
                self.move = D
            else:
                # TFT
                self.move = D if opponent.history[-1:] == [D] else C
                # Check for deadlock
                if opponent.history[-2] != opponent.history[-1]:
                    self.deadlock_counter += 1
                else:
                    self.deadlock_counter = 0
        return self.move

    def reset(self):
        Player.reset(self)
        self.randomness_counter = 0
        self.deadlock_counter = 0
