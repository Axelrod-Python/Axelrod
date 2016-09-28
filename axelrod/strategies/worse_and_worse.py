from axelrod import Actions, Player, random_choice

C, D = Actions.C, Actions.D

class WorseAndWorse (Player):
    """
    Defects with probability of 'current turn / 1000'. Therefore
    it is more and more likely to defect as the round goes on.

    Source code available at the download tab of [PRISON1998]_


    Names:
        - Worse and Worse: [PRISON1998]_

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

    def strategy(self, opponent):
        current_round = len(self.history) + 1
        probability = 1 - float(current_round) / 1000
        return random_choice(probability)


class KnowledgeableWorseAndWorse (Player):
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

    def strategy(self, opponent):
        current_round = len(self.history) + 1
        expected_length = self.match_attributes['length']
        probability = 1 - float(current_round) / expected_length
        return random_choice(probability)
