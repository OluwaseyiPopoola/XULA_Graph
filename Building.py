class Building:
    def __init__(self, name:str, latitude: float, longitude: float):
        self.name = name
        self.coords: tuple[float, float] = (latitude, longitude)
        self.neighbors: list["Building"] = []

    def add_neigbhour(self, target_node: "Building"):
        self.neighbors.append(target_node)

    def __repr__(self):
        return f"{self.name}"