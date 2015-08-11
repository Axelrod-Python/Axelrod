import random

def random_choice(p=0.5):
    """
    Return 'C' with probability `p`, else return 'D'

    Emulates Python's random.choice(['C', 'D']) since it is not consistent
    across Python 2.7 to Python 3.4"""

    r = random.random()
    if r < p:
        return 'C'
    return 'D'
