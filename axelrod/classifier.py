from typing import Any, Callable, Generic, List, Optional, Set, Text, TypeVar, Union
import yaml

from axelrod.player import Player

ALL_CLASSIFIERS_PATH = "data/all_classifiers.yml"

T = TypeVar('T')


class Classifier(Generic[T]):
    def __init__(self, name: Text, f: Callable[[Player], T]):
        self.name = name
        self.f = f

    def calc_for_player(self, player: Player) -> T:
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


def calc_all_classifier_players(classifiers: List[Classifier],
                                players: List[Player]) -> None:
    all_player_dicts = dict()
    for p in players:
        new_player_dict = dict()
        for c in classifiers:
            new_player_dict[c.name] = c.calc_for_player(p)
        all_player_dicts[p.name] = new_player_dict

    with open(ALL_CLASSIFIERS_PATH, 'w') as f:
        yaml.dump(all_player_dicts, f)


class ClassifierManager(object):
    _instance = None
    all_player_dicts = dict()

    # Make this a singleton
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ClassifierManager, cls).__new__(cls)
            with open(ALL_CLASSIFIERS_PATH, 'r') as f:
                cls.all_player_dicts = yaml.load(f, Loader=yaml.FullLoader)

        return cls._instance

    @classmethod
    def get_classifier(cls, classifier: Classifier, player: Player) -> Any:
        if player not in cls.all_player_dicts:
            return None
        player_classifiers = cls.all_player_dicts[player]

        if classifier not in player_classifiers:
            return None
        return player_classifiers[classifier]

