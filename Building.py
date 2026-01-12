from collections import deque
class Building:
    def __init__(self, name:str, latitude: float, longitude: float):
        self.name = name
        self.coords: tuple[float, float] = (latitude, longitude)
        self.neighbors: set["Building"] = set()

    def add_neigbhour(self, target_node: "Building"):
        self.neighbors.add(target_node)

    def find_adjacent_buildings(self) -> list["Building"]:
        return self.neighbors

    def find_buildings_within_n_edges(self, num_edges) -> set["Building"]:
        buildings_within_n_edges: set[Building] = set()

        buildings_queue = deque()
        buildings_queue.append((self, 0))

        while buildings_queue:

            curr_building, curr_depth = buildings_queue.popleft()
            buildings_within_n_edges.add(curr_building)

            curr_depth += 1
            if curr_depth < num_edges + 1:
                for neigbhour in curr_building.neighbors:
                    buildings_queue.append((neigbhour, curr_depth))
                
        return buildings_within_n_edges

    def __repr__(self):
        return f"{self.name}"