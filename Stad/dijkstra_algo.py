import lights_data
import math


# Modified/borrowed/stolen from https://www.pythonpool.com/dijkstras-algorithm-python/
def dijkstra(self, start, destination):
    unvisited_nodes = lights_data.distances
    shortest_distance = {}
    route = []
    predecessor = {}

    for nodes in unvisited_nodes:
        shortest_distance[nodes] = math.inf
    shortest_distance[start] = 0

    while unvisited_nodes:
        min_node = None
        for current_node in unvisited_nodes:
            if min_node is None:
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
        except Exception:
            return 'Path not reachable'
            break
    route.insert(0, start)
    if shortest_distance[destination] != math.inf:
        # Return a list of all the stops along the optimal path.
        return route