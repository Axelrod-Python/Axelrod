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


basic_strategies = [
    Alternator,
    Cooperator,
    Defector,
    Random,
    TitForTat,
]

ordinary_strategies = [
    Aggravater,
    AlternatorHunter,
    Appeaser,
    AntiCycler,
    AntiTitForTat,
    ArrogantQLearner,
    AverageCopier,
    BackStabber,
    Bully,
    Calculator,
    CautiousQLearner,
    Champion,
    CooperatorHunter,
    CyclerCCD,
    CyclerCCCD,
    CyclerCCCCCD,
    Davis,
    DefectorHunter,
    DoubleCrosser,
    Eatherley,
    FoolMeOnce,
    FoolMeForever,
    ForgetfulFoolMeOnce,
    ForgetfulGrudger,
    Forgiver,
    ForgivingTitForTat,
    GTFT,
    GoByMajority,
    GoByMajority10,
    GoByMajority20,
    GoByMajority40,
    GoByMajority5,
    Feld,
    Golden,
    Grofman,
    Grudger,
    Grumpy,
    HardProber,
    HardTitForTat,
    HardTitFor2Tats,
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
    NiceAverageCopier,
    OnceBitten,
    OppositeGrudger,
    Pi,
    Prober,
    Prober2,
    Prober3,
    Punisher,
    RandomHunter,
    Retaliate,
    Retaliate2,
    Retaliate3,
    RiskyQLearner,
    Shubik,
    SoftJoss,
    SneakyTitForTat,
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

# These are strategies that do not follow the rules of Axelrods tournament
cheating_strategies = [
    Darwin,
    Geller,
    GellerCooperator,
    GellerDefector,
    MindBender,
    MindController,
    MindReader,
    MindWarper,
    ProtectedMindReader,
]
