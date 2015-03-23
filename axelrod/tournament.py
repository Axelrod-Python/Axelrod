import multiprocessing
from game import *
from result_set import *
from round_robin import *
from logger import *


class Tournament(object):
    game = Game()

    def __init__(self, players, name='axelrod', game=None, turns=200,
                 repetitions=10, processes=None, logger=None):
        self.name = name
        self.players = players
        self.nplayers = len(self.players)

        if game is not None:
            self.game = game
        self.turns = turns
        self.repetitions = repetitions
        self.processes = processes

        if logger is None:
            self.logger = NullLogger()
        else:
            self.logger = logger

        self.result_set = ResultSet(
            players=players,
            turns=turns,
            repetitions=repetitions)

        # The cache doesn't need to be an instance level variable,
        # it could just be internal to the play method.
        # However, there's no reason why the cache couldn't be passed between
        # tournaments by the tournament manager and so it sits here waiting for
        # that code to be written.
        self.deterministic_cache = {}

    def play(self):
        payoffs_list = []

        # We play the first repetition in order to build the deterministic
        # cache. It's done separately so that only further repetions have
        # any chance of running in parallel. This allows the cache to be made
        # available to processes running in parallel without the problems of
        # cross-process communication.
        payoffs, cache = self.play_round_robin()
        payoffs_list.append(payoffs)
        self.deterministic_cache = cache

        if self.processes is None:
            payoffs_list = self.run_serial_repetitions(payoffs_list)
        else:
            payoffs_list = self.run_parallel_repetitions(payoffs_list)

        self.result_set.finalise(payoffs_list)
        return self.result_set

    def run_serial_repetitions(self, payoffs_list):
        for repetition in range(self.repetitions - 1):
            payoffs, cache = self.play_round_robin()
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
            'Running repetitions with %d parallel processes' % workers)

        for repetition in range(self.repetitions - 1):
            work_queue.put(repetition)

        for worker in range(workers):
            process = multiprocessing.Process(
                target=self.worker, args=(work_queue, done_queue))
            processes.append(process)
            work_queue.put('STOP')
            process.start()

        # There is a 0.5 second timeout here as the all_strategies tournament
        # occasionally hangs the join method for some strange reason.
        for process in processes:
            process.join(0.5)

        done_queue.put('STOP')

        for payoffs in iter(done_queue.get, 'STOP'):
            payoffs_list.append(payoffs)

        return payoffs_list

    def worker(self, work_queue, done_queue):
        for repetition in iter(work_queue.get, 'STOP'):
            payoffs, cache = self.play_round_robin()
            done_queue.put(payoffs)

    def play_round_robin(self):
        round_robin = RoundRobin(
            players=self.players,
            game=self.game,
            turns=self.turns,
            deterministic_cache=self.deterministic_cache)
        payoffs = round_robin.play()
        cache = round_robin.deterministic_cache
        return payoffs, cache
