# XULA Graph — README (generated from `xula_graph.py`)

This README documents the `xula_graph.py` utility in this folder. The script models a directed graph of campus locations (as `Building` objects), computes distances (Haversine), and demonstrates shortest-path computation using Dijkstra's algorithm.

## Quick start

- Requirements: **Python 3.9+** (the code uses `list[...]` and `dict[...]` type annotations).
- Run the example program:

```powershell
python xula_graph.py
```

The script will create a set of sample `Building` nodes, connect them, print two example buildings, then print the shortest distance and path between them.

## What the script provides

- `class Building` — represents a node with `.name`, `.coords` (latitude, longitude), and `.neighbors` (list of neighbor `Building` objects).
- `create_buildings()` — returns a list of sample `Building` objects used by the example. The list includes campus locations (e.g., `Admin`, `Library`, `Convo_Ctr`) and a few outside-city samples.
- `connect_all_buildings(all_locations)` — connects every building to the next two buildings in the list (directed edges). This is the default topology used by the example run.
- `connect_building(building_node, target_node)` — add a directed neighbor.
- `build_adjacency_list(locations)` — builds a dictionary mapping each `Building` to a set of `(neighbor, distance_km)` pairs, where `distance_km` is computed with the Haversine formula.
- `haversine_distance_function(a, b)` — returns great-circle distance in kilometers between two buildings.
- `find_adjacent_buildings(building)` — returns the `.neighbors` list for a building.
- `find_buildings_within_two_edges(building)` — returns a set of buildings reachable within two directed edges.
- `dijkstra(ady, building1, building2)` — computes shortest distances from `building1` to all nodes using Dijkstra's algorithm and returns `[distance_km, path_string]` for `building2`.
- `shortest_distance_btw_two_buildings(ady, b1, b2)` — helper returning formatted distance string.
- `shortest_path_btw_two_buildings(ady, b1, b2)` — helper returning the path string.

## Data / Types

- The in-memory graph is a list of `Building` objects and an adjacency dictionary returned by `build_adjacency_list`.
- Distances are calculated in kilometers (floating-point) by the Haversine function.

Notes on the implementation:
- Edges are treated as directed (neighbors appended only in one direction by `connect_building`). `connect_all_buildings` currently connects each node to the next two nodes in the list (wrap-around), creating a directed circular neighborhood.
- The adjacency dictionary uses `Building` objects as keys. Be careful if you change the code to serialize or reconstruct nodes — hashing/equality are identity-based unless you add `__hash__`/`__eq__`.

## Example output (what to expect)

When run as-is, `xula_graph.py` prints two building objects and then prints the shortest distance and shortest path between them. Example lines (values will vary slightly):

```
Admin Convo_Ctr
2.3456789 km
Admin --> Chapel --> Library --> Convo_Ctr
```

## How to adapt this script

- To change the graph: edit `create_buildings()` (add/remove `Building(...)`) or change `connect_all_buildings()` (use different connection logic or a real campus edge list).
- To use geographic heuristics (A*), provide `coords` and implement an admissible heuristic (e.g., straight-line Haversine distance divided by walking speed).
- To make the graph undirected, call `connect_building(a, b)` and `connect_building(b, a)` when creating edges.
- To persist a graph, export node list and CSV edge list (source,target,weight) and add a loader function.

## Example: import functions from this file

You can import functions and reuse them in other scripts:

```python
from xula_graph import create_buildings, connect_all_buildings, build_adjacency_list, shortest_path_btw_two_buildings

buildings = create_buildings()
connect_all_buildings(buildings)
ady = build_adjacency_list(buildings)
print(shortest_path_btw_two_buildings(ady, buildings[0], buildings[2]))
```

## Suggestions / TODOs

- Add a loader to read edges from `edges.csv` or `edges.txt` so the graph can be edited outside the code.
- Add `__eq__` and `__hash__` to `Building` to make them safer dictionary keys for serialization.
- Add a small CLI wrapper (e.g., `search.py`) to accept `--start`/`--goal` arguments and choose algorithms.

## License

This project currently has no license file. Add a `LICENSE` at the repository root to make reuse terms explicit.

---

