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


def str_to_actions(actions: str):
    """Takes a string like 'cCdD' and returns a generator that yields the appropriate actions."""
    for character in actions:
        as_upper = character.upper()
        if as_upper == 'C':
            yield Actions.C
        elif as_upper == 'D':
            yield Actions.D
        else:
            raise ValueError('The characters of action_str may only be "C", "c", "D" and "d"')
