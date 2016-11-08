import axelrod as axl
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import product
from axelrod.strategy_transformers import JossAnnTransformer, DualTransformer
from axelrod.interaction_utils import compute_final_score_per_turn as cfspt
from collections import OrderedDict


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


class Fingerprint():
    def __init__(self):
        pass

    def plot(self):
        pass


class AshlockFingerprint(Fingerprint):
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

    def create_probe_coords(self, step):
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
        coordinates = list(product(np.arange(0, 1, step),
                                   np.arange(0, 1, step)))
        return coordinates

    def create_probes(self, probe, probe_coords):
        """Creates a set of probe strategies over the unit square.

        Constructs probe strategies that correspond to (x, y) coordinates. The
        precision of the coordinates is determined by `step`. The probes
        are created using the `JossAnnTransformer`.

        Parameters
        ----------
        probe : class
            A class that must be descended from axelrod.strategies.
        probe_coords : ordered dictionary
            An Ordered Dictionary where the keys are tuples representing each
            coordinate, eg. (x, y). The value is automatically set to `None`.

        Returns
        ----------
        probe_dict : ordered dictionary
            An Ordered Dictionary where the keys are tuples representing each
            coordinate, eg. (x, y). The value is a `JossAnnTransformer` with
            parameters that correspond to (x, y).
        """
        probe_dict = OrderedDict((coord, create_jossann(coord, probe))
                                 for coord in probe_coords)
        return probe_dict

    def create_edges(self, probe_dict):
        """Creates a set of edges for a spatial tournament.

        Constructs edges that correspond to the probes in `probe_dict`. Probes
        whose coordinates sum to less/more than 1 will have edges that link them
        to 0/1 correspondingly.

        Parameters
        ----------
        probe_dict : ordered dictionary
            An Ordered Dictionary where the keys are tuples representing each
            coordinate, eg. (x, y). The value is a `JossAnnTransformer` with
            parameters that correspond to (x, y).

        Returns
        ----------
        edges : list of tuples
            A list containing tuples of length 2. All tuples will have either 0
            or 1 as the first element. The second element is the index of the
            corresponding probe (+2 to allow for including the Strategy and it's
            Dual).
        """
        edges = []
        for index, coord in enumerate(probe_dict.keys()):
            #  Add 2 to the index because we will have to allow for the Strategy
            #  and it's Dual
            if sum(coord) > 1:
                edge = (1, index + 2)
            else:
                edge = (0, index + 2)
            edges.append(edge)
        return edges

    def fingerprint(self, turns=50, repetitions=10, step=0.01, processes=None):
        """Build and play a spatial tournament.

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
        probe_coords = self.create_probe_coords(step)
        self.probe_players = self.create_probes(self.probe, probe_coords)
        self.edges = self.create_edges(self.probe_players)
        original = self.strategy()
        dual = DualTransformer()(self.strategy)()
        probes = self.probe_players.values()
        tourn_players = [original, dual] + list(probes)
        spatial_tourn = axl.SpatialTournament(tourn_players, turns=turns,
                                              repetitions=repetitions,
                                              edges=self.edges)
        print("Begin Spatial Tournament")
        self.results = spatial_tourn.play(processes=processes, build_results=False, in_memory=True,
                                          keep_interactions=True)
        print("Spatial Tournament Finished")

    def _generate_data(self, results, probe_coords):
        """Generates useful data from a spatial tournament.

        Matches interactions from `results` to their corresponding coordinate in
        `probe_coords`.

        Parameters
        ----------
        results : axelrod.result_set.ResultSetFromFile
            A results set for a spatial tournament.
        probe_coords : list of tuples
            A list of tuples of length 2, where each tuple represents a
            coordinate, eg. (x, y).

        Returns
        ----------
        data_frame : pandas.core.frame.DataFrame
            A pandas DataFrame object where the row and column headers
            correspond to coordinates. The cell values are the score of the
            original/dual strategy playing the probe with parameters that match
            the coordinate.
        """
        edge_scores = {key: cfspt(value[0])[0] for key, value in
                       results.interactions.items()}

        coord_scores = OrderedDict.fromkeys(probe_coords)
        for index, coord in enumerate(coord_scores.keys()):
            if sum(coord) > 1:
                edge = (1, index + 2)
            else:
                edge = (0, index + 2)
            coord_scores[coord] = edge_scores[edge]

        ser = pd.Series(list(coord_scores.values()),
                        index=pd.MultiIndex.from_tuples(coord_scores.keys()))
        data_frame = ser.unstack().fillna(0)
        data_frame.shape
        return data_frame

    def plot(self, col_map=None):
        """Plot the results of the spatial tournament.

        Parameters
        ----------
        col_map : str, optional
            A matplotlib colour map, full list can be found at
            http://matplotlib.org/examples/color/colormaps_reference.html
        """
        self.data = self._generate_data(self.results, self.probe_players.keys())
        sns.heatmap(self.data, cmap=col_map)
        plt.show()
