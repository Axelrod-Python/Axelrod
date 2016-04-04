from __future__ import absolute_import

# The order of imports matters!
from .actions import Actions, flip_action
from .random_ import random_choice
from .plot import Plot
from .game import DefaultGame, Game
from .player import init_args, is_basic, obey_axelrod, update_history, Player
from .mock_player import MockPlayer, simulate_play
from .match import Match
from .strategies import *
from .tournament_type import *
from .tournament import Tournament, ProbEndTournament
from .tournament_manager import TournamentManager, ProbEndTournamentManager
from .tournament_manager_factory import (TournamentManagerFactory,
                                         ProbEndTournamentManagerFactory)
from .result_set import ResultSet
from .ecosystem import Ecosystem
from .utils import run_tournaments, run_prob_end_tournaments, setup_logging
