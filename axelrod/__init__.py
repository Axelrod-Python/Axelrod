DEFAULT_TURNS = 200

from axelrod import graph
from axelrod.action import Action
from axelrod.classifier import Classifiers
from axelrod.deterministic_cache import DeterministicCache
from axelrod.ecosystem import Ecosystem
from axelrod.evolvable_player import EvolvablePlayer
from axelrod.fingerprint import AshlockFingerprint, TransitiveFingerprint
from axelrod.game import DefaultGame, Game
from axelrod.history import History, LimitedHistory
from axelrod.load_data_ import load_pso_tables, load_weights
from axelrod.match import Match
from axelrod.match_generator import *
from axelrod.mock_player import MockPlayer
from axelrod.moran import ApproximateMoranProcess, MoranProcess
from axelrod.player import Player
from axelrod.plot import Plot
from axelrod.random_ import Pdf, random_choice, random_flip, seed
from axelrod.result_set import ResultSet
from axelrod.strategies import *
from axelrod.tournament import Tournament
# The order of imports matters!
from axelrod.version import __version__
