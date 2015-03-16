import os
import time
from tournament import *
from plot import *
from ecosystem import *


class TournamentManager(object):

    def __init__(self, logger, output_directory, with_ecological):
        self.tournaments = []
        self.ecological_variants = []
        self.logger = logger
        self.output_directory = output_directory
        self.with_ecological = with_ecological

    def one_player_per_strategy(self, strategies):
        return [strategy() for strategy in strategies]

    def add_tournament(self, name, players, game=None,
                       turns=200, repetitions=10):
        tournament = Tournament(
            name=name,
            players=players,
            turns=turns,
            repetitions=repetitions)
        self.tournaments.append(tournament)

    def run_tournaments(self):
        t0 = time.time()
        for tournament in self.tournaments:
            self.run_single_tournament(tournament)
        self.logger.log("Finished all tournaments", t0)

    def run_single_tournament(self, tournament):
            self.logger.log(
                'Starting ' + tournament.name + ' tournament with ' +
                str(tournament.repetitions) + ' round robins of ' +
                str(tournament.turns) + ' turns per pair.')

            t0 = time.time()

            tournament.play()

            self.logger.log(
                "Finished " + tournament.name + " tournament", t0)

            if self.with_ecological:
                ecosystem = Ecosystem(tournament.result_set)
                self.run_ecological_variant(tournament, ecosystem)
            else:
                ecosystem = None

            self.generate_output_files(tournament, ecosystem)

            self.logger.log(
                "Finished all " + tournament.name + " tasks", t0)

    def run_ecological_variant(self, tournament, ecosystem):
        self.logger.log(
            'Starting ecological variant of ' + tournament.name)
        t0 = time.time()
        ecoturns = {
            'basic_strategies': 100,
            'cheating_strategies': 20,
            'strategies': 200,
            'all_strategies': 40,
        }
        ecosystem.reproduce(ecoturns.get(tournament.name))
        self.logger.log(
            "Finished ecological variant of " + tournament.name, t0)

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
            self.logger.log("The matplotlib library is not installed. "
                            "No plots will be produced")
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
