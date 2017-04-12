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


class AshlockFingerprint(object):
    def __init__(self, strategy, probe=axl.TitForTat, step: float = 0.01,
                 progress_bar: bool = False) -> None:
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
        self.player = create_player(strategy)
        self._probe_class, self._probe_kwargs = get_class_and_kwargs(probe)
        self._step = step
        self.progress_bar = progress_bar
        self.points = self.create_points()
        self.probe_list = self.create_probes()

        self.interactions = {}  # type: dict
        self.spatial_tournament = None  # type: axl.SpatialTournament
        self.data = {}  # type: dict

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, new_step: float):
        self._step = new_step
        self.points = self.create_points()
        self.probe_list = self.create_probes()

    @property
    def probe(self):
        return self._probe_class(**self._probe_kwargs)

    @probe.setter
    def probe(self, new_probe):
        self._probe_class, self._probe_kwargs = get_class_and_kwargs(new_probe)
        self.probe_list = self.create_probes()

    def create_points(self):
        return create_points(self._step, self.progress_bar)

    def create_probes(self):
        """Creates a list of probe strategies over the unit square.

        Constructs probe strategies that correspond to points with coordinates
        (x, y). The probes are created using the `JossAnnTransformer` and
        `DualTransformer`."""
        if self.progress_bar:
            points = tqdm.tqdm(self.points, desc="Generating probes")
        else:
            points = self.points
        probes = [self.create_jossann(point) for point in points]
        return probes

    def create_jossann(self, point):
        """Creates a JossAnn probe player that matches the Point.

        If the coordinates of point sums to more than 1 the parameters are
        flipped and subtracted from 1 to give meaningful probabilities. We also
        use the Dual of the probe. This is outlined further in [Ashlock2010]_.
        """
        x, y = point

        if x + y >= 1:
            joss_ann = DualTransformer()(
                JossAnnTransformer((1 - x, 1 - y))(self._probe_class)
            )(**self._probe_kwargs)
        else:
            joss_ann = JossAnnTransformer((x, y))(
                self._probe_class)(**self._probe_kwargs)
        return joss_ann

    def fingerprint(self, turns: int = 50, repetitions: int = 10,
                    new_step: float = None, processes: int = None,
                    filename: str = None, in_memory: bool =False,
                    progress_bar: bool = True) -> dict:
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
        new_step : float, optional
            The separation between each Point. Smaller steps will
            produce more Points that will be closer together.
        processes : integer, optional
            The number of processes to be used for parallel processing
        progress_bar : bool
            Whether or not to create a progress bar which will be updated
        filename : str
            File where results are saved.
        in_memory : bool

        Returns
        ----------
        self.data : dictionary
            A dictionary where the keys are coordinates of the form (x, y) and
            the values are the mean score for the corresponding interactions.
        """

        if on_windows and (filename is None):  # pragma: no cover
            in_memory = True
        elif filename is None:
            output_file = NamedTemporaryFile(mode='w')
            filename = output_file.name
        if new_step:
            self.step = new_step

        edges = self._create_edges()
        tourn_players = [self.player] + self.probe_list

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

        self.data = self._generate_data(edges)
        return self.data

    def _create_edges(self):
        """Creates a list of edges for a spatial tournament.

        Returns
        ----------
        edges : list of tuples
            A list containing tuples of length 2. All tuples will have 0 as the
            first element. The second element is the index of the
            corresponding probe (+1 to allow for including the Strategy).
        """
        if self.progress_bar:
            points = tqdm.tqdm(self.points, desc="Generating network edges")
        else:
            points = self.points
        edges = [(0, probe_index) for probe_index in range(1, len(points) + 1)]
        return edges

    def _generate_data(self, edges: list) -> dict:
        """Generates useful data from a spatial tournament.

        Matches interactions from `results` to their corresponding Point in
        `probe_points`.

        Parameters
        ----------
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
                                   for scores in self.interactions[edge]])
                       for edge in edges
                       ]
        point_scores = dict(zip(self.points, edge_scores))
        return point_scores


    def plot(self):
        pass

class DataManipulation(object):

    def __init__(self, data: dict, points: list) -> None:
        self.data = data.copy()
        self.points = points[:]

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

        plotting_data = self.reshape_data()
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

    def reshape_data(self):
        """Shape the data so that it can be plotted easily.

        Returns
        ----------
        plotting_data : list
            2-D numpy array of the scores, correctly shaped to ensure that the
            score corresponding to Point (0, 0) is in the left hand corner ie.
            the standard origin.
        """
        size = int(len(self.points) ** 0.5)
        ordered_data = [self.data[point] for point in self.points]
        shaped_data = np.reshape(ordered_data, (size, size), order='F')
        plotting_data = np.flipud(shaped_data)
        return plotting_data


def create_points(step: float, progress_bar: bool = True) -> list:
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
    points_per_side = int(1 / step) + 1
    p_bar = None
    if progress_bar:
        p_bar = tqdm.tqdm(total=points_per_side ** 2, desc="Generating points")

    points = []
    for x in np.linspace(0, 1, points_per_side):
        for y in np.linspace(0, 1, points_per_side):
            points.append(Point(x, y))

            if p_bar:
                p_bar.update()

    if p_bar:
        p_bar.close()

    return points


def get_class_and_kwargs(strategy_or_player):
    probe_player = create_player(strategy_or_player)
    return probe_player.__class__, probe_player.init_kwargs


def create_player(strategy_or_player):
    if isinstance(strategy_or_player, axl.Player):
        return strategy_or_player
    return strategy_or_player()
