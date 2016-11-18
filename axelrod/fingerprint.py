import axelrod as axl
import numpy as np
import matplotlib.pyplot as plt
from axelrod.strategy_transformers import JossAnnTransformer, DualTransformer
from axelrod.interaction_utils import compute_final_score_per_turn, read_interactions_from_file
from axelrod import on_windows
from collections import namedtuple
from tempfile import NamedTemporaryFile


Point = namedtuple('Point', 'x y')


def create_points(step):
    """Creates a set of Points over the unit square.

    A Point has coordinates (x, y). This function constructs points that are
    separated by a step equal to `step`. The points are over the unit
    square which implies that the number created will be 1/`step`^2.

    Parameters
    ----------
    step : float
        The separation between each Point. Smaller steps will produce more
        Points with coordinates that will be closer together.

    Returns
    ----------
    points : list
        of Point objects with coordinates (x, y)
    """
    points = list(Point(j, k) for j in np.arange(0, 1, step)
                  for k in np.arange(0, 1, step))

    return points


class AshlockFingerprint():
    def __init__(self, strategy, probe):
        """
        Parameters
        ----------
        strategy : class
            A class that must be descended from axelrod.Player
        probe : class
            A class that must be descended from axelrod.Player
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
        if x + y >= 1:
            joss_ann = DualTransformer()(JossAnnTransformer((1 - x, 1 - y))(probe))()
        else:
            joss_ann = JossAnnTransformer((x, y))(probe)()
        return joss_ann

    @staticmethod
    def create_edges(points):
        """Creates a set of edges for a spatial tournament.

        Constructs edges that correspond to `points`. All edges begin at 0, and
        connect to the index +1 of the probe.

        Parameters
        ----------
        points : list
            of Point objects with coordinates (x, y)

        Returns
        ----------
        edges : list of tuples
            A list containing tuples of length 2. All tuples will have 0 as the
            first element. The second element is the index of the
            corresponding probe (+1 to allow for including the Strategy and its
            Dual).
        """
        edges = [(0, index + 1) for index, point in enumerate(points)]
        return edges

    def create_probes(self, probe, points):
        """Creates a set of probe strategies over the unit square.

        Constructs probe strategies that correspond to points with coordinates
        (x, y). The probes are created using the `JossAnnTransformer`.

        Parameters
        ----------
        probe : class
            A class that must be descended from axelrod.strategies.
        points : list
            of Point objects with coordinates (x, y)

        Returns
        ----------
        probes : list
            A list of `JossAnnTransformer` players with parameters that
            correspond to point.
        """
        probes = [self.create_jossann(point, probe) for point in points]
        return probes

    def construct_tournament_elements(self, step):
        """Build the elements required for a spatial tournament

        Parameters
        ----------
        step : float
            The separation between each Point. Smaller steps will
            produce more Points that will be closer together.

        Returns
        ----------
        edges : list of tuples
            A list containing tuples of length 2. All tuples will have either 0
            or 1 as the first element. The second element is the index of the
            corresponding probe (+2 to allow for including the Strategy and its
            Dual).

        tournament_players : list
            A list containing instances of axelrod.Player. The first item is the
            original player, the second is the dual, the rest are the probes.

        """
        probe_points = create_points(step)
        self.points = probe_points
        edges = self.create_edges(probe_points)

        probe_players = self.create_probes(self.probe, probe_points)
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
            corresponding probe (+2 to allow for including the Strategy and its
            Dual).

        Returns
        ----------
        point_scores : dictionary
            A dictionary where the keys are Points of the form (x, y) and
            the values are the mean score for the corresponding interactions.
        """
        edge_scores = [np.mean([compute_final_score_per_turn(scores)[0] for scores
                                in interactions[edge]]) for edge in edges]
        point_scores = dict(zip(points, edge_scores))
        return point_scores

    def fingerprint(self, turns=50, repetitions=10, step=0.01, processes=None,
                    filename=None, in_memory=False, progress_bar=True):
        """Build and play the spatial tournament.

        Creates the probes and their edges then builds a spatial tournament
        where the original strategy only plays probes whose coordinates sum to
        less than 1 (or equal). Probes whose coordinates sum to more than 1 play
        the Dual Strategy.

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

        if on_windows and (filename is None):
            in_memory = True
        elif filename is not None:
            outputfile = open(filename, 'w')
            filename = outputfile.name
        else:
            outputfile = NamedTemporaryFile(mode='w')
            filename = outputfile.name

        edges, tourn_players = self.construct_tournament_elements(step)
        self.step = step
        self.spatial_tournament = axl.SpatialTournament(tourn_players,
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
            self.interactions = read_interactions_from_file(filename)

        self.data = self.generate_data(self.interactions, self.points, edges)
        return self.data

    def plot(self, col_map='seismic', interpolation='none'):
        """Plot the results of the spatial tournament.

        Parameters
        ----------
        filename : str, optional
            The location and name that the resulting plot should be saved to.
            Defaults to the current directory with the name
            `Strategy and Probe.pdf`
        col_map : str, optional
            A matplotlib colour map, full list can be found at
            http://matplotlib.org/examples/color/colormaps_reference.html
        interpolation : str, optional
            A matplotlib interpolation, full list can be found at
            http://matplotlib.org/examples/images_contours_and_fields/interpolation_methods.html

        Returns
        ----------
        figure : matplotlib figure
            A heat plot of the results of the spatial tournament
        """
        size = int((1 / self.step) // 1)
        ordered_data = [self.data[point] for point in self.points]
        plotting_data = np.reshape(ordered_data, (size, size))
        figure = plt.figure()
        plt.imshow(plotting_data, cmap=col_map, interpolation=interpolation)
        plt.axis('off')
        return figure
