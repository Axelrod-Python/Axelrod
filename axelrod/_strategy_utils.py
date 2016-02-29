"""Utilities used by various strategies"""

def detect_cycle(history, min_size=1, offset=0):
    """Detects cycles in the sequence history.

    Mainly used by hunter strategies.

    Parameters

    history: sequence of C and D
        The sequence to look for cycles within
    min_size: int, 1
        The minimum length of the cycle
    offset: int, 0
        The amount of history to skip initially
    """
    history_tail = history[-offset:]
    for i in range(min_size, len(history_tail) // 2):
        cycle = tuple(history_tail[:i])
        for j,  elem in enumerate(history_tail):
            if elem != cycle[j % len(cycle)]:
                break
        if j == len(history_tail) - 1:
            # We made it to the end, is the cycle itself a cycle?
            # I.E. CCC is not ok as cycle if min_size is really 2
            # Since this is the same as C
            return cycle
    return None
