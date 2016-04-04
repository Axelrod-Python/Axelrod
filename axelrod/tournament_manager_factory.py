from __future__ import absolute_import
from collections import OrderedDict

import axelrod.strategies

from .tournament_manager import *


class TournamentManagerFactory(object):


    tournaments = OrderedDict([
        ('basic_strategies', axelrod.basic_strategies),
        ('ordinary_strategies',
            axelrod.ordinary_strategies),
        ('cheating_strategies', axelrod.cheating_strategies),
        ('strategies',
            axelrod.ordinary_strategies +
            axelrod.cheating_strategies)
    ])

    @classmethod
    def create_tournament_manager(
            cls,
            output_directory,
            no_ecological,
            rebuild_cache,
            cache_file,
            exclusions,
            processes,
            turns,
            repetitions,
            noise,
            image_format="svg"):

        kwargs = {
            'processes': processes,
            'turns': turns,
            'repetitions': repetitions,
            'noise': noise,
        }

        manager = axelrod.TournamentManager(
            output_directory=output_directory,
            with_ecological=not no_ecological,
            save_cache=rebuild_cache,
            cache_file=cache_file,
            image_format=image_format)

        cls._add_tournaments(manager, exclusions, kwargs)

        return manager

    @classmethod
    def _add_tournaments(cls, manager, exclusions, kwargs):
        for name, strategies in cls._tournaments_dict(exclusions).items():
            players = manager.one_player_per_strategy(strategies)
            manager.add_tournament(
                name=name, players=players, **kwargs)

    @classmethod
    def _tournaments_dict(cls, exclusions=None):
        if exclusions is None:
            exclusions = []

        return OrderedDict([
            (key, value) for
            key, value in cls.tournaments.items() if key not in exclusions
        ])


class ProbEndTournamentManagerFactory(TournamentManagerFactory):

    @classmethod
    def create_tournament_manager(
            cls,
            output_directory,
            no_ecological,
            rebuild_cache,
            cache_file,
            exclusions,
            processes,
            prob_end,
            repetitions,
            noise,
            image_format="svg"):

        kwargs = {
            'processes': processes,
            'prob_end': prob_end,
            'repetitions': repetitions,
            'noise': noise,
        }

        manager = axelrod.ProbEndTournamentManager(
            output_directory=output_directory,
            with_ecological=not no_ecological,
            save_cache=rebuild_cache,
            cache_file=cache_file,
            image_format=image_format)

        cls._add_tournaments(manager, exclusions, kwargs)

        return manager

    @classmethod
    def _tournaments_dict(cls, exclusions=None):
        if exclusions is None:
            exclusions = []

        return OrderedDict([
            (key+'_prob_end', value) for
            key, value in cls.tournaments.items() if key not in exclusions
        ])
