from typing import NewType

C = NewType('Action', str)
D = NewType('Action', str)

class Actions(object):
    C = 'C'
    D = 'D'


def flip_action(action: Action) -> Action:
    if action == Actions.C:
        return Actions.D
    elif action == Actions.D:
        return Actions.C
    else:
        raise ValueError("Encountered a invalid action.")
