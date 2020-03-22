from collections import defaultdict
import unittest

from axelrod import graph


class TestGraph(unittest.TestCase):
    def assert_out_mapping(self, g, expected_out_mapping):
        self.assertDictEqual(g.out_mapping, expected_out_mapping)
        for node, out_dict in expected_out_mapping.items():
            self.assertListEqual(g.out_vertices(node), list(out_dict.keys()))
            self.assertDictEqual(g.out_dict(node), out_dict)

    def assert_in_mapping(self, g, expected_in_mapping):
        self.assertDictEqual(g.in_mapping, expected_in_mapping)
        for node, in_dict in expected_in_mapping.items():
            self.assertListEqual(g.in_vertices(node), list(in_dict.keys()))
            self.assertDictEqual(g.in_dict(node), in_dict)

    def test_undirected_graph_with_no_vertices(self):
        g = graph.Graph()
        self.assertFalse(g.directed)
        self.assertIsInstance(g.out_mapping, defaultdict)
        self.assertIsInstance(g.in_mapping, defaultdict)
        self.assertEqual(g._edges, [])
        self.assertEqual(str(g), "<Graph: None>")

    def test_directed_graph_with_no_vertices(self):
        g = graph.Graph(directed=True)
        self.assertTrue(g.directed)
        self.assertIsInstance(g.out_mapping, defaultdict)
        self.assertIsInstance(g.in_mapping, defaultdict)
        self.assertEqual(g._edges, [])
        self.assertEqual(str(g), "<Graph: None>")

    def test_undirected_graph_with_vertices_and_unweighted_edges(self):
        g = graph.Graph(edges=[[1, 2], [2, 3]])
        self.assertFalse(g.directed)
        self.assertEqual(str(g), "<Graph: [[1, 2], [2, 3]]>")

        self.assertEqual(g._edges, [(1, 2), (2, 1), (2, 3), (3, 2)])
        self.assert_out_mapping(g, {1: {2: None}, 2: {1: None, 3: None}, 3: {2: None}})
        self.assert_in_mapping(g, {1: {2: None}, 2: {1: None, 3: None}, 3: {2: None}})

    def test_undirected_graph_with_vertices_and_weighted_edges(self):
        g = graph.Graph(edges=[[1, 2, 10], [2, 3, 5]])
        self.assertFalse(g.directed)
        self.assertEqual(str(g), "<Graph: [[1, 2, 10], [2, 3, 5]]>")

        self.assertEqual(g._edges, [(1, 2), (2, 1), (2, 3), (3, 2)])
        self.assert_out_mapping(g, {1: {2: 10}, 2: {1: 10, 3: 5}, 3: {2: 5}})
        self.assert_in_mapping(g, {1: {2: 10}, 2: {1: 10, 3: 5}, 3: {2: 5}})

    def test_directed_graph_vertices_and_weighted_edges(self):
        g = graph.Graph(edges=[[1, 2, 10], [2, 3, 5]], directed=True)
        self.assertTrue(g.directed)
        self.assertEqual(str(g), "<Graph: [[1, 2, 10], [2, 3, 5]]>")

        self.assertEqual(g._edges, [(1, 2), (2, 3)])
        self.assert_out_mapping(g, {1: {2: 10}, 2: {3: 5}})
        self.assert_in_mapping(g, {2: {1: 10}, 3: {2: 5}})

    def test_add_loops(self):
        edges = [(0, 1), (0, 2), (1, 2)]
        g = graph.Graph(edges)
        g.add_loops()
        self.assertEqual(
            list(sorted(g._edges)),
            list(
                sorted(
                    [
                        (0, 1),
                        (1, 0),
                        (0, 2),
                        (2, 0),
                        (1, 2),
                        (2, 1),
                        (0, 0),
                        (1, 1),
                        (2, 2),
                    ]
                )
            ),
        )

    def test_add_loops_with_existing_loop_and_using_strings(self):
        """In this case there is already a loop present; also uses
        strings instead of integers as the hashable."""
        edges = [("a", "b"), ("b", "a"), ("c", "c")]
        g = graph.Graph(edges)
        g.add_loops()
        self.assertEqual(
            list(sorted(g._edges)),
            list(sorted([("a", "b"), ("b", "a"), ("c", "c"), ("a", "a"), ("b", "b")])),
        )


