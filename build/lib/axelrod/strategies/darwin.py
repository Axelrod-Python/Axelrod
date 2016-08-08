import inspect
from axelrod import Actions, Player

C, D = Actions.C, Actions.D

class Darwin(Player):
    """ A strategy which accumulates a record (the 'genome') of what the most
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
    """

    name = "Darwin"
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'inspects_source': False,
        'makes_use_of': set(),
        'manipulates_source': False,
        'manipulates_state': True  # Does not reset properly.
    }

    genome = [C]
    valid_callers = ["play"]    # What functions may invoke our strategy.

    def __init__(self):
        super(Darwin, self).__init__()
        self.response = Darwin.genome[0]

    def receive_match_attributes(self):
        self.outcomes = self.match_attributes["game"].scores

    def strategy(self, opponent):
        # Frustrate psychics and ensure that simulated rounds
        # do not influence genome.
        if inspect.stack()[1][3] not in Darwin.valid_callers:
            return C

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
        Player.reset(self)
        Darwin.genome[0] = C # Ensure initial Cooperate

    def mutate(self, outcome, trial):
        """ Select response according to outcome. """
        if outcome[0] < 3 and (len(Darwin.genome) >= trial):
            self.response = D if Darwin.genome[trial-1] == C else C
