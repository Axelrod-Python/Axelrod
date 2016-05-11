from __future__ import absolute_import

import csv
from collections import defaultdict
import logging
from multiprocessing import Process, Queue, cpu_count
from tempfile import NamedTemporaryFile
import warnings

import tqdm

from .game import Game
from .match import Match
from .match_generator import RoundRobinMatches, ProbEndRoundRobinMatches
from .result_set import ResultSet, ResultSetFromFile


class Tournament(object):
    game = Game()

    def __init__(self, players, match_generator=RoundRobinMatches,
                 name='axelrod', game=None, turns=200, repetitions=10,
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
        self.match_generator = match_generator(players, turns, self.game,
                                               self.repetitions)
        self._with_morality = with_morality
        self._logger = logging.getLogger(__name__)

    def setup_output_file(self, filename=None):
        """Open a CSV writer for tournament output."""
        if filename:
            self.outputfile = open(filename, 'a')
        else:
            # Setup a temporary file
            self.outputfile = NamedTemporaryFile(mode='w')
            filename = self.outputfile.name
        self.writer = csv.writer(self.outputfile)
        # Save filename for loading ResultSet later
        self.filename = filename

    def play(self, build_results=True, filename=None, processes=None, progress_bar=True):
        """
        Plays the tournament and passes the results to the ResultSet class

        Parameters
        ----------
        build_results : bool
            whether or not to build a results st
        filename : string
            name of output file
        progress_bar : bool
            Whether or not to create a progress bar which will be updated

        Returns
        -------
        axelrod.ResultSet
        """
        if progress_bar:
            self.progress_bar = tqdm.tqdm(total=len(self.match_generator))

        self.setup_output_file(filename)
        if not build_results and not filename:
            warnings.warn("Tournament results will not be accessible since build_results=False and no filename was supplied.")

        if processes is None:
            self._run_serial(progress_bar=progress_bar)
        else:
            self._run_parallel(processes=processes, progress_bar=progress_bar)

        # Make sure that python has finished writing to disk
        self.outputfile.flush()

        if build_results:
            return self._build_result_set()

    def _build_result_set(self):
        """
        Build the result set (used by the play method)

        Returns
        -------
        axelrod.ResultSet
        """
        result_set = ResultSetFromFile(
            filename=self.filename,
            with_morality=self._with_morality)
        self.outputfile.close()
        return result_set

    def _run_serial(self, progress_bar=False):
        """
        Run all matches in serial

        Parameters
        ----------

        progress_bar : bool
            Whether or not to update the tournament progress bar
        """
        chunks = self.match_generator.build_match_chunks()

        for chunk in chunks:
            results = self._play_matches(chunk)
            self._write_interactions(results)

            if progress_bar:
                self.progress_bar.update(1)

        return True

    def _write_interactions(self, results):
        """Write the interactions to csv."""
        for index_pair, interactions in results.items():
            for interaction in interactions:
                row = list(index_pair)
                row.append(str(self.players[index_pair[0]]))
                row.append(str(self.players[index_pair[1]]))
                history1 = "".join([i[0] for i in interaction])
                history2 = "".join([i[1] for i in interaction])
                row.append(history1)
                row.append(history2)
                self.writer.writerow(row)

    def _run_parallel(self, processes=2, progress_bar=False):
        """
        Run all matches in parallel

        Parameters
        ----------

        progress_bar : bool
            Whether or not to update the tournament progress bar
        """
        # At first sight, it might seem simpler to use the multiprocessing Pool
        # Class rather than Processes and Queues. However, Pool can only accept
        # target functions which can be pickled and instance methods cannot.
        work_queue = Queue()
        done_queue = Queue()
        workers = self._n_workers(processes=processes)

        chunks = self.match_generator.build_match_chunks()
        for chunk in chunks:
            work_queue.put(chunk)

        self._start_workers(workers, work_queue, done_queue)
        self._process_done_queue(workers, done_queue, progress_bar=progress_bar)

        return True

    def _n_workers(self, processes=2):
        """
        Determines the number of parallel processes to use.

        Returns
        -------
        integer
        """
        if (2 <= processes <= cpu_count()):
            n_workers = processes
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
        for worker in range(workers):
            process = Process(
                target=self._worker, args=(work_queue, done_queue))
            work_queue.put('STOP')
            process.start()
        return True

    def _process_done_queue(self, workers, done_queue, progress_bar=False):
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
        progress_bar : bool
            Whether or not to update the tournament progress bar
        """
        stops = 0
        while stops < workers:
            results = done_queue.get()

            if results == 'STOP':
                stops += 1
            else:
                self._write_interactions(results)

                if progress_bar:
                    self.progress_bar.update(1)
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
        for chunk in iter(work_queue.get, 'STOP'):
            interactions = self._play_matches(chunk)
            done_queue.put(interactions)
        done_queue.put('STOP')
        return True

    def _play_matches(self, chunk):
        """
        Play matches in a given chunk.

        Parameters
        ----------
        chunk : tuple (index pair, match_parameters, repetitions)
            match_parameters are also a tuple: (turns, game, noise)

        Returns
        -------
        interactions : dictionary
            Mapping player index pairs to results of matches:

                (0, 1) -> [('C', 'D'), ('D', 'C'),...]
        """
        interactions = defaultdict(list)
        index_pair, match_params, repetitions = chunk
        p1_index, p2_index = index_pair
        player1 = self.players[p1_index].clone()
        player2 = self.players[p2_index].clone()
        players = (player1, player2)
        params = [players]
        params.extend(match_params)
        match = Match(*params)
        for _ in range(repetitions):
            match.play()
            interactions[index_pair].append(match.result)
        return interactions


class ProbEndTournament(Tournament):
    """
    A tournament in which the player don't know the length of a given match
    (currently implemented by setting this to be infinite). The length of a
    match is equivalent to randomly sampling after each round whether or not to
    continue.
    """

    def __init__(self, players, match_generator=ProbEndRoundRobinMatches,
                 name='axelrod', game=None, prob_end=.5, repetitions=10,
                 noise=0,
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
        noise : float
            The probability that a player's intended action should be flipped
        with_morality : boolean
            Whether morality metrics should be calculated
        """
        super(ProbEndTournament, self).__init__(
            players, name=name, game=game, turns=float("inf"),
            repetitions=repetitions, noise=noise, with_morality=with_morality)

        self.prob_end = prob_end
        self.match_generator = ProbEndRoundRobinMatches(
            players, prob_end, self.game, repetitions)
