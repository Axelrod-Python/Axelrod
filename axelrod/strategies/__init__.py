from ..player import is_basic, obey_axelrod
from ._strategies import *

# `from ._strategies import *` import the collection `strategies`
# Now import the Meta strategies. This cannot be done in _strategies
# because it creates circular dependencies

from .meta import (
    MetaPlayer, MetaMajority, MetaMinority, MetaWinner, MetaHunter,
    MetaMajorityMemoryOne, MetaWinnerMemoryOne, MetaMajorityFiniteMemory,
    MetaWinnerFiniteMemory, MetaMajorityLongMemory, MetaWinnerLongMemory,
    MetaMixer
    )

strategies.extend((MetaHunter, MetaMajority, MetaMinority, MetaWinner,
                   MetaMajorityMemoryOne, MetaWinnerMemoryOne,
                   MetaMajorityFiniteMemory, MetaWinnerFiniteMemory,
                   MetaMajorityLongMemory, MetaWinnerLongMemory, MetaMixer))

# Distinguished strategy collections in addition to
# `strategies` from _strategies.py

demo_strategies = [Cooperator, Defector, TitForTat, Grudger, Random]
basic_strategies = [s for s in strategies if is_basic(s())]
ordinary_strategies = [s for s in strategies if obey_axelrod(s())]
cheating_strategies = [s for s in strategies if not obey_axelrod(s())]