class TestCycle(unittest.TestCase):
    def test_length_1_directed(self):
        g = graph.cycle(1, directed=True)
        self.assertEqual(g.vertices, [0])
        self.assertEqual(g.edges, [(0, 0)])
        self.assertEqual(g.directed, True)

    def test_length_1_undirected(self):
        g = graph.cycle(1, directed=False)
        self.assertEqual(g.vertices, [0])
        self.assertEqual(g.edges, [(0, 0)])
        self.assertEqual(g.directed, False)

    def test_length_2_directed(self):
        g = graph.cycle(2, directed=True)
        self.assertEqual(g.vertices, [0, 1])
        self.assertEqual(g.edges, [(0, 1), (1, 0)])

    def test_length_2_undirected(self):
        g = graph.cycle(2, directed=False)
        self.assertEqual(g.vertices, [0, 1])
        self.assertEqual(g.edges, [(0, 1), (1, 0)])

    def test_length_3_directed(self):
        g = graph.cycle(3, directed=True)
        self.assertEqual(g.vertices, [0, 1, 2])
        self.assertEqual(g.edges, [(0, 1), (1, 2), (2, 0)])

    def test_length_3_undirected(self):
        g = graph.cycle(3, directed=False)
        edges = [(0, 1), (1, 0), (1, 2), (2, 1), (2, 0), (0, 2)]
        self.assertEqual(g.vertices, [0, 1, 2])
        self.assertEqual(g.edges, edges)

    def test_length_4_directed(self):
        g = graph.cycle(4, directed=True)
        self.assertEqual(g.vertices, [0, 1, 2, 3])
        self.assertEqual(g.edges, [(0, 1), (1, 2), (2, 3), (3, 0)])
        self.assertEqual(g.out_vertices(0), [1])
        self.assertEqual(g.out_vertices(1), [2])
        self.assertEqual(g.out_vertices(2), [3])
        self.assertEqual(g.out_vertices(3), [0])
        self.assertEqual(g.in_vertices(0), [3])
        self.assertEqual(g.in_vertices(1), [0])
        self.assertEqual(g.in_vertices(2), [1])
        self.assertEqual(g.in_vertices(3), [2])

    def test_length_4_undirected(self):
        g = graph.cycle(4, directed=False)
        edges = [(0, 1), (1, 0), (1, 2), (2, 1), (2, 3), (3, 2), (3, 0), (0, 3)]
        self.assertEqual(g.vertices, [0, 1, 2, 3])
        self.assertEqual(g.edges, edges)
        for vertex, neighbors in [(0, (1, 3)), (1, (0, 2)), (2, (1, 3)), (3, (0, 2))]:
            self.assertEqual(set(g.out_vertices(vertex)), set(neighbors))
        for vertex, neighbors in [(0, (1, 3)), (1, (0, 2)), (2, (1, 3)), (3, (0, 2))]:
            self.assertEqual(set(g.in_vertices(vertex)), set(neighbors))


