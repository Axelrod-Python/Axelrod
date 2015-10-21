from __future__ import absolute_import

# The order of imports matters!
from .actions import Actions, flip_action
from .random_ import random_choice
from .plot import Plot
from .game import DefaultGame, Game
from .player import is_basic, obey_axelrod, update_histories, Player
from .mock_player import MockPlayer, simulate_play
from .round_robin import RoundRobin
from .strategies import *
from .tournament import Tournament
from .tournament_manager import TournamentManager
from .tournament_manager_factory import TournamentManagerFactory
from .result_set import ResultSet
from .ecosystem import Ecosystem
from .utils import run_tournaments, setup_logging
