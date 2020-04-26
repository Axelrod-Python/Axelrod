"""Weighted undirected sparse graphs.

Original source:
https://github.com/marcharper/stationary/blob/master/stationary/utils/graph.py
"""

from collections import defaultdict


class Graph(object):
    """Weighted and directed graph class.
    
    This class is intended for the graph associated to a Markov process,
    since it gives easy access to the neighbors of a particular state.

    Vertices can be any hashable Python object.
    
    Initialize with a list of edges:
        [[node1, node2, weights], ...]
    Weights can be omitted for an undirected graph.

    For efficiency, neighbors are cached in dictionaries. Undirected
    graphs are implemented as directed graphs in which every edge (s, t)
    has the opposite edge (t, s).
    
    Attributes
    ----------
    directed: Boolean indicating whether the graph is directed
    original_edges: the edges passed into the initializer
    out_mapping: a dictionary mapping all heads to dictionaries that map
        all tails to their edge weights (None means no weight)
    in_mapping: a dictionary mapping all tails to dictionaries that map
        all heads to their edge weights (none means to weight)
    
    Properties
    ----------
    vertices: the set of vertices in the graph
    edges: the set of current edges in the graph
    """

    def __init__(self, edges=None, directed=False):
        self.directed = directed
        self.original_edges = edges
        self.out_mapping = defaultdict(lambda: defaultdict(float))
        self.in_mapping = defaultdict(lambda: defaultdict(float))
        self._edges = []
        if edges:
            self._add_edges(edges)

    def _add_edge(self, source, target, weight=None):
        if (source, target) not in self._edges:
            self._edges.append((source, target))
            self.out_mapping[source][target] = weight
            self.in_mapping[target][source] = weight
        if (
            not self.directed
            and (source != target)
            and (target, source) not in self._edges
        ):
            self._edges.append((target, source))
            self.out_mapping[target][source] = weight
            self.in_mapping[source][target] = weight

    def _add_edges(self, edges):
        for edge in edges:
            self._add_edge(*edge)

    def add_loops(self):
        """
        Add all loops to edges
        """
        self._add_edges((x, x) for x in self.vertices)

    @property
    def edges(self):
        return self._edges

    @property
    def vertices(self):
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

    def in_vertices(self, source):
        """Returns a list of the outgoing vertices."""
        return list(self.in_mapping[source].keys())

    def __repr__(self):
        s = "<Graph: {}>".format(repr(self.original_edges))
        return s


# Example graph factories.


def cycle(length, directed=False):
    """Produces a cycle of a specified length.

    Parameters
    ----------
    length: int
        Number of vertices in the cycle
    directed: bool, False
        Is the cycle directed?

    Returns
    -------
    a Graph object for the cycle
    """
    edges = [(i, i + 1) for i in range(length - 1)]
    edges.append((length - 1, 0))
    return Graph(edges=edges, directed=directed)


def complete_graph(size, loops=True, directed=False):
    """
    Produces a complete graph of size `length`.
    https://en.wikipedia.org/wiki/Complete_graph

    Parameters
    ----------
    size: int
        Number of vertices in the cycle
    loops: bool, True
        attach loops at each node?
    directed: bool, False
        Is the graph directed?

    Returns
    -------
    a Graph object for the complete graph
    """
    edges = [(i, j) for i in range(size) for j in range(i + 1, size)]
    graph = Graph(directed=directed, edges=edges)
    if loops:
        graph.add_loops()
    return graph


def attached_complete_graphs(length, loops=True, directed=False):
    """Creates two complete undirected graphs of size `length`
    attached by a single edge."""
    edges = []
    # Two complete graphs
    for cluster in range(2):
        for i in range(length):
            for j in range(i + 1, length):
                edges.append(("{}:{}".format(cluster, i),
                              "{}:{}".format(cluster, j)))
    # Attach at one node
    edges.append(("0:0", "1:0"))
    graph = Graph(directed=directed, edges=edges)
    if loops:
        graph.add_loops()

    return graph
