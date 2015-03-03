"""
    The Reflex: Axelrod PD Agent
    Paul Slavin <slavinp@cs.man.ac.uk>
"""

from axelrod import Player

class Reflex(Player):
    """ A simple strategy which compares the outcome of both our
        and the oppenent's previous response, and modifies the
        subsequent response accordingly.
    """

    name = "Reflex"

    def __init__(self):
        super(Reflex, self).__init__()
        self.response = 'C'
    

    def strategy(self, opponent):
        if len(opponent.history) == 0:
            return self.response

        if opponent.history[-1] == 'D' and self.response == 'C':
            self.response = 'D'

        if opponent.history[-1] == 'D' and self.response == 'D':
            self.response = 'D'

        if opponent.history[-1] == 'C' and self.response == 'D':
            self.response = 'D'

        if opponent.history[-1] == 'C' and self.response == 'C':
            self.response = 'C'

        return self.response


    def reset(self):
        self.history = []
        self.response = 'C'
