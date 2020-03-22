from typing import Any, Callable, Generic, List, Optional, Set, Text, Type, \
    TypeVar, Union

import yaml

from axelrod.player import Player

ALL_CLASSIFIERS_PATH = "data/all_classifiers.yml"

T = TypeVar('T')


class Classifier(Generic[T]):
    def __init__(self, name: Text, f: Callable[[Type[Player]], T]):
        self.name = name
        self.f = f

    def calc_for_player(self, player: Type[Player]) -> T:
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


def rebuild_classifier_table(classifiers: List[Classifier],
                             players: List[Type[Player]],
                             path: Text = ALL_CLASSIFIERS_PATH) -> None:
    all_player_dicts = dict()
    for p in players:
        new_player_dict = dict()
        for c in classifiers:
            new_player_dict[c.name] = c.calc_for_player(p)
        all_player_dicts[p.name] = new_player_dict

    with open(path, 'w') as f:
        yaml.dump(all_player_dicts, f)


class Classifiers(object):
    _instance = None
    all_player_dicts = dict()

    # Make this a singleton
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Classifiers, cls).__new__(cls)
            with open(ALL_CLASSIFIERS_PATH, 'r') as f:
                cls.all_player_dicts = yaml.load(f, Loader=yaml.FullLoader)

        return cls._instance

    @classmethod
    def get(cls, classifier: Union[Classifier, Text],
            player: Player) -> Any:
        # Classifier may be the name or an instance.  Convert to name.
        if not isinstance(classifier, str):
            classifier = classifier.name

        # Factory-generated players won't exist in the table.  As well, some
        # players, like Random, may change classifiers at construction time;
        # this get() function takes a player instance, while the saved-values
        # are from operations on the player object itself.
        if classifier in player.classifier:
            return player.classifier[classifier]

        def return_missing() -> None:
            """What to do with a missing entry."""
            nonlocal classifier
            nonlocal player

            print("Classifier {} not found for {}.".format(classifier,
                                                           player.name))
            print("Consider rebuilding classifier table.")
            return None

        if player.name not in cls.all_player_dicts:
            return return_missing()
        player_classifiers = cls.all_player_dicts[player.name]

        if classifier not in player_classifiers:
            return return_missing()
        return player_classifiers[classifier]
