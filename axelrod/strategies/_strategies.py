from __future__ import absolute_import

from .alternator import Alternator
from .apavlov import APavlov2006, APavlov2011
from .appeaser import Appeaser
from .averagecopier import AverageCopier, NiceAverageCopier
from .axelrod_first import (Davis, RevisedDowning, Feld, Grofman, Nydegger,
                            Joss, Shubik, Tullock, UnnamedStrategy)
from .axelrod_second import Champion, Eatherley, Tester
from .backstabber import BackStabber, DoubleCrosser
from .calculator import Calculator
from .cooperator import Cooperator, TrickyCooperator
from .cycler import AntiCycler, Cycler, CyclerCCD, CyclerCCCD, CyclerCCCCCD
from .darwin import Darwin
from .defector import Defector, TrickyDefector
from .forgiver import Forgiver, ForgivingTitForTat
from .geller import Geller, GellerCooperator, GellerDefector
from .gobymajority import (
    GoByMajority, GoByMajority10, GoByMajority20, GoByMajority40,
    GoByMajority5)
from .grudger import Grudger, ForgetfulGrudger, OppositeGrudger, Aggravater
from .grumpy import Grumpy
from .hunter import (
    DefectorHunter, CooperatorHunter, CycleHunter, AlternatorHunter,
    MathConstantHunter, RandomHunter, EventualCycleHunter)
from .inverse import Inverse
from .mathematicalconstants import Golden, Pi, e
from .memoryone import (
    WinStayLoseShift, GTFT, StochasticCooperator, StochasticWSLS, ZDGTFT2,
    ZDExtort2, SoftJoss, MemoryOnePlayer)
from .mindcontrol import MindController, MindWarper, MindBender
from .mindreader import MindReader, ProtectedMindReader, MirrorMindReader
from .oncebitten import OnceBitten, FoolMeOnce, ForgetfulFoolMeOnce, FoolMeForever
from .prober import Prober, Prober2, Prober3, HardProber
from .punisher import Punisher, InversePunisher
from .qlearner import RiskyQLearner, ArrogantQLearner, HesitantQLearner, CautiousQLearner
from .rand import Random
from .retaliate import (
    Retaliate, Retaliate2, Retaliate3, LimitedRetaliate, LimitedRetaliate2,
    LimitedRetaliate3)
from .titfortat import (
    TitForTat, TitFor2Tats, TwoTitsForTat, Bully, SneakyTitForTat,
    SuspiciousTitForTat, AntiTitForTat, HardTitForTat, HardTitFor2Tats,
    OmegaTFT)


# Note: Meta* strategies are handled in .__init__.py

strategies = [
    Aggravater,
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
    Cooperator,
    CooperatorHunter,
    CycleHunter,
    CyclerCCCCCD,
    CyclerCCCD,
    CyclerCCD,
    Darwin,
    Davis,
    Defector,
    DefectorHunter,
    DoubleCrosser,
    Eatherley,
    EventualCycleHunter,
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
    Prober,
    Prober2,
    Prober3,
    ProtectedMindReader,
    Punisher,
    Random,
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
    TitForTat,
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
