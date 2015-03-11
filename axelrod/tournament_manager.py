import os
from tournament import *


class TournamentManager(object):

    def __init__(self, output_directory):
        self.tournaments = []
        self.output_directory = output_directory

    def one_player_per_strategy(self, strategies):
        return [strategy() for strategy in strategies]

    def output_file_path(self, file_name, file_extension):
        return os.path.join(
            self.output_directory,
            file_name + '.' + file_extension)

    def save_plot(self, figure, file_name):
        figure.savefig(file_name, bbox_inches='tight')
        figure.clf()

    def add_tournament(self, name, players, turns, repetitions):
        tournament = axelrod.Tournament(
            name=name,
            players=players,
            turns=turns,
            repetitions=repetitions)
        self.tournaments.append(tournament)

    def run_tournaments(self):
        for tournament in self.tournaments:
            self.run_single_tournament(tournament)

    def run_single_tournament(self, tournament):
            tournament.play()
            self.save_plots(tournament)

    def save_plots(self, tournament):
        plot = axelrod.Plot(tournament.result_set)
        if not plot.matplotlib_installed:
            print ("The matplotlib library is not installed. "
                   "No plots will be produced")
            return
        for plot_type in ('boxplot', 'payoff'):
            figure = plot[plot_type]()
            file_name = self.output_file_path(
                tournament.name + '_' + plot_type, 'png')
            self.save_plot(figure, file_name)