class TestComplete(unittest.TestCase):
    def test_size_2(self):
        g = graph.complete_graph(2, loops=False)
        self.assertEqual(g.vertices, [0, 1])
        self.assertEqual(g.edges, [(0, 1), (1, 0)])
        self.assertEqual(g.directed, False)

    def test_size_3(self):
        g = graph.complete_graph(3, loops=False)
        self.assertEqual(g.vertices, [0, 1, 2])
        edges = [(0, 1), (1, 0), (0, 2), (2, 0), (1, 2), (2, 1)]
        self.assertEqual(g.edges, edges)
        self.assertEqual(g.directed, False)

    def test_size_4(self):
        g = graph.complete_graph(4, loops=False)
        self.assertEqual(g.vertices, [0, 1, 2, 3])
        edges = [
            (0, 1),
            (1, 0),
            (0, 2),
            (2, 0),
            (0, 3),
            (3, 0),
            (1, 2),
            (2, 1),
            (1, 3),
            (3, 1),
            (2, 3),
            (3, 2),
        ]
        self.assertEqual(g.edges, edges)
        self.assertEqual(g.directed, False)
        for vertex, neighbors in [
            (0, (1, 2, 3)),
            (1, (0, 2, 3)),
            (2, (0, 1, 3)),
            (3, (0, 1, 2)),
        ]:
            self.assertEqual(set(g.out_vertices(vertex)), set(neighbors))
        for vertex, neighbors in [
            (0, (1, 2, 3)),
            (1, (0, 2, 3)),
            (2, (0, 1, 3)),
            (3, (0, 1, 2)),
        ]:
            self.assertEqual(set(g.in_vertices(vertex)), set(neighbors))

    def test_size_2_with_loops(self):
        g = graph.complete_graph(2, loops=True)
        self.assertEqual(g.vertices, [0, 1])
        self.assertEqual(g.edges, [(0, 1), (1, 0), (0, 0), (1, 1)])
        self.assertEqual(g.directed, False)

    def test_size_3_with_loops(self):
        g = graph.complete_graph(3, loops=True)
        self.assertEqual(g.vertices, [0, 1, 2])
        edges = [(0, 1), (1, 0), (0, 2), (2, 0), (1, 2), (2, 1), (0, 0), (1, 1), (2, 2)]
        self.assertEqual(g.edges, edges)
        self.assertEqual(g.directed, False)

    def test_size_4_with_loops(self):
        g = graph.complete_graph(4, loops=True)
        self.assertEqual(g.vertices, [0, 1, 2, 3])
        edges = [
            (0, 1),
            (1, 0),
            (0, 2),
            (2, 0),
            (0, 3),
            (3, 0),
            (1, 2),
            (2, 1),
            (1, 3),
            (3, 1),
            (2, 3),
            (3, 2),
            (0, 0),
            (1, 1),
            (2, 2),
            (3, 3),
        ]
        self.assertEqual(g.edges, edges)
        self.assertEqual(g.directed, False)
        neighbors = range(4)
        for vertex in range(4):
            self.assertEqual(set(g.out_vertices(vertex)), set(neighbors))
            self.assertEqual(set(g.in_vertices(vertex)), set(neighbors))


class TestAttachedComplete(unittest.TestCase):
    def test_size_2(self):
        g = graph.attached_complete_graphs(2, loops=False)
        self.assertEqual(g.vertices, ['0:0', '0:1', '1:0', '1:1'])
        self.assertEqual(
            g.edges,
            [('0:0', '0:1'), ('0:1', '0:0'), ('1:0', '1:1'), ('1:1', '1:0'), ('0:0', '1:0'), ('1:0', '0:0')]
        )
        self.assertEqual(g.directed, False)

    def test_size_3(self):
        g = graph.attached_complete_graphs(3, loops=False)
        self.assertEqual(g.vertices, ['0:0', '0:1', '0:2', '1:0', '1:1', '1:2'])
        self.assertEqual(
            g.edges,
            [('0:0', '0:1'),
             ('0:1', '0:0'),
             ('0:0', '0:2'),
             ('0:2', '0:0'),
             ('0:1', '0:2'),
             ('0:2', '0:1'),
             ('1:0', '1:1'),
             ('1:1', '1:0'),
             ('1:0', '1:2'),
             ('1:2', '1:0'),
             ('1:1', '1:2'),
             ('1:2', '1:1'),
             ('0:0', '1:0'),
             ('1:0', '0:0')]
        )
        self.assertEqual(g.directed, False)

    def test_size_3_with_loops(self):
        g = graph.attached_complete_graphs(3, loops=True)
        self.assertEqual(g.vertices, ['0:0', '0:1', '0:2', '1:0', '1:1', '1:2'])
        self.assertEqual(
            g.edges,
            [('0:0', '0:1'),
             ('0:1', '0:0'),
             ('0:0', '0:2'),
             ('0:2', '0:0'),
             ('0:1', '0:2'),
             ('0:2', '0:1'),
             ('1:0', '1:1'),
             ('1:1', '1:0'),
             ('1:0', '1:2'),
             ('1:2', '1:0'),
             ('1:1', '1:2'),
             ('1:2', '1:1'),
             ('0:0', '1:0'),
             ('1:0', '0:0'),
             ('0:0', '0:0'),
             ('0:1', '0:1'),
             ('0:2', '0:2'),
             ('1:0', '1:0'),
             ('1:1', '1:1'),
             ('1:2', '1:2')]
        )
        self.assertEqual(g.directed, False)
