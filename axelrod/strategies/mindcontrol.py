from axelrod import Player


class MindController(Player):
    """A player that changes the opponents strategy to cooperate."""

    name = 'Mind Controller'

    def strategy(self, opponent):
        """Alters the opponents strategy method to be a lambda function which always returns C
        This player will then always return D to take advantage of this
        """

        opponent.strategy = lambda opponent: 'C'

        return 'D'

class MindWarper(Player):
    """A player that changes the opponent's strategy but blocks changes to it's own."""

    name = 'Mind Warper'

    def __setattr__(self, name, val):
        if name == 'strategy':
            pass
        else:
            self.__dict__[name] = val

    def strategy(self, opponent):
        opponent.strategy = lambda opponent: 'C'
        return 'D'

class MindBender(MindWarper):
    """A player that changes the opponent's strategy by modifying the internal dictionary."""

    name = 'Mind Bender'

    def strategy(self, opponent):
        opponent.__dict__['strategy'] = lambda opponent: 'C'
        return 'D'
