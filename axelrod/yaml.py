from dataclasses import asdict
import inspect
from typing import Tuple

from dacite import from_dict, Config
import yaml

import axelrod
from axelrod.action import Action, actions_to_str, str_to_actions
from axelrod.data_classes import ExpectedMatchOutcome, PlayerConfig, MatchConfig, MatchParameters, TestMatchConfig

filename = "test_matches.yaml"
# f = open("test_matches.yaml", 'w')
# f.close()


def build_player_spec(name, init_kwargs=None):
    # if name == "MockPlayer":
    #     init_kwargs["actions"] = actions_to_str(init_kwargs["actions"])
    return PlayerConfig(name=name, init_kwargs=dict(init_kwargs))


def build_expected_spec(player_actions, coplayer_actions, player_attributes=None):
    return ExpectedMatchOutcome(
        player_actions=player_actions,
        coplayer_actions=coplayer_actions,
        player_attributes=player_attributes)


def build_match_parameters_spec(noise=None, seed=None, match_attributes=None):
    return MatchParameters(noise=noise, seed=seed, match_attributes=match_attributes)


def build_match_spec(player_name, coplayer_name, player_actions, coplayer_actions, noise=None, seed=None,
                     player_init_kwargs=None, coplayer_init_kwargs=None, player_attributes=None, match_attributes=None):
    return MatchConfig(
        player=build_player_spec(player_name, init_kwargs=player_init_kwargs.copy()),
        coplayer=build_player_spec(coplayer_name, init_kwargs=coplayer_init_kwargs.copy()),
        match_parameters=build_match_parameters_spec(noise=noise, seed=seed, match_attributes=match_attributes),
        expected_outcome=build_expected_spec(player_actions, coplayer_actions, player_attributes=player_attributes)
    )


def build_test_match_config(name, description, match_config):
    return TestMatchConfig(name=name, description=description, match_config=match_config)


def log_kwargs(func):
    def wrapper(*args, **kwargs):
        try:
            noise = kwargs["noise"]
        except KeyError:
            noise = None
        try:
            seed = kwargs["seed"]
        except KeyError:
            seed = None
        try:
            match_attributes = kwargs["match_attributes"]
        except KeyError:
            match_attributes = None
        try:
            player_attributes = kwargs["attrs"]
        except KeyError:
            player_attributes = None

        # Some inspect shenanigans to get the calling function name and docstring
        outer_frame = inspect.getouterframes(inspect.currentframe(), context=2)
        calling_frame_info = outer_frame[2]
        function_name = calling_frame_info.function
        code = calling_frame_info.frame.f_code
        f = getattr(calling_frame_info.frame.f_locals['self'], code.co_name)
        docstring = inspect.getdoc(f)

        test_config = build_test_match_config(
            name=function_name,
            description=docstring,
            match_config=build_match_spec(
                str(args[1].__class__.__name__),
                str(args[2].__class__.__name__),
                actions_to_str(args[-2]), actions_to_str(args[-1]),
                noise=noise, seed=seed,
                player_init_kwargs=args[1].init_kwargs,
                coplayer_init_kwargs=args[2].init_kwargs,
                match_attributes=match_attributes,
                player_attributes=player_attributes)
        )
        stream = open(filename, 'a')
        stream.write("---\n")
        yaml.dump(asdict(test_config), stream)
        stream.close()
        return func(*args, **kwargs)
    return wrapper


def load_matches():
    stream = open(filename, 'r')
    matches = yaml.load_all(stream, Loader=yaml.Loader)
    return [from_dict(data_class=TestMatchConfig, data=match, config=Config(
        type_hooks={Tuple[Action, ...]: str_to_actions})) for match in matches]


