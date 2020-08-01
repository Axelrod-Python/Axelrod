import os
import warnings
from typing import (
    Any,
    Callable,
    Generic,
    List,
    Optional,
    Set,
    Text,
    Type,
    TypeVar,
    Union,
)

import yaml
from axelrod.makes_use_of import makes_use_of
from axelrod.player import Player

ALL_CLASSIFIERS_PATH = "data/all_classifiers.yml"

T = TypeVar("T")


class Classifier(Generic[T]):
    """Describes a Player (strategy).

    User sets a name and function, f, at initialization.  Through
    classify_player, looks for the classifier to be set in the passed Player
    class.  If not set, then passes to f for calculation.

    f must operate on the class, and not an instance.  If necessary, f may
    initialize an instance, but this shouldn't depend on runtime states, because
    the result gets stored in a file.  If a strategy's classifier depends on
    runtime states, such as those created by transformers, then it can set the
    field in its classifier dict, and that will take precedent over saved
    values.

    Attributes
    ----------
    name: An identifier for the classifier, used as a dict key in storage and in
        'classifier' dicts of Player classes.
    player_class_classifier: A function that takes in a Player class (not an
        instance) and returns a value.
    """

    def __init__(
        self, name: Text, player_class_classifier: Callable[[Type[Player]], T]
    ):
        self.name = name
        self.player_class_classifier = player_class_classifier

    def classify_player(self, player: Type[Player]) -> T:
        """Look for this classifier in the passed player's 'classifier' dict,
        otherwise pass to the player to f."""
        try:
            return player.classifier[self.name]
        except:
            return self.player_class_classifier(player)


stochastic = Classifier[bool]("stochastic", lambda _: False)
memory_depth = Classifier[Union[float, int]](
    "memory_depth", lambda _: float("inf")
)
makes_use_of = Classifier[Optional[Set[Text]]]("makes_use_of", makes_use_of)
long_run_time = Classifier[bool]("long_run_time", lambda _: False)
inspects_source = Classifier[Optional[bool]]("inspects_source", lambda _: None)
manipulates_source = Classifier[Optional[bool]](
    "manipulates_source", lambda _: None
)
manipulates_state = Classifier[Optional[bool]](
    "manipulates_state", lambda _: None
)

# Should list all known classifiers.
all_classifiers = [
    stochastic,
    memory_depth,
    makes_use_of,
    long_run_time,
    inspects_source,
    manipulates_source,
    manipulates_state,
]

all_classifiers_map = {c.name: c.classify_player for c in all_classifiers}


def rebuild_classifier_table(
    classifiers: List[Classifier],
    players: List[Type[Player]],
    path: Text = ALL_CLASSIFIERS_PATH,
) -> None:
    """Builds the classifier table in data.

    Parameters
    ----------
    classifiers: A list of classifiers to calculate on the strategies
    players: A list of strategies (classes, not instances) to compute the
        classifiers for.
    path: Where to save the resulting yaml file.
    """
    # Get absolute path
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, path)

    all_player_dicts = dict()
    for p in players:
        new_player_dict = dict()
        for c in classifiers:
            new_player_dict[c.name] = c.classify_player(p)
        all_player_dicts[p.name] = new_player_dict

    with open(filename, "w") as f:
        yaml.dump(all_player_dicts, f)


class _Classifiers(object):
    """A singleton used to calculate any known classifier.

    Attributes
    ----------
    all_player_dicts: A local copy of the dict saved in the classifier table.
        The keys are player names, and the values are 'classifier' dicts (keyed
        by classifier name).
    """

    _instance = None
    all_player_dicts = dict()

    # Make this a singleton
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(_Classifiers, cls).__new__(cls)
            # When this is first created, read from the classifier table file.
            # Get absolute path
            dirname = os.path.dirname(__file__)
            filename = os.path.join(dirname, ALL_CLASSIFIERS_PATH)
            with open(filename, "r") as f:
                cls.all_player_dicts = yaml.load(f, Loader=yaml.FullLoader)

        return cls._instance

    @classmethod
    def known_classifier(cls, classifier_name: Text) -> bool:
        """Returns True if the passed classifier_name is known."""
        global all_classifiers
        return classifier_name in (c.name for c in all_classifiers)

    @classmethod
    def __getitem__(
        cls, key: Union[Classifier, Text]
    ) -> Callable[[Union[Player, Type[Player]]], Any]:
        """Looks up the classifier for the player.

        Given a passed classifier key, return a function that:

        Takes a player.  If the classifier is found in the 'classifier' dict on
        the player, then return that.  Otherwise look for the classifier for the
        player in the all_player_dicts.  Returns None if the classifier is not
        found in either of those.

        The returned function expects Player instances, but if a Player class is
        passed, then it will create an instance by calling an argument-less
        initializer.  If no such initializer exists on the class, then an error
        will result.

        Parameters
        ----------
        key: A classifier or classifier name that we want to calculate for the
            player.

        Returns
        -------
        A function that will map Player (or Player instances) to their value for
            this classification.
        """
        # Key may be the name or an instance.  Convert to name.
        if not isinstance(key, str):
            key = key.name

        if not cls.known_classifier(key):
            raise KeyError("Unknown classifier")

        def classify_player_for_this_classifier(
            player: Union[Player, Type[Player]]
        ) -> Any:
            def try_lookup() -> Any:
                try:
                    player_classifiers = cls.all_player_dicts[player.name]
                except:
                    return None

                return player_classifiers.get(key, None)

            # If the passed player is not an instance, then try to initialize an
            # instance without arguments.
            if not isinstance(player, Player):
                try:
                    player = player()
                    warnings.warn(
                        "Classifiers are intended to run on player instances. "
                        "Passed player {} was initialized with default "
                        "arguments.".format(player.name)
                    )
                except:
                    # All strategies must have trivial initializers.
                    raise Exception(
                        "Passed player class doesn't have a trivial initializer."
                    )

            # Factory-generated players won't exist in the table.  As well, some
            # players, like Random, may change classifiers at construction time;
            # this get() function takes a player instance, while the saved-values
            # are from operations on the player object itself.
            if key in player.classifier:
                return player.classifier[key]

            # Try to find the name in the all_player_dicts, read from disk.
            lookup = try_lookup()
            if lookup is not None:
                return lookup

            # If we can't find it, then return a function that calculates fresh.
            global all_classifiers_map
            return all_classifiers_map[key](player)

        return classify_player_for_this_classifier

    @classmethod
    def is_basic(cls, s: Union[Player, Type[Player]]):
        """
        Defines criteria for a strategy to be considered 'basic'
        """
        stochastic = cls.__getitem__("stochastic")(s)
        depth = cls.__getitem__("memory_depth")(s)
        inspects_source = cls.__getitem__("inspects_source")(s)
        manipulates_source = cls.__getitem__("manipulates_source")(s)
        manipulates_state = cls.__getitem__("manipulates_state")(s)
        return (
            not stochastic
            and not inspects_source
            and not manipulates_source
            and not manipulates_state
            and depth in (0, 1)
        )

    @classmethod
    def obey_axelrod(cls, s: Union[Player, Type[Player]]):
        """
        A function to check if a strategy obeys Axelrod's original tournament
        rules.
        """
        for c in ["inspects_source", "manipulates_source", "manipulates_state"]:
            if cls.__getitem__(c)(s):
                return False
        return True


Classifiers = _Classifiers()
