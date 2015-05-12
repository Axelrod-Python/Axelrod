import multiprocessing
from game import *
from result_set import *
from round_robin import *
import logging


class Tournament(object):
    game = Game()

    def __init__(self, players, name='axelrod', game=None, turns=200,
                 repetitions=10, processes=None, prebuilt_cache=False,
                 noise=0):
        self.name = name
        self.players = players
        self.nplayers = len(self.players)
        if game is not None:
            self.game = game
        self.turns = turns
        self.repetitions = repetitions
        self.prebuilt_cache = prebuilt_cache
        self.result_set = ResultSet(
            players=players,
            turns=turns,
            repetitions=repetitions)
        self.deterministic_cache = {}
        self.noise = noise

        self._processes = processes
        self._logger = logging.getLogger(__name__)

    def play(self):
        payoffs_list = []

        if self._processes is None:
            self._run_serial_repetitions(payoffs_list)
        else:
            if self._build_cache_required():
                self._logger.debug('Playing first round robin to build cache')
                self._run_single_repetition(payoffs_list)
                self.repetitions -= 1
            self._run_parallel_repetitions(payoffs_list)

        self.result_set.payoffs_list = payoffs_list
        return self.result_set

    def _build_cache_required(self):
        return (
            not self.noise and (
                len(self.deterministic_cache) == 0 or
                not self.prebuilt_cache))

    def _run_single_repetition(self, payoffs_list):
        payoffs = self._play_round_robin()
        payoffs_list.append(payoffs)

    def _run_serial_repetitions(self, payoffs_list):
        self._logger.debug('Playing %d round robins' % self.repetitions)
        for repetition in range(self.repetitions):
            self._run_single_repetition(payoffs_list)
        return True

    def _run_parallel_repetitions(self, payoffs_list):
        # At first sight, it might seem simpler to use the multiprocessing Pool
        # Class rather than Processes and Queues. However, Pool can only accept
        # target functions which can be pickled and instance methods cannot.
        work_queue = multiprocessing.Queue()
        done_queue = multiprocessing.Queue()
        workers = self._n_workers()

        for repetition in range(self.repetitions):
            work_queue.put(repetition)

        self._logger.debug(
            'Playing %d round robins with %d parallel processes' %
            (self.repetitions, workers))
        self._start_workers(workers, work_queue, done_queue)
        self._process_done_queue(workers, done_queue, payoffs_list)

        return True

    def _n_workers(self):
        if (self._processes < 2 or self._processes > multiprocessing.cpu_count()):
            n_workers = multiprocessing.cpu_count()
        else:
            n_workers = self._processes
        return n_workers

    def _start_workers(self, workers, work_queue, done_queue):
        for worker in range(workers):
            process = multiprocessing.Process(
                target=self._worker, args=(work_queue, done_queue))
            work_queue.put('STOP')
            process.start()
        return True

    def _process_done_queue(self, workers, done_queue, payoffs_list):
        stops = 0
        while stops < workers:
            payoffs = done_queue.get()
            if payoffs == 'STOP':
                stops += 1
            else:
                payoffs_list.append(payoffs)
        return True

    def _worker(self, work_queue, done_queue):
        for repetition in iter(work_queue.get, 'STOP'):
            payoffs = self._play_round_robin(cache_mutable=False)
            done_queue.put(payoffs)
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
        payoffs = round_robin.play()
        return payoffs
