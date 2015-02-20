from cooperator import *
from defector import *
from grudger import *
from rand import *
from titfortat import *
from gobymajority import *
from alternator import *
from grumpy import *
from mindreader import *
from averagecopier import *
from grumpy import *

#These are strategies that follow the rules of Axelrods tournement, which can be found in the readme
strategies = [
        Defector,
        Cooperator,
        TitForTat,
        Grudger,
        GoByMajority,
        Random,
        Alternator,
        Grumpy,
        AverageCopier,
        Grumpy,
        ]

#These are strategies that do not follow the rules of Axelrods tournement.
cheating_strategies = [
        MindReader,
        ]
