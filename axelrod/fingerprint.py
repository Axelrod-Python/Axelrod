from collections import namedtuple
from tempfile import NamedTemporaryFile
from typing import Any, Union, Dict, Tuple, List
import matplotlib.pyplot as plt
import numpy as np
import tqdm
import axelrod as axl

from axelrod import on_windows, Player
from axelrod.actions import Action
from axelrod.strategy_transformers import JossAnnTransformer, DualTransformer
from axelrod.interaction_utils import (
    compute_final_score_per_turn, read_interactions_from_file)


Point = namedtuple('Point', 'x y')


PlayerOrStrategy = Union[Player, type]
Edges = Tuple[int, int]
Matches = List[List[Tuple[Action, Action]]]

PointsPlayers = Dict[Point, Player]
PointsFloats = Dict[Point, float]
PointsEdges = Dict[Point, Edges]
PointsMatches = Dict[Point, Matches]


class AshlockFingerprint(object):
    def __init__(self, strategy: PlayerOrStrategy,
                 probe: PlayerOrStrategy) -> None:
        self._strategy = strategy
        self._probe = probe
        self._data = None  # type: DataOrganizer

    @property
    def interactions(self) -> PointsMatches:
        if not self._data:
            interactions = None  # type: PointsMatches
            return interactions
        return self._data.get_points_interactions_dict()

    @property
    def data(self) -> PointsFloats:
        if not self._data:
            data = None  # type: PointsFloats
            return data
        return self._data.get_points_averages_dict()

    def fingerprint(self, turns: int = 50, repetitions: int = 10,
                    step: float = 0.01, processes: int = None,
                    filename: str = None, in_memory: bool = False,
                    progress_bar: bool = True) -> PointsFloats:

        tournament_creator = SpatialTournamentCreator(self._strategy,
                                                      self._probe,
                                                      step)
        tournament_kwargs = {'turns': turns, 'repetitions': repetitions}

        play_kwargs = _get_play_kwargs(filename=filename, in_memory=in_memory,
                                       processes=processes,
                                       progress_bar=progress_bar)

        tournament = tournament_creator.get_tournament(**tournament_kwargs)
        tournament.play(**play_kwargs)

        point_edge_map = tournament_creator.get_points_to_edges()
        if play_kwargs['in_memory']:
            interactions = tournament.interactions_dict
        else:
            interactions = read_interactions_from_file(
                filename, progress_bar=progress_bar)

        self._data = DataOrganizer(point_edge_map, interactions)
        return self.data

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

        plotting_data = self._data.get_plotting_data()
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


def _get_play_kwargs(filename: Any, in_memory: bool,
                     processes: Union[int, None], progress_bar: bool
                     ) -> Dict[str, Any]:
    """Adjust and build the kwargs for tournament.play() based on issues
    with Windows OS."""
    play_kwargs = {'build_results': False,
                   'processes': processes,
                   'progress_bar': progress_bar}

    if on_windows and filename is None:  # pragma: no cover
        in_memory = True
    elif filename is None:
        output_file = NamedTemporaryFile(mode='w')
        filename = output_file.name
    play_kwargs['filename'] = filename
    play_kwargs['in_memory'] = in_memory
    return play_kwargs


class SpatialTournamentCreator(object):
    """Creates a list of Points.  Creates probes mapped to Points.
    Creates a SpatialTournament where player plays exactly one match with each
    probe per repetition."""
    def __init__(self, player: PlayerOrStrategy, probe: PlayerOrStrategy,
                 step: float) -> None:
        """0.0 <= step <= 1.0"""
        self._player = create_player(player)
        self._probe_gen = JossAnnProbeCreator(probe)
        self._points = create_points(step)

    def get_points_to_edges(self) -> PointsEdges:
        """

        :return: A map of each point to corresponding key in
            tournament.interactions_dict
        """
        return {point: (0, index + 1)
                for index, point in enumerate(self._points)}

    def get_tournament(self, **tournament_kwargs) -> axl.SpatialTournament:
        players = [self._player]
        edges = []
        edge_map = self.get_points_to_edges()
        probe_map = self._probe_gen.get_probe_dict(self._points)

        for point in self._points:
            players.append(probe_map[point])
            edges.append(edge_map[point])

        return axl.SpatialTournament(players=players, edges=edges,
                                     **tournament_kwargs)


