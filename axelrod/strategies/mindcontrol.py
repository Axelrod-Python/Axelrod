from axelrod.action import Action
from axelrod.player import Player

C, D = Action.C, Action.D


class MindController(Player):
    """A player that changes the opponents strategy to cooperate.

    Names

    - Mind Controller: Original name by Karol Langner
    """

    name = 'Mind Controller'
    classifier = {
        'memory_depth': -10,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': True,  # Finds out what opponent will do
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent: Player) -> Action:
        """
        Alters the opponents strategy method to be a lambda function which
        always returns C. This player will then always return D to take
        advantage of this
        """

        opponent.strategy = lambda opponent: C
        return D


class MindWarper(Player):
    """
    A player that changes the opponent's strategy but blocks changes to
    its own.

    Names

    - Mind Warper: Original name by Karol Langner
    """

    name = 'Mind Warper'
    classifier = {
        'memory_depth': -10,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': True,  # changes what opponent will do
        'manipulates_state': False
    }

    def __setattr__(self, name: str, val: str):
        if name == 'strategy':
            pass
        else:
            self.__dict__[name] = val

    @staticmethod
    def strategy(opponent: Player) -> Action:
        opponent.strategy = lambda opponent: C
        return D


class MindBender(MindWarper):
    """
    A player that changes the opponent's strategy by modifying the internal
    dictionary.

    Names

    - Mind Bender: Original name by Karol Langner
    """

    name = 'Mind Bender'
    classifier = {
        'memory_depth': -10,
        'makes_use_of': set(),
        'stochastic': False,
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': True,  # changes what opponent will do
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent: Player) -> Action:
        opponent.__dict__['strategy'] = lambda opponent: C
        return D
