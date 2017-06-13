import os

on_windows = os.name == 'nt'
DEFAULT_TURNS = 200

# The order of imports matters!
from .version import __version__
from .load_data_ import load_pso_tables, load_weights
from . import graph
from .actions import Actions, flip_action
from .random_ import random_choice, seed, Pdf
from .plot import Plot
from .game import DefaultGame, Game
from .player import (
    get_state_distribution_from_history, is_basic, obey_axelrod,
    update_history, update_state_distribution, Player)
from .mock_player import MockPlayer
from .match import Match
from .moran import MoranProcess, ApproximateMoranProcess
from .strategies import *
from .deterministic_cache import DeterministicCache
from .match_generator import *
from .tournament import Tournament
from .result_set import ResultSet, ResultSetFromFile
from .ecosystem import Ecosystem
from .fingerprint import AshlockFingerprint

