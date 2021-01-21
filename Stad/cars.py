import random   # In the end this is a game, no need to make it cryptographically secure.
import lights_data
import math


class Car:
    def __init__(self, x, y, speed):
        self.start, self.destination = self.generate_entry_destination()
        self.route = self.dijkstra(self.start, self.destination)
        self.x_position = x
        self.y_position = y
        self.x_direction = speed                                # Temporary speed assignment for debugging purposes.
        self.y_direction = speed                                # Eventually it will be handled by Dijkstra.
        self.coordinates = (self.x_position, self.y_position)

    # TODO: Add collision detection. We don't want it to move onto an already occupied square
    #       On second thought. Probably best this is handled in the game file
    def drive(self):
        self.x_position += self.x_direction
        self.y_position += self.y_direction
        self.coordinates = (self.x_position, self.y_position)   # Update coordinate tuple.
        # if self.x == self.destination_x and self.y == self.destination_y:
        #     return "Arrived"

    def crossing(self, current_position, next_position):
        # TODO: Change x_direction and y_direction to head for the next crossing.
        pass

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

    def generate_entry_destination(self):
        destination = random.choice(lights_data.destinations)
        start = random.choice(lights_data.starting_points)
        return start, destination
