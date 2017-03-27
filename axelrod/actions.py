# Type alias for actions.
Action = str


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


def str_to_actions(actions: str) -> tuple:
    """Takes a string like 'CCDD' and returns a tuple of the appropriate actions."""
    action_dict = {'C': Actions.C,
                   'D': Actions.D}
    try:
        return tuple(action_dict[action] for action in actions)
    except KeyError:
        raise ValueError('The characters of "actions" str may only be "C" or "D"')
