from __future__ import absolute_import, unicode_literals, print_function

import os
import pickle

from .tournament import *
from .plot import *
from .ecosystem import *
from .utils import *


class TournamentManager(object):

    def __init__(self, output_directory, with_ecological,
                 pass_cache=True, load_cache=True, save_cache=False,
                 cache_file='./cache.txt'):
        self._tournaments = []
        self._ecological_variants = []
        self._logger = logging.getLogger(__name__)
        self._output_directory = output_directory
        self._with_ecological = with_ecological
        self._pass_cache = pass_cache
        self._save_cache = save_cache
        self._cache_file = cache_file
        self._deterministic_cache = {}
        self._cache_valid_for_turns = None
        self._load_cache = False

        if load_cache and not save_cache:
            self.load_cache = self._load_cache_from_file(cache_file)

    @staticmethod
    def one_player_per_strategy(strategies):
        return [strategy() for strategy in strategies]

    def add_tournament(self, name, players, game=None, turns=200,
                       repetitions=10, processes=None, noise=0,
                       with_morality=True):
        tournament = Tournament(
            name=name,
            players=players,
            turns=turns,
            repetitions=repetitions,
            processes=processes,
            noise=noise,
            with_morality=with_morality)
        self._tournaments.append(tournament)

    def run_tournaments(self):
        t0 = time.time()
        for tournament in self._tournaments:
            self._run_single_tournament(tournament)
        if self._save_cache and not tournament.noise:
            self._save_cache_to_file(self._deterministic_cache, self._cache_file)
        self._logger.info(timed_message('Finished all tournaments', t0))

    def _run_single_tournament(self, tournament):
        self._logger.info(
            'Starting %s tournament with %d round robins of %d turns per pair.'
            % (tournament.name, tournament.repetitions, tournament.turns))

        t0 = time.time()

        if not tournament.noise and self._pass_cache and self._valid_cache(tournament.turns):
            self._logger.debug('Passing cache with %d entries to %s tournament' %
                            (len(self._deterministic_cache), tournament.name))
            tournament.deterministic_cache = self._deterministic_cache
            if self._load_cache:
                tournament.prebuilt_cache = True
        else:
            self._logger.debug('Cache is not valid for %s tournament' %
                            tournament.name)
        tournament.play()

        self._logger.debug(timed_message('Finished %s tournament' % tournament.name, t0))

        if self._with_ecological:
            ecosystem = Ecosystem(tournament.result_set)
            self.run_ecological_variant(tournament, ecosystem)
        else:
            ecosystem = None

        self._generate_output_files(tournament, ecosystem)
        self._cache_valid_for_turns = tournament.turns

        self._logger.debug('Cache now has %d entries' %
                        len(self._deterministic_cache))

        self._logger.info(
            timed_message('Finished all %s tasks' % tournament.name, t0))

    def _valid_cache(self, turns):
        return ((len(self._deterministic_cache) == 0) or
                (len(self._deterministic_cache) > 0) and
                turns == self._cache_valid_for_turns)

    def run_ecological_variant(self, tournament, ecosystem):
        self._logger.debug(
            'Starting ecological variant of %s' % tournament.name)
        t0 = time.time()
        ecoturns = {
            'basic_strategies': 1000,
            'cheating_strategies': 10,
            'strategies': 1000,
            'all_strategies': 10,
        }
        ecosystem.reproduce(ecoturns.get(tournament.name))
        self._logger.debug(
            timed_message('Finished ecological variant of %s' % tournament.name, t0))

    def _generate_output_files(self, tournament, ecosystem=None):
        self._save_csv(tournament)
        self._save_plots(tournament, ecosystem)

    def _save_csv(self, tournament):
        csv = tournament.result_set.csv()
        file_name = self._output_file_path(
                tournament.name, 'csv')
        with open(file_name, 'w') as f:
            f.write(csv)

    def _save_plots(self, tournament, ecosystem=None, image_format="svg"):
        results = tournament.result_set
        plot = Plot(results)
        if not plot.matplotlib_installed:
            self._logger.error('The matplotlib library is not installed. '
                            'No plots will be produced')
            return
        for plot_type in ('boxplot', 'payoff'):
            figure = getattr(plot, plot_type)()
            file_name = self._output_file_path(
                tournament.name + '_' + plot_type, image_format)
            self._save_plot(figure, file_name)
        if ecosystem is not None:
            figure = plot.stackplot(ecosystem.population_sizes)
            file_name = self._output_file_path(
                    tournament.name + '_reproduce', image_format)
            self._save_plot(figure, file_name)

    def _output_file_path(self, file_name, file_extension):
        return os.path.join(
            self._output_directory,
            file_name + '.' + file_extension)

    @staticmethod
    def _save_plot(figure, file_name, dpi=400):
        figure.savefig(file_name, bbox_inches='tight', dpi=dpi)
        figure.clf()
        plt.close(figure)

    def _save_cache_to_file(self, cache, file_name):
        self._logger.debug(
            'Saving cache with %d entries to %s' % (len(cache), file_name))
        deterministic_cache = DeterministicCache(
            cache, self._cache_valid_for_turns)
        with open(file_name, 'wb') as io:
            pickle.dump(deterministic_cache, io)
        return True

    def _load_cache_from_file(self, file_name):
        try:
            with open(file_name, 'rb') as io:
                deterministic_cache = pickle.load(io)
            self._deterministic_cache = deterministic_cache.cache
            self._cache_valid_for_turns = deterministic_cache.turns
            self._logger.debug(
                'Loaded cache with %d entries' % len(self._deterministic_cache))
            return True
        except IOError:
            self._logger.debug('Cache file not found. Starting with empty cache')
            return False


class DeterministicCache(object):

    def __init__(self, cache, turns):
        self.cache = cache
        self.turns = turns
