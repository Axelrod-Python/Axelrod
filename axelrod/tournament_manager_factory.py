from tournament_manager import *
import axelrod.strategies


class TournamentManagerFactory(object):

    @classmethod
    def create_tournament_manager(
            cls,
            output_directory,
            no_ecological,
            rebuild_cache,
            cache_file,
            processes,
            turns,
            repetitions,
            noise,
            exclusions=[]):

        manager = axelrod.TournamentManager(
            output_directory=output_directory,
            with_ecological=not no_ecological,
            save_cache=rebuild_cache,
            cache_file=cache_file)

        cls._add_tournaments(manager, processes, turns, repetitions, noise, exclusions)

        return manager

    @classmethod
    def _add_tournaments(cls, manager, processes, turns, repetitions, noise, exclusions=[]):
        for name, strategies in cls._tournaments_dict(exclusions).items():
            players = manager.one_player_per_strategy(strategies)
            manager.add_tournament(
                name=name, players=players, processes=processes, turns=turns, repetitions=repetitions, noise=noise)

    @staticmethod
    def _tournaments_dict(exclusions=[]):

        tournaments = {
            'basic_strategies': axelrod.basic_strategies,
            'strategies':
                axelrod.basic_strategies +
                axelrod.ordinary_strategies,
            'cheating_strategies': axelrod.cheating_strategies,
            'all_strategies':
                axelrod.basic_strategies +
                axelrod.ordinary_strategies +
                axelrod.cheating_strategies}

        return {
            key: value for
            key, value in tournaments.items() if key not in exclusions}
