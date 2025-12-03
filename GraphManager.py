from Building import Building
import random
import math
import heapq

class GraphManager:
    def __init__(self, all_locations: list[Building] = []):
        self.all_locations: list[Building] = all_locations
        self.adjacency_list: dict[Building, set[tuple[Building, float]]] = {}

    @classmethod
    def create_buildings(cls) -> list[Building]:
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

        return cls(locations)
        
    def connect_all_buildings(self):
        num_locations = len(self.all_locations)

        # Connect each building to the next two buildings in the list (circularly)
        for i in range(num_locations):
            current_building = self.all_locations[i]
            
            neighbor_index_1 = (i + 1) % num_locations
            neighbor_index_2 = (i + 2) % num_locations
            
            current_building.add_neigbhour(self.all_locations[neighbor_index_1])
            current_building.add_neigbhour(self.all_locations[neighbor_index_2])

    def connect_random_buildings(self, num_edges: int):
        for _ in range(num_edges):
            current_building_1 = random.choice(self.all_locations)
            current_building_2 = random.choice(self.all_locations)

            current_building_1.add_neigbhour(current_building_2)
            current_building_2.add_neigbhour(current_building_1)

    def connect_complete_graph(self):
        num_locations = len(self.all_locations)

        # Connect each building to every other building == a COMPLETE graph
        for i in range(num_locations):
            for j in range(i + 1, len(self.all_locations)):
                self.all_locations[i].add_neigbhour(self.all_locations[j])
                self.all_locations[j].add_neigbhour(self.all_locations[i])
    
    def build_adjacency_list(self) -> dict[Building, set[tuple[Building, float]]]:
        ady = {building : {(neigbhor, self.__haversine_distance_function(building, neigbhor) ) for neigbhor in building.neighbors} for building in self.all_locations}
        return ady

    @staticmethod
    def __find_euclidean_distance(building_a: Building, building_b: Building) -> float:
        lat_a, long_a = building_a.coords
        lat_b, long_b = building_b.coords

        long_diff_sq: float = (long_b - long_a) ** 2
        lat_diff_sq: float = (lat_b - lat_a) ** 2

        return math.sqrt(long_diff_sq + lat_diff_sq)

    @staticmethod
    def __haversine_distance_function(building_a: Building, building_b: Building) -> float:
        R = 6371.0 

        lat1, long1 = map(math.radians, building_a.coords)
        lat2, long2 = map(math.radians, building_b.coords)

        dlon = long2 - long1
        dlat = lat2 - lat1

        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c
        return distance

    def dijkstra(self, building1: Building, building2: Building) -> tuple[float, str]:
        INF = float('inf')

        previous: dict[Building, Building | None] = {building: None for building in self.all_locations}
        distance_frm_src: dict[Building, float] = {building: INF for building in self.all_locations}
        visited: dict[Building, bool] = {building: False for building in self.all_locations}
        pq: list[tuple[float, Building]] = []

        heapq.heappush(pq, (0.0, building1))
        distance_frm_src[building1] = 0.0

        while pq:
            curr_shortest_ditance_from_src, curr_building = heapq.heappop(pq)

            for neigbhour, edge_distance in self.adjacency_list[curr_building]:
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

    def shortest_distance_btw_two_buildings(self,
        building1: Building, 
        building2: Building
    ) -> str:
        return f"{self.dijkstra(building1, building2)[0]} km"
    
    def shortest_path_btw_two_buildings(self,
        building1: Building, 
        building2: Building
    ) -> str:
        return self.dijkstra(building1, building2)[1]