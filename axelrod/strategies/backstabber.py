from axelrod import Player


class BackStabber(Player):
    """
    Forgives the first 3 defections but on the fourth
    will defect forever. Defects on the last 2 rounds unconditionally.
    """

    name = 'BackStabber'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        if not opponent.history:
            return 'C'
        if len(opponent.history) > (self.tournament_attributes['length'] - 3):
            return 'D'
        if opponent.defections > 3:
            return 'D'
        return 'C'


class DoubleCrosser(Player):
    """
    Forgives the first 3 defections but on the fourth
    will defect forever. If the opponent did not defect
    in the first 6 rounds the player will cooperate until
    the 180th round. Defects on the last 2 rounds unconditionally.
    """

    name = 'DoubleCrosser'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        cutoff = 6

        if not opponent.history:
            return 'C'
        if len(opponent.history) > (self.tournament_attributes['length'] - 3):
            return 'D'
        if len(opponent.history) < 180:
            if len(opponent.history) > cutoff:
                if 'D' not in opponent.history[:cutoff + 1]:
                    if opponent.history[-2:] != ['D', 'D']:  # Fail safe
                        return 'C'
        if opponent.defections > 3:
            return 'D'
        return 'C'
