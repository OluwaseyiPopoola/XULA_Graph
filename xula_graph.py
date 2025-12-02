import math
import heapq
import random
from Building import Building
from Buildings import Buildings


def main():
    buildings_instance: Buildings = Buildings.create_buildings()
    all_locations = buildings_instance.all_locations
    buildings_instance.connect_all_buildings()
    
    # print("Graph Connection Verification")
    # for i, location in enumerate(all_locations):
    #     neighbor_names = [node.name for node in location.neighbors]
    #     print(f"{location.name}: -> {neighbor_names}")

    # print(find_adjacent_buildings(all_locations[0]))

    # print(find_buildings_within_two_edges(all_locations[0]))

    ady: dict[Building, set[tuple[Building, float]]] = build_adjacency_list(all_locations)
    # print(ady)

    print(all_locations[0], all_locations[8])

    print(shortest_distance_btw_two_buildings(ady, all_locations[0], all_locations[8]))
    print(shortest_path_btw_two_buildings(ady, all_locations[0], all_locations[8]))



# TODO You need a Buildings.py file that has a list[Building] instance variable.

# TODO This should be a @staticmethod within the Buildings class.
# locations = Buildings.create_buildings()  # class calls because no object needed


# TODO This should be a method (with self as first parameter) within the Buildings class.


# TODO This should be a @staticmethod (no self) within the Buildings class.


# TODO This should be a method (with self as first parameter) within the Buildings class.


# TODO This should be a method (with self as first parameter) within the Buildings class.


# TODO This should be a method (with self as first parameter) within the Buildings class.
def build_adjacency_list(locations: list[Building]) -> dict[Building, set[tuple[Building, float]]]:
    ady = {building : {(neigbhor, haversine_distance_function(building, neigbhor) ) for neigbhor in building.neighbors} for building in locations}
    return ady

# TODO This should be a __private method (with self as first parameter) within the Buildings class.
def find_euclidean_distance(building_a: Building, building_b: Building) -> float:
    lat_a, long_a = building_a.coords
    lat_b, long_b = building_b.coords

    long_diff_sq: float = (long_b - long_a) ** 2
    lat_diff_sq: float = (lat_b - lat_a) ** 2

    return math.sqrt(long_diff_sq + lat_diff_sq)

# TODO This should be a __private method (with self as first parameter) within the Buildings class.
def haversine_distance_function(building_a: Building, building_b: Building) -> float:
    R = 6371.0 

    lat1, long1 = map(math.radians, building_a.coords)
    lat2, long2 = map(math.radians, building_b.coords)

    dlon = long2 - long1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

# TODO This should be a method (with self as first parameter) within the Buildings class.
def find_adjacent_buildings(building: Building) -> list[Building]:
    return building.neighbors

# TODO Buildings.find_buildings_within(num_edges, building: Building)
def find_buildings_within_two_edges(building: Building) -> set[Building]:
    buildings: set[Building] = set()
    for neigbhour in building.neighbors:
        buildings.add(neigbhour)

        for neigbhour_of_neigbhour in neigbhour.neighbors:
            buildings.add(neigbhour_of_neigbhour)

    return buildings


# TODO This should be a method (with self as first parameter) within the Buildings class.
def dijkstra(ady: dict[Building, set[tuple[Building, float]]], building1: Building, building2: Building) -> tuple[float, str]:
    INF = float('inf')

    previous: dict[Building, Building | None] = {building: None for building in ady}
    distance_frm_src: dict[Building, float] = {building: INF for building in ady}
    visited: dict[Building, bool] = {building: False for building in ady}
    pq: list[tuple[float, Building]] = []

    heapq.heappush(pq, (0.0, building1))
    distance_frm_src[building1] = 0.0

    while pq:
        curr_shortest_ditance_from_src, curr_building = heapq.heappop(pq)

        for neigbhour, edge_distance in ady[curr_building]:
            if visited[neigbhour]:
                continue

            if edge_distance + curr_shortest_ditance_from_src < distance_frm_src[neigbhour]:
                distance_frm_src[neigbhour] = edge_distance + curr_shortest_ditance_from_src
                previous[neigbhour] = curr_building
                heapq.heappush(pq, (distance_frm_src[neigbhour], neigbhour))

    curr = building2
    path = [repr(curr)]
    

    while curr != building1:
        if curr is None or previous[curr] is None:
            break
        path.append(repr(previous[curr]))
        curr = previous[curr]

    for i in range(len(path)//2):
        path[i], path[len(path)-1-i] = path[len(path)-1-i], path[i] 

    return (distance_frm_src[building2], " --> ".join(path))

# TODO This should be a method (with self as first parameter) within the Buildings class.
def shortest_distance_btw_two_buildings(
    ady: dict[Building, set[tuple[Building, float]]], 
    building1: Building, 
    building2: Building
) -> str:
    return f"{dijkstra(ady, building1, building2)[0]} km"
    

# TODO This should be a method (with self as first parameter) within the Buildings class.
def shortest_path_btw_two_buildings(
    ady: dict[Building, set[tuple[Building, float]]], 
    building1: Building, 
    building2: Building
) -> str:
    return dijkstra(ady, building1, building2)[1]


if __name__ == "__main__":
    main()


