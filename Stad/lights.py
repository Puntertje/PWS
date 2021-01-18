class Intersection:
    def __init__(self, coordinates, name):
        self.x_position, self.y_position = coordinates
        self.coordinates = (self.x_position, self.y_position)
        self.direction = 1
        self.name = name

