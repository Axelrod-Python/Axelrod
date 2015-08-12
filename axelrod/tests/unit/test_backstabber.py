import axelrod

from .test_player import TestPlayer

C, D = 'C', 'D'

class TestBackStabber(TestPlayer):

    name = "BackStabber"
    player = axelrod.BackStabber
    stochastic = False

    def test_strategy(self):
        """
        Forgives the first 3 defections but on the fourth
        will defect forever. Defects after the 198th round unconditionally.
        """

        self.first_play_test(C)

        # Forgives three defections
        self.responses_test([C], [D], [C], tournament_length=200)
        self.responses_test([C, C], [D, D], [C], tournament_length=200)
        self.responses_test([C, C, C], [D, D, D], [C], tournament_length=200)
        self.responses_test([C, C, C, C], [D, D, D, D], [D],
                            tournament_length=200)

        # Defects on rounds 199, and 200 no matter what
        self.responses_test([C] * 198 , [C] * 198, [D, D, D],
                            tournament_length=200)


class TestDoubleCrosser(TestPlayer):

    name = "DoubleCrosser"
    player = axelrod.DoubleCrosser
    stochastic = False

    def test_strategy(self):
        """
        Forgives the first 3 defections but on the fourth
        will defect forever. If the opponent did not defect
        in the first 6 rounds the player will cooperate until
        the 180th round. Defects after the 198th round unconditionally.
        """

        self.first_play_test(C)

        # Forgives three defections
        self.responses_test([C], [D], [C], tournament_length=200)
        self.responses_test([C, C], [D, D], [C], tournament_length=200)
        self.responses_test([C, C, C], [D, D, D], [C], tournament_length=200)
        self.responses_test([C, C, C, C], [D, D, D, D], [D],
                            tournament_length=200)

        # If opponent did not defect in the first six rounds, cooperate until
        # round 180
        self.responses_test([C] * 6, [C] * 6, [C] * 174, tournament_length=200)
        self.responses_test([C] * 12, [C] * 6 + [D] + [C] * 5, [C] * 160,
                            tournament_length=200)

        # Defects on rounds 199, and 200 no matter what
        self.responses_test([C] * 198 , [C] * 198, [D, D, D],
                            tournament_length=200)

