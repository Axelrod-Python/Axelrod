"""
A script to run the Axelrod tournament using all the strategies present in `axelrod/strategies`
"""
from __future__ import division

import argparse
import time

def run_tournament(turns, repetitions, exclude_strategies, exclude_cheating, exclude_all):

    import axelrod
    import matplotlib.pyplot as plt
    from numpy import median

    strategies = []
    cheating_strategies = []
    all_strategies = []
    graphs_to_plot = {}

    if not exclude_strategies:
        strategies = [strategy() for strategy in axelrod.strategies]
        graphs_to_plot['results.png'] = strategies
    if not exclude_cheating:
        cheating_strategies = [strategy() for strategy in axelrod.cheating_strategies]
        graphs_to_plot['cheating_results.png'] = cheating_strategies
    if not exclude_all:
        all_strategies = strategies + cheating_strategies
        graphs_to_plot['all_results'] = all_strategies

    for plot in graphs_to_plot:
        if len(graphs_to_plot[plot]) != 1:
            axelrod_tournament = axelrod.Axelrod(*graphs_to_plot[plot])
            results = axelrod_tournament.tournament(turns=turns, repetitions=repetitions)
            players = sorted(axelrod_tournament.players, key=lambda x: median(results[x]))

            plt.boxplot([[score / (turns * (len(players) - 1)) for score in results[player]] for player in players])
            plt.xticks(range(1, len(axelrod_tournament.players) + 2), [str(p) for p in players], rotation=90)
            plt.title('Mean score per stage game over {} rounds repeated {} times ({} strategies)'.format(turns, repetitions, len(players)))
            plt.savefig(plot, bbox_inches='tight')
            plt.clf()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help='show verbose messages')
    parser.add_argument('-t', '--turns', type=int, default=200, help='turns per pair')
    parser.add_argument('-r', '--repetitions', type=int, default=50, help='round-robin repetitions')
    parser.add_argument('--xs', action='store_true', help='exlude ordinary strategies plot')
    parser.add_argument('--xc', action='store_true', help='exclude cheating strategies plot')
    parser.add_argument('--xa', action='store_true', help='exclude combined strategies plot')
    args = parser.parse_args()

    t0 = time.time()
    if args.verbose:
        print 'Starting tournament with ' + str(args.repetitions) + ' round robins of ' + str(args.turns) + ' turns per pair.'
        print 'Ordinary strategies plot: ' + str(not args.xs)
        print 'Cheating strategies plot: ' + str(not args.xc)
        print 'Combined strategies plot: ' + str(not args.xa)
    run_tournament(args.turns, args.repetitions, args.xs, args.xc, args.xa)
    dt = time.time() - t0
    print "Finished in %.1fs" % dt
