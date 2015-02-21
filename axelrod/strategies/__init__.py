from cooperator import *
from defector import *
from grudger import *
from rand import *
from titfortat import *
from gobymajority import *
from alternator import *
from grumpy import *
from averagecopier import *
from grumpy import *
from geller import *
from inverse import *
from forgiver import *

strategies = [
        Defector,
        Cooperator,
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
        Forgiver,
        ]

#These are strategies that do not follow the rules of Axelrods tournement.
cheating_strategies = [
        Geller,
        ]
