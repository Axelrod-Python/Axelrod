import csv
import os
from collections import namedtuple
from tempfile import mkstemp

import matplotlib.pyplot as plt
import numpy as np
import tqdm
import dask.dataframe as dd
import dask as da
from mpl_toolkits.axes_grid1 import make_axes_locatable

import axelrod as axl
from axelrod import Player
from axelrod.strategy_transformers import JossAnnTransformer, DualTransformer
from axelrod.interaction_utils import (
    compute_final_score_per_turn, read_interactions_from_file)

from typing import List, Any, Union

Point = namedtuple('Point', 'x y')


def create_points(step: float, progress_bar: bool = True) -> List[Point]:
    """Creates a set of Points over the unit square.

    A Point has coordinates (x, y). This function constructs points that are
    separated by a step equal to `step`. The points are over the unit
    square which implies that the number created will be (1/`step` + 1)^2.

    Parameters
    ----------
    step : float
        The separation between each Point. Smaller steps will produce more
        Points with coordinates that will be closer together.
    progress_bar : bool
        Whether or not to create a progress bar which will be updated

    Returns
    ----------
    points : list
        of Point objects with coordinates (x, y)
    """
    num = int((1 / step) // 1) + 1

    if progress_bar:
        p_bar = tqdm.tqdm(total=num ** 2, desc="Generating points")

    points = []
    for x in np.linspace(0, 1, num):
        for y in np.linspace(0, 1, num):
            points.append(Point(x, y))

            if progress_bar:
                p_bar.update()

    if progress_bar:
        p_bar.close()

    return points


def create_jossann(point: Point, probe: Any) -> Player:
    """Creates a JossAnn probe player that matches the Point.

    If the coordinates of point sums to more than 1 the parameters are
    flipped and subtracted from 1 to give meaningful probabilities. We also
    use the Dual of the probe. This is outlined further in [Ashlock2010]_.

    Parameters
    ----------
    point : Point
    probe : class or instance
        A class that must be descended from axelrod.Player or an instance of
        axelrod.Player.

    Returns
    ----------
    joss_ann: Joss-AnnTitForTat object
        `JossAnnTransformer` with parameters that correspond to `point`.
    """
    x, y = point

    if isinstance(probe, axl.Player):
        init_kwargs = probe.init_kwargs
        probe = probe.__class__
    else:
        init_kwargs = {}

    if x + y >= 1:
        joss_ann = DualTransformer()(
            JossAnnTransformer((1 - x, 1 - y))(probe))(**init_kwargs)
    else:
        joss_ann = JossAnnTransformer((x, y))(probe)(**init_kwargs)
    return joss_ann


def create_probes(probe: Union[type, Player], points: list,
                  progress_bar: bool = True) -> List[Player]:
    """Creates a set of probe strategies over the unit square.

    Constructs probe strategies that correspond to points with coordinates
    (x, y). The probes are created using the `JossAnnTransformer`.

    Parameters
    ----------
    probe : class or instance
        A class that must be descended from axelrod.Player or an instance of
        axelrod.Player.
    points : list
        of Point objects with coordinates (x, y)
    progress_bar : bool
        Whether or not to create a progress bar which will be updated

    Returns
    ----------
    probes : list
        A list of `JossAnnTransformer` players with parameters that
        correspond to point.
    """
    if progress_bar:
        points = tqdm.tqdm(points, desc="Generating probes")
    probes = [create_jossann(point, probe) for point in points]
    return probes


def create_edges(points: List[Point], progress_bar: bool = True) -> list:
    """Creates a set of edges for a spatial tournament.

    Constructs edges that correspond to `points`. All edges begin at 0, and
    connect to the index +1 of the probe.

    Parameters
    ----------
    points : list
        of Point objects with coordinates (x, y)
    progress_bar : bool
        Whether or not to create a progress bar which will be updated


    Returns
    ----------
    edges : list of tuples
        A list containing tuples of length 2. All tuples will have 0 as the
        first element. The second element is the index of the
        corresponding probe (+1 to allow for including the Strategy).
    """
    if progress_bar:
        points = tqdm.tqdm(points, desc="Generating network edges")
    edges = [(0, index + 1) for index, point in enumerate(points)]
    return edges


def generate_data(interactions: dict, points: list, edges: list) -> dict:
    """Generates useful data from a spatial tournament.

    Matches interactions from `results` to their corresponding Point in
    `probe_points`.

    Parameters
    ----------
    interactions : dict
        A dictionary mapping edges to the corresponding interactions of
        those players.
    points : list
        of Point objects with coordinates (x, y).
    edges : list of tuples
        A list containing tuples of length 2. All tuples will have either 0
        or 1 as the first element. The second element is the index of the
        corresponding probe (+1 to allow for including the Strategy).

    Returns
    ----------
    point_scores : dict
        A dictionary where the keys are Points of the form (x, y) and
        the values are the mean score for the corresponding interactions.
    """
    edge_scores = [np.mean([
        compute_final_score_per_turn(scores)[0]
        for scores in interactions[edge]])
        for edge in edges
    ]
    point_scores = dict(zip(points, edge_scores))
    return point_scores


def reshape_data(data: dict, points: list, size: int) -> np.ndarray:
    """Shape the data so that it can be plotted easily.

    Parameters
    ----------
    data : dictionary
        A dictionary where the keys are Points of the form (x, y) and
        the values are the mean score for the corresponding interactions.

    points : list
        of Point objects with coordinates (x, y).

    size : int
        The number of Points in every row/column.

    Returns
    ----------
    plotting_data : list
        2-D numpy array of the scores, correctly shaped to ensure that the
        score corresponding to Point (0, 0) is in the left hand corner ie.
        the standard origin.
    """
    ordered_data = [data[point] for point in points]
    shaped_data = np.reshape(ordered_data, (size, size), order='F')
    plotting_data = np.flipud(shaped_data)
    return plotting_data


class AshlockFingerprint(object):
    def __init__(self, strategy: Union[type, Player],
                 probe: Union[type, Player]=axl.TitForTat) -> None:
        """
        Parameters
        ----------
        strategy : class or instance
            A class that must be descended from axelrod.Player or an instance of
            axelrod.Player.
        probe : class or instance
            A class that must be descended from axelrod.Player or an instance of
            axelrod.Player.
            Default: Tit For Tat
        """
        self.strategy = strategy
        self.probe = probe

    def construct_tournament_elements(self, step: float,
                                      progress_bar: bool = True) -> tuple:
        """Build the elements required for a spatial tournament

        Parameters
        ----------
        step : float
            The separation between each Point. Smaller steps will
            produce more Points that will be closer together.
        progress_bar : bool
            Whether or not to create a progress bar which will be updated


        Returns
        ----------
        edges : list of tuples
            A list containing tuples of length 2. All tuples will have either 0
            or 1 as the first element. The second element is the index of the
            corresponding probe (+1 to allow for including the Strategy).

        tournament_players : list
            A list containing instances of axelrod.Player. The first item is the
            original player, the rest are the probes.

        """
        self.points = create_points(step, progress_bar=progress_bar)
        edges = create_edges(self.points, progress_bar=progress_bar)
        probe_players = create_probes(self.probe, self.points,
                                      progress_bar=progress_bar)

        if isinstance(self.strategy, axl.Player):
            tournament_players = [self.strategy] + probe_players
        else:
            tournament_players = [self.strategy()] + probe_players

        return edges, tournament_players

    def fingerprint(
        self, turns: int = 50, repetitions: int = 10, step: float = 0.01,
        processes: int = None, filename: str = None,
        progress_bar: bool = True
) -> dict:
        """Build and play the spatial tournament.

        Creates the probes and their edges then builds a spatial tournament.
        When the coordinates of the probe sum to more than 1, the dual of the
        probe is taken instead and then the Joss-Ann Transformer is applied. If
        the coordinates sum to less than 1 (or equal), then only the Joss-Ann is
        applied, a dual is not required.

        Parameters
        ----------
        turns : int, optional
            The number of turns per match
        repetitions : int, optional
            The number of times the round robin should be repeated
        step : float, optional
            The separation between each Point. Smaller steps will
            produce more Points that will be closer together.
        processes : int, optional
            The number of processes to be used for parallel processing
        filename: str, optional
            The name of the file for self.spatial_tournament's interactions.
            if None, will auto-generate a filename.
        progress_bar : bool
            Whether or not to create a progress bar which will be updated

        Returns
        ----------
        self.data : dict
            A dictionary where the keys are coordinates of the form (x, y) and
            the values are the mean score for the corresponding interactions.
        """

        temp_file_descriptor = None
        if filename is None:
            temp_file_descriptor, filename = mkstemp()  # type: ignore

        edges, tourn_players = self.construct_tournament_elements(
            step, progress_bar=progress_bar)

        self.step = step
        self.spatial_tournament = axl.Tournament(tourn_players, turns=turns,
                                                 repetitions=repetitions,
                                                 edges=edges)
        self.spatial_tournament.play(build_results=False,
                                     filename=filename,
                                     processes=processes,
                                     progress_bar=progress_bar)

        self.interactions = read_interactions_from_file(
            filename, progress_bar=progress_bar)

        if temp_file_descriptor is not None:
            assert filename is not None
            os.close(temp_file_descriptor)
            os.remove(filename)

        self.data = generate_data(self.interactions, self.points, edges)
        return self.data

    def plot(self, cmap: str = 'seismic', interpolation: str = 'none',
             title: str = None, colorbar: bool = True,
             labels: bool = True) -> plt.Figure:
        """Plot the results of the spatial tournament.

        Parameters
        ----------
        cmap : str, optional
            A matplotlib colour map, full list can be found at
            http://matplotlib.org/examples/color/colormaps_reference.html
        interpolation : str, optional
            A matplotlib interpolation, full list can be found at
            http://matplotlib.org/examples/images_contours_and_fields/interpolation_methods.html
        title : str, optional
            A title for the plot
        colorbar : bool, optional
            Choose whether the colorbar should be included or not
        labels : bool, optional
            Choose whether the axis labels and ticks should be included

        Returns
        ----------
        figure : matplotlib figure
            A heat plot of the results of the spatial tournament
        """
        size = int((1 / self.step) // 1) + 1
        plotting_data = reshape_data(self.data, self.points, size)
        fig, ax = plt.subplots()
        cax = ax.imshow(
            plotting_data, cmap=cmap, interpolation=interpolation)

        if colorbar:
            max_score = max(self.data.values())
            min_score = min(self.data.values())
            ticks = [min_score, (max_score + min_score) / 2, max_score]
            fig.colorbar(cax, ticks=ticks)

        plt.xlabel('$x$')
        plt.ylabel('$y$', rotation=0)
        ax.tick_params(axis='both', which='both', length=0)
        plt.xticks([0, len(plotting_data) - 1], ['0', '1'])
        plt.yticks([0, len(plotting_data) - 1], ['1', '0'])

        if not labels:
            plt.axis('off')

        if title is not None:
            plt.title(title)
        return fig


class TransitiveFingerprint(object):
    def __init__(self, strategy, opponents=None, number_of_opponents=50):
        """
        Parameters
        ----------
        strategy : class or instance
            A class that must be descended from axelrod.Player or an instance of
            axelrod.Player.
        opponents : list of instances
            A list that contains a list of opponents
            Default: A spectrum of Random  players
        number_of_opponents: int
            The number of Random opponents
            Default: 50
        """
        self.strategy = strategy

        if opponents is None:
            self.opponents = [axl.Random(p) for p in
                              np.linspace(0, 1, number_of_opponents)]
        else:
            self.opponents = opponents

    def fingerprint(self, turns: int = 50, repetitions: int = 1000,
                    noise: float = None, processes: int = None,
                    filename: str = None,
                    progress_bar: bool = True) -> np.array:
        """Creates a spatial tournament to run the necessary matches to obtain
        fingerprint data.

          Creates the opponents and their edges then builds a spatial tournament.

        Parameters
        ----------
        turns : int, optional
            The number of turns per match
        repetitions : int, optional
            The number of times the round robin should be repeated
        noise : float, optional
            The probability that a player's intended action should be flipped
        processes : int, optional
            The number of processes to be used for parallel processing
        filename: str, optional
            The name of the file for spatial tournament's interactions.
            if None, a filename will be generated.
        progress_bar : bool
            Whether or not to create a progress bar which will be updated

        Returns
        ----------
        self.data : np.array
            A numpy array containing the mean cooperation rate against each
            opponent in each turn. The ith row corresponds to the ith opponent
            and the jth column the jth turn.
        """

        if isinstance(self.strategy, axl.Player):
            players = [self.strategy] + self.opponents
        else:
            players = [self.strategy()] + self.opponents

        temp_file_descriptor = None
        if filename is None:
            temp_file_descriptor, filename = mkstemp()  # type: ignore

        edges = [(0, k + 1) for k in range(len(self.opponents))]
        tournament = axl.Tournament(players=players,
                                    edges=edges, turns=turns, noise=noise,
                                    repetitions=repetitions)
        tournament.play(filename=filename, build_results=False,
                        progress_bar=progress_bar, processes=processes)

        self.data = self.analyse_cooperation_ratio(filename)

        if temp_file_descriptor is not None:
            assert filename is not None
            os.close(temp_file_descriptor)
            os.remove(filename)

        return self.data

    @staticmethod
    def analyse_cooperation_ratio(filename):
        """Generates the data used from the tournament

        Return an M by N array where M is the number of opponents and N is the
        number of turns.

        Parameters
        ----------
        filename : str
            The filename of the interactions

        Returns
        ----------
        self.data : np.array
            A numpy array containing the mean cooperation rate against each
            opponent in each turn. The ith row corresponds to the ith opponent
            and the jth column the jth turn.
        """
        did_c = np.vectorize(lambda actions: [int(action == 'C')
                                              for action in actions])

        cooperation_rates = {}
        df = dd.read_csv(filename)
        # We ignore the actions of all opponents. So we filter the dataframe to
        # only include the results of the player with index `0`.
        df = df[df["Player index"] == 0][["Opponent index", "Actions"]]

        for _, row in df.iterrows():
            opponent_index, player_history = row["Opponent index"], row["Actions"]
            if opponent_index in cooperation_rates:
                cooperation_rates[opponent_index].append(did_c(player_history))
            else:
                cooperation_rates[opponent_index] = [did_c(player_history)]

        for index, rates in cooperation_rates.items():
            cooperation_rates[index] = np.mean(rates, axis=0)

        return np.array([cooperation_rates[index]
                         for index in sorted(cooperation_rates)])

    def plot(self, cmap: str = 'viridis', interpolation: str = 'none',
             title: str = None, colorbar: bool = True, labels: bool = True,
             display_names: bool = False,
             ax: plt.Figure = None) -> plt.Figure:
        """Plot the results of the spatial tournament.
        Parameters
        ----------
        cmap : str, optional
            A matplotlib colour map, full list can be found at
            http://matplotlib.org/examples/color/colormaps_reference.html
        interpolation : str, optional
            A matplotlib interpolation, full list can be found at
            http://matplotlib.org/examples/images_contours_and_fields/interpolation_methods.html
        title : str, optional
            A title for the plot
        colorbar : bool, optional
            Choose whether the colorbar should be included or not
        labels : bool, optional
            Choose whether the axis labels and ticks should be included
        display_names : bool, optional
            Choose whether to display the names of the strategies
        ax: matplotlib axis
            Allows the plot to be written to a given matplotlib axis.
            Default is None.
        Returns
        ----------
        figure : matplotlib figure
            A heat plot of the results of the spatial tournament
        """
        if ax is None:
            fig, ax = plt.subplots()
        else:
            ax = ax

        fig = ax.get_figure()
        mat = ax.imshow(self.data, cmap=cmap, interpolation=interpolation)

        width = len(self.data) / 2
        height = width
        fig.set_size_inches(width, height)

        plt.xlabel('turns')
        ax.tick_params(axis='both', which='both', length=0)

        if display_names:
            plt.yticks(range(len(self.opponents)), [str(player) for player in
                                                    self.opponents])
        else:
            plt.yticks([0, len(self.opponents) - 1], [0, 1])
            plt.ylabel("Probability of cooperation")

        if not labels:
            plt.axis('off')

        if title is not None:
            plt.title(title)

        if colorbar:
            max_score = 0
            min_score = 1
            ticks = [min_score, 1 / 2, max_score]

            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.2)
            cbar = fig.colorbar(mat, cax=cax, ticks=ticks)

        plt.tight_layout()
        return fig
