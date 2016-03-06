from __future__ import absolute_import

import logging
import multiprocessing

from .game import Game
from .result_set import ResultSet
from .tournament_type import round_robin
from .payoff import payoff_matrix
from .cooperation import cooperation_matrix


class Tournament(object):
    game = Game()

    def __init__(self, players, tournament_type=round_robin, name='axelrod',
                 game=None, turns=200,
                 repetitions=10, processes=None, prebuilt_cache=False,
                 noise=0, with_morality=True, keep_matches=False):
        """
        Parameters
        ----------
        players : list
            A list of axelrod.Player objects
        tournament_type : function
            Returning a dictionary mapping a tuple of player index numbers to
            an axelrod Match object
        name : string
            A name for the tournament
        game : axelrod.Game
            The game object used to score the tournament
        turns : integer
            The number of turns per match
        repetitions : integer
            The number of times the round robin should be repeated
        processes : integer
            The number of processes to be used for parallel processing
        prebuilt_cache : boolean
            Whether a cache has been passed in from an external object
        noise : float
            The probability that a player's intended action should be flipped
        with_morality : boolean
            Whether morality metrics should be calculated
        with_interactions : boolean
            Whether interaction results should be included in the output
        """
        self.name = name
        self.tournament_type = tournament_type
        self.turns = turns
        self.noise = noise
        if game is not None:
            self.game = game
        self.players = players
        self.repetitions = repetitions
        self.prebuilt_cache = prebuilt_cache
        self.deterministic_cache = {}
        self._with_morality = with_morality
        self._keep_matches = keep_matches
        self._parallel_repetitions = repetitions
        self._processes = processes
        self._logger = logging.getLogger(__name__)
        self._outcome = {'payoff': [], 'cooperation': []}
        self.matches = []

    @property
    def players(self):
        return self._players

    @players.setter
    def players(self, players):
        """Ensure that players are passed the tournament attributes"""
        newplayers = []
        for player in players:
            player.set_tournament_attributes(
                length=self.turns,
                 game=self.game,
                 noise=self.noise)
            newplayers.append(player)
        self._players = newplayers

    def play(self):
        """
        Plays the tournament and passes the results to the ResultSet class

        Returns
        -------
        axelrod.ResultSet
        """
        if self._processes is None:
            self._run_serial_repetitions(self._outcome)
        else:
            if self._build_cache_required():
                self._build_cache(self._outcome)
            self._run_parallel_repetitions(self._outcome)

        self.result_set = ResultSet(
            players=self.players,
            turns=self.turns,
            repetitions=self.repetitions,
            outcome=self._outcome,
            with_morality=self._with_morality)
        return self.result_set

    def _build_cache_required(self):
        """
        A boolean to indicate whether it is necessary to build the
        deterministic cache.
        """
        return (
            not self.noise and (
                len(self.deterministic_cache) == 0 or
                not self.prebuilt_cache))

    def _build_cache(self, outcome):
        """
        For parallel processing, this runs a single round robin in order to
        build the deterministic cache.

        Parameters
        ----------
        outcome : dictionary
            The outcome dictionary to update with results
        """
        self._logger.debug('Playing first round robin to build cache')
        self._run_single_repetition(outcome)
        self._parallel_repetitions -= 1

    def _run_single_repetition(self, outcome):
        """
        Runs a single round robin and updates the outcome dictionary.
        """
        matches = self.tournament_type(
            players=self.players,
            turns=self.turns,
            deterministic_cache=self.deterministic_cache,
            cache_mutable=True,
            noise=self.noise)
        output = self._play_matches(matches)
        outcome['payoff'].append(output['payoff'])
        outcome['cooperation'].append(output['cooperation'])
        if self._keep_matches:
            self.matches.append(output['matches'])

    def _run_serial_repetitions(self, outcome):
        """
        Runs all repetitions of the round robin in serial.

        Parameters
        ----------
        outcome : dictionary
            The outcome dictionary to update with results
        """
        self._logger.debug('Playing %d round robins' % self.repetitions)
        for repetition in range(self.repetitions):
            self._run_single_repetition(outcome)
        return True

    def _run_parallel_repetitions(self, outcome):
        """
        Run all except the first round robin using parallel processing.

        Parameters
        ----------
        outcome : dictionary
            The outcome dictionary to update with results
        """
        # At first sight, it might seem simpler to use the multiprocessing Pool
        # Class rather than Processes and Queues. However, Pool can only accept
        # target functions which can be pickled and instance methods cannot.
        work_queue = multiprocessing.Queue()
        done_queue = multiprocessing.Queue()
        workers = self._n_workers()

        for repetition in range(self._parallel_repetitions):
            work_queue.put(repetition)

        self._logger.debug(
            'Playing %d round robins with %d parallel processes' %
            (self._parallel_repetitions, workers))
        self._start_workers(workers, work_queue, done_queue)
        self._process_done_queue(workers, done_queue, outcome)

        return True

    def _n_workers(self):
        """
        Determines the number of parallel processes to use.

        Returns
        -------
        integer
        """
        if (2 <= self._processes <= multiprocessing.cpu_count()):
            n_workers = self._processes
        else:
            n_workers = multiprocessing.cpu_count()
        return n_workers

    def _start_workers(self, workers, work_queue, done_queue):
        """
        Initiates the sub-processes to carry out parallel processing.

        Parameters
        ----------
        workers : integer
            The number of sub-processes to create
        work_queue : multiprocessing.Queue
            A queue containing an entry for each round robin to be processed
        done_queue : multiprocessing.Queue
            A queue containing the output dictionaries from each round robin
        """
        for worker in range(workers):
            process = multiprocessing.Process(
                target=self._worker, args=(work_queue, done_queue))
            work_queue.put('STOP')
            process.start()
        return True

    def _process_done_queue(self, workers, done_queue, outcome):
        """
        Retrieves the outcome dictionaries from the parallel sub-processes

        Parameters
        ----------
        workers : integer
            The number of sub-processes in existence
        done_queue : multiprocessing.Queue
            A queue containing the output dictionaries from each round robin
        outcome : dictionary
           The outcome dictionary to update with results
        """
        stops = 0
        while stops < workers:
            output = done_queue.get()
            if output == 'STOP':
                stops += 1
            else:
                outcome['payoff'].append(output['payoff'])
                outcome['cooperation'].append(output['cooperation'])
                if self._keep_matches:
                    self.matches.append(outcome['matches'])
        return True

    def _worker(self, work_queue, done_queue):
        """
        The work for each parallel sub-process to execute.

        Parameters
        ----------
        work_queue : multiprocessing.Queue
            A queue containing an entry for each round robin to be processed
        done_queue : multiprocessing.Queue
            A queue containing the output dictionaries from each round robin
        """
        for repetition in iter(work_queue.get, 'STOP'):
            matches = self.tournament_type(
                players=self.players,
                turns=self.turns,
                deterministic_cache=self.deterministic_cache,
                cache_mutable=False,
                noise=self.noise)
            output = self._play_matches(matches)
            done_queue.put(output)
        done_queue.put('STOP')
        return True

    def _play_matches(self, matches):
        """
        Play the supplied matches.

        Parameters
        ----------
        matches : dictionary
            Mapping a tuple of player index numbers to an axelrod Match object

        Returns
        -------
        dictionary
            Containing the payoff and cooperation matrices
        """
        interactions = {}
        if self._keep_matches:
            matches_to_keep = []

        for key, match in matches.items():
            interactions[key] = match.play()
            if self._keep_matches:
                matches_to_keep.append(match)

        payoff = payoff_matrix(interactions, self.game)
        cooperation = cooperation_matrix(interactions)

        output = {'payoff': payoff, 'cooperation': cooperation}
        if self._keep_matches:
            output['matches'] = matches_to_keep
        return output
