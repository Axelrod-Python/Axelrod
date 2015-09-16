from ..player import is_basic, is_cheater
from ._strategies import *

# `from ._strategies import *` import the collection `strategies`
# Now import the Meta strategies. This cannot be done in _strategies
# because it creates circular dependencies

from .meta import MetaMajority, MetaMinority, MetaWinner, MetaHunter
strategies.extend((MetaHunter, MetaMajority, MetaMinority, MetaWinner))

# Distinguished strategy collections in addition to
# `strategies` from _strategies.py

demo_strategies = [Cooperator, Defector, TitForTat, Grudger, Random]
basic_strategies = [s for s in strategies if is_basic(s())]
ordinary_strategies = [s for s in strategies if not is_cheater(s())]
cheating_strategies = [s for s in strategies if is_cheater(s())]
