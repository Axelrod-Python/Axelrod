from axelrod.action import Action
from axelrod.player import Player
from axelrod.random_ import random_choice

C, D = Action.C, Action.D


class WorseAndWorse(Player):
    """
    Defects with probability of 'current turn / 1000'. Therefore
    it is more and more likely to defect as the round goes on.

    Source code available at the download tab of [Prison1998]_


    Names:
        - Worse and Worse: [Prison1998]_
    """

    name = 'Worse and Worse'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent: Player) -> Action:
        current_round = len(self.history) + 1
        probability = 1 - current_round / 1000
        return random_choice(probability)


class KnowledgeableWorseAndWorse(Player):
    """
    This strategy is based on 'Worse And Worse' but will defect with probability
    of 'current turn / total no. of turns'.

    Names:
        - Knowledgeable Worse and Worse: Original name by Adam Pohl
    """

    name = 'Knowledgeable Worse and Worse'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(['length']),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent: Player) -> Action:
        current_round = len(self.history) + 1
        expected_length = self.match_attributes['length']
        probability = 1 - current_round / expected_length
        return random_choice(probability)


class WorseAndWorse2(Player):
    """
    Plays as tit for tat during the first 20 moves.
    Then defects with probability (current turn - 20) / current turn.
    Therefore it is more and more likely to defect as the round goes on.

    Names:
        - Worse and Worse 2: [Prison1998]_
    """

    name = 'Worse and Worse 2'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent: Player) -> Action:
        current_round = len(self.history) + 1

        if current_round == 1:
            return C
        elif current_round <= 20:
            return opponent.history[-1]
        else:
            probability = 20 / current_round
            return random_choice(probability)


class WorseAndWorse3(Player):
    """
    Cooperates in the first turn.
    Then defects with probability no. of opponent defects / (current turn - 1).
    Therefore it is more likely to defect when the opponent defects for a larger
    proportion of the turns.

    Names:
        - Worse and Worse 3: [Prison1998]_
    """

    name = 'Worse and Worse 3'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent: Player) -> Action:
        current_round = len(self.history) + 1

        if current_round == 1:
            return C
        else:
            probability = 1 - opponent.defections / (current_round - 1)
            return random_choice(probability)
