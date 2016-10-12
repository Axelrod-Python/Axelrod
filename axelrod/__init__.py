from __future__ import absolute_import
import os

on_windows = os.name == 'nt'

# The order of imports matters!
from .version import __version__
from .actions import Actions, flip_action
from .random_ import random_choice, seed
from .plot import Plot
from .game import DefaultGame, Game
from .player import init_args, is_basic, obey_axelrod, update_history, Player
from .mock_player import MockPlayer, simulate_play
from .match import Match
from .moran import MoranProcess
from .strategies import *
from .deterministic_cache import DeterministicCache
from .match_generator import *
from .tournament import Tournament, ProbEndTournament, SpatialTournament, ProbEndSpatialTournament
from .result_set import ResultSet, ResultSetFromFile
from .ecosystem import Ecosystem
