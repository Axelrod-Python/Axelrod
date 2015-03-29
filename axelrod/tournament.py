import multiprocessing
from game import *
from result_set import *
from round_robin import *
import logging

class Tournament(object):
    game = Game()

    def __init__(self, players, name='axelrod', game=None, turns=200,
                 repetitions=10, processes=None, prebuilt_cache=False):
        self.name = name
        self.players = players
        self.nplayers = len(self.players)

        if game is not None:
            self.game = game
        self.turns = turns
        self.repetitions = repetitions
        self.processes = processes
        self.prebuilt_cache=prebuilt_cache

        self.logger = logging.getLogger(__name__)

        self.result_set = ResultSet(
            players=players,
            turns=turns,
            repetitions=repetitions)

        self.deterministic_cache = {}

    def play(self):
        payoffs_list = []

        if self.processes is None:
            self.run_serial_repetitions(payoffs_list)
        else:
            if len(self.deterministic_cache) == 0 or not self.prebuilt_cache:
                self.logger.debug('Playing first round robin to build cache')
                payoffs = self.play_round_robin()
                payoffs_list.append(payoffs)
                self.repetitions -= 1
            self.run_parallel_repetitions(payoffs_list)

        self.result_set.finalise(payoffs_list)
        return self.result_set

    def run_serial_repetitions(self, payoffs_list):
        self.logger.debug('Playing %d round robins' % self.repetitions)
        for repetition in range(self.repetitions):
            payoffs = self.play_round_robin()
            payoffs_list.append(payoffs)
        return True

    def run_parallel_repetitions(self, payoffs_list):
        # At first sight, it might seem simpler to use the multiprocessing Pool
        # Class rather than Processes and Queues. However, Pool can only accept
        # target functions which can be pickled and instance methods cannot.
        work_queue = multiprocessing.Queue()
        done_queue = multiprocessing.Queue()

        if self.processes < 2 or self.processes > multiprocessing.cpu_count():
            workers = multiprocessing.cpu_count()
        else:
            workers = self.processes

        for repetition in range(self.repetitions):
            work_queue.put(repetition)

        self.logger.debug(
            'Playing %d round robins with %d parallel processes' % (self.repetitions, workers))
        self.start_workers(workers, work_queue, done_queue)
        self.process_done_queue(workers, done_queue, payoffs_list)

        return True

    def start_workers(self, workers, work_queue, done_queue):
        for worker in range(workers):
            process = multiprocessing.Process(
                target=self.worker, args=(work_queue, done_queue))
            work_queue.put('STOP')
            process.start()
        return True

    def process_done_queue(self, workers, done_queue, payoffs_list):
        stops = 0
        while stops < workers:
            payoffs = done_queue.get()
            if payoffs == 'STOP':
                stops += 1
            else:
                payoffs_list.append(payoffs)
        return True

    def worker(self, work_queue, done_queue):
        for repetition in iter(work_queue.get, 'STOP'):
            payoffs = self.play_round_robin(cache_mutable=False)
            done_queue.put(payoffs)
        done_queue.put('STOP')
        return True

    def play_round_robin(self, cache_mutable=True):
        round_robin = RoundRobin(
            players=self.players,
            game=self.game,
            turns=self.turns,
            deterministic_cache=self.deterministic_cache,
            cache_mutable=cache_mutable)
        payoffs = round_robin.play()
        return payoffs
