import inspect
import re
from typing import Callable, Set, Text, Type, Union

from axelrod.player import Player


def method_makes_use_of(method: Callable) -> Set[Text]:
    result = set()
    method_code = inspect.getsource(method)
    attr_string = r".match_attributes\[\"(\w+)\"\]"
    all_attrs = re.findall(attr_string, method_code)
    for attr in all_attrs:
        result.add(attr)
    return result


def makes_use_of(player: Type[Player]) -> Set[Text]:
    if not isinstance(player, Player):
        player = player()

    result = set()
    for method in inspect.getmembers(player, inspect.ismethod):
        if method[0] == "__init__":
            continue
        result.update(method_makes_use_of(method[1]))
    return result


# def makes_use_of_variant(
#     player_or_method: Union[Callable, Type[Player]], verbose=False
# ) -> Set[Text]:
#     """A version of makes_use_of that works on functions or player classes."""
#     try:
#         return method_makes_use_of(player_or_method)
#     except:
#         return makes_use_of(player_or_method)
