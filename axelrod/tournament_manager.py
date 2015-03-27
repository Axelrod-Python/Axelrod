import os
import time
import cPickle as pickle
from tournament import *
from plot import *
from ecosystem import *
import logging
from utils import *


class TournamentManager(object):

    def __init__(self, output_directory, with_ecological,
                 pass_cache=True, load_cache=True, save_cache=False,
                 cache_file='./cache.txt'):
        self.tournaments = []
        self.ecological_variants = []
        self.logger = logging.getLogger(__name__)
        self.output_directory = output_directory
        self.with_ecological = with_ecological
        self.pass_cache = pass_cache
        self.save_cache = save_cache
        self.cache_file = cache_file
        self.deterministic_cache = {}
        self.cache_valid_for_turns = None
        self.load_cache = False

        if load_cache and not save_cache:
            self.load_cache = self.load_cache_from_file(cache_file)

    def one_player_per_strategy(self, strategies):
        return [strategy() for strategy in strategies]

    def add_tournament(self, name, players, game=None, turns=200,
                       repetitions=10, processes=None):
        tournament = Tournament(
            name=name,
            players=players,
            turns=turns,
            repetitions=repetitions,
            processes=processes)
        self.tournaments.append(tournament)

    def run_tournaments(self):
        t0 = time.time()
        for tournament in self.tournaments:
            self.run_single_tournament(tournament)
        if self.save_cache:
            self.save_cache_to_file(self.deterministic_cache, self.cache_file)
        self.logger.debug(timed_message('Finished all tournaments', t0))

    def run_single_tournament(self, tournament):
        self.logger.debug(
            'Starting %s tournament with %d round robins of %d turns per pair.'
            % (tournament.name, tournament.repetitions, tournament.turns))

        t0 = time.time()

        if self.pass_cache and self.valid_cache(tournament.turns):
            self.logger.debug('Passing cache with %d entries to %s tournament' %
                            (len(self.deterministic_cache), tournament.name))
            tournament.deterministic_cache = self.deterministic_cache
            if self.load_cache:
                tournament.prebuilt_cache = True
        else:
            self.logger.debug('Cache is not valid for %s tournament' %
                            tournament.name)
        tournament.play()

        self.logger.debug(timed_message('Finished %s tournament' % tournament.name, t0))

        if self.with_ecological:
            ecosystem = Ecosystem(tournament.result_set)
            self.run_ecological_variant(tournament, ecosystem)
        else:
            ecosystem = None

        self.generate_output_files(tournament, ecosystem)
        self.cache_valid_for_turns = tournament.turns

        self.logger.debug('Cache now has %d entries' %
                        len(self.deterministic_cache))

        self.logger.debug(
            timed_message('Finished all %s tasks' % tournament.name, t0))

    def valid_cache(self, turns):
        return ((len(self.deterministic_cache) == 0) or
                (len(self.deterministic_cache) > 0) and
                turns == self.cache_valid_for_turns)

    def run_ecological_variant(self, tournament, ecosystem):
        self.logger.debug(
            'Starting ecological variant of %s' % tournament.name)
        t0 = time.time()
        ecoturns = {
            'basic_strategies': 100,
            'cheating_strategies': 20,
            'strategies': 200,
            'all_strategies': 40,
        }
        ecosystem.reproduce(ecoturns.get(tournament.name))
        self.logger.debug(
            timed_message('Finished ecological variant of %s' % tournament.name, t0))

    def generate_output_files(self, tournament, ecosystem=None):
        self.save_csv(tournament)
        self.save_plots(tournament, ecosystem)

    def save_csv(self, tournament):
        csv = tournament.result_set.csv()
        file_name = self.output_file_path(
                tournament.name, 'csv')
        with open(file_name, 'w') as f:
            f.write(csv)

    def save_plots(self, tournament, ecosystem=None):
        results = tournament.result_set
        plot = Plot(results)
        if not plot.matplotlib_installed:
            self.logger.debug('The matplotlib library is not installed. '
                            'No plots will be produced')
            return
        for plot_type in ('boxplot', 'payoff'):
            figure = getattr(plot, plot_type)()
            file_name = self.output_file_path(
                tournament.name + '_' + plot_type, 'png')
            self.save_plot(figure, file_name)
        if ecosystem is not None:
            figure = plot.stackplot(ecosystem.population_sizes)
            file_name = self.output_file_path(
                    tournament.name + '_reproduce', 'png')
            self.save_plot(figure, file_name)

    def output_file_path(self, file_name, file_extension):
        return os.path.join(
            self.output_directory,
            file_name + '.' + file_extension)

    def save_plot(self, figure, file_name):
        figure.savefig(file_name, bbox_inches='tight')
        figure.clf()

    def save_cache_to_file(self, cache, file_name):
        self.logger.debug(
            'Saving cache with %d entries to %s' % (len(cache), file_name))
        deterministic_cache = DeterministicCache(
            cache, self.cache_valid_for_turns)
        file = open(file_name, 'w')
        pickle.dump(deterministic_cache, file)
        return True

    def load_cache_from_file(self, file_name):
        try:
            file = open(file_name, 'r')
            deterministic_cache = pickle.load(file)
            self.deterministic_cache = deterministic_cache.cache
            self.cache_valid_for_turns = deterministic_cache.turns
            self.logger.debug(
                'Loaded cache with %d entries' % len(self.deterministic_cache))
            return True
        except IOError:
            self.logger.debug('Cache file not found. Starting with empty cache')
            return False


class DeterministicCache(object):

    def __init__(self, cache, turns):
        self.cache = cache
        self.turns = turns
