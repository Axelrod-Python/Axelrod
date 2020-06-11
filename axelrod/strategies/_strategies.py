"""
This file imports all the strategies in to the base name space. Note that some
of the imports are imports of classes that make generic classes available to
users. In these cases the imports are done separately so that they can be
annotated as to avoid some static testing. For example:

    from .memoryone import (
        GTFT,
        ALLCorALLD,
        FirmButFair,
        SoftJoss,
        StochasticCooperator,
        StochasticWSLS,
        WinShiftLoseStay,
        WinStayLoseShift,
    )
    from .memoryone import ( # pylint: disable=unused-import
        ReactivePlayer,
        MemoryOnePlayer
    )
    # isort:skip_file
"""
from .adaptive import Adaptive
from .adaptor import AdaptorBrief, AdaptorLong
from .alternator import Alternator
from .ann import EvolvedANN, EvolvedANN5, EvolvedANNNoise05
from .ann import ANN, EvolvableANN  # pylint: disable=unused-import
from .apavlov import APavlov2006, APavlov2011
from .appeaser import Appeaser
from .averagecopier import AverageCopier, NiceAverageCopier
from .axelrod_first import (
    FirstByDavis,
    FirstByFeld,
    FirstByGraaskamp,
    FirstByGrofman,
    FirstByJoss,
    FirstByNydegger,
    FirstByDowning,
    FirstByShubik,
    FirstBySteinAndRapoport,
    FirstByTidemanAndChieruzzi,
    FirstByTullock,
    FirstByAnonymous,
)
from .axelrod_second import (
    SecondByAppold,
    SecondByBlack,
    SecondByBorufsen,
    SecondByCave,
    SecondByChampion,
    SecondByColbert,
    SecondByEatherley,
    SecondByGetzler,
    SecondByGladstein,
    SecondByGraaskampKatzen,
    SecondByHarrington,
    SecondByKluepfel,
    SecondByLeyvraz,
    SecondByMikkelson,
    SecondByGrofman,
    SecondByTidemanAndChieruzzi,
    SecondByRichardHufford,
    SecondByRowsam,
    SecondByTester,
    SecondByTranquilizer,
    SecondByWeiner,
    SecondByWhite,
    SecondByWmAdams,
    SecondByYamachi,
)
from .backstabber import BackStabber, DoubleCrosser
from .better_and_better import BetterAndBetter
from .bush_mosteller import BushMosteller
from .calculator import Calculator
from .cooperator import Cooperator, TrickyCooperator
from .cycler import (
    AntiCycler,
    CyclerCCCCCD,
    CyclerCCCD,
    CyclerCCCDCD,
    CyclerCCD,
    CyclerDC,
    CyclerDDC,
)
from .cycler import Cycler, EvolvableCycler  # pylint: disable=unused-import
from .darwin import Darwin
from .dbs import DBS
from .defector import Defector, TrickyDefector
from .doubler import Doubler
from .finite_state_machines import (
    TF1,
    TF2,
    TF3,
    EvolvedFSM4,
    EvolvedFSM16,
    EvolvedFSM16Noise05,
    Fortress3,
    Fortress4,
    Predator,
    Pun1,
    Raider,
    Ripoff,
    UsuallyCooperates,
    UsuallyDefects,
    SolutionB1,
    SolutionB5,
    Thumper,
)
from .finite_state_machines import (  # pylint: disable=unused-import
    EvolvableFSMPlayer,
    FSMPlayer,
)
from .forgiver import Forgiver, ForgivingTitForTat
from .gambler import (
    PSOGambler1_1_1,
    PSOGambler2_2_2,
    PSOGambler2_2_2_Noise05,
    PSOGamblerMem1,
    ZDMem2,
)
from .gambler import EvolvableGambler, Gambler  # pylint: disable=unused-import
from .geller import Geller, GellerCooperator, GellerDefector
from .gobymajority import (
    GoByMajority,
    GoByMajority5,
    GoByMajority10,
    GoByMajority20,
    GoByMajority40,
    HardGoByMajority,
    HardGoByMajority5,
    HardGoByMajority10,
    HardGoByMajority20,
    HardGoByMajority40,
)
from .gradualkiller import GradualKiller
from .grudger import (
    Aggravater,
    EasyGo,
    ForgetfulGrudger,
    GeneralSoftGrudger,
    Grudger,
    GrudgerAlternator,
    OppositeGrudger,
    SoftGrudger,
)
from .grumpy import Grumpy
from .handshake import Handshake
from .hmm import EvolvedHMM5
from .hmm import EvolvableHMMPlayer, HMMPlayer  # pylint: disable=unused-import
from .human import Human  # pylint: disable=unused-import
from .hunter import (
    AlternatorHunter,
    CooperatorHunter,
    CycleHunter,
    DefectorHunter,
    EventualCycleHunter,
    MathConstantHunter,
    RandomHunter,
)
from .inverse import Inverse
from .lookerup import (
    EvolvedLookerUp1_1_1,
    EvolvedLookerUp2_2_2,
    Winner12,
    Winner21,
)
from .lookerup import (  # pylint: disable=unused-import
    EvolvableLookerUp,
    LookerUp,
)

