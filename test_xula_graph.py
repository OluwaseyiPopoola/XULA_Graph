import unittest
from xula_graph import (
    Building,
    create_buildings,
    connect_building,
    connect_all_buildings,
    connect_complete_graph,
    connect_random_buildings,
    find_adjacent_buildings,
    find_buildings_within_two_edges,
    build_adjacency_list,
    find_euclidean_distance,
    haversine_distance_function,
    dijkstra,
    shortest_distance_btw_two_buildings,
    shortest_path_btw_two_buildings
)


class TestBuilding(unittest.TestCase):
    """Test cases for the Building class"""
    
    def test_building_initialization(self):
        """Test that a Building is initialized correctly"""
        building = Building("Admin", 29.964440, -90.106995)
        self.assertEqual(building.name, "Admin")
        self.assertEqual(building.coords, (29.964440, -90.106995))
        self.assertEqual(building.neighbors, [])
    
    def test_building_repr(self):
        """Test the string representation of a Building"""
        building = Building("Chapel", 29.965934, -90.106465)
        self.assertEqual(repr(building), "Chapel")
    
    def test_building_coords_tuple(self):
        """Test that coordinates are stored as a tuple"""
        building = Building("Library", 29.965995, -90.107162)
        self.assertIsInstance(building.coords, tuple)
        self.assertEqual(len(building.coords), 2)


class TestCreateBuildings(unittest.TestCase):
    """Test cases for create_buildings function"""
    
    def test_create_buildings_count(self):
        """Test that create_buildings returns the correct number of buildings"""
        buildings = create_buildings()
        self.assertEqual(len(buildings), 13)
    
    def test_create_buildings_types(self):
        """Test that all created buildings are Building instances"""
        buildings = create_buildings()
        for building in buildings:
            self.assertIsInstance(building, Building)
    
    def test_create_buildings_names(self):
        """Test that buildings have the expected names"""
        buildings = create_buildings()
        expected_names = ["Admin", "Chapel", "Library", "U_Center", "Pharmacy", 
                         "St_Joseph", "St_Michael", "Xavier_S", "Convo_Ctr", "DP",
                         "New_Orleans", "Abuja", "Harare"]
        actual_names = [b.name for b in buildings]
        self.assertEqual(actual_names, expected_names)
    
    def test_create_buildings_initial_neighbors(self):
        """Test that newly created buildings have no neighbors"""
        buildings = create_buildings()
        for building in buildings:
            self.assertEqual(len(building.neighbors), 0)


class TestConnectBuilding(unittest.TestCase):
    """Test cases for connect_building function"""
    
    def setUp(self):
        """Set up test buildings"""
        self.building1 = Building("Building1", 0.0, 0.0)
        self.building2 = Building("Building2", 1.0, 1.0)
    
    def test_connect_single_building(self):
        """Test connecting two buildings"""
        connect_building(self.building1, self.building2)
        self.assertIn(self.building2, self.building1.neighbors)
        self.assertEqual(len(self.building1.neighbors), 1)
    
    def test_connect_multiple_buildings(self):
        """Test connecting a building to multiple neighbors"""
        building3 = Building("Building3", 2.0, 2.0)
        connect_building(self.building1, self.building2)
        connect_building(self.building1, building3)
        self.assertEqual(len(self.building1.neighbors), 2)
        self.assertIn(self.building2, self.building1.neighbors)
        self.assertIn(building3, self.building1.neighbors)
    
    def test_connect_is_directional(self):
        """Test that connection is directional (one-way)"""
        connect_building(self.building1, self.building2)
        self.assertIn(self.building2, self.building1.neighbors)
        self.assertNotIn(self.building1, self.building2.neighbors)


class TestConnectAllBuildings(unittest.TestCase):
    """Test cases for connect_all_buildings function"""
    
    def test_connect_all_buildings_neighbor_count(self):
        """Test that each building is connected to exactly 2 neighbors"""
        buildings = create_buildings()
        connect_all_buildings(buildings)
        for building in buildings:
            self.assertEqual(len(building.neighbors), 2)
    
    def test_connect_all_buildings_circular(self):
        """Test that connections wrap around circularly"""
        buildings = create_buildings()
        connect_all_buildings(buildings)
        # Last building should be connected to first and second buildings
        last_building = buildings[-1]
        self.assertIn(buildings[0], last_building.neighbors)
        self.assertIn(buildings[1], last_building.neighbors)


