import random   # In the end this is a game, no need to make it cryptographically secure.
import lights_data
import dijkstra_algo


class Car:
    def __init__(self, x, y, speed):
        self.destination = random.choice(lights_data.destinations)
        self.start = random.choice(lights_data.starting_points)
        while self.start == self.destination:                           # We want the car to go somewhere.
            self.destination = random.choice(lights_data.destinations)
        self.route = dijkstra_algo.dijkstra(self.start, self.destination)
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

    # Get the car's next position, this is done in order to prevent collisions
    def next_position(self):
        return tuple(self.x_position + self.x_direction, self.y_position + self.y_direction)

    def crossing(self, current_position, next_position):
        # TODO: Change x_direction and y_direction to head for the next crossing.
        pass

