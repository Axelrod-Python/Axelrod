from collections import defaultdict
import csv
import logging
from multiprocessing import Process, Queue, cpu_count
from tempfile import mkstemp
import warnings
import os

import tqdm

from axelrod import DEFAULT_TURNS
from axelrod.player import Player
from axelrod.action import actions_to_str
from .game import Game
from .match import Match
from .match_generator import MatchGenerator
from .result_set import ResultSetFromFile, ResultSet

from typing import List, Tuple


class Tournament(object):

    def __init__(self, players: List[Player],
                 name: str = 'axelrod', game: Game = None, turns: int = None,
                 prob_end: float = None, repetitions: int = 10,
                 noise: float = 0, edges: List[Tuple] = None,
                 match_attributes: dict = None) -> None:
        """
        Parameters
        ----------
        players : list
            A list of axelrod.Player objects
        name : string
            A name for the tournament
        game : axelrod.Game
            The game object used to score the tournament
        turns : integer
            The number of turns per match
        prob_end : float
            The probability of a given turn ending a match
        repetitions : integer
            The number of times the round robin should be repeated
        noise : float
            The probability that a player's intended action should be flipped
        prob_end : float
            The probability of a given turn ending a match
        edges : list
            A list of edges between players
        match_attributes : dict
            Mapping attribute names to values which should be passed to players.
            The default is to use the correct values for turns, game and noise
            but these can be overridden if desired.
        """
        if game is None:
            self.game = Game()
        else:
            self.game = game
        self.name = name
        self.noise = noise
        self.num_interactions = 0
        self.players = players
        self.repetitions = repetitions
        self.edges = edges

        if turns is None and prob_end is None:
            turns = DEFAULT_TURNS

        self.turns = turns
        self.prob_end = prob_end
        self.match_generator = MatchGenerator(players=players, turns=turns,
                                              game=self.game,
                                              repetitions=self.repetitions,
                                              prob_end=prob_end,
                                              noise=self.noise,
                                              edges=edges,
                                              match_attributes=match_attributes)
        self._logger = logging.getLogger(__name__)

        self.use_progress_bar = True
        self.filename = None  # type: str
        self._temp_file_descriptor = None  # type: int

    def setup_output(self, filename=None, in_memory=False):
        """assign/create `filename` to `self`. If file should be deleted once
        `play` is finished, assign a file descriptor. """
        temp_file_descriptor = None
        if in_memory:
            self.interactions_dict = {}
            filename = None
        if not in_memory and filename is None:
            temp_file_descriptor, filename = mkstemp()

        self.filename = filename
        self._temp_file_descriptor = temp_file_descriptor

    def play(self, build_results: bool = True, filename: str = None,
             processes: int = None, progress_bar: bool = True,
             keep_interactions: bool = False, in_memory: bool = False
             ) -> ResultSetFromFile:
        """
        Plays the tournament and passes the results to the ResultSet class

        Parameters
        ----------
        build_results : bool
            whether or not to build a results st
        filename : string
            name of output file
        processes : integer
            The number of processes to be used for parallel processing
        progress_bar : bool
            Whether or not to create a progress bar which will be updated
        keep_interactions : bool
            Whether or not to load the interactions in to memory
        in_memory : bool
            By default interactions are written to a file.
            If this is True they will be kept in memory.
            This is not advised for large tournaments.

        Returns
        -------
        axelrod.ResultSetFromFile
        """
        self.num_interactions = 0

        self.use_progress_bar = progress_bar

        self.setup_output(filename, in_memory)

        if not build_results and not filename:
            warnings.warn(
                "Tournament results will not be accessible since "
                "build_results=False and no filename was supplied.")

        if processes is None:
            self._run_serial()
        else:
            self._run_parallel(processes=processes)

        result_set = None
        if build_results:
            result_set = self._build_result_set(
                keep_interactions=keep_interactions, in_memory=in_memory
            )

        if self._temp_file_descriptor is not None:
            os.close(self._temp_file_descriptor)
            os.remove(self.filename)

        return result_set

    def _build_result_set(self, keep_interactions: bool = False,
                          in_memory: bool = False):
        """
        Build the result set (used by the play method)

        Returns
        -------
        axelrod.BigResultSet
        """
        if not in_memory:
            result_set = ResultSetFromFile(
                filename=self.filename,
                progress_bar=self.use_progress_bar,
                num_interactions=self.num_interactions,
                repetitions=self.repetitions,
                players=[str(p) for p in self.players],
                keep_interactions=keep_interactions,
                game=self.game)
        else:
            result_set = ResultSet(
                players=[str(p) for p in self.players],
                interactions=self.interactions_dict,
                repetitions=self.repetitions,
                progress_bar=self.use_progress_bar,
                game=self.game)
        return result_set

    def _run_serial(self) -> bool:
        """Run all matches in serial."""

        chunks = self.match_generator.build_match_chunks()

        out_file, writer = self._get_file_objects()
        progress_bar = self._get_progress_bar()

        for chunk in chunks:
            results = self._play_matches(chunk)
            self._write_interactions(results, writer=writer)

            if self.use_progress_bar:
                progress_bar.update(1)

        _close_objects(out_file, progress_bar)

        return True

    def _get_file_objects(self):
        """Returns the file object and writer for writing results or
        (None, None) if self.filename is None"""
        file_obj = None
        writer = None
        if self.filename is not None:
            file_obj = open(self.filename, 'w')
            writer = csv.writer(file_obj, lineterminator='\n')
        return file_obj, writer

    def _get_progress_bar(self):
        if self.use_progress_bar:
            return tqdm.tqdm(total=self.match_generator.size,
                             desc="Playing matches")
        return None

    def _write_interactions(self, results, writer=None):
        """Write the interactions to file or to a dictionary"""
        if writer is not None:
            self._write_interactions_to_file(results, writer)
        elif self.interactions_dict is not None:
            self._write_interactions_to_dict(results)

    def _write_interactions_to_file(self, results, writer):
        """Write the interactions to csv."""
        for index_pair, interactions in results.items():
            for interaction in interactions:
                row = list(index_pair)
                row.append(str(self.players[index_pair[0]]))
                row.append(str(self.players[index_pair[1]]))
                history1 = actions_to_str([i[0] for i in interaction])
                history2 = actions_to_str([i[1] for i in interaction])
                row.append(history1)
                row.append(history2)
                writer.writerow(row)
                self.num_interactions += 1

    def _write_interactions_to_dict(self, results):
        """Write the interactions to memory"""
        for index_pair, interactions in results.items():
            for interaction in interactions:
                try:
                    self.interactions_dict[index_pair].append(interaction)
                except KeyError:
                    self.interactions_dict[index_pair] = [interaction]
                self.num_interactions += 1

    def _run_parallel(self, processes: int=2) -> bool:
        """
        Run all matches in parallel

        Parameters
        ----------

        processes : int
            How many processes to use.
        """
        # At first sight, it might seem simpler to use the multiprocessing Pool
        # Class rather than Processes and Queues. However, this way is faster.
        work_queue = Queue()  # type: Queue
        done_queue = Queue()  # type: Queue
        workers = self._n_workers(processes=processes)

        chunks = self.match_generator.build_match_chunks()
        for chunk in chunks:
            work_queue.put(chunk)

        self._start_workers(workers, work_queue, done_queue)
        self._process_done_queue(workers, done_queue)

        return True

    def _n_workers(self, processes: int = 2) -> int:
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

    def _start_workers(self, workers: int, work_queue: Queue,
                       done_queue: Queue) -> bool:
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

    def _process_done_queue(self, workers: int, done_queue: Queue):
        """
        Retrieves the matches from the parallel sub-processes

        Parameters
        ----------
        workers : integer
            The number of sub-processes in existence
        done_queue : multiprocessing.Queue
            A queue containing the output dictionaries from each round robin
        """
        out_file, writer = self._get_file_objects()
        progress_bar = self._get_progress_bar()

        stops = 0
        while stops < workers:
            results = done_queue.get()
            if results == 'STOP':
                stops += 1
            else:
                self._write_interactions(results, writer)

                if self.use_progress_bar:
                    progress_bar.update(1)

        _close_objects(out_file, progress_bar)
        return True

    def _worker(self, work_queue: Queue, done_queue: Queue):
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

                (0, 1) -> [(C, D), (D, C),...]
        """
        interactions = defaultdict(list)
        index_pair, match_params, repetitions = chunk
        p1_index, p2_index = index_pair
        player1 = self.players[p1_index].clone()
        player2 = self.players[p2_index].clone()
        match_params["players"] = (player1, player2)
        match = Match(**match_params)
        for _ in range(repetitions):
            match.play()
            interactions[index_pair].append(match.result)
        return interactions


def _close_objects(*objs):
    """If the objects have a `close` method, closes them."""
    for obj in objs:
        if hasattr(obj, 'close'):
            obj.close()