class TestConnectCompleteGraph(unittest.TestCase):
    """Test cases for connect_complete_graph function"""
    
    def test_complete_graph_small(self):
        """Test complete graph with a small set of buildings"""
        buildings = [
            Building("A", 0.0, 0.0),
            Building("B", 1.0, 1.0),
            Building("C", 2.0, 2.0)
        ]
        connect_complete_graph(buildings)
        # In a complete graph with 3 nodes, each node has 2 neighbors
        for building in buildings:
            self.assertEqual(len(building.neighbors), 2)
    
    def test_complete_graph_connections(self):
        """Test that complete graph creates all possible connections"""
        buildings = [
            Building("A", 0.0, 0.0),
            Building("B", 1.0, 1.0),
            Building("C", 2.0, 2.0)
        ]
        connect_complete_graph(buildings)
        # A should be connected to B and C
        self.assertIn(buildings[1], buildings[0].neighbors)
        self.assertIn(buildings[2], buildings[0].neighbors)


class TestFindAdjacentBuildings(unittest.TestCase):
    """Test cases for find_adjacent_buildings function"""
    
    def test_find_adjacent_buildings_empty(self):
        """Test finding adjacent buildings when there are none"""
        building = Building("Isolated", 0.0, 0.0)
        adjacent = find_adjacent_buildings(building)
        self.assertEqual(len(adjacent), 0)
    
    def test_find_adjacent_buildings_single(self):
        """Test finding a single adjacent building"""
        building1 = Building("Building1", 0.0, 0.0)
        building2 = Building("Building2", 1.0, 1.0)
        connect_building(building1, building2)
        adjacent = find_adjacent_buildings(building1)
        self.assertEqual(len(adjacent), 1)
        self.assertIn(building2, adjacent)
    
    def test_find_adjacent_buildings_multiple(self):
        """Test finding multiple adjacent buildings"""
        building1 = Building("Building1", 0.0, 0.0)
        building2 = Building("Building2", 1.0, 1.0)
        building3 = Building("Building3", 2.0, 2.0)
        connect_building(building1, building2)
        connect_building(building1, building3)
        adjacent = find_adjacent_buildings(building1)
        self.assertEqual(len(adjacent), 2)
        self.assertIn(building2, adjacent)
        self.assertIn(building3, adjacent)


class TestFindBuildingsWithinTwoEdges(unittest.TestCase):
    """Test cases for find_buildings_within_two_edges function"""
    
    def test_buildings_within_two_edges_simple(self):
        """Test finding buildings within two edges in a simple graph"""
        b1 = Building("B1", 0.0, 0.0)
        b2 = Building("B2", 1.0, 1.0)
        b3 = Building("B3", 2.0, 2.0)
        connect_building(b1, b2)
        connect_building(b2, b3)
        
        result = find_buildings_within_two_edges(b1)
        self.assertIn(b2, result)
        self.assertIn(b3, result)
    
    def test_buildings_within_two_edges_includes_direct(self):
        """Test that result includes directly connected buildings"""
        b1 = Building("B1", 0.0, 0.0)
        b2 = Building("B2", 1.0, 1.0)
        b3 = Building("B3", 2.0, 2.0)
        connect_building(b1, b2)
        connect_building(b1, b3)
        
        result = find_buildings_within_two_edges(b1)
        self.assertIn(b2, result)
        self.assertIn(b3, result)


class TestDistanceFunctions(unittest.TestCase):
    """Test cases for distance calculation functions"""
    
    def test_euclidean_distance_same_location(self):
        """Test Euclidean distance between same location"""
        building = Building("Same", 29.964440, -90.106995)
        distance = find_euclidean_distance(building, building)
        self.assertEqual(distance, 0.0)
    
    def test_euclidean_distance_different_locations(self):
        """Test Euclidean distance between different locations"""
        building1 = Building("B1", 0.0, 0.0)
        building2 = Building("B2", 3.0, 4.0)
        distance = find_euclidean_distance(building1, building2)
        self.assertAlmostEqual(distance, 5.0, places=5)
    
    def test_haversine_distance_same_location(self):
        """Test Haversine distance between same location"""
        building = Building("Same", 29.964440, -90.106995)
        distance = haversine_distance_function(building, building)
        self.assertAlmostEqual(distance, 0.0, places=5)
    
    def test_haversine_distance_positive(self):
        """Test that Haversine distance is always positive"""
        building1 = Building("Admin", 29.964440, -90.106995)
        building2 = Building("Chapel", 29.965934, -90.106465)
        distance = haversine_distance_function(building1, building2)
        self.assertGreater(distance, 0)
    
    def test_haversine_distance_symmetry(self):
        """Test that Haversine distance is symmetric"""
        building1 = Building("Admin", 29.964440, -90.106995)
        building2 = Building("Chapel", 29.965934, -90.106465)
        distance1 = haversine_distance_function(building1, building2)
        distance2 = haversine_distance_function(building2, building1)
        self.assertAlmostEqual(distance1, distance2, places=5)


