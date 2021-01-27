import random   # In the end this is a game, no need to make it cryptographically secure.
from . import lights_data
from . import dijkstra_algo
import numpy


class Car:
    def __init__(self, x, y, speed):
        self.destination = random.choice(lights_data.destinations)
        self.start = random.choice(lights_data.starting_points)
        while self.start == self.destination:                           # We want the car to go somewhere.
            self.destination = random.choice(lights_data.destinations)
        self.route = dijkstra_algo.dijkstra(self.start, self.destination)
        self.x_position, self.y_position = lights_data.coordinates[self.start]
        self.x_direction, self.y_direction = (1, 1)            # Temporary speed. Used for the first future position
        self.coordinates = (self.x_position, self.y_position)

    def drive(self):
        if self.coordinates == lights_data.intersection_and_corner_coordinates[self.destination]:
            return "Arrived"
        if self.coordinates == lights_data.intersection_and_corner_coordinates[self.route[0]]:
            self.crossing()
        self.x_position += self.x_direction
        self.y_position += self.y_direction
        self.coordinates = (self.x_position, self.y_position)

    # Get the car's next position, this is done to prevent collisions.
    def next_position(self):
        return self.x_position + self.x_direction, self.y_position + self.y_direction

    def crossing(self):
        self.route.pop(0)
        new_direction = tuple(numpy.subtract(
            lights_data.intersection_and_corner_coordinates[self.route[0]], self.coordinates
        ))
        new_direction = (new_direction[0]//abs(new_direction[0]), new_direction[1]//abs(new_direction[1]))
        self.x_direction, self.y_direction = new_direction


