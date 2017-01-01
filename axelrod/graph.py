"""
Labeled and weighted graph class for Markov simulations. Not a full-featured
class, rather an appropriate organizational data structure for handling various
Markov process calculations, which are typically sparse.

Original source:
https://github.com/marcharper/stationary/blob/master/stationary/utils/graph.py

"""

from collections import defaultdict


class Graph(object):
    """Weighted and directed graph object intended for the graph associated to a
    Markov process. Gives easy access to the neighbors of a particular state
    needed for various calculations.

    Vertices can be any hashable / immutable python object. Initialize with a
    list of edges:
        [[node1, node2, transition_probability],
         [...]
         ...
        ]

    For efficiency, neighbors are cached in dictionaries.

    """

    def __init__(self, edges=None, directed=False):
        self.out_mapping = defaultdict(lambda: defaultdict(float))
        self.in_mapping = defaultdict(lambda: defaultdict(float))
        self.directed = directed
        if edges:
            self.add_edges(edges)

    def add_vertex(self, label):
        self._vertices.add(label)

    def add_edge(self, source, target, weight=1.):
        self.out_mapping[source][target] = weight
        self.in_mapping[target][source] = weight
        if not self.directed:
            self.out_mapping[target][source] = weight
            self.in_mapping[source][target] = weight

    def add_edges(self, edges):
        try:
            for source, target, weight in edges:
                self.add_edge(source, target, weight)
        except ValueError:
            for source, target in edges:
                self.add_edge(source, target, 1.0)

    def vertices(self):
        """Returns the set of vertices of the graph."""
        return list(self.out_mapping.keys())

    def out_dict(self, source):
        """Returns a dictionary of the outgoing edges of source with weights."""
        return self.out_mapping[source]

    def out_vertices(self, source):
        """Returns a list of the outgoing vertices."""
        return list(self.out_mapping[source].keys())

    def in_dict(self, target):
        """Returns a dictionary of the incoming edges of source with weights."""
        return self.in_mapping[target]

    def normalize_weights(self):
        """Normalizes the weights coming out of each vertex to be probability
        distributions."""
        new_edges = []
        for source in self.out_mapping.keys():
            total = float(sum(out_mapping[source].values()))
            for target, weight in self.out_mapping.items():
                self.out_mapping[target] = weight / total
        self._edges = new_edges

    def __getitem__(self, k):
        """Returns the dictionary of outgoing edges. You can access the weight
        of an edge with g[source][target]."""
        return self.out_mapping[k]


## Example Graphs


def cycle(length, directed=False):
    """
    Produces a cycle of length `length`.
    Parameters
    ----------
    length: int
        Number of vertices in the cycle
    directed: bool, False
        Is the cycle directed?
    Returns
    -------
    a Graph object
    """

    graph = Graph(directed=directed)
    edges = []
    for i in range(length - 1):
        edges.append((i, i+1))
    edges.append((length - 1, 0))
    graph.add_edges(edges)
    return graph


def complete_graph(length, directed=False):
    """
    Produces a complete graph of size `length`.
    Parameters
    ----------
    length: int
        Number of vertices in the cycle
    directed: bool, False
        Is the graph directed?
    Returns
    -------
    a Graph object
    """
    graph = Graph(directed=directed)
    edges = []
    for i in range(length):
        for j in range(length):
            edges.append((i, j))
    graph.add_edges(edges)
    return graph

