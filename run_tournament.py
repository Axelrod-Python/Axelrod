"""
A script to run the Axelrod tournament using all the strategies present in `axelrod/strategies`
"""
from __future__ import division
import csv
import axelrod
import matplotlib.pyplot as plt
from numpy import median

turns = 200  # Number of turns in the round robin tournament
repetitions = 50  # Number of repetitions of the tournament

strategies = [strategy() for strategy in axelrod.strategies]
cheating_strategies = [strategy() for strategy in axelrod.cheating_strategies]
all_strategies = strategies + cheating_strategies

results_to_gather = {'results':strategies, 'cheating_results':cheating_strategies, 'all_results':all_strategies}

for result in results_to_gather:
    if len(results_to_gather[result]) != 1:

        axelrod_tournament = axelrod.Axelrod(*results_to_gather[result])
        results = axelrod_tournament.tournament(turns=turns, repetitions=repetitions)
        players = sorted(axelrod_tournament.players, key = lambda x: median(results[x]))

        with open('{}.csv'.format(result), 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, ['player', 'scores'])
            csv_writer.writeheader()
            for player in players:
                csv_writer.writerow({'player': player, 'scores': results[player]})

        plt.boxplot([[score / (turns * (len(players) - 1)) for score in results[player]] for player in players])
        plt.xticks(range(1, len(axelrod_tournament.players) + 2), [str(p) for p in players], rotation=90)
        plt.title('Mean score per stage game over {} rounds repeated {} times ({} strategies)'.format(turns, repetitions, len(players)))
        plt.savefig('{}.png'.format(result), bbox_inches='tight')
        plt.clf()
