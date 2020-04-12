import inspect
import re
from typing import Set, Text, Type

from axelrod.player import Player


def makes_use_of(player: Type[Player]) -> Set[Text]:
    result = set()
    for method in inspect.getmembers(player, inspect.ismethod):
        if method[0] == "__init__":
            continue
        method_code = inspect.getsource(method[1])
        attr_string = r"self.match_attributes\[\"(\w+)\"\]"
        all_attrs = re.findall(attr_string, method_code)
        for attr in all_attrs:
            result.add(attr)
    return result
