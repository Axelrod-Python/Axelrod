from __future__ import absolute_import

import time
import logging

from .tournament_manager_factory import TournamentManagerFactory

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
    level = logging.getLevelName(verbosity.upper())
    logger.setLevel(verbosity.upper())
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

    exclusions_dict = {
        'basic_strategies': exclude_basic,
        'strategies': exclude_ordinary,
        'cheating_strategies': exclude_cheating,
        'all_strategies': exclude_combined}

    exclusions = [key for key, value in exclusions_dict.items() if value]

    manager = TournamentManagerFactory.create_tournament_manager(
        output_directory=output_directory,
        no_ecological=no_ecological,
        rebuild_cache=rebuild_cache,
        cache_file=cache_file,
        exclusions=exclusions,
        processes=processes,
        turns=turns,
        repetitions=repetitions,
        noise=noise)

    manager.run_tournaments()
