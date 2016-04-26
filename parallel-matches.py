"""
Run Axelrod Matches in parallel.

Because we generally don't want to share mutable objects between threads,
the parallelization works by generating the necessary parameters to
initialize matches.

Matches are parcelled out to maximize the usage of deterministic caching,
and to keep worker threads fed.

Todo:
-- format of data returned (players are not enumerated)
-- modify the library's match generators
-- compress the on disk data? it compresses a lot
-- move this code into the library proper (where exactly?)
-- Tests!
"""

from collections import defaultdict
import csv
import itertools
import random
import time

from multiprocessing import Event, Process, Queue

import axelrod as axl
from axelrod import MetaPlayer

def generate_turns(turns, repetitions=1):
    """This is a constant generator that yields `turns` `repetitions` times."""
    for _ in range(repetitions):
        yield turns

def generate_turns_prob(p, repetitions=1):
    """Generate probabilistic match lengths."""
    for _ in repetitions:
        try:
            x = random.random()
            return int(ceil(log(1 - x) / log(1 - self.prob_end)))
        except ZeroDivisionError:
            return float("inf")
        except ValueError:
            return 1

def generate_match_parameters(players, turns=100, repetitions=1, noise=0,
                              p=None):
    """Generate matches in chunks to feed to worker threads, trying
    to achieve the following:
    * All matches between the same two players are in the same chunk
    so that the deterministic cache can be utilized
    * Grab enough chunks to prevent the worker threads from exiting frequently
    """

    match_chunks = []
    for i in range(len(players)):
        for j in range(i, len(players)):
            player1 = players[i]
            player2 = players[j]
            players_ = [player1.clone(), player2.clone()]
            players_[0].typeid = i
            players_[1].typeid = j
            if p:
                turns_generator = generate_turns_prob(p, repetitions)
            else:
                turns_generator = generate_turns(turns, repetitions)
            noise_generator = generate_turns(noise, repetitions)
            match_chunks.append((players_, turns_generator, noise_generator))
            if (len(match_chunks) * repetitions > 500) or issubclass(player1.__class__, MetaPlayer):
                yield match_chunks
                match_chunks = []
        if len(match_chunks):
            yield match_chunks

def process_match_results(match):
    """Manipulate results data for writing to a CSV file."""
    player1_name = str(match.players[0])
    player2_name = str(match.players[1])
    result = match.result
    return [players[0].typeid, players[1].typeid, player1_name, player2_name,
            result]

def play_matches(queue, match_chunks, callback=process_match_results):
    """Plays the matches in each chunk of matches in chunks."""
    for players, turns_generator, noise_generator in match_chunks:
        first_turns = next(turns_generator)
        first_noise = next(noise_generator)
        match = axl.Match(players, first_turns, noise=noise)
        results = match.play()
        queue.put(callback(match))
        for turns, noise in zip(turns_generator, noise_generator):
            match.turns = turns
            match.noise = noise
            results = match.play()
            queue.put(callback(match))
        del match

class QueueConsumer(Process):
    """Process the results queue. Using a separate process reduces
    the total memory footprint because of how python allocates memory
    for child processes."""

    def __init__(self, queue, filename=None):
        Process.__init__(self)
        self.queue = queue
        self.filename = filename
        if filename:
            self.writer = csv.writer(open(filename, 'w'))
        else:
            self.interactions = defaultdict(list)
        self.shutdown = Event()

    def consume_queue(self):
        if self.filename:
            # Write Queue to disk
            qsize = self.queue.qsize()
            for _ in range(qsize):
                row = self.queue.get()
                concatenated_histories = list(map(lambda x: "".join(x),
                                                  zip(*row[-1])))
                self.writer.writerow(results[:4] + [concatenated_histories])
        else:
            # Keep it in memory
            qsize = self.queue.qsize()
            for _ in range(qsize):
                row = self.queue.get()
                self.interactions[(row[0], row[1])].append([row[-1])

    def run(self):
        while not self.shutdown.is_set():
            self.consume_queue()
            # Allow this thread to rest while data is generated
            time.sleep(0.01)
        self.consume_queue()
        if not self.filename:
            return self.interactions


class ProcessManager(Process):
    def __init__(self, matches_generator, queue_consumer, max_workers=4):
        Process.__init__(self)
        self.max_workers = max_workers
        self.matches_generator = matches_generator
        self.processes = []
        self.queue_consumer = queue_consumer
        self.queue = queue_consumer.queue

    def clean_pool(self):
        """Remove finished worker threads."""
        terminated = []
        for p in self.processes:
            # Look for naturally terminated processes.
            if not p.is_alive():
                terminated.append(p)
        for t in terminated:
            self.processes.remove(t)

    def spawn_workers(self):
        # Add new workers
        if not self.matches_remaining:
            return
        #self.clean_pool()
        for _ in range(self.max_workers - len(self.processes)):
            try:
                match_chunks = next(self.matches_generator)
                p = Process(target=play_matches,
                            args=(self.queue, match_chunks))
                self.processes.append(p)
                p.start()
            except StopIteration:
                self.matches_remaining = False
                break

    def run(self):
        """Pass all the required matches out to worker threads."""
        self.matches_remaining = True
        while self.matches_remaining or (len(self.processes) > 0):
            self.clean_pool()
            self.spawn_workers()
            time.sleep(0.1)
        # Shutdown the consumer
        self.queue_consumer.shutdown.set()

def play_matches_parallel(matches, queue=None, filename=None, max_workers=4):
    queue = Queue()
    qc = QueueConsumer(queue, filename=filename)
    pm = ProcessManager(matches, queue_consumer=qc, max_workers=max_workers)
    interactions = qc.start()
    pm.start()
    qc.join()
    return interactions

if __name__ == "__main__":
    players = [s() for s in axl.ordinary_strategies]
    matches = generate_match_parameters(players, turns=200, repetitions=100)
    #results = play_matches_parallel(matches, filename="data.out")
    interactions = play_matches_parallel(matches, filename=None)
    rs = axl.ResultSet(players, interactions)

