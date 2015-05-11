import time
import logging
import axelrod


def timed_message(message, start_time):
    elapsed_time = time.time() - start_time
    return message + " in %.1fs" % elapsed_time


def setup_logging(logging_destination='console', verbosity='INFO'):
    """Sets up logging. Call this outside of run_tournaments to avoid
    accumulating logging handlers."""
    logHandlers = {
        'console': logging.StreamHandler(),
        'none': logging.NullHandler(),
        'file': logging.FileHandler('./axelrod.log')
    }
    logHandler = logHandlers[logging_destination]

    logFormatters = {
        'console': '%(message)s',
        'none': '',
        'file': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    }
    logFormatter = logging.Formatter(logFormatters[logging_destination])

    logHandler.setFormatter(logFormatter)
    logger = logging.getLogger('axelrod')
    logger.setLevel(logging.getLevelName(verbosity.upper()))
    logger.addHandler(logHandler)


def tournaments_dict(exclusions=[]):

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


def run_tournaments(cache_file='./cache.txt',
                    output_directory='./',
                    repetitions=10,
                    turns=200,
                    processes=None,
                    no_ecological=False,
                    rebuild_cache=False,
                    exclude_combined=False,
                    exclude_basic=False,
                    exclude_cheating=False,
                    exclude_ordinary=False,
                    noise=0):

    stdkwargs = {
        'processes': processes,
        'turns': turns,
        'repetitions': repetitions,
        'noise': noise}

    exclusions_dict = {
        'basic_strategies': exclude_basic,
        'strategies': exclude_ordinary,
        'cheating_strategies': exclude_cheating,
        'all_strategies': exclude_combined}

    exclusions = [key for key, value in exclusions_dict.items() if value]

    manager = axelrod.TournamentManager(
        output_directory=output_directory,
        with_ecological=not no_ecological,
        save_cache=rebuild_cache,
        cache_file=cache_file)

    for name, strategies in tournaments_dict(exclusions).items():
        players = manager.one_player_per_strategy(strategies)
        manager.add_tournament(
            name=name, players=players, **stdkwargs)

    manager.run_tournaments()
