import math
import heapq

def main():
    all_locations = create_buildings()
    connect_all_buildings(all_locations)
    
    # print("Graph Connection Verification")
    # for i, location in enumerate(all_locations):
    #     neighbor_names = [node.name for node in location.neighbors]
    #     print(f"{location.name}: -> {neighbor_names}")

    # print(find_adjacent_buildings(all_locations[0]))

    # print(find_buildings_within_two_edges(all_locations[0]))

    ady = build_adjacency_list(all_locations)
    # print(ady)

    print(all_locations[0], all_locations[8])

    print(shortest_distance_btw_two_buildings(ady, all_locations[0], all_locations[8]))
    print(shortest_path_btw_two_buildings(ady, all_locations[0], all_locations[8]))



class Building:
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.coords = (latitude, longitude)
        self.neighbors = []

    def __repr__(self):
        return f"{self.name}"

def create_buildings() -> list[Building]:
    locations = [
        Building("Admin", 29.964440282121426, -90.10699538972723),
        Building("Chapel",29.96593408811449, -90.1064650276058),
        Building("Library",29.96599544988278, -90.10716232208914), 
        Building("U_Center",29.964703488401312, -90.10535987770028),
        Building("Pharmacy",29.96578980910307, -90.10667462208916),
        Building("St_Joseph",29.963506522473068, -90.10636098690512),
        Building("St_Michael",29.96477061529604, -90.10569579909495),
        Building("Xavier_S",29.961747090734512, -90.10206360674651),
        Building("Convo_Ctr",29.964097325222845, -90.10923296221479),
        Building("DP",29.96168994182377, -90.10292977127155),
        
        Building("New_Orleans",29.9547, -90.0751),
        Building("Abuja",9.084576, 7.483333),
        Building("Harare",-17.824858, 31.053028)
    ]
    return locations

def connect_all_buildings(all_locations: list[Building]):
    num_locations = len(all_locations)

    # Connect each building to every other building
    # for i in range(len(all_locations)):
    #     for j in range(i + 1, len(all_locations)):
    #         connect_building(all_locations[i], all_locations[j])
    #         connect_building(all_locations[j], all_locations[i])



    # Connect each building to the next two buildings in the list (circularly)
    for i in range(num_locations):
        current_building = all_locations[i]
        
        neighbor_index_1 = (i + 1) % num_locations
        neighbor_index_2 = (i + 2) % num_locations
        
        connect_building(current_building, all_locations[neighbor_index_1])
        connect_building(current_building, all_locations[neighbor_index_2])

def connect_building(building_node: Building, target_node: Building):
    building_node.neighbors.append(target_node)

def build_adjacency_list(locations: list[Building]) -> dict[Building: set[(Building, float)]]:
    ady = {building : {(neigbhor, haversine_distance_function(building, neigbhor) ) for neigbhor in building.neighbors} for building in locations}
    return ady

def find_euclidean_distance(building_a: Building, building_b: Building) -> float:
    long_a, lat_a = building_a.coords
    long_b, lat_b = building_b.coords

    long_diff_sq = (long_b - long_a)**2
    lat_diff_sq = (lat_b - lat_a)**2

    return math.sqrt(long_diff_sq + lat_diff_sq)

def haversine_distance_function(building_a: Building, building_b: Building) -> float:
    R = 6371.0 

    long1, lat1 = map(math.radians, building_a.coords)
    long2, lat2 = map(math.radians, building_b.coords)

    dlon = long2 - long1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

def find_adjacent_buildings(building: Building) -> list:
    return building.neighbors

def find_buildings_within_two_edges(building: Building) -> set:
    buildings = set()
    for neigbhour in building.neighbors:
        buildings.add(neigbhour)

        for neigbhour_of_neigbhour in neigbhour.neighbors:
            buildings.add(neigbhour_of_neigbhour)

    return buildings


def dijkstra(ady, building1: Building, building2: Building) -> list[float, str]:
    INF = 10**8

    previous = {building: None for building in ady}
    distance_frm_src = {building: INF for building in ady}
    visited = {building: False for building in ady}
    pq = []

    heapq.heappush(pq, (0, building1))
    distance_frm_src[building1] = 0

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
        path.append(repr(previous[curr]))
        curr = previous[curr]

    for i in range(len(path)//2):
        path[i], path[len(path)-1-i] = path[len(path)-1-i], path[i] 

    return [distance_frm_src[building2], " --> ".join(path)]

def shortest_distance_btw_two_buildings(ady, building1: Building, building2: Building) -> str:
    return f"{dijkstra(ady, building1, building2)[0]} km"
    

def shortest_path_btw_two_buildings(ady, building1: Building, building2: Building) -> str:
    return dijkstra(ady, building1, building2)[1]

if __name__ == "__main__":
    main()


