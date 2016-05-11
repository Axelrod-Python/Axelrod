"""
A module for creating hypothesis based strategies for property based testing
"""
import axelrod
from hypothesis.strategies import composite, tuples, sampled_from, integers, floats, random_module, lists


@composite
def strategy_lists(draw, strategies=axelrod.strategies, min_size=1,
                   max_size=len(axelrod.strategies)):
    """
    A hypothesis decorator to return a list of strategies

    Parameters
    ----------
    min_size : integer
        The minimum number of strategies to include
    max_size : integer
        The maximum number of strategies to include
    """
    strategies = draw(lists(sampled_from(strategies), min_size=min_size,
                            max_size=max_size))
    return strategies

@composite
def matches(draw, strategies=axelrod.strategies,
            min_turns=1, max_turns=200,
            min_noise=0, max_noise=1):
    """
    A hypothesis decorator to return a random match as well as a random seed (to
    ensure reproducibility when instance of class need the random library).

    Parameters
    ----------
    strategies : list
        The strategies from which to sample the two the players
    min_turns : integer
        The minimum number of turns
    max_turns : integer
        The maximum number of turns
    min_noise : float
        The minimum noise
    max_noise : float
        The maximum noise

    Returns
    -------
    tuple : a random match as well as a random seed
    """
    seed = draw(random_module())
    strategies = draw(strategy_lists(min_size=2, max_size=2))
    players = [s() for s in strategies]
    turns = draw(integers(min_value=min_turns, max_value=max_turns))
    noise = draw(floats(min_value=min_noise, max_value=max_noise))
    match = axelrod.Match(players, turns=turns, noise=noise)
    return match, seed

@composite
def tournaments(draw, strategies=axelrod.strategies,
                min_size=1, max_size=10,
                min_turns=1, max_turns=200,
                min_noise=0, max_noise=1,
                min_repetitions=1, max_repetitions=20):
    """
    A hypothesis decorator to return a tournament and a random seed (to ensure
    reproducibility for strategies that make use of the random module when
    initiating).

    Parameters
    ----------
    min_size : integer
        The minimum number of strategies to include
    max_size : integer
        The maximum number of strategies to include
    min_turns : integer
        The minimum number of turns
    max_turns : integer
        The maximum number of turns
    min_noise : float
        The minimum noise value
    min_noise : float
        The maximum noise value
    min_repetitions : integer
        The minimum number of repetitions
    max_repetitions : integer
        The maximum number of repetitions
    """
    seed = draw(random_module())
    strategies = draw(strategy_lists(strategies=strategies,
                                     min_size=min_size,
                                     max_size=max_size))
    players = [s() for s in strategies]
    turns = draw(integers(min_value=min_turns, max_value=max_turns))
    repetitions = draw(integers(min_value=min_repetitions,
                                max_value=max_repetitions))
    noise = draw(floats(min_value=min_noise, max_value=max_noise))

    tournament = axelrod.Tournament(players, turns=turns,
                                    repetitions=repetitions, noise=noise)
    return tournament, seed


@composite
def prob_end_tournaments(draw, strategies=axelrod.strategies,
                        min_size=1, max_size=10,
                        min_prob_end=0, max_prob_end=1,
                        min_noise=0, max_noise=1,
                        min_repetitions=1, max_repetitions=20):
    """
    A hypothesis decorator to return a tournament and a random seed (to ensure
    reproducibility for strategies that make use of the random module when
    initiating).

    Parameters
    ----------
    min_size : integer
        The minimum number of strategies to include
    max_size : integer
        The maximum number of strategies to include
    min_prob_end : float
        The minimum probability of a match ending
    max_prob_end : float
        The maximum probability of a match ending
    min_noise : float
        The minimum noise value
    min_noise : float
        The maximum noise value
    min_repetitions : integer
        The minimum number of repetitions
    max_repetitions : integer
        The maximum number of repetitions
    """
    seed = draw(random_module())
    strategies = draw(strategy_lists(strategies=strategies,
                                     min_size=min_size,
                                     max_size=max_size))
    players = [s() for s in strategies]
    prob_end = draw(floats(min_value=min_prob_end, max_value=max_prob_end))
    repetitions = draw(integers(min_value=min_repetitions,
                                max_value=max_repetitions))
    noise = draw(floats(min_value=min_noise, max_value=max_noise))

    tournament = axelrod.ProbEndTournament(players, prob_end=prob_end,
                                           repetitions=repetitions, noise=noise)
    return tournament, seed


@composite
def games(draw, prisoners_dilemma=True, max_value=100):
    """
    A hypothesis decorator to return a random game.

    Parameters
    ----------
    prisoners_dilemma : bool
        If set not True the R,P,S,T values will be uniformly random. True by
        default which ensures T > R > P > S and 2R > T + S.
    max_value : the maximal payoff value
    """

    if prisoners_dilemma:
        s_upper_bound = max_value - 4  # Ensures there is enough room
        s = draw(integers(max_value=s_upper_bound))

        t_lower_bound = s + 3  # Ensures there is enough room
        t = draw(integers(min_value=t_lower_bound, max_value=max_value))

        r_upper_bound = t - 1
        r_lower_bound = min(max(int((t + s) / 2), s) + 2, r_upper_bound)
        r = draw(integers(min_value=r_lower_bound, max_value=r_upper_bound))

        p_lower_bound = s + 1
        p_upper_bound = r - 1
        p = draw(integers(min_value=p_lower_bound, max_value=p_upper_bound))

    else:
        s = draw(integers(max_value=max_value))
        t = draw(integers(max_value=max_value))
        r = draw(integers(max_value=max_value))
        p = draw(integers(max_value=max_value))

    game = axelrod.Game(r=r, s=s, t=t, p=p)
    return game
