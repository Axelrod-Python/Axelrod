"""
The player class in this module does not obey standard rules of the IPD (as
indicated by their classifier). We do not recommend putting a lot of time in to
optimising it.
"""
from axelrod.actions import Action, Actions
from axelrod.player import Player

C, D = Actions.C, Actions.D


class Darwin(Player):
    """
    A strategy which accumulates a record (the 'genome') of what the most
    favourable response in the previous round should have been, and naively
    assumes that this will remain the correct response at the same round of
    future trials.

    This 'genome' is preserved between opponents, rounds and repetitions of
    the tournament.  It becomes a characteristic of the type and so a single
    version of this is shared by all instances for each loading of the class.

    As this results in information being preserved between tournaments, this
    is classified as a cheating strategy!

    If no record yet exists, the opponent's response from the previous round
    is returned.

    Names:

    - Darwin: Original name by Paul Slavin
    """

    name = "Darwin"
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'inspects_source': True,  # Checks to see if opponent is using simulated matches.
        'long_run_time': False,
        'makes_use_of': set(),
        'manipulates_source': False,
        'manipulates_state': True  # Does not reset properly.
    }

    genome = [C]
    valid_callers = ["play"]    # What functions may invoke our strategy.

    def __init__(self) -> None:
        self.outcomes = None  # type: dict
        self.response = Darwin.genome[0]
        super().__init__()

    def receive_match_attributes(self):
        self.outcomes = self.match_attributes["game"].scores

    @staticmethod
    def foil_strategy_inspection() -> Action:
        """Foils _strategy_utils.inspect_strategy and _strategy_utils.look_ahead"""
        return C

    def strategy(self, opponent: Player) -> Action:
        trial = len(self.history)

        if trial > 0:
            outcome = self.outcomes[(self.history[-1], opponent.history[-1])]
            self.mutate(outcome, trial)
            # Update genome with selected response
            Darwin.genome[trial-1] = self.response

        if trial < len(Darwin.genome):
            # Return response from genome where available...
            current = Darwin.genome[trial]
        else:
            # ...otherwise use Tit-for-Tat
            Darwin.genome.append(opponent.history[-1])
            current = opponent.history[-1]

        return current

    def reset(self):
        """ Reset instance properties. """
        super().reset()
        Darwin.genome[0] = C  # Ensure initial Cooperate

    def mutate(self, outcome: tuple, trial: int) -> None:
        """ Select response according to outcome. """
        if outcome[0] < 3 and (len(Darwin.genome) >= trial):
            self.response = D if Darwin.genome[trial-1] == C else C

    @staticmethod
    def reset_genome() -> None:
        """For use in testing methods."""
        Darwin.genome = [C]