class JossAnnProbeCreator(object):
    """Creates JossAnn Players and Dual JossAnn Players based on points
    where Point(0.0) <= point <= Point(1.0, 1.0)"""
    def __init__(self, probe: PlayerOrStrategy) -> None:
        self._probe_class, self._probe_kwargs = get_class_and_kwargs(probe)

    def get_probe(self, point: Point) -> Player:
        x, y = point
        if x + y >= 1:
            joss_ann = DualTransformer()(
                JossAnnTransformer((1 - x, 1 - y))(self._probe_class)
            )(**self._probe_kwargs)
        else:
            joss_ann = JossAnnTransformer((x, y))(
                self._probe_class
            )(**self._probe_kwargs)
        return joss_ann

    def get_probe_dict(self, point_list: list) -> PointsPlayers:
        return {point: self.get_probe(point) for point in point_list}

    def get_probe_dict_from_step(self, step: float) -> PointsPlayers:
        point_list = create_points(step)
        return self.get_probe_dict(point_list)


def create_points(step: float) -> List[Point]:
    """

    :param step: step rounds up to the nearest value such that
        1/step == int(1/step) (so step=0.48 becomes step=0.5)
    :return: The list of all Points in the unit square
        where 0.0 <= Point.x or Point.y <=1.0  and Point.x|y / step ==
        int(Point.x|y / step) (so for step=0.5, x and y are in [0.0, 0.5, 1.0])
    """
    points_per_side = int(1 / step) + 1
    points = []
    for x in np.linspace(0, 1, points_per_side):
        for y in np.linspace(0, 1, points_per_side):
            points.append(Point(x, y))
    return points


class DataOrganizer(object):
    def __init__(self, point_edge_map: PointsEdges,
                 interactions_dict: Dict[Edges, Matches]) -> None:
        """

        :param point_edge_map: The points in this map must make an evenly
            spaced square with 0.0 <= Point.x or Point.y <= 1.0
        :param interactions_dict: point_edge_map.values() ==
            interaction_dict.keys()
        """
        self._point_to_edge = point_edge_map.copy()
        self._interactions = interactions_dict.copy()

    def get_points_interactions_dict(self) -> PointsMatches:
        return {point: self._interactions[edge]
                for point, edge in self._point_to_edge.items()}

    def get_points_averages_dict(self) -> PointsFloats:
        point_interactions = self.get_points_interactions_dict()
        return {point: get_mean_score(matches_list)
                for point, matches_list in point_interactions.items()}

    def get_plotting_data(self) -> np.ndarray:
        ordered_edges = [item[1] for item in
                         sorted(self._point_to_edge.items())]
        side_len = int(round(len(ordered_edges) ** 0.5))

        ordered_data = [get_mean_score(self._interactions[edge])
                        for edge in ordered_edges]
        shaped_data = np.reshape(ordered_data, (side_len, side_len), order='F')
        plotting_data = np.flipud(shaped_data)
        return plotting_data


def get_mean_score(matches_list: Matches) -> float:
        match_scores = [compute_final_score_per_turn(match)[0]
                        for match in matches_list]
        return sum(match_scores)/len(match_scores)



"""
the above objects and functions can be called/created as needed for whatever
funkiness AshlockFingerprint wants.  If other fingerprints show up, they
might even be easily extendable.
"""

