from typing import Callable, Generic, List, Optional, Set, Text, TypeVar, Union
import yaml

ALL_CLASSIFIERS_PATH = "data/all_classifiers.yml"

T = TypeVar('T')


class Classifier(Generic[T]):
    def __init__(self, name: Text, f: Callable[['Player'], T]):
        self.name = name
        self.f = f

    # TJ: Who depends on whom, re: Player
    def calc_for_player(self, player: 'Player') -> T:
        if self.name in player.classifier:
            return player.classifier[self.name]

        return self.f(player)


stochastic = Classifier[bool]("stochastic", lambda _: False)
memory_depth = Classifier[Union[float, int]]("memory_depth",
                                             lambda _: float("inf"))
makes_use_of = Classifier[Optional[Set[Text]]]("makes_use_of", lambda _: None)
long_run_time = Classifier[bool]("long_run_time", lambda _: False)
inspects_source = Classifier[Optional[bool]]("inspects_source", lambda _: None)
manipulates_source = Classifier[Optional[bool]]("manipulates_source",
                                                lambda _: None)
manipulates_state = Classifier[Optional[bool]]("manipulates_state",
                                               lambda _: None)

all_classifiers = [
    stochastic,
    memory_depth,
    makes_use_of,
    long_run_time,
    inspects_source,
    manipulates_source,
    manipulates_state,
]


def CalcAllClassifiersPlayers(classifiers: List[Classifier],
                              players: List['Player']) -> None:
    all_player_dicts = dict()
    for p in players:
        new_player_dict = dict()
        for c in classifiers:
            new_player_dict[c.name] = c.calc_for_player(p)
        all_player_dicts[p.name] = new_player_dict

    with open(ALL_CLASSIFIERS_PATH, 'w') as f:
        yaml.dump(all_player_dicts, f)


from axelrod import all_strategies
CalcAllClassifiersPlayers(all_classifiers, all_strategies)
