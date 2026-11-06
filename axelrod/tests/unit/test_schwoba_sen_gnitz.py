import axelrod as axl
from axelrod.action import Action
from axelrod.strategies.schwoba_sen_gnitz import SchwobaSenGnitz

class TestSchwoba_Sen_Gnitz(axl.TestPlayer):
    name = "schwoba sen gnitz"
    player = SchwobaSenGnitz

    def test_strategy_initial_cooperation(self):
        """Prüft, ob die Strategie absolut friedlich startet, solange der Gegner kooperiert."""
        self.versus_test(axl.Cooperator, expected_actions=[(Action.C, Action.C)] * 5)

    def test_schutz_modus(self):
        """Prüft, ob nach 10 Runden unversöhnlichem Verrat der Schutzmodus aktiv blockiert."""
        # Wir testen nur die allererste Runde (garantiert C) 
        # und die Runden 11 und 12 (garantiert D wegen Schutzmodus)
        player = self.player()
        opponent = axl.Defector()
        
        # Runde 1 bis 10 simulieren (Gegner betrügt immer)
        for _ in range(10):
            player.play(opponent)
            
        # Ab Runde 11 MUSS der Schutzmodus aktiv sein und nur noch D liefern,
        # völlig egal, was der Zufall sagt!
        self.assertEqual(player.strategy(opponent), Action.D)
        
        player.play(opponent)  # Runde 11 spielen
        self.assertEqual(player.strategy(opponent), Action.D)  # Runde 12 prüfen
