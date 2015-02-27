from cooperator import *
from defector import *
from grudger import *
from rand import *
from titfortat import *
from gobymajority import *
from alternator import *
from grumpy import *
from averagecopier import *
from qlearner import *
from grumpy import *
from geller import *
from inverse import *
from appeaser import *
from forgiver import *
from forgetfulgrudger import *
from punisher import *
from inversepunisher import *
from oppositegrudger import *
from oncebitten import *
from mathematicalconstants import *
from retaliate import *
from mindcontrol import *
from mindreader import *

strategies = [
        Defector,
        TrickyDefector,
        Cooperator,
        TrickyCooperator,
        AntiTitForTat,
        TitForTat,
        TitFor2Tats,
        TwoTitsForTat,
        Grudger,
        GoByMajority,
        GoByMajority5,
        GoByMajority10,
        GoByMajority20,
        GoByMajority40,
        Random,
        Alternator,
        Grumpy,
        Inverse,
        AverageCopier,
        Appeaser,
        Forgiver,
        ForgivingTitForTat,
        RiskyQLearner,
        ArrogantQLearner,
        HesitantQLearner,
        CautiousQLearner,
        ForgetfulGrudger,
        Punisher,
        InversePunisher,
        OppositeGrudger,
        OnceBitten,
        Golden,
        Retaliate,
        Pi,
        e,
        LimitedRetaliate,
        ]

#These are strategies that do not follow the rules of Axelrods tournement.
cheating_strategies = [
        Geller,
        GellerCooperator,
        GellerDefector,
        MindControl,
        MindWarp,
        MindReader,
        ProtectedMindReader,
        ]
