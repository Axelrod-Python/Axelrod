from __future__ import absolute_import

from .alternator import *
from .appeaser import *
from .averagecopier import *
from .axelrod_tournaments import *
from .backstabber import *
from .calculator import Calculator
from .cooperator import *
from .cycler import *
from .darwin import *
from .defector import *
from .forgiver import *
from .geller import *
from .gobymajority import *
from .grudger import *
from .grumpy import *
from .hunter import *
from .inverse import *
from .mathematicalconstants import *
from .memoryone import *
from .meta import *
from .mindcontrol import *
from .mindreader import *
from .oncebitten import *
from .prober import *
from .punisher import *
from .qlearner import *
from .rand import *
from .retaliate import *
from .titfortat import *

# A list of strategies to quickly create a tournament
basic_strategies = [
    Alternator,
    Cooperator,
    Defector,
    Random,
    TitForTat,
]

# All the strategies in the tournament
strategies = basic_strategies + [
    Aggravater,
    AlternatorHunter,
    AntiCycler,
    AntiTitForTat,
    Appeaser,
    ArrogantQLearner,
    AverageCopier,
    BackStabber,
    Bully,
    Calculator,
    CautiousQLearner,
    Champion,
    CooperatorHunter,
    CyclerCCCCCD,
    CyclerCCCD,
    CyclerCCD,
    Darwin,
    Davis,
    DefectorHunter,
    DoubleCrosser,
    Eatherley,
    Feld,
    FoolMeForever,
    FoolMeOnce,
    ForgetfulFoolMeOnce,
    ForgetfulGrudger,
    Forgiver,
    ForgivingTitForTat,
    GTFT,
    Geller,
    GellerCooperator,
    GellerDefector,
    GoByMajority,
    GoByMajority10,
    GoByMajority20,
    GoByMajority40,
    GoByMajority5,
    Golden,
    Grofman,
    Grudger,
    Grumpy,
    HardProber,
    HardTitFor2Tats,
    HardTitForTat,
    HesitantQLearner,
    Inverse,
    InversePunisher,
    Joss,
    LimitedRetaliate,
    LimitedRetaliate2,
    LimitedRetaliate3,
    MathConstantHunter,
    MetaHunter,
    MetaMajority,
    MetaMinority,
    MetaWinner,
    MindBender,
    MindController,
    MindReader,
    MindWarper,
    NiceAverageCopier,
    OnceBitten,
    OppositeGrudger,
    Pi,
    Prober,
    Prober2,
    Prober3,
    ProtectedMindReader,
    Punisher,
    RandomHunter,
    Retaliate,
    Retaliate2,
    Retaliate3,
    RiskyQLearner,
    Shubik,
    SneakyTitForTat,
    SoftJoss,
    StochasticWSLS,
    SuspiciousTitForTat,
    Tester,
    TitFor2Tats,
    TrickyCooperator,
    TrickyDefector,
    Tullock,
    TwoTitsForTat,
    WinStayLoseShift,
    ZDExtort2,
    ZDGTFT2,
    e,
    ]


def is_cheater(s):
    """
    A function to check if a strategy cheats.
    """
    classifier = s.classifier
    return classifier['inspects_source'] or\
           classifier['manipulates_source'] or\
           classifier['manipulates_state']

ordinary_strategies = [s for s in strategies if not is_cheater(s)]
cheating_strategies = [s for s in strategies if is_cheater(s)]
