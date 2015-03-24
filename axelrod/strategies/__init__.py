from alternator import *
from appeaser import *
from averagecopier import *
from cooperator import *
from darwin import *
from defector import *
from forgiver import *
from geller import *
from gobymajority import *
from grudger import *
from grumpy import *
from inverse import *
from mathematicalconstants import *
from memoryone import *
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
    Appeaser,
    ArrogantQLearner,
    AverageCopier,
    CautiousQLearner,
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
    Golden,
    Grudger,
    Grumpy,
    HesitantQLearner,
    Inverse,
    InversePunisher,
    LimitedRetaliate,
    LimitedRetaliate2,
    LimitedRetaliate3,
    NiceAverageCopier,
    OnceBitten,
    OppositeGrudger,
    Pi,
    Punisher,
    Retaliate,
    Retaliate2,
    Retaliate3,
    RiskyQLearner,
    SneakyTitForTat,
    StochasticWSLS,
    SuspiciousTitForTat,
    TitFor2Tats,
    TrickyCooperator,
    TrickyDefector,
    TwoTitsForTat,
    WinStayLoseShift,
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
