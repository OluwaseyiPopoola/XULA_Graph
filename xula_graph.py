from GraphManager import GraphManager

def main():
    xula_map: GraphManager = GraphManager.create_buildings()
    
    xula_map.connect_random_buildings(20)
    xula_map.adjacency_list = xula_map.build_adjacency_list()
    

    # print("Graph Connection Verification")
    # for location in xula_map.all_locations:
    #     neighbor_names = [node.name for node in location.neighbors]
    #     print(f"{location.name}: -> {neighbor_names}")

    # Test find_adjacent_buildings and find_buildings_within_n_edges
    # print(xula_map.all_locations[0].find_adjacent_buildings())
    # print(xula_map.all_locations[0].find_buildings_within_n_edges(2))

    # Test shortest path and distance using Dijkstra's algorithm
    # print(xula_map.all_locations[0], xula_map.all_locations[8])
    # print(xula_map.shortest_distance_btw_two_buildings(xula_map.all_locations[0], xula_map.all_locations[8]))
    # print(xula_map.shortest_path_btw_two_buildings(xula_map.all_locations[0], xula_map.all_locations[8]))

if __name__ == "__main__":
    main()


