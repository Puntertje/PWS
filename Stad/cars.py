import random   # In the end this is a game, no need to make it cryptographically secure.


class Car:
    def __init__(self, x, y, speed):
        self.x_position = x
        self.y_position = y
        self.x_direction = speed                                # Temporary speed assignment for debugging purposes.
        self.y_direction = speed                                # Eventually it will be handled by Dijkstra.
        self.coordinates = (self.x_position, self.y_position)

    # TODO: Add collision detection. We don't want it to move onto an already occupied square
    def drive(self):
        self.x_position += self.x_direction
        self.y_position += self.y_direction
        self.coordinates = (self.x_position, self.y_position)   # Update coordinate tuple.
        # if self.x == self.destination_x and self.y == self.destination_y:
        #     return "Arrived"

    def crossing(self):
        # TODO: Change x_direction and y_direction to head for the next crossing.
        pass

    def dijkstra(self):
        # TODO: Find the shortest path to the destination using Dijkstra.
        pass

    def generate_entry_destination(self):
        # TODO: Pick a destination from the list of crossings.
        return  # [(x_start, y_start), (x_dest, y_dest)]
