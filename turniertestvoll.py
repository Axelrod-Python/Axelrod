import axelrod as axl

# Wir erzeugen die Instanzen korrekt mit s()
# Falls eine kaputte Fremd-Strategie dabei ist, filtert der try-except Block sie aus
all_players = []
for s in axl.all_strategies:
    try:
        all_players.append(s())
    except Exception:
        continue

print(f"Starte das große Turnier mit {len(all_players)} Strategien...")

# 1000 Runden, 1 Wiederholung. Keine Extrafunktionen, um den RAM zu schonen.
tournament = axl.Tournament(players=all_players, turns=200, repetitions=1)
results = tournament.play(progress_bar=False)

print("\n" + "="*50)
print("     DAS OFFIZIELLE AXELROD HAIFISCHBECKEN (TOP 20)")
print("="*50)
for position, player in enumerate(results.ranked_names[:20], start=1):
    print(f"{position}. Platz: {player}")
print("="*50 + "\n")
