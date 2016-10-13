from __future__ import absolute_import

from collections import defaultdict
from multiprocessing import Process, Queue, cpu_count
from tempfile import NamedTemporaryFile
import csv
import logging
import tqdm
import warnings

from axelrod import on_windows
from .game import Game
from .match import Match
from .match_generator import RoundRobinMatches, ProbEndRoundRobinMatches, SpatialMatches, ProbEndSpatialMatches
from .result_set import ResultSetFromFile, ResultSet


class Tournament(object):

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
        noise : float
            The probability that a player's intended action should be flipped
        with_morality : boolean
            Whether morality metrics should be calculated
        """
        if game is None:
            self.game = Game()
        else:
            self.game = game
        self.name = name
        self.turns = turns
        self.noise = noise
        self.num_interactions = 0
        self.players = players
        self.repetitions = repetitions
        self.match_generator = match_generator(
            players, turns, self.game, self.repetitions, self.noise)
        self._with_morality = with_morality
        self._logger = logging.getLogger(__name__)

    def setup_output(self, filename=None, in_memory=False):
        """Open a CSV writer for tournament output."""
        if in_memory:
            self.interactions_dict = {}
            self.writer = None
        else:
            if filename:
                self.outputfile = open(filename, 'w')
            else:
                # Setup a temporary file
                self.outputfile = NamedTemporaryFile(mode='w')
                filename = self.outputfile.name
            self.writer = csv.writer(self.outputfile, lineterminator='\n')
            # Save filename for loading ResultSet later
            self.filename = filename

    def play(self, build_results=True, filename=None,
             processes=None, progress_bar=True,
             keep_interactions=False, in_memory=False):
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
        if progress_bar:
            self.progress_bar = tqdm.tqdm(total=len(self.match_generator),
                                          desc="Playing matches")

        if on_windows and (filename is None):
            in_memory = True

        self.setup_output(filename, in_memory)

        if not build_results and not filename:
            warnings.warn("Tournament results will not be accessible since build_results=False and no filename was supplied.")

        if (processes is None) or (on_windows):
            self._run_serial(progress_bar=progress_bar)
        else:
            self._run_parallel(processes=processes, progress_bar=progress_bar)

        if progress_bar:
            self.progress_bar.close()

        # Make sure that python has finished writing to disk
        if not in_memory:
            self.outputfile.flush()

        if build_results:
            return self._build_result_set(progress_bar=progress_bar,
                                          keep_interactions=keep_interactions,
                                          in_memory=in_memory)
        elif not in_memory:
            self.outputfile.close()

    def _build_result_set(self, progress_bar=True, keep_interactions=False,
                          in_memory=False):
        """
        Build the result set (used by the play method)

        Returns
        -------
        axelrod.BigResultSet
        """
        if not in_memory:
            result_set = ResultSetFromFile(filename=self.filename,
                                           progress_bar=progress_bar,
                                           num_interactions=self.num_interactions,
                                           repetitions=self.repetitions,
                                           players=[str(p) for p in self.players],
                                           keep_interactions=keep_interactions,
                                           game=self.game)
            self.outputfile.close()
        else:
            result_set = ResultSet(players=[str(p) for p in self.players],
                                   interactions=self.interactions_dict,
                                   num_interactions=self.num_interactions,
                                   repetitions=self.repetitions,
                                   progress_bar=progress_bar,
                                   game=self.game)
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
        """Write the interactions to file or to a dictionary"""
        if self.writer is not None:
          self._write_interactions_to_file(results)
        elif self.interactions_dict is not None:
          self._write_interactions_to_dict(results)

    def _write_interactions_to_file(self, results):
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
    A tournament in which the player don't know the length of a given match. The
    length of a match is equivalent to randomly sampling after each round
    whether or not to continue.
    """

    def __init__(self, players, match_generator=ProbEndRoundRobinMatches,
                 name='axelrod', game=None, prob_end=.5, repetitions=10,
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
        prob_end : a float
            The probability of a given match ending
        repetitions : integer
            The number of times the round robin should be repeated
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


class SpatialTournament(Tournament):
    """
    A tournament in which the players are allocated in a graph as nodes
    and they players only play the others that are connected to with an edge.
    """
    def __init__(self, players, edges, name='axelrod', game=None, turns=200,
                 repetitions=10, noise=0, with_morality=True):
        """
        Parameters
        ----------
        players : list
            A list of axelrod.Player objects
        name : string
            A name for the tournament
        game : axelrod.Game
            The game object used to score the tournament
        edges : list
            A list of tuples containing the existing edges
        repetitions : integer
            The number of times the round robin should be repeated
        noise : float
            The probability that a player's intended action should be flipped
        with_morality : boolean
            Whether morality metrics should be calculated
        """
        super(SpatialTournament, self).__init__(
            players, name=name, game=game, turns=turns,
            repetitions=repetitions, noise=noise, with_morality=with_morality)

        self.edges = edges
        self.match_generator = SpatialMatches(
            players, turns, self.game, repetitions, edges, noise)


class ProbEndSpatialTournament(ProbEndTournament):
    """
    A tournament in which the players are allocated in a graph as nodes
    and they players only play the others that are connected to with an edge.
    Players do not know the length of a given match (it is randomly sampled).
    """
    def __init__(self, players, edges, name='axelrod', game=None, prob_end=.5,
                 repetitions=10, noise=0, with_morality=True):
        """
        Parameters
        ----------
        players : list
            A list of axelrod.Player objects
        name : string
            A name for the tournament
        game : axelrod.Game
            The game object used to score the tournament
        prob_end : a float
            The probability of a given match ending
        edges : list
            A list of tuples containing the existing edges
        repetitions : integer
            The number of times the round robin should be repeated
        noise : float
            The probability that a player's intended action should be flipped
        with_morality : boolean
            Whether morality metrics should be calculated
        """
        super(ProbEndSpatialTournament, self).__init__(
            players, name=name, game=game, prob_end=prob_end,
            repetitions=repetitions, noise=noise, with_morality=with_morality)

        self.edges = edges
        self.match_generator = ProbEndSpatialMatches(
            players, prob_end, self.game, repetitions, noise, edges)
