from typing import Any, Callable, Text


# TJ: Template the value type
def Classifier(object):
    def __init__(self, name: Text, f: Callable[['Player'], Any]):
        self.name = name
        self.f = f

    # TJ: Who depends on whom, re: Player
    def calc_for_player(self, player: 'Player'):
        if self.name in player.classifier:
            return player.classifier[self.name]

        return self.f(player)


stochastic = Classifier("stochastic", lambda _: False)
memory_depth = Classifier("memory_depth", lambda _: float("inf"))
makes_use_of = Classifier("makes_use_of", lambda _: None)
long_run_time = Classifier("long_run_time", lambda _: False)
inspects_source = Classifier("inspects_source", lambda _: None)
manipulates_source = Classifier("manipulates_source", lambda _: None)
manipulates_state = Classifier("manipulates_state", lambda _: None)

all_classifiers = [
    stochastic,
    memory_depth,
    makes_use_of,
    long_run_time,
    inspects_source,
    manipulates_source,
    manipulates_state,
]
