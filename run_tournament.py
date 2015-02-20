"""
A script to run the Axelrod tournament using all the strategies present in `axelrod/strategies`
"""
from __future__ import division
import axelrod
import matplotlib.pyplot as plt
from numpy import median

turns = 200  # Number of turns in the round robin tournament
repetitions = 50  # Number of repetitions of the tournament

strategies = [strategy() for strategy in axelrod.strategies]
cheating_strategies = [strategy() for strategy in axelrod.cheating_strategies]
all_strategies = strategies + cheating_strategies

graphs_to_plot = {'results.png':strategies, 'cheating_results.png':cheating_strategies, 'all_results':all_strategies}

for plot in graphs_to_plot:
    if len(graphs_to_plot[plot]) != 1:
        axelrod_tournament = axelrod.Axelrod(*graphs_to_plot[plot])
        results = axelrod_tournament.tournament(turns=turns, repetitions=repetitions)
        players = sorted(axelrod_tournament.players, key = lambda x: median(results[x]))

        plt.boxplot([[score / (turns * (len(players) - 1)) for score in results[player]] for player in players])
        plt.xticks(range(1, len(axelrod_tournament.players) + 2), [str(p) for p in players], rotation=90)
        plt.title('Mean score per stage game over {} rounds repeated {} times'.format(turns, repetitions))
        plt.savefig(plot, bbox_inches='tight')
        plt.clf()
