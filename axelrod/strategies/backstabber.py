from axelrod import Player


class BackStabber(Player):
    """
    Forgives the first 3 defections but on the fourth
    will defect forever. Defects on the last 2 rounds unconditionally.
    """

    name = 'BackStabber'
    behaviour = {
        'memory_depth': float('inf')
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
    behaviour = {
        'memory_depth': float('inf')
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
