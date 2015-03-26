import multiprocessing
from game import *
from result_set import *
from round_robin import *
from logger import *


class Tournament(object):
    game = Game()

    def __init__(self, players, name='axelrod', game=None, turns=200,
                 repetitions=10, processes=None, logger=None, prebuilt_cache=False):
        self.name = name
        self.players = players
        self.nplayers = len(self.players)

        if game is not None:
            self.game = game
        self.turns = turns
        self.repetitions = repetitions
        self.processes = processes
        self.prebuilt_cache=prebuilt_cache

        if logger is None:
            self.logger = NullLogger()
        else:
            self.logger = logger

        self.result_set = ResultSet(
            players=players,
            turns=turns,
            repetitions=repetitions)

        self.deterministic_cache = {}

    def play(self):
        payoffs_list = []

        if self.processes is None:
            payoffs_list = self.run_serial_repetitions(payoffs_list)
        else:
            if len(self.deterministic_cache) == 0 or not self.prebuilt_cache:
                self.logger.log('Playing first round robin to build cache')
                payoffs = self.play_round_robin()
                payoffs_list.append(payoffs)
                self.repetitions -= 1
            payoffs_list = self.run_parallel_repetitions(payoffs_list)

        self.result_set.finalise(payoffs_list)
        return self.result_set

    def run_serial_repetitions(self, payoffs_list):
        self.logger.log('Playing %d round robins' % self.repetitions)
        for repetition in range(self.repetitions):
            payoffs = self.play_round_robin()
            payoffs_list.append(payoffs)
        return payoffs_list

    def run_parallel_repetitions(self, payoffs_list):
        # At first sight, it might seem simpler to use the multiprocessing Pool
        # Class rather than Processes and Queues. However, Pool can only accept
        # target functions which can be pickled and instance methods cannot.
        processes = []
        work_queue = multiprocessing.Queue()
        done_queue = multiprocessing.Queue()

        if self.processes < 2 or self.processes > multiprocessing.cpu_count():
            workers = multiprocessing.cpu_count()
        else:
            workers = self.processes

        self.logger.log(
            'Playing %d round robins with %d parallel processes' % (self.repetitions, workers))

        for repetition in range(self.repetitions):
            work_queue.put(repetition)

        for worker in range(workers):
            process = multiprocessing.Process(
                target=self.worker, args=(work_queue, done_queue))
            processes.append(process)
            work_queue.put('STOP')
            process.start()

        for process in processes:
            process.join()

        done_queue.put('STOP')

        for payoffs in iter(done_queue.get, 'STOP'):
            payoffs_list.append(payoffs)

        return payoffs_list

    def worker(self, work_queue, done_queue):
        for repetition in iter(work_queue.get, 'STOP'):
            payoffs = self.play_round_robin(cache_mutable=False)
            done_queue.put(payoffs)

    def play_round_robin(self, cache_mutable=True):
        round_robin = RoundRobin(
            players=self.players,
            game=self.game,
            turns=self.turns,
            deterministic_cache=self.deterministic_cache,
            cache_mutable=cache_mutable)
        payoffs = round_robin.play()
        return payoffs
