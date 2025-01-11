"""Benchmark test

Use this on an ad hoc basis to test the performance of library changes.

To run:
`pip install pytest-benchmark`
`pytest benchmark.py`
"""

import axelrod as axl
from axelrod.graph import Graph


def few_players_no_mutations():
    edges = [(0, 1), (1, 2), (2, 3), (3, 1)]
    graph = Graph(edges)
    players = [
        axl.Cooperator(),
        axl.Cooperator(),
        axl.Cooperator(),
        axl.Defector(),
    ]
    mp = axl.MoranProcess(players, interaction_graph=graph, seed=40)
    _ = mp.play()


def few_players_mutations():
    edges = [(0, 1), (1, 2), (2, 3), (3, 1)]
    graph = Graph(edges)
    players = [
        axl.Cooperator(),
        axl.Cooperator(),
        axl.Cooperator(),
        axl.Defector(),
    ]
    mp = axl.MoranProcess(
        players, interaction_graph=graph, mutation_rate=0.5, seed=40
    )
    for _ in range(100):
        try:
            mp.__next__()
        except StopIteration:
            break


def four_distinct_players_no_mutations():
    players = [axl.Cooperator(), axl.Defector(), axl.TitForTat(), axl.Grudger()]
    mp = axl.MoranProcess(players, seed=40)
    _ = mp.play()


def four_distinct_players_mutations():
    players = [axl.Cooperator(), axl.Defector(), axl.TitForTat(), axl.Grudger()]
    mp = axl.MoranProcess(players, mutation_rate=0.5, seed=40)
    for _ in range(50):
        try:
            mp.__next__()
        except StopIteration:
            break


def more_players_no_mutations():
    players = [axl.Cooperator() for _ in range(9)] + [
        axl.Defector() for _ in range(3)
    ]
    mp = axl.MoranProcess(players, seed=40)
    _ = mp.play()


def more_players_mutations():
    players = [axl.Cooperator() for _ in range(9)] + [
        axl.Defector() for _ in range(3)
    ]
    mp = axl.MoranProcess(players, mutation_rate=0.5, seed=40)
    for _ in range(50):
        try:
            mp.__next__()
        except StopIteration:
            break


def test_few_players_no_mutations(benchmark):
    benchmark(few_players_no_mutations)


def test_few_players_mutations(benchmark):
    benchmark(few_players_mutations)


def test_four_distinct_players_no_mutations(benchmark):
    benchmark(four_distinct_players_no_mutations)


def test_four_distinct_players_mutations(benchmark):
    benchmark(four_distinct_players_mutations)


def test_more_players_no_mutations(benchmark):
    benchmark(more_players_no_mutations)


def test_more_players_mutations(benchmark):
    benchmark(more_players_mutations)
