import axelrod as axl
len(axl.strategies)  

players = (axl.Alternator(), axl.TitForTat())
match = axl.Match(players, 5)
interactions = match.play()
print(interactions)  # [(C, C), (D, C), (C, D), (D, C), (C, D)]