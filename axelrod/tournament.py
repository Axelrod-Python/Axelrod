from __future__ import absolute_import

import logging
from multiprocess import Process, Queue, cpu_count
import csv

from .game import Game
from .result_set import ResultSet
from .deterministic_cache import DeterministicCache
from .match_generator import RoundRobinMatches, ProbEndRoundRobinMatches

from tqdm import tqdm

class Tournament(object):
    game = Game()

    def __init__(self, players, match_generator=RoundRobinMatches,
                 name='axelrod', game=None, turns=200, repetitions=10,
                 processes=None, deterministic_cache=None, prebuilt_cache=False,
                 noise=0, with_morality=True):
        """
        Parameters
        ----------
        players : list
            A list of axelrod.Player objects
        match_generator : class
            A class that must be descended from axelrod.MatchGenerator
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
        deterministic_cache : instance
            An instance of the axelrod.DeterministicCache class
        prebuilt_cache : boolean
            Whether a cache has been passed in from an external object
        noise : float
            The probability that a player's intended action should be flipped
        with_morality : boolean
            Whether morality metrics should be calculated
        """
        self.name = name
        self.turns = turns
        self.noise = noise
        if game is not None:
            self.game = game
        self.players = players
        self.repetitions = repetitions
        if deterministic_cache is not None:
            self.prebuilt_cache = True
            self.deterministic_cache = deterministic_cache
        else:
            self.prebuilt_cache = prebuilt_cache
            self.deterministic_cache = DeterministicCache()
        self.match_generator = match_generator(
            players, turns, self.game, self.deterministic_cache)
        self._with_morality = with_morality
        self._parallel_repetitions = repetitions
        self._processes = processes
        self._logger = logging.getLogger(__name__)
        self.interactions = []

    def play(self, filename=None, progress_bar=None):
        """
        Plays the tournament and passes the results to the ResultSet class
        If a filename is passed it write the results to file.

        Returns
        -------
        axelrod.ResultSet

        Parameters
        ----------

        progress_bar : Boolean
            Whether or not to display a progress bar
        """
        if progress_bar is not None:  # Create a progress bar
            progress_bar = tqdm(total=self.repetitions)

        if self._processes is None:
            self._run_serial_repetitions(self.interactions,
                                         progress_bar=progress_bar)
        else:
            if self._build_cache_required():
                self._build_cache(self.interactions, progress_bar)
            self._run_parallel_repetitions(self.interactions,
                                           progress_bar=progress_bar)

        if filename is None:
            self.result_set = self._build_result_set()
            return self.result_set
        self._write_to_csv(filename)

        if progress_bar is not None:  # Close the progress bar
            progress_bar.close()

    def _build_result_set(self):
        """
        Build the result set (used by the play method)

        Returns
        -------
        axelrod.ResultSet
        """
        result_set = ResultSet(
            players=self.players,
            interactions=self.interactions,
            with_morality=self._with_morality)
        return result_set

    def _build_cache_required(self):
        """
        A boolean to indicate whether it is necessary to build the
        deterministic cache.
        """
        return (
            not self.noise and (
                len(self.deterministic_cache) == 0 or
                not self.prebuilt_cache))

    def _build_cache(self, matches, progress_bar=None):
        """
        For parallel processing, this runs a single round robin in order to
        build the deterministic cache.

        Parameters
        ----------
        matches : list
            The list of matches to update
        progress_bar : tqdm.tqdm progress bar object
            The progress bar being updated
        """
        self._logger.debug('Playing first round robin to build cache')
        self._run_single_repetition(matches, progress_bar)
        self._parallel_repetitions -= 1

    def _run_single_repetition(self, interactions, progress_bar=None):
        """
        Runs a single round robin and updates the matches list.

        Parameters
        ----------
        progress_bar : tqdm.tqdm progress bar object
            The progress bar being updated
        """
        new_matches = self.match_generator.build_matches(noise=self.noise)
        interactions = self._play_matches(new_matches)
        self.interactions.append(interactions)
        if progress_bar is not None:
            progress_bar.update(1)

    def _run_serial_repetitions(self, interactions, progress_bar=None):
        """
        Runs all repetitions of the round robin in serial.

        Parameters
        ----------
        interactions : list
            The list of interactions per repetition to update with results
        progress_bar : tqdm.tqdm progress bar object
            The progress bar being updated
        """
        self._logger.debug('Playing %d round robins' % self.repetitions)

        for repetition in range(self.repetitions):
            self._run_single_repetition(interactions, progress_bar)

        return True

    def _run_parallel_repetitions(self, interactions, progress_bar=None):
        """
        Run all except the first round robin using parallel processing.

        Parameters
        ----------
        interactions : list
            The list of interactions per repetition to update with results
        progress_bar : tqdm.tqdm progress bar object
            The progress bar being updated
        """
        # At first sight, it might seem simpler to use the multiprocessing Pool
        # Class rather than Processes and Queues. However, Pool can only accept
        # target functions which can be pickled and instance methods cannot.
        work_queue = Queue()
        done_queue = Queue()
        workers = self._n_workers()
        for repetition in range(self._parallel_repetitions):
            work_queue.put(repetition)

        self._logger.debug(
            'Playing %d round robins with %d parallel processes' %
            (self._parallel_repetitions, workers))
        self._start_workers(workers, work_queue, done_queue)
        self._process_done_queue(workers, done_queue, interactions, progress_bar)

        return True

    def _n_workers(self):
        """
        Determines the number of parallel processes to use.

        Returns
        -------
        integer
        """
        if (2 <= self._processes <= cpu_count()):
            n_workers = self._processes
        else:
            n_workers = cpu_count()
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
        self.deterministic_cache.mutable = False
        for worker in range(workers):
            process = Process(
                target=self._worker, args=(work_queue, done_queue))
            work_queue.put('STOP')
            process.start()
        return True

    def _process_done_queue(self, workers, done_queue, interactions,
            progress_bar=None):
        """
        Retrieves the matches from the parallel sub-processes

        Parameters
        ----------
        workers : integer
            The number of sub-processes in existence
        done_queue : multiprocessing.Queue
            A queue containing the output dictionaries from each round robin
        interactions : list
            The list of interactions per repetition to update with results
        progress_bar : tqdm.tqdm progress bar object
            The progress bar being updated
        """
        stops = 0
        while stops < workers:
            results = done_queue.get()

            if results == 'STOP':
                stops += 1
            else:
                interactions.append(results)
                if progress_bar is not None:
                    progress_bar.update(1)
        return True

    def _worker(self, work_queue, done_queue, progress_bar=None):
        """
        The work for each parallel sub-process to execute.

        Parameters
        ----------
        work_queue : multiprocessing.Queue
            A queue containing an entry for each round robin to be processed
        done_queue : multiprocessing.Queue
            A queue containing the output dictionaries from each round robin
        progress_bar : tqdm.tqdm progress bar object
            The progress bar being updated
        """

        for repetition in iter(work_queue.get, 'STOP'):
            new_matches = self.match_generator.build_matches(noise=self.noise)
            interactions = self._play_matches(new_matches)

            done_queue.put(interactions)
        done_queue.put('STOP')

        return True

    def _play_matches(self, matches):
        """
        Play the supplied matches.

        Parameters
        ----------
        matches : generator
            Generator of tuples: player index pair, match

        Returns
        -------
        interactions : dictionary
            Mapping player index pairs to results of matches:

                (0, 1) -> [('C', 'D'), ('D', 'C'),...]
        """
        interactions = {}
        for index_pair, match in matches:
            match.play()
            interactions[index_pair] = match.result
        return interactions

    def _write_to_csv(self, filename):
        """Write the interactions to csv."""
        with open(filename, 'w') as csvfile:
            writer = csv.writer(csvfile)
            for row in self._data_for_csv():
                writer.writerow(row)

    def _data_for_csv(self):
        """
        Returns
        -------
        A generator of the interactions to a list of lists of the form:

        [p1index, p2index, p1name, p2name, p1rep1ac1p2rep1ac1p1rep1ac2p2rep1ac2,
        ...]
        [0, 1, Defector, Cooperator, DCDCDC, DCDCDC, DCDCDC,...]
        [0, 2, Defector, Alternator, DCDDDC, DCDDDC, DCDDDC,...]
        [1, 2, Cooperator, Alternator, CCCDCC, CCCDCC, CCCDCC,...]
        """
        index_pairs = self.interactions[0].keys()
        for index_pair in index_pairs:
            p1, p2 = index_pair
            row = [p1, p2, self.players[p1].name, self.players[p2].name]
            for rep in self.interactions:
                interaction = rep[index_pair]
                matchstringrep = ''.join([act for inter in interaction
                                          for act in inter])
                row.append(matchstringrep)
            yield row


class ProbEndTournament(Tournament):
    """
    A tournament in which the player don't know the length of a given match
    (currently implemented by setting this to be infinite). The length of a
    match is equivalent to randomly sampling after each round whether or not to
    continue.
    """

    def __init__(self, players, match_generator=ProbEndRoundRobinMatches,
                 name='axelrod', game=None, prob_end=.5, repetitions=10,
                 processes=None, prebuilt_cache=False, noise=0,
                 with_morality=True):
        """
        Parameters
        ----------
        players : list
            A list of axelrod.Player objects
        match_generator : class
            A class that must be descended from axelrod.MatchGenerator
        name : string
            A name for the tournament
        game : axelrod.Game
            The game object used to score the tournament
        prob_end : a float
            The probability of a given match ending
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
        """
        super(ProbEndTournament, self).__init__(
            players, name=name, game=game, turns=float("inf"),
            repetitions=repetitions, processes=processes,
            prebuilt_cache=prebuilt_cache, noise=noise,
            with_morality=with_morality)

        self.prob_end = prob_end
        self.match_generator = ProbEndRoundRobinMatches(
            players, prob_end, self.game, self.deterministic_cache)

    def _build_cache_required(self):
        """
        A cache is never required (as every Match length can be different)
        """
        return False
