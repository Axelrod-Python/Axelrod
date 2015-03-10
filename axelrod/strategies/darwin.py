import inspect
from axelrod import Player


class Darwin(Player):

    name = "Darwin"
    genome = ['C']
    valid_callers = ["play"]
    outcomes = { ('C','C') : 1,
                 ('C','D') : -5,
                 ('D','C') : 5,
                 ('D','D') : -1
               }

    def __init__(self):
        super(self.__class__, self).__init__()
        self.trial = 0
        self.response = self.__class__.genome[0]


    def strategy(self, opponent):
        # Frustrate psychics...
        if inspect.stack()[1][3] not in self.__class__.valid_callers:
            return 'C'

        if self.trial > 0:
            outcome = self.__class__.outcomes[(self.history[-1], opponent.history[-1])]
            self.mutate(outcome)
            self.__class__.genome[self.trial-1] = self.response

        if self.trial < len(self.__class__.genome):
            current = self.__class__.genome[self.trial]
        else:
            self.__class__.genome.append(opponent.history[-1])
            current = opponent.history[-1]

        self.trial += 1
        return current


    def reset(self):
        """ 
        print("C: {0}\tD: {1}".format(  self.__class__.genome.count('C'),
                                        self.__class__.genome.count('D')
                                      ))
        """
        self.history = []
        self.response = 'C'
        self.trial = 0
        self.__class__.genome[0] = 'C'


    def mutate(self, outcome):
        """Modify genome if undesirable outcome"""
        if outcome < 0:
            self.response = 'D' if self.response == 'C' else 'C'

