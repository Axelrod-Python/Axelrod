from __future__ import absolute_import

import logging
import multiprocessing

from .game import *
from .result_set import *
from .round_robin import *


class Tournament(object):
    game = Game()

    def __init__(self, players, name='axelrod', game=None, turns=200,
                 repetitions=10, processes=None, prebuilt_cache=False,
                 noise=0, with_morality=True):
        self.name = name
        self.turns = turns
        self.players = players
        self.nplayers = len(self.players)
        if game is not None:
            self.game = game
        self.repetitions = repetitions
        self.prebuilt_cache = prebuilt_cache
        self.deterministic_cache = {}
        self.noise = noise
        self._with_morality = with_morality
        self._parallel_repetitions = repetitions
        self._processes = processes
        self._logger = logging.getLogger(__name__)
        self._outcome = {'payoff': [], 'cooperation': []}

    @property
    def players(self):
        return self._players

    @players.setter
    def players(self, players):
        newplayers = []
        for player in players:
            player.set_tournament_attributes(length=self.turns,
                                             game= self.game)
            newplayers.append(player)
        self._players = newplayers

    def play(self):
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
        return (
            not self.noise and (
                len(self.deterministic_cache) == 0 or
                not self.prebuilt_cache))

    def _build_cache(self, outcome):
        self._logger.debug('Playing first round robin to build cache')
        self._run_single_repetition(outcome)
        self._parallel_repetitions -= 1

    def _run_single_repetition(self, outcome):
        output = self._play_round_robin()
        outcome['payoff'].append(output['payoff'])
        outcome['cooperation'].append(output['cooperation'])

    def _run_serial_repetitions(self, outcome):
        self._logger.debug('Playing %d round robins' % self.repetitions)
        for repetition in range(self.repetitions):
            self._run_single_repetition(outcome)
        return True

    def _run_parallel_repetitions(self, outcome):
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
        if (2 <= self._processes <= multiprocessing.cpu_count()):
            n_workers = self._processes
        else:
            n_workers = multiprocessing.cpu_count()
        return n_workers

    def _start_workers(self, workers, work_queue, done_queue):
        for worker in range(workers):
            process = multiprocessing.Process(
                target=self._worker, args=(work_queue, done_queue))
            work_queue.put('STOP')
            process.start()
        return True

    @staticmethod
    def _process_done_queue(workers, done_queue, outcome):
        stops = 0
        while stops < workers:
            output = done_queue.get()
            if output == 'STOP':
                stops += 1
            else:
                outcome['payoff'].append(output['payoff'])
                outcome['cooperation'].append(output['cooperation'])
        return True

    def _worker(self, work_queue, done_queue):
        for repetition in iter(work_queue.get, 'STOP'):
            output = self._play_round_robin(cache_mutable=False)
            done_queue.put(output)
        done_queue.put('STOP')
        return True

    def _play_round_robin(self, cache_mutable=True):
        round_robin = RoundRobin(
            players=self.players,
            game=self.game,
            turns=self.turns,
            deterministic_cache=self.deterministic_cache,
            cache_mutable=cache_mutable,
            noise=self.noise)
        return round_robin.play()
