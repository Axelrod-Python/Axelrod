"""
Script to obtain plots for the running axelrod tournament tutorial.
"""

import axelrod as axl
import matplotlib.pyplot as plt

first_tournament_participants_ordered_by_reported_rank = [
    s() for s in axl.axelrod_first_strategies
]
number_of_strategies = len(
    first_tournament_participants_ordered_by_reported_rank
)
axl.seed(0)
tournament = axl.Tournament(
    players=first_tournament_participants_ordered_by_reported_rank,
    turns=200,
    repetitions=5,
)
results = tournament.play()

plt.figure(figsize=(15, 6))
plt.plot((0, 15), (0, 15), color="grey", linestyle="--")
for original_rank, strategy in enumerate(
    first_tournament_participants_ordered_by_reported_rank
):
    rank = results.ranked_names.index(str(strategy))
    if rank == original_rank:
        symbol = "+"
        plt.plot((rank, rank), (rank, 0), color="grey")
    else:
        symbol = "o"
    plt.scatter([rank], [original_rank], marker=symbol, color="black", s=50)
plt.xticks(range(number_of_strategies), results.ranked_names, rotation=90)
plt.ylabel("Reported rank")
plt.xlabel("Reproduced rank")
plt.savefig("rank_comparison.svg")

plot = axl.Plot(results)
p = plot.boxplot()
p.savefig("boxplot.svg")
