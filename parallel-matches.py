"""
Run Axelrod Matches in parallel.

Because we generally don't want to share mutable objects between threads,
the parallelization works by generating the necessary parameters to
initialize matches.

Matches are parcelled out to maximize the usage of deterministic caching,
and to keep worker threads fed.
"""

from collections import defaultdict
import csv
import itertools
import random
import time

from multiprocessing import Process, Queue

import axelrod as axl

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

def generate_match_parameters(players, turns=100, repetitions=1):
    """Generate matches in chunks to feed to worker threads, trying
    to achieve the following:
    * All matches between the same two players are in the same chunk
    so that the deterministic cache can be utilized
    * Grab enough chunks to prevent the worker threads from exiting frequently
    """
    # Do all the deterministic matches first
    #match_chunks = []
    #for player1, player2 in itertools.product(players, players):
        #if player1.classifier["stochastic"] or player1.classifier["stochastic"]:
            #continue
        #players = (player1.clone(), player2.clone())
        #turns_generator = generate_turns(turns, repetitions)
        #match_chunks.append((players, turns_generator))
    #yield match_chunks

    # Now the stochastic
    match_chunks = []
    for player1, player2 in itertools.product(players, players):
        #if not (player1.classifier["stochastic"] or player1.classifier["stochastic"]):
            #continue
        players = (player1.clone(), player2.clone())
        turns_generator = generate_turns(turns, repetitions)
        match_chunks.append((players, turns_generator))
        if len(match_chunks) * repetitions > 1000:
            yield match_chunks
            match_chunks = []
    if len(match_chunks):
        yield match_chunks

def process_match_results(match):
    """Manipulate results data for writing to a CSV file."""
    player1_name = str(match.players[0])
    player2_name = str(match.players[1])
    results = match.result
    concatenated_histories = list(map(lambda x: "".join(x), zip(*results)))
    return [player1_name, player2_name] + concatenated_histories

def play_matches(queue, match_chunks):
    """Plays the matches in each chunk of matches in chunks."""
    for players, turns_generator in match_chunks:
        first_turns = next(turns_generator)
        match = axl.Match(players, first_turns)
        results = match.play()
        queue.put(process_match_results(match))
        for turns in turns_generator:
            match.turns = turns
            results = match.play()
            queue.put(process_match_results(match))

class ProcessManager(object):
    def __init__(self, matches_generator, queue=None, max_processes=4,
                 filename=None):
        self.max_processes = max_processes
        self.matches_generator = matches_generator
        if queue:
            self.queue = queue
        else:
            self.queue = Queue()
        self.filename = filename
        if filename:
            self.writer = csv.writer(open(filename, 'w'))
        else:
            self.interactions = defaultdict(list)
        self.processes = []

    def clean_pool(self):
        """Remove finished worker threads."""
        terminated = []
        for p in self.processes:
            # Look for naturally terminated processes.
            if not p.is_alive():
                terminated.append(p)
        for t in terminated:
            self.processes.remove(t)

    def consume_queue(self):
        if self.filename:
            # Write Queue to disk
            qsize = self.queue.qsize()
            for _ in range(qsize):
                results = self.queue.get()
                self.writer.writerow(results)
        else:
            qsize = self.queue.qsize()
            for _ in range(qsize):
                row = self.queue.get()
                self.interactions[(row[0], row[1])].append((row[2], row[3]))

    def run(self):
        """Pass all the required matches out to worker threads."""
        no_matches_remaining = False
        while True:
            # Add new workers
            while len(self.processes) < self.max_processes:
                try:
                    match_chunks = next(self.matches_generator)
                    p = Process(target=play_matches,
                                args=(self.queue, match_chunks))
                    self.processes.append(p)
                    p.start()
                except StopIteration:
                    no_matches_remaining = True
                    break
            self.consume_queue()
            # Allow this thread to rest while data is generated
            time.sleep(0.1)
            # Clean Pool
            self.clean_pool()
            # Can we exit? All processes must be finished and we have also
            # exhausted the generator
            if (len(self.processes) == 0) & (no_matches_remaining):
                break
        self.consume_queue()
        return self.queueright


def play_matches_parallel(matches, queue=None, filename=None, max_processes=4):
    pm = ProcessManager(matches, queue=queue, filename=filename,
                        max_processes=max_processes)
    queue = pm.run()
    return queue

if __name__ == "__main__":
    players = [s() for s in axl.ordinary_strategies]
    matches = generate_match_parameters(players, turns=100, repetitions=100)
    #queue = play_matches_parallel(matches, filename="data.out")
    queue = play_matches_parallel(matches, filename=None)
