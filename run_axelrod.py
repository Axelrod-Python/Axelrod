#!/usr/bin/env python

"""A script to run the Axelrod tournament.

The code for strategies is present in `axelrod/strategies`.
"""

from __future__ import division

import argparse
import logging
import axelrod


def run_tournaments(cache_file='./cache.txt', logging_destination='console', no_ecological=False, output_directory='./', processes=None, rebuild_cache=False, repetitions=10, turns=200, verbosity='INFO', exclude_combined=False, exclude_basic=False, exclude_cheating=False, exclude_ordinary=False, noise=0):
    manager = axelrod.TournamentManager(
        output_directory=output_directory,
        with_ecological=not no_ecological, save_cache=rebuild_cache,
        cache_file=cache_file)

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

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run a recreationg of Axelrod's tournament")
    parser.add_argument('-l', '--logging', type=str, default='console',
                        dest="logging_destination", help='logging (none, console or file)')
    parser.add_argument('-v', '--verbosity', type=str, default='INFO',
                        help='Logging level. DEBUG, INFO, ERROR or CRITICAL')
    parser.add_argument('-t', '--turns', type=int, default=200,
                        help='turns per pair')
    parser.add_argument('-r', '--repetitions', type=int, default=10,
                        help='round-robin repetitions')
    parser.add_argument('-o', '--output_directory', default='./',
                        help='output directory')
    parser.add_argument('--xb', "--exclude-basic", action='store_true',
                        help='exclude basic strategies plot', dest="exclude_basic")
    parser.add_argument('--xs', "--exclude-ordinary", action='store_true',
                        help='exclude ordinary strategies plot', dest="exclude_ordinary")
    parser.add_argument('--xc', "--exclude-cheating", action='store_true',
                        help='exclude cheating strategies plot', dest="exclude_cheating")
    parser.add_argument('--xa', "--exclude-combined", action='store_true',
                        help='exclude combined strategies plot', dest="exclude_combined")
    parser.add_argument('--ne', "--no-ecological", action='store_true',
                        help='no ecological variant', dest="no_ecological")
    parser.add_argument('-p', '--processes', type=int, default=None,
                        help='Number of parallel processes to spawn. 0 uses cpu count.')
    parser.add_argument('--rc', "--rebuild-cache", action='store_true',
                        help='rebuild cache and save to file', dest="rebuild_cache")
    parser.add_argument('-c', '--cache_file', type=str, default='./cache.txt',
                        help='Path to cache file')
    parser.add_argument('-n', '--noise', type=float, default=0,
                        help='Noise level')
    args = parser.parse_args()

    if all([args.exclude_basic, args.exclude_ordinary, args.exclude_cheating, args.exclude_combined]):
        print "You've excluded everything - nothing for me to do"
    else:
        # Unravel argparse Namespace object to python keyword arguments.
        run_tournaments(**vars(args))
