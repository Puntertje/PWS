from . import lights_data
import math
from termcolor import colored


# Modified/borrowed/stolen from https://www.pythonpool.com/dijkstras-algorithm-python/
# TODO: improve commenting
def dijkstra(start, destination):
    unvisited_nodes = lights_data.distances.copy()
    shortest_distance = {}
    route = []
    predecessor = {}

    for nodes in unvisited_nodes:
        shortest_distance[nodes] = math.inf
    shortest_distance[start] = 0

    while unvisited_nodes:
        min_node = None                     # Reset min_node
        for current_node in unvisited_nodes:
            if min_node is None:            # Assign min_node
                min_node = current_node

            elif shortest_distance[min_node] > shortest_distance[current_node]:
                min_node = current_node

        for child_node, value in unvisited_nodes[min_node].items():
            if value + shortest_distance[min_node] < shortest_distance[child_node]:
                shortest_distance[child_node] = value + shortest_distance[min_node]
                predecessor[child_node] = min_node
        unvisited_nodes.pop(min_node)

    node = destination
    while node != start:
        try:
            route.insert(0, node)
            node = predecessor[node]
        except KeyError as error:
            print(colored("Error in Dijkstra's algorithm:", "blue"), colored(error, "red"))
            return 'Path not reachable'
    route.insert(0, start)
    if shortest_distance[destination] != math.inf:
        # Return a list of all the stops along the optimal path.
        return route
    else:
        print(colored("Error in Dijkstra's algorithm:", "blue"), colored("No shortest path", "red"))
        print(colored("Starting point:", "blue"), start)
        print(colored("Destination:", "blue"), destination)
