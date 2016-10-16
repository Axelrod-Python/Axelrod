from __future__ import absolute_import

from .alternator import Alternator
from .adaptive import Adaptive
from .apavlov import APavlov2006, APavlov2011
from .appeaser import Appeaser
from .averagecopier import AverageCopier, NiceAverageCopier
from .axelrod_first import (Davis, RevisedDowning, Feld, Grofman, Nydegger,
                            Joss, Shubik, Tullock, UnnamedStrategy)
from .axelrod_second import Champion, Eatherley, Tester
from .backstabber import BackStabber, DoubleCrosser
from .calculator import Calculator
from .cooperator import Cooperator, TrickyCooperator
from .cycler import (
    AntiCycler, Cycler, CyclerCCD, CyclerCCCD, CyclerCCCCCD,
    CyclerDC, CyclerDDC, CyclerCCCDCD)
from .darwin import Darwin
from .defector import Defector, TrickyDefector
from .finite_state_machines import (
    Fortress3, Fortress4, Predator, Raider, Ripoff, SolutionB1, SolutionB5,
    Thumper, FSMPlayer)
from .forgiver import Forgiver, ForgivingTitForTat
from .geller import Geller, GellerCooperator, GellerDefector
from .gambler import Gambler, PSOGambler
from .gobymajority import (GoByMajority,
    GoByMajority10, GoByMajority20, GoByMajority40,
    GoByMajority5,
    HardGoByMajority, HardGoByMajority10, HardGoByMajority20, HardGoByMajority40,
    HardGoByMajority5)
from .gradualkiller import GradualKiller
from .grudger import (Grudger, ForgetfulGrudger, OppositeGrudger, Aggravater,
    SoftGrudger, GrudgerAlternator, EasyGo)
from .grumpy import Grumpy
from .handshake import Handshake
from .human import Human
from .hunter import (
    DefectorHunter, CooperatorHunter, CycleHunter, AlternatorHunter,
    MathConstantHunter, RandomHunter, EventualCycleHunter)
from .inverse import Inverse
from .lookerup import LookerUp, EvolvedLookerUp
from .mathematicalconstants import Golden, Pi, e
from .memoryone import (
    MemoryOnePlayer, ALLCorALLD, FirmButFair, GTFT, SoftJoss,
    StochasticCooperator, StochasticWSLS, ZDExtort2, ZDExtort2v2, ZDExtort4,
    ZDGen2, ZDGTFT2, ZDSet2, WinStayLoseShift, WinShiftLoseStay)
from .mindcontrol import MindController, MindWarper, MindBender
from .mindreader import MindReader, ProtectedMindReader, MirrorMindReader
from .mutual import Desperate, Hopeless, Willing
from .oncebitten import OnceBitten, FoolMeOnce, ForgetfulFoolMeOnce, FoolMeForever
from .prober import (Prober, Prober2, Prober3, Prober4, HardProber,
                     NaiveProber, RemorsefulProber)
from .punisher import Punisher, InversePunisher
from .qlearner import RiskyQLearner, ArrogantQLearner, HesitantQLearner, CautiousQLearner
from .rand import Random
from .retaliate import (
    Retaliate, Retaliate2, Retaliate3, LimitedRetaliate, LimitedRetaliate2,
    LimitedRetaliate3)
from .sequence_player import SequencePlayer, ThueMorse, ThueMorseInverse
from .titfortat import (
    TitForTat, TitFor2Tats, TwoTitsForTat, Bully, SneakyTitForTat,
    SuspiciousTitForTat, AntiTitForTat, HardTitForTat, HardTitFor2Tats,
    OmegaTFT, Gradual, ContriteTitForTat, SlowTitForTwoTats, AdaptiveTitForTat)
from .worse_and_worse import (WorseAndWorse, KnowledgeableWorseAndWorse)

# Note: Meta* strategies are handled in .__init__.py

all_strategies = [
    Adaptive,
    AdaptiveTitForTat,
    Aggravater,
    ALLCorALLD,
    Alternator,
    AlternatorHunter,
    AntiCycler,
    AntiTitForTat,
    APavlov2006,
    APavlov2011,
    Appeaser,
    ArrogantQLearner,
    AverageCopier,
    BackStabber,
    Bully,
    Calculator,
    CautiousQLearner,
    Champion,
    ContriteTitForTat,
    Cooperator,
    CooperatorHunter,
    CycleHunter,
    CyclerCCCCCD,
    CyclerCCCD,
    CyclerCCD,
    CyclerDC,
    CyclerDDC,
    CyclerCCCDCD,
    Darwin,
    Davis,
    Defector,
    DefectorHunter,
    Desperate,
    DoubleCrosser,
    EasyGo,
    Eatherley,
    EventualCycleHunter,
    Feld,
    FirmButFair,
    FoolMeForever,
    FoolMeOnce,
    ForgetfulFoolMeOnce,
    ForgetfulGrudger,
    Forgiver,
    ForgivingTitForTat,
    Fortress3,
    Fortress4,
    PSOGambler,
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
    Gradual,
    GradualKiller,
    Grofman,
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
    Joss,
    KnowledgeableWorseAndWorse,
    LimitedRetaliate,
    LimitedRetaliate2,
    LimitedRetaliate3,
    EvolvedLookerUp,
    MathConstantHunter,
    NaiveProber,
    MindBender,
    MindController,
    MindReader,
    MindWarper,
    MirrorMindReader,
    NiceAverageCopier,
    Nydegger,
    OmegaTFT,
    OnceBitten,
    OppositeGrudger,
    Pi,
    Predator,
    Prober,
    Prober2,
    Prober3,
    Prober4,
    ProtectedMindReader,
    Punisher,
    Raider,
    Random,
    RandomHunter,
    RemorsefulProber,
    Retaliate,
    Retaliate2,
    Retaliate3,
    Ripoff,
    RiskyQLearner,
    Shubik,
    SlowTitForTwoTats,
    SneakyTitForTat,
    SoftGrudger,
    SoftJoss,
    SolutionB1,
    SolutionB5,
    StochasticWSLS,
    SuspiciousTitForTat,
    Tester,
    ThueMorse,
    ThueMorseInverse,
    Thumper,
    TitForTat,
    TitFor2Tats,
    TrickyCooperator,
    TrickyDefector,
    Tullock,
    TwoTitsForTat,
    Willing,
    WinShiftLoseStay,
    WinStayLoseShift,
    WorseAndWorse,
    ZDExtort2,
    ZDExtort2v2,
    ZDExtort4,
    ZDGTFT2,
    ZDGen2,
    ZDSet2,
    e,
]
