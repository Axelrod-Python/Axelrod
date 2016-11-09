import axelrod as axl
import numpy as np
# import matplotlib.pyplot as plt
from axelrod.strategy_transformers import JossAnnTransformer, DualTransformer
from axelrod.interaction_utils import compute_final_score_per_turn as cfspt
from collections import namedtuple


def create_jossann(coordinate, probe):
    """Creates a JossAnn probe player that matches the coordinate.

    If the coordinate sums to more than 1 the parameters are flipped and
    subtracted from 1 to give meaningful probabilities. This is outlined further
    in [Ashlock2010]_.

    Parameters
    ----------
    coordinate : tuple of length 2
        coordinate of the form (x, y)
    probe : class
        A class that must be descended from axelrod.strategies

    Returns
    ----------
    joss_ann: Joss-AnnTitForTat object
        `JossAnnTransformer` with parameters that correspond to (x, y).
    """
    x, y = coordinate
    if x + y > 1:
        joss_ann = JossAnnTransformer((1 - y, 1 - x))(probe)()
    else:
        joss_ann = JossAnnTransformer((x, y))(probe)()
    return joss_ann


def create_coordinates(step):
    """Creates a set of coordinates over the unit square.

    Constructs (x, y) coordinates that are separated by a step equal to
    `step`. The coordinates are over the unit squeare which implies
    that the number of points created will be 1/`step`^2.

    Parameters
    ----------
    step : float
        The separation between each coordinate. Smaller steps will
        produce more coordinates that will be closer together.

    Returns
    ----------
    coordinates : list of tuples
        Tuples of length 2 representing each coordinate, eg. (x, y)
    """
    Point = namedtuple('Point', 'x y')
    coordinates = list(Point(j, k) for j in np.arange(0, 1, step)
                       for k in np.arange(0, 1, step))

    return coordinates


def create_probes(probe, coordinates):
    """Creates a set of probe strategies over the unit square.

    Constructs probe strategies that correspond to (x, y) coordinates. The
    probes are created using the `JossAnnTransformer`.

    Parameters
    ----------
    probe : class
        A class that must be descended from axelrod.strategies.
    coordinates : list of tuples
        Tuples of length 2 representing each coordinate, eg. (x, y)

    Returns
    ----------
    probe_dict : ordered dictionary
        An Ordered Dictionary where the keys are tuples representing each
        coordinate, eg. (x, y). The value is a `JossAnnTransformer` with
        parameters that correspond to (x, y).
    """
    probes = [create_jossann(coordinate, probe) for coordinate in coordinates]
    return probes


def create_edges(coordinates):
    """Creates a set of edges for a spatial tournament.

    Constructs edges that correspond to `coordinates`. Coordinates that sum to
    1 or less will have edges that start at 0, those who sum to more than will
    have an edge that starts at 1.

    Parameters
    ----------
    coordinates : list of tuples
        Tuples of length 2 representing each coordinate, eg. (x, y)

    Returns
    ----------
    edges : list of tuples
        A list containing tuples of length 2. All tuples will have either 0
        or 1 as the first element. The second element is the index of the
        corresponding probe (+2 to allow for including the Strategy and it's
        Dual).
    """
    edges = []
    for index, coordinate in enumerate(coordinates):
        #  Add 2 to the index because we will have to allow for the Strategy
        #  and it's Dual
        if sum(coordinate) > 1:
            edge = (1, index + 2)
        else:
            edge = (0, index + 2)
        edges.append(edge)
    return edges


def generate_data(interactions, coordinates, edges):
    """Generates useful data from a spatial tournament.

    Matches interactions from `results` to their corresponding coordinate in
    `probe_coords`.

    Parameters
    ----------
    interactions : dictionary
        A dictionary of the interactions of a tournament
    coordinates : list of tuples
        A list of tuples of length 2, where each tuple represents a
        coordinate, eg. (x, y).
    edges : list of tuples
        A list containing tuples of length 2. All tuples will have either 0
        or 1 as the first element. The second element is the index of the
        corresponding probe (+2 to allow for including the Strategy and it's
        Dual).

    Returns
    ----------
    coordinate_scores : dictionary
        A dictionary where the keys are coordinates of the form (x, y) and
        the values are the mean score for the corresponding interactions.
    """
    edge_scores = [np.mean([cfspt(scores) for scores in interactions[edge]])
                   for edge in edges]
    coordinate_scores = dict(zip(coordinates, edge_scores))
    return coordinate_scores


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

    def construct_tournament_elements(self, step):
        """Build the elements required for a spatial tournament

        Parameters
        ----------
        step : float
            The separation between each coordinate. Smaller steps will
            produce more coordinates that will be closer together.

        Returns
        ----------
        edges : list of tuples
            A list containing tuples of length 2. All tuples will have either 0
            or 1 as the first element. The second element is the index of the
            corresponding probe (+2 to allow for including the Strategy and it's
            Dual).

        tournament_players : list
            A list containing instances of axelrod.Player. The first item is the
            original player, the second is the dual, the rest are the probes.

        """
        probe_coordinates = create_coordinates(step)
        self.coordinates = probe_coordinates
        edges = create_edges(probe_coordinates)

        dual = DualTransformer()(self.strategy)()
        probe_players = create_probes(self.probe, probe_coordinates)
        # probes = probe_players.values()
        tournament_players = [self.strategy(), dual] + probe_players

        return edges, tournament_players

    def fingerprint(self, turns=50, repetitions=10, step=0.01, processes=None):
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
            The separation between each coordinate. Smaller steps will
            produce more coordinates that will be closer together.
        processes : integer, optional
            The number of processes to be used for parallel processing
        """
        edges, tourn_players = self.construct_tournament_elements(step)
        self.spatial_tourn = axl.SpatialTournament(tourn_players, turns=turns,
                                                   repetitions=repetitions,
                                                   edges=edges)
        self.results = self.spatial_tourn.play(processes=processes,
                                               build_results=True,
                                               in_memory=True,
                                               keep_interactions=True)
        self.data = generate_data(self.results.interactions, self.coordinates)

    def plot(self, col_map=None):
        """Plot the results of the spatial tournament.

        Parameters
        ----------
        col_map : str, optional
            A matplotlib colour map, full list can be found at
            http://matplotlib.org/examples/color/colormaps_reference.html
        """

        # sns.heatmap(self.data, cmap=col_map)
        # plt.show()

        pass
