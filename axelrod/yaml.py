from dataclasses import asdict
from typing import Tuple

from dacite import from_dict, Config
import yaml

import axelrod
from axelrod.action import Action, actions_to_str, str_to_actions
from axelrod.data_classes import ExpectedMatchOutcome, PlayerConfig, MatchConfig, MatchParameters

filename = "test_matches.yaml"


def build_player_spec(name, init_kwargs=None):
    if name == "MockPlayer":
        init_kwargs["actions"] = actions_to_str(init_kwargs["actions"])
    return PlayerConfig(name=name, init_kwargs=dict(init_kwargs))


def build_expected_spec(player_actions, coplayer_actions, attr=None):
    return ExpectedMatchOutcome(
        player_actions=player_actions,
        coplayer_actions=coplayer_actions,
        player_attributes=attr)


def build_match_parameters_spec(noise=None, seed=None):
    return MatchParameters(noise=noise, seed=seed)


def build_match_spec(player_name, coplayer_name, player_actions, coplayer_actions, noise=None, seed=None,
                     player_init_kwargs=None, coplayer_init_kwargs=None, attr=None):
    return MatchConfig(
        player=build_player_spec(player_name, init_kwargs=player_init_kwargs.copy()),
        coplayer=build_player_spec(coplayer_name, init_kwargs=coplayer_init_kwargs.copy()),
        match_parameters=build_match_parameters_spec(noise=noise, seed=seed),
        expected_outcome=build_expected_spec(player_actions, coplayer_actions, attr=attr)
    )


def log_kwargs(func):
    def wrapper(*args, **kwargs):
        stream = open('test_matches.yaml', 'a')
        spec = build_match_spec(str(args[1].__class__.__name__), str(args[2].__class__.__name__),
                                actions_to_str(args[-2]), actions_to_str(args[-1]),
                                noise=kwargs["noise"], seed=kwargs["seed"],
                                player_init_kwargs=args[1].init_kwargs,
                                coplayer_init_kwargs=args[2].init_kwargs)
        stream.write("---\n")
        yaml.dump(asdict(spec), stream)
        return func(*args, **kwargs)
    return wrapper


def load_matches():
    stream = open(filename, 'r')
    matches = yaml.load_all(stream, Loader=yaml.Loader)
    return [from_dict(data_class=MatchConfig, data=match, config=Config(
        type_hooks={Tuple[Action, ...]: str_to_actions})) for match in matches]