from .mathematicalconstants import Golden, Pi, e
from .memoryone import (
    GTFT,
    ALLCorALLD,
    FirmButFair,
    SoftJoss,
    StochasticCooperator,
    StochasticWSLS,
    WinShiftLoseStay,
    WinStayLoseShift,
)
from .memoryone import (  # pylint: disable=unused-import
    ReactivePlayer,
    MemoryOnePlayer,
)

from .memorytwo import AON2, MEM2, DelayedAON1
from .memorytwo import MemoryTwoPlayer  # pylint: disable=unused-import

from .mindcontrol import MindBender, MindController, MindWarper
from .mindreader import MindReader, MirrorMindReader, ProtectedMindReader
from .mutual import Desperate, Hopeless, Willing
from .negation import Negation
from .oncebitten import FoolMeOnce, ForgetfulFoolMeOnce, OnceBitten
from .prober import (
    CollectiveStrategy,
    Detective,
    HardProber,
    NaiveProber,
    Prober,
    Prober2,
    Prober3,
    Prober4,
    RemorsefulProber,
)
from .punisher import (
    InversePunisher,
    LevelPunisher,
    Punisher,
    TrickyLevelPunisher,
)
from .qlearner import (
    ArrogantQLearner,
    CautiousQLearner,
    HesitantQLearner,
    RiskyQLearner,
)
from .rand import Random
from .resurrection import DoubleResurrection, Resurrection
from .retaliate import (
    LimitedRetaliate,
    LimitedRetaliate2,
    LimitedRetaliate3,
    Retaliate,
    Retaliate2,
    Retaliate3,
)
from .revised_downing import RevisedDowning
from .selfsteem import SelfSteem
from .sequence_player import (  # pylint: disable=unused-import
    SequencePlayer,
    ThueMorse,
    ThueMorseInverse,
)
from .shortmem import ShortMem
from .stalker import Stalker
from .titfortat import (
    AdaptiveTitForTat,
    Alexei,
    AntiTitForTat,
    Bully,
    ContriteTitForTat,
    DynamicTwoTitsForTat,
    EugineNier,
    Gradual,
    HardTitFor2Tats,
    HardTitForTat,
    Michaelos,
    NTitsForMTats,
    OmegaTFT,
    OriginalGradual,
    RandomTitForTat,
    SlowTitForTwoTats2,
    SneakyTitForTat,
    SpitefulTitForTat,
    SuspiciousTitForTat,
    TitFor2Tats,
    TitForTat,
    TwoTitsForTat,
)
from .verybad import VeryBad
from .worse_and_worse import (
    KnowledgeableWorseAndWorse,
    WorseAndWorse,
    WorseAndWorse2,
    WorseAndWorse3,
)
from .zero_determinant import (
    ZDGTFT2,
    ZDExtort2,
    ZDExtort2v2,
    ZDExtort3,
    ZDExtort4,
    ZDExtortion,
    ZDGen2,
    ZDMischief,
    ZDSet2,
)

# Note: Meta* strategies are handled in .__init__.py


