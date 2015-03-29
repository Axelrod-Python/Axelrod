"""A script to run the Axelrod tournament.

The code for strategies is present in `axelrod/strategies`.
"""

from __future__ import division

import argparse
import logging
import axelrod


def run_tournaments(turns, repetitions, exclude_basic, exclude_strategies,
                    exclude_cheating, exclude_all, no_eco, output_directory,
                    logging_option, processes, save_cache):
    manager = axelrod.TournamentManager(
        output_directory=output_directory,
        with_ecological=not no_eco, save_cache=save_cache)

    logHandlers = {
        'console': logging.StreamHandler(),
        'none': logging.NullHandler(),
        'file': logging.FileHandler('./axelrod.log')
    }
    logHandler = logHandlers[logging_option]

    logFormatters = {
        'console': '%(message)s',
        'none': '',
        'file': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    }
    logFormatter = logging.Formatter(logFormatters[logging_option])

    logHandler.setFormatter(logFormatter)
    logger = logging.getLogger('axelrod')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logHandler)

    if not exclude_basic:
        players = manager.one_player_per_strategy(axelrod.basic_strategies)
        manager.add_tournament(
            name='basic_strategies', players=players, processes=processes)
    if not exclude_strategies:
        strategies = axelrod.basic_strategies + axelrod.ordinary_strategies
        players = manager.one_player_per_strategy(strategies)
        manager.add_tournament(
            name='strategies', players=players, processes=processes)
    if not exclude_cheating:
        players = manager.one_player_per_strategy(axelrod.cheating_strategies)
        manager.add_tournament(
            name='cheating_strategies', players=players, processes=processes)
    if not exclude_all:
        strategies = (
            axelrod.basic_strategies +
            axelrod.ordinary_strategies +
            axelrod.cheating_strategies)
        players = manager.one_player_per_strategy(strategies)
        manager.add_tournament(
            name='all_strategies', players=players, processes=processes)

    manager.run_tournaments()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--logging', type=str, default='console',
                        help='logging (none, console or file)')
    parser.add_argument('-t', '--turns', type=int, default=200,
                        help='turns per pair')
    parser.add_argument('-r', '--repetitions', type=int, default=50,
                        help='round-robin repetitions')
    parser.add_argument('-o', '--output_directory', default='./assets/',
                        help='output directory')
    parser.add_argument('--xb', action='store_true',
                        help='exlude basic strategies plot')
    parser.add_argument('--xs', action='store_true',
                        help='exlude ordinary strategies plot')
    parser.add_argument('--xc', action='store_true',
                        help='exclude cheating strategies plot')
    parser.add_argument('--xa', action='store_true',
                        help='exclude combined strategies plot')
    parser.add_argument('--ne', action='store_true',
                        help='no ecological variant')
    parser.add_argument('-p', '--processes', type=int, default=None,
                        help='Number of parallel processes to spawn. 0 uses cpu count.')
    parser.add_argument('--rc', action='store_true',
                        help='rebuild cache and save to file')
    args = parser.parse_args()

    if args.xb and args.xs and args.xc and args.xa:
        print "You've excluded everything - nothing for me to do"
    else:
        run_tournaments(args.turns, args.repetitions, args.xb, args.xs,
                        args.xc, args.xa, args.ne, args.output_directory,
                        args.logging, args.processes, args.rc)
