"""A script to run the Axelrod tournament.

The code for strategies is present in `axelrod/strategies`.
"""

from __future__ import division

import argparse
import os
import time

import axelrod


def strategies_list(strategies):
    return [strategy() for strategy in strategies]


def output_file_path(output_directory, tournament_name, file_extension):
    return os.path.join(
        output_directory,
        tournament_name + '.' + file_extension)


def run_tournament(turns, repetitions, exclude_basic, exclude_strategies,
                   exclude_cheating, exclude_all, output_directory):
    """Main function for running Axelrod tournaments."""
    tournaments = {}

    if not exclude_basic:
        tournaments['basic_strategies'] = strategies_list(
            axelrod.basic_strategies)
    if not exclude_strategies:
        tournaments['strategies'] = strategies_list(
            axelrod.strategies)
    if not exclude_cheating:
        tournaments['cheating_strategies'] = strategies_list(
            axelrod.cheating_strategies)
    if not exclude_all:
        tournaments['all_strategies'] = strategies_list(axelrod.all_strategies)

    for tournament_name in tournaments:
        if len(tournaments[tournament_name]) != 1:

            tournament = axelrod.Tournament(
                players=tournaments[tournament_name],
                turns=turns,
                repetitions=repetitions
            )

            # This is where the actual tournament takes place.
            results = tournament.play()

            # # Save the scores from this tournament to a CSV file.
            csv = results.csv()
            file_namename = output_file_path(
                output_directory, tournament_name, 'csv')
            with open(file_namename, 'w') as f:
                f.write(csv)

            # Create a Plot instance and test whether matplotlib
            # is installed before proceeding
            plot = axelrod.Plot(results)
            if not plot.matplotlib_installed:
                print ("The matplotlib library is not installed. "
                       "Only .csv output will be produced.")
                continue

            # Save boxplots
            boxplot = plot.boxplot()
            file_name = output_file_path(
                    output_directory, tournament_name + '_boxplot', 'png')
            boxplot.savefig(file_name, bbox_inches='tight')
            boxplot.clf()

            # Save plot with average payoff matrix with winners at top.
            payoff = plot.payoff()
            file_name = output_file_path(
                    output_directory, tournament_name + '_payoff', 'png')
            payoff.savefig(file_name, bbox_inches='tight')
            payoff.clf()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='show verbose messages')
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
    args = parser.parse_args()

    t0 = time.time()

    if args.verbose:
        print ('Starting tournament with ' + str(args.repetitions) +
               ' round robins of ' + str(args.turns) + ' turns per pair.')
        print 'Basics strategies plot: ' + str(not args.xb)
        print 'Ordinary strategies plot: ' + str(not args.xs)
        print 'Cheating strategies plot: ' + str(not args.xc)
        print 'Combined strategies plot: ' + str(not args.xa)
    run_tournament(args.turns, args.repetitions, args.xb, args.xs,
                   args.xc, args.xa, args.output_directory)

    dt = time.time() - t0
    print "Finished in %.1fs" % dt