class TestBuildAdjacencyList(unittest.TestCase):
    """Test cases for build_adjacency_list function"""
    
    def test_adjacency_list_structure(self):
        """Test that adjacency list has correct structure"""
        buildings = [
            Building("B1", 0.0, 0.0),
            Building("B2", 1.0, 1.0)
        ]
        connect_building(buildings[0], buildings[1])
        adj_list = build_adjacency_list(buildings)
        
        self.assertIsInstance(adj_list, dict)
        self.assertEqual(len(adj_list), 2)
        for building in buildings:
            self.assertIn(building, adj_list)
            self.assertIsInstance(adj_list[building], set)
    
    def test_adjacency_list_weights(self):
        """Test that adjacency list includes distance weights"""
        buildings = [
            Building("B1", 0.0, 0.0),
            Building("B2", 1.0, 1.0)
        ]
        connect_building(buildings[0], buildings[1])
        adj_list = build_adjacency_list(buildings)
        
        # Check that the adjacency list for B1 contains a tuple (B2, distance)
        self.assertEqual(len(adj_list[buildings[0]]), 1)
        neighbor, distance = list(adj_list[buildings[0]])[0]
        self.assertEqual(neighbor, buildings[1])
        self.assertGreater(distance, 0)
    
    def test_adjacency_list_empty_neighbors(self):
        """Test adjacency list with building that has no neighbors"""
        building = Building("Isolated", 0.0, 0.0)
        adj_list = build_adjacency_list([building])
        self.assertEqual(len(adj_list[building]), 0)


class TestDijkstra(unittest.TestCase):
    """Test cases for Dijkstra's algorithm"""
    
    def setUp(self):
        """Set up a simple graph for testing"""
        self.b1 = Building("B1", 0.0, 0.0)
        self.b2 = Building("B2", 1.0, 0.0)
        self.b3 = Building("B3", 2.0, 0.0)
        connect_building(self.b1, self.b2)
        connect_building(self.b2, self.b3)
        self.adj_list = build_adjacency_list([self.b1, self.b2, self.b3])
    
    def test_dijkstra_same_building(self):
        """Test Dijkstra with source and destination being the same"""
        distance, path = dijkstra(self.adj_list, self.b1, self.b1)
        self.assertEqual(distance, 0.0)
        self.assertIn("B1", path)
    
    def test_dijkstra_adjacent_buildings(self):
        """Test Dijkstra between adjacent buildings"""
        distance, path = dijkstra(self.adj_list, self.b1, self.b2)
        self.assertGreater(distance, 0)
        self.assertIn("B1", path)
        self.assertIn("B2", path)
    
    def test_dijkstra_path_format(self):
        """Test that Dijkstra returns path in correct format"""
        distance, path = dijkstra(self.adj_list, self.b1, self.b2)
        self.assertIsInstance(distance, float)
        self.assertIsInstance(path, str)
        self.assertIn("-->", path)
    
    def test_dijkstra_returns_tuple(self):
        """Test that Dijkstra returns a tuple of (distance, path)"""
        result = dijkstra(self.adj_list, self.b1, self.b2)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)


