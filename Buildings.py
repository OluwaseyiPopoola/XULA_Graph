from Building import Building
import random

class Buildings:
    def __init__(self, all_locations: list[Building] = []):
        self.all_locations: list[Building] = all_locations

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