import axelrod as axl
from axelrod.strategies.schwoba_sen_gnitz import SchwobaSenGnitz

# 1. Wir laden deine Strategie und ein paar offizielle Gegner
players = [
    SchwobaSenGnitz(),
    axl.TitForTat(),
    axl.Grudger(),            # Das ist der Grudger
    axl.Cooperator(),      # AllC
    axl.Defector(),        # AllD
    axl.Alternator() if hasattr(axl, 'Altenator') else axl.Alternator(),
    axl.Random()
]

# 2. Turnier starten: 1000 Runden, 5 Wiederholungen für stabile Zufallswerte
tournament = axl.Tournament(players=players, turns=1000, repetitions=5)
results = tournament.play()

# 3. Ergebnis sauber im Terminal ausdrucken
print("\n" + "="*40)
print("     ERGEBNIS DES CT-RELOADED TURNIERS")
print("="*40)
for position, player in enumerate(results.ranked_names, start=1):
    print(f"{position}. Platz: {player}")
print("="*40 + "\n")
