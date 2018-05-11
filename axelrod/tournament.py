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
from .result_set import ResultSet
from axelrod.action import Action, str_to_actions

import axelrod.interaction_utils as iu

C, D = Action.C, Action.D

from typing import List, Tuple, Optional


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
        self.filename = None  # type: Optional[str]
        self._temp_file_descriptor = None  # type: Optional[int]

    def setup_output(self, filename=None):
        """assign/create `filename` to `self`. If file should be deleted once
        `play` is finished, assign a file descriptor. """
        temp_file_descriptor = None
        if filename is None:
            temp_file_descriptor, filename = mkstemp()

        self.filename = filename
        self._temp_file_descriptor = temp_file_descriptor


    def play(self, build_results: bool = True, filename: str = None,
             processes: int = None, progress_bar: bool = True,
             ) -> ResultSet:
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

        Returns
        -------
        axelrod.ResultSet
        """
        self.num_interactions = 0

        self.use_progress_bar = progress_bar

        self.setup_output(filename)

        if not build_results and not filename:
            warnings.warn(
                "Tournament results will not be accessible since "
                "build_results=False and no filename was supplied.")

        if processes is None:
            self._run_serial(build_results=build_results)
        else:
            self._run_parallel(build_results=build_results, processes=processes)

        result_set = None
        if build_results:
            result_set = ResultSet(filename=self.filename,
                                   players=[str(p) for p in self.players],
                                   repetitions=self.repetitions,
                                   processes=processes,
                                   progress_bar=progress_bar)
        if self._temp_file_descriptor is not None:
            assert self.filename is not None
            os.close(self._temp_file_descriptor)
            os.remove(self.filename)

        return result_set


    def _run_serial(self, build_results: bool=True) -> bool:
        """Run all matches in serial."""

        chunks = self.match_generator.build_match_chunks()

        out_file, writer = self._get_file_objects(build_results)
        progress_bar = self._get_progress_bar()

        for chunk in chunks:
            results = self._play_matches(chunk, build_results=build_results)
            self._write_interactions_to_file(results, writer=writer)

            if self.use_progress_bar:
                progress_bar.update(1)

        _close_objects(out_file, progress_bar)

        return True

    def _get_file_objects(self, build_results=True):
        """Returns the file object and writer for writing results or
        (None, None) if self.filename is None"""
        file_obj = None
        writer = None
        if self.filename is not None:
            file_obj = open(self.filename, 'w')
            writer = csv.writer(file_obj, lineterminator='\n')

            header = ["Interaction index",
                      "Player index",
                      "Opponent index",
                      "Repetition",
                      "Player name",
                      "Opponent name",
                      "Actions"]
            if build_results:
                header.extend(["Score",
                               "Score difference",
                               "Turns",
                               "Score per turn",
                               "Score difference per turn",
                               "Win",
                               "Initial cooperation",
                               "Cooperation count",
                               "CC count",
                               "CD count",
                               "DC count",
                               "DD count",
                               "CC to C count",
                               "CC to D count",
                               "CD to C count",
                               "CD to D count",
                               "DC to C count",
                               "DC to D count",
                               "DD to C count",
                               "DD to D count",
                               "Good partner"])

            writer.writerow(header)
        return file_obj, writer

    def _get_progress_bar(self):
        if self.use_progress_bar:
            return tqdm.tqdm(total=self.match_generator.size,
                             desc="Playing matches")
        return None

    def _write_interactions_to_file(self, results, writer):
        """Write the interactions to csv."""
        for index_pair, interactions in results.items():
            repetition = 0
            for interaction, results in interactions:

                if results is not None:
                    (scores,
                     score_diffs,
                     turns, score_per_turns,
                     score_diffs_per_turns,
                     initial_cooperation,
                     cooperations,
                     state_distribution,
                     state_to_action_distributions,
                     winner_index) = results
                for index, player_index in enumerate(index_pair):
                    opponent_index = index_pair[index - 1]
                    row = [self.num_interactions, player_index, opponent_index,
                           repetition]
                    row.append(str(self.players[player_index]))
                    row.append(str(self.players[opponent_index]))
                    history = actions_to_str([i[index] for i in interaction])
                    row.append(history)

                    if results is not None:
                        row.append(scores[index])
                        row.append(score_diffs[index])
                        row.append(turns)
                        row.append(score_per_turns[index])
                        row.append(score_diffs_per_turns[index])
                        row.append(int(winner_index is index))
                        row.append(initial_cooperation[index])
                        row.append(cooperations[index])

                        states = [(C, C), (C, D), (D, C), (D, D)]
                        if index == 1:
                            states = [s[::-1] for s in states]
                        for state in states:
                            row.append(state_distribution[state])
                        for state in states:
                            row.append(state_to_action_distributions[index][(state, C)])
                            row.append(state_to_action_distributions[index][(state, D)])

                        row.append(int(cooperations[index] >= cooperations[index - 1]))

                    writer.writerow(row)
                repetition += 1
                self.num_interactions += 1

    def _run_parallel(self, processes: int=2, build_results: bool=True) -> bool:
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

        self._start_workers(workers, work_queue, done_queue, build_results)
        self._process_done_queue(workers, done_queue, build_results)

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
                       done_queue: Queue, build_results: bool=True) -> bool:
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
                target=self._worker, args=(work_queue, done_queue, build_results))
            work_queue.put('STOP')
            process.start()
        return True

    def _process_done_queue(self, workers: int, done_queue: Queue,
                            build_results: bool=True):
        """
        Retrieves the matches from the parallel sub-processes

        Parameters
        ----------
        workers : integer
            The number of sub-processes in existence
        done_queue : multiprocessing.Queue
            A queue containing the output dictionaries from each round robin
        """
        out_file, writer = self._get_file_objects(build_results)
        progress_bar = self._get_progress_bar()

        stops = 0
        while stops < workers:
            results = done_queue.get()
            if results == 'STOP':
                stops += 1
            else:
                self._write_interactions_to_file(results, writer)

                if self.use_progress_bar:
                    progress_bar.update(1)

        _close_objects(out_file, progress_bar)
        return True

    def _worker(self, work_queue: Queue, done_queue: Queue,
                build_results: bool=True):
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
            interactions = self._play_matches(chunk, build_results)
            done_queue.put(interactions)
        done_queue.put('STOP')
        return True

    def _play_matches(self, chunk, build_results=True):
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

            if build_results:
                results = self._calculate_results(match.result)
            else:
                results = None

            interactions[index_pair].append([match.result, results])
        return interactions

    def _calculate_results(self, interactions):
        results = []

        scores = iu.compute_final_score(interactions, self.game)
        results.append(scores)

        score_diffs = scores[0] - scores[1], scores[1] - scores[0]
        results.append(score_diffs)

        turns = len(interactions)
        results.append(turns)

        score_per_turns = iu.compute_final_score_per_turn(interactions,
                                                          self.game)
        results.append(score_per_turns)

        score_diffs_per_turns = score_diffs[0] / turns, score_diffs[1] / turns
        results.append(score_diffs_per_turns)

        initial_coops = tuple(map(
                                bool,
                                iu.compute_cooperations(interactions[:1])))
        results.append(initial_coops)

        cooperations = iu.compute_cooperations(interactions)
        results.append(cooperations)

        state_distribution = iu.compute_state_distribution(interactions)
        results.append(state_distribution)

        state_to_action_distributions = iu.compute_state_to_action_distribution(interactions)
        results.append(state_to_action_distributions)

        winner_index = iu.compute_winner_index(interactions, self.game)
        results.append(winner_index)

        return results


def _close_objects(*objs):
    """If the objects have a `close` method, closes them."""
    for obj in objs:
        if hasattr(obj, 'close'):
            obj.close()
