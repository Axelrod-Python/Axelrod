import axelrod as axl
from axelrod.action import Action
from axelrod.strategies.schwoba_sen_gnitz import SchwobaSenGnitz


class TestSchwoba_Sen_Gnitz(axl.TestPlayer):
    name = "schwoba sen gnitz"
    player = SchwobaSenGnitz

    def test_strategy_initial_cooperation(self):
        self.versus_test(
            axl.Cooperator, expected_actions=[(Action.C, Action.C)] * 5
        )

    def test_schutz_modus(self):
        player = self.player()
        opponent = axl.Defector()

        for _ in range(10):
            player.play(opponent)

        self.assertEqual(player.strategy(opponent), Action.D)

        player.play(opponent)
        self.assertEqual(player.strategy(opponent), Action.D)
