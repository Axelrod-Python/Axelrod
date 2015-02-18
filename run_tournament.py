"""
A script to run the Axelrod tournament using all the strategies present in `axelrod/strategies`
"""
import axelrod

strategies = [strategy() for strategy in axelrod.strategies]
axelrod = axelrod.Axelrod(*strategies)
results = axelrod.tournament(turns=1000, repetitions=50)
print results
