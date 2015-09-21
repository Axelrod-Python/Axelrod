from __future__ import absolute_import

from .alternator import Alternator
from .appeaser import Appeaser
from .averagecopier import AverageCopier, NiceAverageCopier
from .axelrod_tournaments import (
    Davis, Feld, Grofman, Joss, Shubik, Tullock, Champion, Eatherley, Tester)
from .backstabber import BackStabber, DoubleCrosser
from .calculator import Calculator
from .cooperator import Cooperator, TrickyCooperator
from .cycler import AntiCycler, CyclerCCD, CyclerCCCD, CyclerCCCCCD
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
    DefectorHunter, CooperatorHunter, AlternatorHunter, MathConstantHunter,
    RandomHunter)
from .inverse import Inverse
from .mathematicalconstants import Golden, Pi, e
from .memoryone import (
    WinStayLoseShift,GTFT, StochasticCooperator, StochasticWSLS, ZDGTFT2,
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
    SuspiciousTitForTat, AntiTitForTat, HardTitForTat, HardTitFor2Tats)


# Note: Meta* strategies are handled in .__init__.py

strategies = [
    Aggravater,
    Alternator,
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
    Cooperator,
    CooperatorHunter,
    CyclerCCCCCD,
    CyclerCCCD,
    CyclerCCD,
    Darwin,
    Davis,
    Defector,
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
    MindBender,
    MindController,
    MindReader,
    MindWarper,
    MirrorMindReader,
    NiceAverageCopier,
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
