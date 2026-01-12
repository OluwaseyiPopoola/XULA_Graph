import unittest

from Building import Building


class TestBuildingModule(unittest.TestCase):
    def test_add_and_find_adjacent(self):
        a = Building("A", 0.0, 0.0)
        b = Building("B", 1.0, 1.0)
        a.add_neigbhour(b)
        adj = a.find_adjacent_buildings()
        self.assertIn(b, adj)
        self.assertIsInstance(adj, set)

    def test_find_buildings_within_n_edges(self):
        a = Building("A", 0.0, 0.0)
        b = Building("B", 0.0, 1.0)
        c = Building("C", 0.0, 2.0)
        a.add_neigbhour(b)
        b.add_neigbhour(c)

        within_1 = a.find_buildings_within_n_edges(1)
        # should include A and B
        self.assertIn(a, within_1)
        self.assertIn(b, within_1)
        self.assertNotIn(c, within_1)

        within_2 = a.find_buildings_within_n_edges(2)
        self.assertIn(c, within_2)

    def test_repr_and_neighbor_set(self):
        a = Building("Admin", 10.0, 20.0)
        self.assertEqual(repr(a), "Admin")
        # neighbors should be a set and start empty
        self.assertIsInstance(a.neighbors, set)
        self.assertEqual(len(a.neighbors), 0)


if __name__ == "__main__":
    unittest.main()
