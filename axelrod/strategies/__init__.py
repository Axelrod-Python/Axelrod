# isort:skip_file
from ..classifier import Classifiers
from ._strategies import *
from ._filters import passes_filterset

# `from ._strategies import *` import the collection `strategies`
# Now import the Meta strategies. This cannot be done in _strategies
# because it creates circular dependencies

from .meta import (
    MemoryDecay,
    MetaHunter,
    MetaHunterAggressive,
    MetaPlayer,
    MetaMajority,
    MetaMajorityMemoryOne,
    MetaMajorityFiniteMemory,
    MetaMajorityLongMemory,
    MetaMinority,
    MetaMixer,
    MetaWinner,
    MetaWinnerDeterministic,
    MetaWinnerEnsemble,
    MetaWinnerMemoryOne,
    MetaWinnerFiniteMemory,
    MetaWinnerLongMemory,
    MetaWinnerStochastic,
    NMWEDeterministic,
    NMWEFiniteMemory,
    NMWELongMemory,
    NMWEMemoryOne,
    NMWEStochastic,
    NiceMetaWinner,
    NiceMetaWinnerEnsemble,
)

all_strategies += [
    MemoryDecay,
    MetaHunter,
    MetaHunterAggressive,
    MetaMajority,
    MetaMajorityMemoryOne,
    MetaMajorityFiniteMemory,
    MetaMajorityLongMemory,
    MetaMinority,
    MetaMixer,
    MetaWinner,
    MetaWinnerDeterministic,
    MetaWinnerEnsemble,
    MetaWinnerMemoryOne,
    MetaWinnerFiniteMemory,
    MetaWinnerLongMemory,
    MetaWinnerStochastic,
    NMWEDeterministic,
    NMWEFiniteMemory,
    NMWELongMemory,
    NMWEMemoryOne,
    NMWEStochastic,
    NiceMetaWinner,
    NiceMetaWinnerEnsemble,
]


# Distinguished strategy collections in addition to
# `all_strategies` from _strategies.py
demo_strategies = [Cooperator, Defector, TitForTat, Grudger, Random]
axelrod_first_strategies = [
    TitForTat,
    FirstByTidemanAndChieruzzi,
    FirstByNydegger,
    FirstByGrofman,
    FirstByShubik,
    FirstBySteinAndRapoport,
    Grudger,
    FirstByDavis,
    FirstByGraaskamp,
    FirstByDowning,
    FirstByFeld,
    FirstByJoss,
    FirstByTullock,
    FirstByAnonymous,
    Random,
]
basic_strategies = [s for s in all_strategies if Classifiers.is_basic(s())]
strategies = [s for s in all_strategies if Classifiers.obey_axelrod(s())]

long_run_time_strategies = [
    s for s in all_strategies if Classifiers["long_run_time"](s())
]
short_run_time_strategies = [
    s for s in strategies if not Classifiers["long_run_time"](s())
]
cheating_strategies = [s for s in all_strategies if not Classifiers.obey_axelrod(s())]

ordinary_strategies = strategies  # This is a legacy and will be removed


def filtered_strategies(filterset, strategies=all_strategies):
    """
    Applies the filters defined in the given filterset dict and returns those
    strategy classes which pass all of those filters from the given list of
    strategies.

    e.g.

    For the filterset dict:
        {
            'stochastic': True,
            'min_memory_depth': 2
        }

    the function will return a list of all deterministic strategies with a
    memory_depth of 2 or more.

    Parameters
    ----------
        filterset : dict
            mapping filter name to criterion.
            e.g.
                {
                    'stochastic': True,
                    'min_memory_depth': 2
                }
        strategies: list
            of subclasses of axelrod.Player

    Returns
    -------
        list

        of subclasses of axelrod.Player

    """
    return [s for s in strategies if passes_filterset(s, filterset)]
