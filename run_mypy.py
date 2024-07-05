import subprocess
import sys

modules = [
    "run_strategy_indexer.py",
    "axelrod/action.py",
    "axelrod/deterministic_cache.py",
    "axelrod/ecosystem.py",
    "axelrod/evolvable_player.py",
    "axelrod/fingerprint.py",
    "axelrod/game.py",
    "axelrod/load_data_.py",
    "axelrod/mock_player.py",
    "axelrod/moran.py",
    "axelrod/plot.py",
    "axelrod/random_.py",
    "axelrod/tournament.py",
    "axelrod/strategies/adaptive.py",
    "axelrod/strategies/alternator.py",
    "axelrod/strategies/ann.py",
    "axelrod/strategies/apavlov.py",
    "axelrod/strategies/appeaser.py",
    "axelrod/strategies/averagecopier.py",
    "axelrod/strategies/axelrod_first.py",
    "axelrod/strategies/axelrod_second.py",
    "axelrod/strategies/backstabber.py",
    "axelrod/strategies/better_and_better.py",
    "axelrod/strategies/calculator.py",
    "axelrod/strategies/cooperator.py",
    "axelrod/strategies/cycler.py",
    "axelrod/strategies/darwin.py",
    "axelrod/strategies/defector.py",
    "axelrod/strategies/forgiver.py",
    "axelrod/strategies/frequency_analyzer.py",
    "axelrod/strategies/gradualkiller.py",
    "axelrod/strategies/grudger.py",
    "axelrod/strategies/grumpy.py",
    "axelrod/strategies/handshake.py",
    "axelrod/strategies/hunter.py",
    "axelrod/strategies/inverse.py",
    "axelrod/strategies/mathematicalconstants.py",
    "axelrod/strategies/memoryone.py",
    "axelrod/strategies/memorytwo.py",
    "axelrod/strategies/mutual.py",
    "axelrod/strategies/negation.py",
    "axelrod/strategies/oncebitten.py",
    "axelrod/strategies/prober.py",
    "axelrod/strategies/punisher.py",
    "axelrod/strategies/qlearner.py",
    "axelrod/strategies/rand.py",
    "axelrod/strategies/titfortat.py",
    "axelrod/strategies/hmm.py",
    "axelrod/strategies/human.py",
    "axelrod/strategies/finite_state_machines.py",
    "axelrod/strategies/worse_and_worse.py",
]

exit_codes = []
for module in modules:
    rc = subprocess.call(
        ["mypy", "--ignore-missing-imports", "--follow-imports", "skip", module]
    )
    exit_codes.append(rc)
sys.exit(max(exit_codes))