all_strategies = [
    ALLCorALLD,
    AON2,
    APavlov2006,
    APavlov2011,
    Adaptive,
    AdaptiveTitForTat,
    AdaptorBrief,
    AdaptorLong,
    Aggravater,
    Alexei,
    Alternator,
    AlternatorHunter,
    AntiCycler,
    AntiTitForTat,
    Appeaser,
    ArrogantQLearner,
    AverageCopier,
    BackStabber,
    BetterAndBetter,
    Bully,
    BushMosteller,
    Calculator,
    CautiousQLearner,
    CollectiveStrategy,
    ContriteTitForTat,
    Cooperator,
    CooperatorHunter,
    CycleHunter,
    CyclerCCCCCD,
    CyclerCCCD,
    CyclerCCCDCD,
    CyclerCCD,
    CyclerDC,
    CyclerDDC,
    DBS,
    Darwin,
    Defector,
    DefectorHunter,
    DelayedAON1,
    Desperate,
    Detective,
    DoubleCrosser,
    DoubleResurrection,
    Doubler,
    DynamicTwoTitsForTat,
    EasyGo,
    EugineNier,
    EventualCycleHunter,
    EvolvedANN,
    EvolvedANN5,
    EvolvedANNNoise05,
    EvolvedFSM16,
    EvolvedFSM16Noise05,
    EvolvedFSM4,
    EvolvedHMM5,
    EvolvedLookerUp1_1_1,
    EvolvedLookerUp2_2_2,
    FirmButFair,
    FirstByAnonymous,
    FirstByDavis,
    FirstByDowning,
    FirstByFeld,
    FirstByGraaskamp,
    FirstByGrofman,
    FirstByJoss,
    FirstByNydegger,
    FirstByShubik,
    FirstBySteinAndRapoport,
    FirstByTidemanAndChieruzzi,
    FirstByTullock,
    FoolMeOnce,
    ForgetfulFoolMeOnce,
    ForgetfulGrudger,
    Forgiver,
    ForgivingTitForTat,
    Fortress3,
    Fortress4,
    GTFT,
    Geller,
    GellerCooperator,
    GellerDefector,
    GeneralSoftGrudger,
    GoByMajority,
    GoByMajority10,
    GoByMajority20,
    GoByMajority40,
    GoByMajority5,
    Golden,
    Gradual,
    GradualKiller,
    Grudger,
    GrudgerAlternator,
    Grumpy,
    Handshake,
    HardGoByMajority,
    HardGoByMajority10,
    HardGoByMajority20,
    HardGoByMajority40,
    HardGoByMajority5,
    HardProber,
    HardTitFor2Tats,
    HardTitForTat,
    HesitantQLearner,
    Hopeless,
    Inverse,
    InversePunisher,
    KnowledgeableWorseAndWorse,
    LevelPunisher,
    LimitedRetaliate,
    LimitedRetaliate2,
    LimitedRetaliate3,
    MEM2,
    MathConstantHunter,
    Michaelos,
    MindBender,
    MindController,
    MindReader,
    MindWarper,
    MirrorMindReader,
    NTitsForMTats,
    NaiveProber,
    Negation,
    NiceAverageCopier,
    OmegaTFT,
    OnceBitten,
    OppositeGrudger,
    OriginalGradual,
    PSOGambler1_1_1,
    PSOGambler2_2_2,
    PSOGambler2_2_2_Noise05,
    PSOGamblerMem1,
    Pi,
    Predator,
    Prober,
    Prober2,
    Prober3,
    Prober4,
    ProtectedMindReader,
    Pun1,
    Punisher,
    Raider,
    Random,
    RandomHunter,
    RandomTitForTat,
    RemorsefulProber,
    Resurrection,
    Retaliate,
    Retaliate2,
    Retaliate3,
    RevisedDowning,
    Ripoff,
    RiskyQLearner,
    SecondByAppold,
    SecondByBlack,
    SecondByBorufsen,
    SecondByCave,
    SecondByChampion,
    SecondByColbert,
    SecondByEatherley,
    SecondByGetzler,
    SecondByGladstein,
    SecondByGraaskampKatzen,
    SecondByGrofman,
    SecondByHarrington,
    SecondByKluepfel,
    SecondByLeyvraz,
    SecondByMikkelson,
    SecondByRichardHufford,
    SecondByRowsam,
    SecondByTester,
    SecondByTidemanAndChieruzzi,
    SecondByTranquilizer,
    SecondByWeiner,
    SecondByWhite,
    SecondByWmAdams,
    SecondByYamachi,
    SelfSteem,
    ShortMem,
    SlowTitForTwoTats2,
    SneakyTitForTat,
    SoftGrudger,
    SoftJoss,
    SolutionB1,
    SolutionB5,
    SpitefulTitForTat,
    Stalker,
    StochasticCooperator,
    StochasticWSLS,
    SuspiciousTitForTat,
    TF1,
    TF2,
    TF3,
    ThueMorse,
    ThueMorseInverse,
    Thumper,
    TitFor2Tats,
    TitForTat,
    TrickyCooperator,
    TrickyDefector,
    TrickyLevelPunisher,
    TwoTitsForTat,
    UsuallyCooperates,
    UsuallyDefects,
    VeryBad,
    Willing,
    WinShiftLoseStay,
    WinStayLoseShift,
    Winner12,
    Winner21,
    WorseAndWorse,
    WorseAndWorse2,
    WorseAndWorse3,
    ZDExtort2,
    ZDExtort2v2,
    ZDExtort3,
    ZDExtort4,
    ZDExtortion,
    ZDGTFT2,
    ZDGen2,
    ZDMem2,
    ZDMischief,
    ZDSet2,
    e,
]
