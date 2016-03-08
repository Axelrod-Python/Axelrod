from .match import Match


class TournamentType(object):

    clone_opponents = True

    def __init__(self, players, turns, deterministic_cache):
        self.players = players
        self.turns = turns
        self.deterministic_cache = deterministic_cache
        self.opponents = players

    @property
    def opponents(self):
        return self._opponents

    @property.setter
    def opponents(self, players):
        if self._clone_opponents:
            opponents = []
            for player in players:
                opponents.append(player.clone())
        else:
            opponents = players
        self._opponents = opponents

    def build_matches():
        raise NotImplementedError()


class RoundRobin(TournamentType):

    clone_opponents = True

    def build_matches(self, cache_mutable=True, noise=0):
        """
        Create a dictionary of match objects for a round robin tournament.

        Parameters
        ----------
        players : list
            A list of axelrod.Player objects
        opponents : list
            A list of axelrod.Player objects
        turns : integer
            The number of turns per match
        deterministic_cache : dictionary
            A cache of resulting actions for deterministic matches
        cache_mutable : boolean
            Whether the deterministic cache should be updated
        noise : float
            The probability that a player's intended action should be flipped

        Returns
        -------
        dictionary
            Mapping a tuple of player index numbers to an axelrod Match object
        """
        matches = {}
        for player1_index in range(len(self.players)):
            for player2_index in range(player1_index, len(self.players)):
                pair = (
                    self.players[player1_index], self.opponents[player2_index])
                match = Match(
                    pair, self.turns, self.deterministic_cache,
                    cache_mutable, noise)
                matches[(player1_index, player2_index)] = match
        return matches
