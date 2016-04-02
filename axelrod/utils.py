from __future__ import absolute_import

import time
import logging

from .tournament_manager_factory import (TournamentManagerFactory,
                                         ProbEndTournamentManagerFactory)


def timed_message(message, start_time):
    elapsed_time = time.time() - start_time
    return message + " in %.1fs" % elapsed_time


def setup_logging(logging_destination='console', verbosity='INFO'):
    """Sets up logging. Call this outside of run_tournaments to avoid
    accumulating logging handlers."""
    logHandlers = {
        'console': logging.StreamHandler,
        'none': logging.NullHandler,
    }
    if logging_destination == 'file':
        logHandler = logging.FileHandler('./axelrod.log')
    else:
        logHandler = logHandlers[logging_destination]()

    logFormatters = {
        'console': '%(message)s',
        'none': '',
        'file': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    }
    logFormatter = logging.Formatter(logFormatters[logging_destination])

    logHandler.setFormatter(logFormatter)
    logger = logging.getLogger('axelrod')
    logger.setLevel(verbosity.upper())
    logger.addHandler(logHandler)


def build_exclusions_dict(exclude_basic, exclude_ordinary,
                          exclude_cheating, exclude_combined):
    """A utility function to return a dictionary mapping tournament string names
    to booleans."""
    return {
        'basic_strategies': exclude_basic,
        'ordinary_strategies': exclude_ordinary,
        'cheating_strategies': exclude_cheating,
        'strategies': exclude_combined}


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
                    noise=0,
                    image_format="svg"):

    exclusions_dict = build_exclusions_dict(exclude_basic, exclude_ordinary,
                                            exclude_cheating, exclude_combined)

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
        noise=noise,
        image_format=image_format)

    manager.run_tournaments()


def run_prob_end_tournaments(cache_file='./cache.txt',
                    output_directory='./',
                    repetitions=10,
                    prob_end=.01,  # By default have mean of 100 rounds
                    processes=None,
                    no_ecological=False,
                    rebuild_cache=False,
                    exclude_combined=False,
                    exclude_basic=False,
                    exclude_cheating=False,
                    exclude_ordinary=False,
                    noise=0,
                    image_format="svg"):

    exclusions_dict = build_exclusions_dict(exclude_basic, exclude_ordinary,
                                            exclude_cheating, exclude_combined)

    exclusions = [key for key, value in exclusions_dict.items() if value]

    manager = ProbEndTournamentManagerFactory.create_tournament_manager(
        output_directory=output_directory,
        no_ecological=no_ecological,
        rebuild_cache=rebuild_cache,
        cache_file=cache_file,
        exclusions=exclusions,
        processes=processes,
        prob_end=prob_end,
        repetitions=repetitions,
        noise=noise,
        image_format=image_format)

    manager.run_tournaments()
