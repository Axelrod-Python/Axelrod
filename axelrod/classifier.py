# TJ: Template the value type
def Classifier(object):
    name = None

    def __init__(self):
        pass

    def default_calc_for_player(self, player: 'Player'):
        return None

    # TJ: Who depends on whom
    def calc_for_player(self, player: 'Player'):
        if self.name is None:
            raise NotImplementedError("Classifier isn't properly implemented.")

        if self.name in player.classifier:
            return player.classifier[self.name]

        return self.default_calc_for_player(player)


def Stochastic(Classifier):
    name = "stochastic"

    def __init__(self):
        super().__init__()

    def default_calc_for_player(self, player: 'Player'):
        return False


def MemoryDepth(Classifier):
    name = "memory_depth"

    def __init__(self):
        super().__init__()

    def default_calc_for_player(self, player: 'Player'):
        return float("inf")


def MakesUseOf(Classifier):
    name = "makes_use_of"

    def __init__(self):
        super().__init__()

    def default_calc_for_player(self, player: 'Player'):
        return None


def LongRunTime(Classifier):
    name = "long_run_time"

    def __init__(self):
        super().__init__()

    def default_calc_for_player(self, player: 'Player'):
        return False


def InspectsSource(Classifier):
    name = "inspects_source"

    def __init__(self):
        super().__init__()

    def default_calc_for_player(self, player: 'Player'):
        return None


def ManipulatesSource(Classifier):
    name = "manipulates_source"

    def __init__(self):
        super().__init__()

    def default_calc_for_player(self, player: 'Player'):
        return None


def ManipulatesState(Classifier):
    name = "manipulates_state"

    def __init__(self):
        super().__init__()

    def default_calc_for_player(self, player: 'Player'):
        return None


all_classifiers = [
    Stochastic,
    MemoryDepth,
    MakesUseOf,
    LongRunTime,
    InspectsSource,
    ManipulatesSource,
    ManipulatesState,
]
