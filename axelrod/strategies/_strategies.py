from alternator import *
from appeaser import *
from averagecopier import *
from backstabber import *
from cooperator import *
from darwin import *
from defector import *
from forgiver import *
from geller import *
from gobymajority import *
from grudger import *
from grumpy import *
from hunter import *
from inverse import *
from mathematicalconstants import *
from memoryone import *
from meta import *
from mindcontrol import *
from mindreader import *
from oncebitten import *
from punisher import *
from qlearner import *
from rand import *
from retaliate import *
from titfortat import *

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
    AntiTitForTat,
    ArrogantQLearner,
    AverageCopier,
    BackStabber,
    Bully,
    CautiousQLearner,
    CooperatorHunter,
    Davis,
    DefectorHunter,
    FoolMeOnce,
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
