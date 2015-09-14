from axelrod import Player


class MindController(Player):
    """A player that changes the opponents strategy to cooperate."""

    name = 'Mind Controller'
    classifier = {
        'memory_depth': -10,
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': True,  # Finds out what opponent will do
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        """
        Alters the opponents strategy method to be a lambda function which
        always returns C. This player will then always return D to take
        advantage of this
        """

        opponent.strategy = lambda opponent: 'C'

        return 'D'


class MindWarper(Player):
    """
    A player that changes the opponent's strategy but blocks changes to
    its own.
    """

    name = 'Mind Warper'
    classifier = {
        'memory_depth': -10,
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': True,  # changes what opponent will do
        'manipulates_state': False
    }

    def __setattr__(self, name, val):
        if name == 'strategy':
            pass
        else:
            self.__dict__[name] = val

    @staticmethod
    def strategy(opponent):
        opponent.strategy = lambda opponent: 'C'
        return 'D'


class MindBender(MindWarper):
    """
    A player that changes the opponent's strategy by modifying the internal
    dictionary.
    """

    name = 'Mind Bender'
    classifier = {
        'memory_depth': -10,
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': True,  # changes what opponent will do
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        opponent.__dict__['strategy'] = lambda opponent: 'C'
        return 'D'
