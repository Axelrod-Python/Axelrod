import random
import axelrod as axl
from axelrod.action import Action
from axelrod.strategies.schwobasengnitz import SchwobaSenGnitz

class TestSchwobaSenGnitz(axl.TestPlayer):
    name = "Schwoba sen gnitz"
    player = SchwobaSenGnitz

    def test_strategy_initial_cooperation(self):
        """Prüft, ob die Strategie absolut friedlich startet, solange der Gegner kooperiert."""
        self.versus_test(axl.Cooperator, expected_actions=[(Action.C, Action.C)] * 5)

    def test_raubtier_erwacht(self):
        """Prüft, ob nach dem ersten Verrat die reziproke Reaktion einsetzt (mit festem Zufallssamen)."""
        random.seed(42)  # Fixiert den Zufall für reproduzierbare Tests
        # Erste Runde: C vs D -> Raubtier erwacht. Danach greift die Wahrscheinlichkeit.
        self.versus_test(
            axl.Defector,
            expected_actions=[
                (Action.C, Action.D),  # Runde 1: Start-C vs D
                (Action.C, Action.D),  # Runde 2: Deeskalation greift bei Seed 42
                (Action.C, Action.D),  # Runde 3: Deeskalation greift erneut
            ],
        )

    def test_schutz_modus(self):
        """Prüft, ob nach 10 durchgehenden Verraten des Gegners der Schutzmodus dauerhaft abriegelt."""
        random.seed(42)
        # Wir simulieren 12 Runden gegen einen reinen Defector
        expected = [(Action.C, Action.D)]  # Runde 1
        expected.extend([(Action.C, Action.D)] * 9)  # Runden 2-10 (Deeskalation/Zufall)
        expected.extend([(Action.D, Action.D)] * 2)  # Runden 11-12: Schutzmodus MUSS D liefern
        
        self.versus_test(axl.Defector, expected_actions=expected)
