from collections import namedtuple
from tempfile import NamedTemporaryFile
import matplotlib.pyplot as plt
import numpy as np
import tqdm
import axelrod as axl

from axelrod import on_windows
from axelrod.strategy_transformers import JossAnnTransformer, DualTransformer
from axelrod.interaction_utils import (
    compute_final_score_per_turn, read_interactions_from_file)


Point = namedtuple('Point', 'x y')


def create_points(step, progress_bar=True):
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


class AshlockFingerprint():
    def __init__(self, strategy, probe=axl.TitForTat):
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

    @staticmethod
    def create_jossann(point, probe):
        """Creates a JossAnn probe player that matches the Point.

        If the coordinates of point sums to more than 1 the parameters are
        flipped and subtracted from 1 to give meaningful probabilities. We also
        use the Dual of the probe. This is outlined further in [Ashlock2010]_.

        Parameters
        ----------
        point : Point
        probe : class
            A class that must be descended from axelrod.strategies

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

    @staticmethod
    def create_edges(points, progress_bar=True):
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

    def create_probes(self, probe, points, progress_bar=True):
        """Creates a set of probe strategies over the unit square.

        Constructs probe strategies that correspond to points with coordinates
        (x, y). The probes are created using the `JossAnnTransformer`.

        Parameters
        ----------
        probe : class
            A class that must be descended from axelrod.strategies.
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
        probes = [self.create_jossann(point, probe) for point in points]
        return probes

    def construct_tournament_elements(self, step, progress_bar=True):
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
        edges = self.create_edges(self.points, progress_bar=progress_bar)
        probe_players = self.create_probes(self.probe, self.points,
                                           progress_bar=progress_bar)

        if isinstance(self.strategy, axl.Player):
            tournament_players = [self.strategy] + probe_players
        else:
            tournament_players = [self.strategy()] + probe_players

        return edges, tournament_players

    @staticmethod
    def generate_data(interactions, points, edges):
        """Generates useful data from a spatial tournament.

        Matches interactions from `results` to their corresponding Point in
        `probe_points`.

        Parameters
        ----------
        interactions : dictionary
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
        point_scores : dictionary
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

    def fingerprint(self, turns=50, repetitions=10, step=0.01, processes=None,
                    filename=None, in_memory=False, progress_bar=True):
        """Build and play the spatial tournament.

        Creates the probes and their edges then builds a spatial tournament.
        When the coordinates of the probe sum to more than 1, the dual of the
        probe is taken instead and then the Joss-Ann Transformer is applied. If
        the coordinates sum to less than 1 (or equal), then only the Joss-Ann is
        applied, a dual is not required.

        Parameters
        ----------
        turns : integer, optional
            The number of turns per match
        repetitions : integer, optional
            The number of times the round robin should be repeated
        step : float, optional
            The separation between each Point. Smaller steps will
            produce more Points that will be closer together.
        processes : integer, optional
            The number of processes to be used for parallel processing
        progress_bar : bool
            Whether or not to create a progress bar which will be updated

        Returns
        ----------
        self.data : dictionary
            A dictionary where the keys are coordinates of the form (x, y) and
            the values are the mean score for the corresponding interactions.
        """

        if on_windows and (filename is None):  # pragma: no cover
            in_memory = True
        elif filename is None:
            outputfile = NamedTemporaryFile(mode='w')
            filename = outputfile.name

        edges, tourn_players = self.construct_tournament_elements(
            step, progress_bar=progress_bar)

        self.step = step
        self.spatial_tournament = axl.SpatialTournament(
            tourn_players,
            turns=turns,
            repetitions=repetitions,
            edges=edges)
        self.spatial_tournament.play(build_results=False,
                                     filename=filename,
                                     processes=processes,
                                     in_memory=in_memory,
                                     progress_bar=progress_bar)
        if in_memory:
            self.interactions = self.spatial_tournament.interactions_dict
        else:
            self.interactions = read_interactions_from_file(
                filename, progress_bar=progress_bar)

        self.data = self.generate_data(self.interactions, self.points, edges)
        return self.data

    @staticmethod
    def reshape_data(data, points, size):
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

    def plot(self, col_map='seismic', interpolation='none', title=None,
             colorbar=True, labels=True):
        """Plot the results of the spatial tournament.

        Parameters
        ----------
        col_map : str, optional
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
        plotting_data = self.reshape_data(self.data, self.points, size)
        fig, ax = plt.subplots()
        cax = ax.imshow(
            plotting_data, cmap=col_map, interpolation=interpolation)

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