class TestShortestDistanceFunctions(unittest.TestCase):
    """Test cases for shortest distance and path functions"""
    
    def setUp(self):
        """Set up a simple graph for testing"""
        self.buildings = create_buildings()
        connect_all_buildings(self.buildings)
        self.adj_list = build_adjacency_list(self.buildings)
    
    def test_shortest_distance_format(self):
        """Test that shortest distance returns formatted string with 'km'"""
        result = shortest_distance_btw_two_buildings(
            self.adj_list, 
            self.buildings[0], 
            self.buildings[1]
        )
        self.assertIsInstance(result, str)
        self.assertIn("km", result)
    
    def test_shortest_distance_is_numeric(self):
        """Test that shortest distance contains a numeric value"""
        result = shortest_distance_btw_two_buildings(
            self.adj_list, 
            self.buildings[0], 
            self.buildings[1]
        )
        # Extract numeric part
        numeric_part = result.replace("km", "").strip()
        try:
            float(numeric_part)
            is_numeric = True
        except ValueError:
            is_numeric = False
        self.assertTrue(is_numeric)
    
    def test_shortest_path_format(self):
        """Test that shortest path returns formatted string"""
        result = shortest_path_btw_two_buildings(
            self.adj_list, 
            self.buildings[0], 
            self.buildings[1]
        )
        self.assertIsInstance(result, str)
        self.assertIn("-->", result)
    
    def test_shortest_path_contains_buildings(self):
        """Test that shortest path contains building names"""
        result = shortest_path_btw_two_buildings(
            self.adj_list, 
            self.buildings[0], 
            self.buildings[1]
        )
        self.assertIn(self.buildings[0].name, result)
        self.assertIn(self.buildings[1].name, result)
    
    def test_shortest_distance_same_building(self):
        """Test shortest distance when source equals destination"""
        result = shortest_distance_btw_two_buildings(
            self.adj_list, 
            self.buildings[0], 
            self.buildings[0]
        )
        self.assertIn("0.0", result)


class TestConnectRandomBuildings(unittest.TestCase):
    """Test cases for connect_random_buildings function"""
    
    def test_connect_random_buildings_adds_connections(self):
        """Test that random connections are added"""
        buildings = create_buildings()
        initial_neighbor_count = sum(len(b.neighbors) for b in buildings)
        connect_random_buildings(buildings, 5)
        final_neighbor_count = sum(len(b.neighbors) for b in buildings)
        # Should have added 10 connections (2 per iteration, 5 iterations)
        self.assertEqual(final_neighbor_count - initial_neighbor_count, 10)
    
    def test_connect_random_buildings_zero_edges(self):
        """Test random connections with zero edges"""
        buildings = create_buildings()
        initial_neighbor_count = sum(len(b.neighbors) for b in buildings)
        connect_random_buildings(buildings, 0)
        final_neighbor_count = sum(len(b.neighbors) for b in buildings)
        self.assertEqual(initial_neighbor_count, final_neighbor_count)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete graph system"""
    
    def test_complete_workflow(self):
        """Test the complete workflow from creation to pathfinding"""
        # Create buildings
        buildings = create_buildings()
        self.assertEqual(len(buildings), 13)
        
        # Connect buildings
        connect_all_buildings(buildings)
        for building in buildings:
            self.assertGreater(len(building.neighbors), 0)
        
        # Build adjacency list
        adj_list = build_adjacency_list(buildings)
        self.assertEqual(len(adj_list), 13)
        
        # Find shortest path
        distance = shortest_distance_btw_two_buildings(
            adj_list, 
            buildings[0], 
            buildings[5]
        )
        path = shortest_path_btw_two_buildings(
            adj_list, 
            buildings[0], 
            buildings[5]
        )
        
        self.assertIsInstance(distance, str)
        self.assertIsInstance(path, str)
        self.assertIn("km", distance)
        self.assertIn("-->", path)
    
    def test_graph_with_complete_connections(self):
        """Test graph with complete connections between all nodes"""
        buildings = [
            Building("A", 0.0, 0.0),
            Building("B", 1.0, 0.0),
            Building("C", 2.0, 0.0)  # Changed to avoid equal distances
        ]
        connect_complete_graph(buildings)
        adj_list = build_adjacency_list(buildings)
        
        # Test that all buildings are in the adjacency list
        for building in buildings:
            self.assertIn(building, adj_list)
            # In a complete graph with 3 nodes, each should have 2 neighbors
            self.assertEqual(len(adj_list[building]), 2)
        
        # Test a simple path from A to C
        distance, path = dijkstra(adj_list, buildings[0], buildings[2])
        self.assertGreater(distance, 0)
        self.assertIn(buildings[0].name, path)
        self.assertIn(buildings[2].name, path)


if __name__ == '__main__':
    unittest.main()
