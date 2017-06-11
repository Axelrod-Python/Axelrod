"""
Weighted undirected sparse graphs.

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
        [[node1, node2, weights], ...]
    Weights can be omitted for an undirected graph.

    For efficiency, neighbors are cached in dictionaries. Undirected graphs
    are implemented as directed graphs in which every edge (s, t) has the
    opposite edge (t, s).
    """

    def __init__(self, edges=None, directed=False):
        self.directed = directed
        self.original_edges = edges
        self.out_mapping = defaultdict(lambda: defaultdict(float))
        self.in_mapping = defaultdict(lambda: defaultdict(float))
        self._edges = []
        if edges:
            self.add_edges(edges)

    def add_edge(self, source, target, weight=None):
        if (source, target) not in self._edges:
            self._edges.append((source, target))
            self.out_mapping[source][target] = weight
            self.in_mapping[target][source] = weight
        if not self.directed and (source != target) and \
                (target, source) not in self._edges:
            self._edges.append((target, source))
            self.out_mapping[target][source] = weight
            self.in_mapping[source][target] = weight

    def add_edges(self, edges):
        for edge in edges:
            self.add_edge(*edge)

    def add_loops(self):
        """
        Add all loops to edges
        """
        self.add_edges((i, i) for i, _ in enumerate(self.vertices()))

    def edges(self):
        return self._edges

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

    def in_vertices(self, source):
        """Returns a list of the outgoing vertices."""
        return list(self.in_mapping[source].keys())

    def __repr__(self):
        s = "<Graph: {}>".format(repr(self.original_edges))
        return s


# Example Graphs


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
        edges.append((i, i + 1))
    edges.append((length - 1, 0))
    graph.add_edges(edges)
    return graph


def complete_graph(length, loops=True):
    """
    Produces a complete graph of size `length`, with loops.
    https://en.wikipedia.org/wiki/Complete_graph

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
    graph = Graph(directed=False)
    edges = []
    for i in range(length):
        for j in range(i + 1, length):
            edges.append((i, j))
    graph.add_edges(edges)

    if loops:
        graph.add_loops()

    return graph
