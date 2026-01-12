import unittest

from GraphManager import GraphManager
from Building import Building


class TestBuildingsModule(unittest.TestCase):
    def test_create_buildings_returns_manager(self):
        gm = GraphManager.create_buildings()
        self.assertIsInstance(gm, GraphManager)
        self.assertGreaterEqual(len(gm.all_locations), 3)

    def test_connect_all_buildings_and_adjacency(self):
        gm = GraphManager.create_buildings()
        gm.connect_all_buildings()
        # each building should have two neighbors as a set
        for b in gm.all_locations:
            self.assertEqual(len(b.neighbors), 2)

        ady = gm.build_adjacency_list()
        self.assertIsInstance(ady, dict)
        # each key should be a Building and value a set
        for k, v in ady.items():
            self.assertIsInstance(k, Building)
            self.assertIsInstance(v, set)
            # neighbor tuples should be (Building, float)
            for nb, w in v:
                self.assertIsInstance(nb, Building)
                self.assertIsInstance(w, float)

    def test_connect_random_and_complete(self):
        gm = GraphManager.create_buildings()
        initial_counts = [len(b.neighbors) for b in gm.all_locations]
        gm.connect_random_buildings(3)
        after_counts = [len(b.neighbors) for b in gm.all_locations]
        self.assertNotEqual(initial_counts, after_counts)

        # test complete graph creates connections between all nodes
        gm2 = GraphManager.create_buildings()
        gm2.connect_complete_graph()
        n = len(gm2.all_locations)
        # in complete undirected graph each node neighbors should be n-1
        for b in gm2.all_locations:
            self.assertEqual(len(b.neighbors), n-1)

    def test_dijkstra_and_shortest_helpers(self):
        # build a tiny graph and test dijkstra
        a = Building("A", 0.0, 0.0)
        b = Building("B", 0.0, 1.0)
        c = Building("C", 0.0, 2.0)
        gm = GraphManager([a, b, c])
        a.add_neigbhour(b)
        b.add_neigbhour(c)
        gm.adjacency_list = gm.build_adjacency_list()

        dist, path = gm.dijkstra(a, c)
        self.assertIsInstance(dist, float)
        self.assertIsInstance(path, str)
        self.assertIn("A", path)
        self.assertIn("C", path)

        dstr = gm.shortest_distance_btw_two_buildings(a, c)
        pstr = gm.shortest_path_btw_two_buildings(a, c)
        self.assertIsInstance(dstr, str)
        self.assertIn("km", dstr)
        self.assertIsInstance(pstr, str)


if __name__ == "__main__":
    unittest.main()
