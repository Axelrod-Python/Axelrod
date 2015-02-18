"""
A script to run the Axelrod tournament using all the strategies present in `axelrod/strategies`
"""
from __future__ import division
import axelrod
import matplotlib.pyplot as plt

turns = 1000  # Number of turns in the round robin tournament
repetitions = 50  # Number of repetitions of the tournament

strategies = [strategy() for strategy in axelrod.strategies]
axelrod = axelrod.Axelrod(*strategies)
results = axelrod.tournament(turns=turns, repetitions=repetitions)

plt.boxplot([[score / turns for score in results[player]] for player in axelrod.players])
plt.xticks(range(1, len(axelrod.players) + 2), [str(p) for p in axelrod.players], rotation=90)
plt.title('Mean score per stage game over {} rounds repeated {} times'.format(turns, repetitions))
plt.savefig('results.png', bbox_inches='tight')
