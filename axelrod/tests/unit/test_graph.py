import unittest

from axelrod import graph


class TestGraph(unittest.TestCase):

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
        self.assertEqual(g.edges(), [(0, 0), (0, 1), (1, 0), (1, 1)])
        self.assertEqual(g.directed, False)
        g = graph.complete_graph(3, loops=True)
        self.assertEqual(g.vertices(), [0, 1, 2])
        edges = [(0, 0), (0, 1), (1, 0), (0, 2), (2, 0), (1, 1),
                 (1, 2), (2, 1), (2, 2)]
        self.assertEqual(g.edges(), edges)
        self.assertEqual(g.directed, False)
        g = graph.complete_graph(4, loops=True)
        self.assertEqual(g.vertices(), [0, 1, 2, 3])
        edges = [(0, 0), (0, 1), (1, 0), (0, 2), (2, 0), (0, 3), (3, 0),
                  (1, 1), (1, 2), (2, 1), (1, 3), (3, 1),
                  (2, 2), (2, 3), (3, 2), (3, 3)]
        self.assertEqual(g.edges(), edges)
        self.assertEqual(g.directed, False)
        neighbors = range(4)
        for vertex in range(4):
            self.assertEqual(set(g.out_vertices(vertex)), set(neighbors))
            self.assertEqual(set(g.in_vertices(vertex)), set(neighbors))