class AshlockFingerprint2(object):
    def __init__(self, strategy: Any, probe: Any = axl.TitForTat,
                 step: float = 0.01, progress_bar: bool = True) -> None:
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
        step: float = 0.01
            The separation between each Point. Smaller steps will
            produce more Points that will be closer together.
        progress_bar: bool = True
            True = show a progress bar when constructing probes and running
            tournament.
        """
        self.player = create_player(strategy)
        self._probe_class, self._probe_kwargs = get_class_and_kwargs(probe)
        self._step = step
        self.progress_bar = progress_bar
        self.points = self._create_points()
        self._probe_list = self._create_probes()

        self.interactions = {}  # type: dict
        self.spatial_tournament = None  # type: axl.SpatialTournament
        self.data = {}  # type: dict

    @property
    def step(self):
        integer_inverse = int(1 / self._step)
        return 1.0 / integer_inverse

    @step.setter
    def step(self, new_step: float):
        self._step = new_step
        self.points = self._create_points()
        self._probe_list = self._create_probes()

    @property
    def probe(self):
        return self._probe_class(**self._probe_kwargs)

    @probe.setter
    def probe(self, new_probe):
        self._probe_class, self._probe_kwargs = get_class_and_kwargs(new_probe)
        self._probe_list = self._create_probes()

    def _create_points(self) -> list:
        """Returns a list of Points(x=0.0-1.0, y=0.0-1.0) at
        intervals=self._step. self._step=0.1 produces the list
        [Point(0.0, 0.0), Point(0.1, 0.0), ... Point(1.0, 0.9), Point(1.0, 1.0)]
        """
        points_per_side = int(1 / self._step) + 1
        points = []
        for x in np.linspace(0, 1, points_per_side):
            for y in np.linspace(0, 1, points_per_side):
                points.append(Point(x, y))
        return points

    def _create_probes(self):
        """Creates a list of probe strategies over the unit square.

        Constructs probe strategies that correspond to points with coordinates
        (x, y). The probes are created using the `JossAnnTransformer` and
        `DualTransformer`."""
        if self.progress_bar:
            points = tqdm.tqdm(self.points, desc="Generating probes")
        else:
            points = self.points
        probes = [self._create_jossann(point) for point in points]
        return probes

    def _create_jossann(self, point):
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
                self._probe_class
            )(**self._probe_kwargs)
        return joss_ann

    def fingerprint(self, turns: int = 50, repetitions: int = 10,
                    new_step: float = None, processes: int = None,
                    filename: str = None, in_memory: bool =False) -> dict:
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
        filename : str
            File where results are saved.
        in_memory : bool

        Returns
        ----------
        self.data : dictionary
            A dictionary where the keys are coordinates of the form (x, y) and
            the values are the mean score for the corresponding interactions.
        """

        if on_windows and filename is None:  # pragma: no cover
            in_memory = True
        elif filename is None:
            output_file = NamedTemporaryFile(mode='w')
            filename = output_file.name

        if new_step:
            self.step = new_step

        tournament_players = [self.player] + self._probe_list
        edges = [(0, probe_index) for probe_index in
                 range(1, len(self._probe_list) + 1)]

        self.spatial_tournament = axl.SpatialTournament(
            tournament_players,
            turns=turns,
            repetitions=repetitions,
            edges=edges
        )
        self.spatial_tournament.play(build_results=False,
                                     filename=filename,
                                     processes=processes,
                                     in_memory=in_memory,
                                     progress_bar=self.progress_bar)
        if in_memory:
            self.interactions = self.spatial_tournament.interactions_dict
        else:
            self.interactions = read_interactions_from_file(
                filename, progress_bar=self.progress_bar)

        self.data = self._generate_data(edges)
        return self.data

    def _generate_data(self, edges: list) -> dict:
        """Generates useful data from a spatial tournament.

        Matches interactions from `results` to their corresponding Point in
        `probe_points`.

        Returns
        ----------
        point_scores : dictionary
            A dictionary where the keys are Points of the form (x, y) and
            the values are the mean score for the corresponding interactions.
        """
        edge_scores = [
            np.mean(
                [compute_final_score_per_turn(scores)[0]
                 for scores in self.interactions[edge]]
            ) for edge in edges
        ]
        point_scores = dict(zip(self.points, edge_scores))
        return point_scores

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

        plotting_data = self._reshape_data()
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

    def _reshape_data(self):
        """Shape the data so that it can be plotted easily.

        Returns
        ----------
        plotting_data : list
            2-D numpy array of the scores, correctly shaped to ensure that the
            score corresponding to Point (0, 0) is in the left hand corner ie.
            the standard origin.
        """
        side_len = int(1 / self._step) + 1
        ordered_data = [self.data[point] for point in self.points]
        shaped_data = np.reshape(ordered_data, (side_len, side_len), order='F')
        plotting_data = np.flipud(shaped_data)
        return plotting_data


def get_class_and_kwargs(strategy_or_player: Any) -> tuple:
    """If strategy, returns a class and kwargs to create default player.
    If Player, returns a class and kwargs to re-create that instance."""
    probe_player = create_player(strategy_or_player)
    return probe_player.__class__, probe_player.init_kwargs


def create_player(strategy_or_player: Any) -> Player:
    """If strategy, returns the default Player of that strategy. Else
    returns the Player."""
    if isinstance(strategy_or_player, axl.Player):
        return strategy_or_player.clone()
    return strategy_or_player()
