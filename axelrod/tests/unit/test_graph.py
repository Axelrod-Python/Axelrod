import unittest
from collections import defaultdict

from axelrod import graph


class TestGraph(unittest.TestCase):

    def test_init(self):
        # Undirected graph with no vertices
        g = graph.Graph()
        self.assertFalse(g.directed)
        self.assertIsInstance(g.out_mapping, defaultdict)
        self.assertIsInstance(g.in_mapping, defaultdict)
        self.assertEqual(g._edges, [])

        # Directed graph with no vertices
        g = graph.Graph(directed=True)
        self.assertTrue(g.directed)
        self.assertIsInstance(g.out_mapping, defaultdict)
        self.assertIsInstance(g.in_mapping, defaultdict)
        self.assertEqual(g._edges, [])

        # Undirected graph with vertices and unweighted edges
        g = graph.Graph(edges=[[1, 2], [2, 3]])
        expected_edges = [(1, 2), (2, 1), (2, 3), (3, 2)]
        expected_out_mapping = {
            1: {2: None},
            2: {1: None, 3: None},
            3: {2: None}
        }
        expected_in_mapping = {
            1: {2: None},
            2: {1: None, 3: None},
            3: {2: None}
        }

        self.assertFalse(g.directed)
        self.assertEqual(len(g.out_mapping), len(expected_out_mapping))
        for node in expected_out_mapping:
            self.assertEqual(g.out_mapping[node], expected_out_mapping[node])
        self.assertEqual(len(g.in_mapping), len(expected_in_mapping))
        for node in expected_in_mapping:
            self.assertEqual(g.in_mapping[node], expected_in_mapping[node])
        self.assertEqual(g._edges, expected_edges)

        # Undirected graph with vertices and weighted edges
        g = graph.Graph(edges=[[1, 2, 10], [2, 3, 5]])
        expected_edges = [(1, 2), (2, 1), (2, 3), (3, 2)]
        expected_out_mapping = {
            1: {2: 10},
            2: {1: 10, 3: 5},
            3: {2: 5}
        }
        expected_in_mapping = {
            1: {2: 10},
            2: {1: 10, 3: 5},
            3: {2: 5}
        }
        self.assertFalse(g.directed)
        self.assertEqual(len(g.out_mapping), len(expected_out_mapping))
        for node in expected_out_mapping:
            self.assertEqual(g.out_mapping[node], expected_out_mapping[node])
        self.assertEqual(len(g.in_mapping), len(expected_in_mapping))
        for node in expected_in_mapping:
            self.assertEqual(g.in_mapping[node], expected_in_mapping[node])
        self.assertEqual(g._edges, expected_edges)

        # Directed graph with vertices and weighted edges
        g = graph.Graph(edges=[[1, 2, 10], [2, 3, 5]], directed=True)
        expected_edges = [(1, 2), (2, 3)]
        expected_out_mapping = {
            1: {2: 10},
            2: {3: 5},
        }
        expected_in_mapping = {
            2: {1: 10},
            3: {2: 5}
        }
        self.assertTrue(g.directed)
        self.assertEqual(len(g.out_mapping), len(expected_out_mapping))
        for node in expected_out_mapping:
            self.assertEqual(g.out_mapping[node], expected_out_mapping[node])
        self.assertEqual(len(g.in_mapping), len(expected_in_mapping))
        for node in expected_in_mapping:
            self.assertEqual(g.in_mapping[node], expected_in_mapping[node])
        self.assertEqual(g._edges, expected_edges)

    def test_add_loops(self):
        edges = [(0, 1), (0, 2), (1, 2)]
        g = graph.Graph(edges)
        g.add_loops()
        self.assertEqual(
            list(sorted(g._edges)),
            list(sorted([(0, 1), (1, 0), (0, 2), (2, 0), (1, 2),
                         (2, 1), (0, 0), (1, 1), (2, 2)]))
        )

    def test_add_loops2(self):
        """In this case there is already a loop present; also uses
        strings instead of integers as the hashable."""
        edges = [('a', 'b'), ('b', 'a'), ('c', 'c')]
        g = graph.Graph(edges)
        g.add_loops()
        self.assertEqual(
            list(sorted(g._edges)),
            list(sorted(
                [('a', 'b'), ('b', 'a'), ('c', 'c'), ('a', 'a'), ('b', 'b')]))
        )

    def test_out_dict(self):
        # Undirected graph with vertices and unweighted edges
        g = graph.Graph(edges=[[1, 2], [2, 3]])
        expected_out_mapping = {
            1: {2: None},
            2: {1: None, 3: None},
            3: {2: None}
        }
        for key in expected_out_mapping:
            self.assertEqual(g.out_dict(key), expected_out_mapping[key])

        # Undirected graph with vertices and weighted edges
        g = graph.Graph(edges=[[1, 2, 10], [2, 3, 5]])
        expected_out_mapping = {
            1: {2: 10},
            2: {1: 10, 3: 5},
            3: {2: 5}
        }
        for key in expected_out_mapping:
            self.assertEqual(g.out_dict(key), expected_out_mapping[key])

        # Directed graph with vertices and weighted edges
        g = graph.Graph(edges=[[1, 2, 10], [2, 3, 5]], directed=True)
        expected_out_mapping = {
            1: {2: 10},
            2: {3: 5},
        }
        for key in expected_out_mapping:
            self.assertEqual(g.out_dict(key), expected_out_mapping[key])

    def test_in_dict(self):
        # Undirected graph with vertices and unweighted edges
        g = graph.Graph(edges=[[1, 2], [2, 3]])
        expected_in_mapping = {
            1: {2: None},
            2: {1: None, 3: None},
            3: {2: None}
        }
        for key in expected_in_mapping:
            self.assertEqual(g.in_dict(key), expected_in_mapping[key])

        # Undirected graph with vertices and weighted edges
        g = graph.Graph(edges=[[1, 2, 10], [2, 3, 5]])
        expected_in_mapping = {
            1: {2: 10},
            2: {1: 10, 3: 5},
            3: {2: 5}
        }
        for key in expected_in_mapping:
            self.assertEqual(g.in_dict(key), expected_in_mapping[key])

        # Directed graph with vertices and weighted edges
        g = graph.Graph(edges=[[1, 2, 10], [2, 3, 5]], directed=True)
        expected_in_mapping = {
            2: {1: 10},
            3: {2: 5}
        }
        for key in expected_in_mapping:
            self.assertEqual(g.in_dict(key), expected_in_mapping[key])

    def test_repr(self):
        # Undirected graph with no vertices
        g = graph.Graph()
        self.assertEqual(str(g), '<Graph: None>')

        # Directed graph with no vertices
        g = graph.Graph(directed=True)
        self.assertEqual(str(g), '<Graph: None>')

        # Undirected graph with vertices and unweighted edges
        g = graph.Graph(edges=[[1, 2], [2, 3]])
        self.assertEqual(str(g), '<Graph: [[1, 2], [2, 3]]>')

        # Undirected graph with vertices and weighted edges
        g = graph.Graph(edges=[[1, 2, 10], [2, 3, 5]])
        self.assertEqual(str(g), '<Graph: [[1, 2, 10], [2, 3, 5]]>')

        # Directed graph with vertices and weighted edges
        g = graph.Graph(edges=[[1, 2, 10], [2, 3, 5]], directed=True)
        self.assertEqual(str(g), '<Graph: [[1, 2, 10], [2, 3, 5]]>')

    def test_cycle(self):
        g = graph.cycle(1, directed=False)
        self.assertEqual(g.vertices(), [0])
        self.assertEqual(g.edges(), [(0, 0)])
        self.assertEqual(g.directed, False)
        g = graph.cycle(1, directed=True)
        self.assertEqual(g.vertices(), [0])
        self.assertEqual(g.edges(), [(0, 0)])
        self.assertEqual(g.directed, True)
        g = graph.cycle(2, directed=True)
        self.assertEqual(g.vertices(), [0, 1])
        self.assertEqual(g.edges(), [(0, 1), (1, 0)])
        g = graph.cycle(2, directed=False)
        self.assertEqual(g.vertices(), [0, 1])
        self.assertEqual(g.edges(), [(0, 1), (1, 0)])
        g = graph.cycle(3, directed=True)
        self.assertEqual(g.vertices(), [0, 1, 2])
        self.assertEqual(g.edges(), [(0, 1), (1, 2), (2, 0)])
        g = graph.cycle(3, directed=False)
        edges = [(0, 1), (1, 0), (1, 2), (2, 1), (2, 0), (0, 2)]
        self.assertEqual(g.vertices(), [0, 1, 2])
        self.assertEqual(g.edges(), edges)
        g = graph.cycle(4, directed=True)
        self.assertEqual(g.vertices(), [0, 1, 2, 3])
        self.assertEqual(g.edges(), [(0, 1), (1, 2), (2, 3), (3, 0)])
        self.assertEqual(g.out_vertices(0), [1])
        self.assertEqual(g.out_vertices(1), [2])
        self.assertEqual(g.out_vertices(2), [3])
        self.assertEqual(g.out_vertices(3), [0])
        self.assertEqual(g.in_vertices(0), [3])
        self.assertEqual(g.in_vertices(1), [0])
        self.assertEqual(g.in_vertices(2), [1])
        self.assertEqual(g.in_vertices(3), [2])
        g = graph.cycle(4, directed=False)
        edges = [(0, 1), (1, 0), (1, 2), (2, 1),
                 (2, 3), (3, 2), (3, 0), (0, 3)]
        self.assertEqual(g.vertices(), [0, 1, 2, 3])
        self.assertEqual(g.edges(), edges)
        for vertex, neighbors in [
            (0, (1, 3)), (1, (0, 2)), (2, (1, 3)), (3, (0, 2))]:
            self.assertEqual(set(g.out_vertices(vertex)), set(neighbors))
        for vertex, neighbors in [
            (0, (1, 3)), (1, (0, 2)), (2, (1, 3)), (3, (0, 2))]:
            self.assertEqual(set(g.in_vertices(vertex)), set(neighbors))

    def test_complete(self):
        g = graph.complete_graph(2, loops=False)
        self.assertEqual(g.vertices(), [0, 1])
        self.assertEqual(g.edges(), [(0, 1), (1, 0)])
        self.assertEqual(g.directed, False)

        g = graph.complete_graph(3, loops=False)
        self.assertEqual(g.vertices(), [0, 1, 2])
        edges = [(0, 1), (1, 0), (0, 2), (2, 0), (1, 2), (2, 1)]
        self.assertEqual(g.edges(), edges)
        self.assertEqual(g.directed, False)

        g = graph.complete_graph(4, loops=False )
        self.assertEqual(g.vertices(), [0, 1, 2, 3])
        edges = [(0, 1), (1, 0), (0, 2), (2, 0), (0, 3), (3, 0),
                 (1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (3, 2)]
        self.assertEqual(g.edges(), edges)
        self.assertEqual(g.directed, False)
        for vertex, neighbors in [
            (0, (1, 2, 3)), (1, (0, 2, 3)), (2, (0, 1, 3)), (3, (0, 1, 2))]:
            self.assertEqual(set(g.out_vertices(vertex)), set(neighbors))
        for vertex, neighbors in [
            (0, (1, 2, 3)), (1, (0, 2, 3)), (2, (0, 1, 3)), (3, (0, 1, 2))]:
            self.assertEqual(set(g.in_vertices(vertex)), set(neighbors))

    def test_complete_with_loops(self):
        g = graph.complete_graph(2, loops=True)
        self.assertEqual(g.vertices(), [0, 1])
        self.assertEqual(g.edges(), [(0, 1), (1, 0), (0, 0), (1, 1)])
        self.assertEqual(g.directed, False)
        g = graph.complete_graph(3, loops=True)
        self.assertEqual(g.vertices(), [0, 1, 2])
        edges = [(0, 1), (1, 0), (0, 2), (2, 0),
                 (1, 2), (2, 1), (0, 0), (1, 1), (2, 2)]
        self.assertEqual(g.edges(), edges)
        self.assertEqual(g.directed, False)
        g = graph.complete_graph(4, loops=True)
        self.assertEqual(g.vertices(), [0, 1, 2, 3])
        edges = [(0, 1), (1, 0), (0, 2), (2, 0), (0, 3), (3, 0), (1, 2), (2, 1),
                 (1, 3), (3, 1), (2, 3), (3, 2), (0, 0), (1, 1), (2, 2), (3, 3)]
        self.assertEqual(g.edges(), edges)
        self.assertEqual(g.directed, False)
        neighbors = range(4)
        for vertex in range(4):
            self.assertEqual(set(g.out_vertices(vertex)), set(neighbors))
            self.assertEqual(set(g.in_vertices(vertex)), set(neighbors))
