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
    logger.setLevel(logging.getLevelName(verbosity))
    logger.addHandler(logHandler)


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

    manager = axelrod.TournamentManager(
        output_directory=output_directory,
        with_ecological=not no_ecological, save_cache=rebuild_cache,
        cache_file=cache_file)

    stdkwargs = {
        'processes': processes,
        'turns': turns,
        'repetitions': repetitions,
        'noise': noise}

    if not exclude_basic:
        players = manager.one_player_per_strategy(axelrod.basic_strategies)
        manager.add_tournament(
            name='basic_strategies', players=players, **stdkwargs)

    if not exclude_ordinary:
        strategies = axelrod.basic_strategies + axelrod.ordinary_strategies
        players = manager.one_player_per_strategy(strategies)
        manager.add_tournament(
            name='strategies', players=players, **stdkwargs)

    if not exclude_cheating:
        players = manager.one_player_per_strategy(axelrod.cheating_strategies)
        manager.add_tournament(
            name='cheating_strategies', players=players, **stdkwargs)

    if not exclude_combined:
        strategies = (
            axelrod.basic_strategies +
            axelrod.ordinary_strategies +
            axelrod.cheating_strategies)
        players = manager.one_player_per_strategy(strategies)
        manager.add_tournament(
            name='all_strategies', players=players, **stdkwargs)

    manager.run_tournaments()
