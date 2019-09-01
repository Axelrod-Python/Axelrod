DEFAULT_TURNS = 200

# The order of imports matters!
from axelrod.version import __version__
from axelrod.load_data_ import load_pso_tables, load_weights
from axelrod import graph
from axelrod.action import Action
from axelrod.random_ import random_choice, random_flip, seed, Pdf
from axelrod.plot import Plot
from axelrod.game import DefaultGame, Game
from axelrod.history import History, LimitedHistory
from axelrod.player import EvolvablePlayer, is_basic, obey_axelrod, Player
from axelrod.mock_player import MockPlayer
from axelrod.match import Match
from axelrod.moran import MoranProcess, ApproximateMoranProcess
from axelrod.strategies import *
from axelrod.deterministic_cache import DeterministicCache
from axelrod.match_generator import *
from axelrod.tournament import Tournament
from axelrod.result_set import ResultSet
from axelrod.ecosystem import Ecosystem
from axelrod.fingerprint import AshlockFingerprint, TransitiveFingerprint
