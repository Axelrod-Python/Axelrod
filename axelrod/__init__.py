DEFAULT_TURNS = 200

# The order of imports matters!
from axelrod.ipd import graph
from axelrod.ipd.action import Action
from axelrod.ipd.random_ import random_choice, random_flip, seed, Pdf
from axelrod.ipd import eigen
from axelrod.ipd.plot import Plot
from axelrod.ipd.history import History, LimitedHistory
from axelrod.player import BasePlayer
from axelrod.ipd.player import IpdPlayer
from axelrod.ipd.classifier import Classifiers
from axelrod.ipd.evolvable_player import EvolvablePlayer
from axelrod.game import BaseGame
from axelrod.ipd.game import IpdGame, DefaultGame
from axelrod.ipd.moran import MoranProcess, ApproximateMoranProcess
from axelrod.ipd.strategies import *
from axelrod.ipd.match_generator import *
from axelrod.ipd.tournament import IpdTournament
from axelrod.ipd.ecosystem import Ecosystem
from axelrod.ipd.match import IpdMatch
from axelrod.ipd.result_set import ResultSet
from axelrod.ipd.deterministic_cache import DeterministicCache
from axelrod.ipd import fingerprint
from axelrod.ipd.fingerprint import AshlockFingerprint, TransitiveFingerprint
from axelrod.ipd import interaction_utils
from axelrod.ipd.mock_player import MockPlayer
from axelrod.version import __version__
