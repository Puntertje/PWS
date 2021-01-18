import roads, cars, lights, lights_data     # Local python modules, each controlling their respective game aspect.
from time import sleep
import pygame
import random


# Variables
WINDOW_WIDTH = 2510                     # Window dimensions
WINDOW_HEIGHT = 1400                    # Window dimensions
BlOCK_SIZE = 15                         # Size of each block in the grid.
MAX_AMOUNT_CARS = 20                    # Maximum cars allowed to exist at once.

# Colors                                # Welcome to 50 shades of colors
BACKGROUND_COLOR = (200, 200, 200)      # RGB white(ish)
GRID_COLOR = (0, 0, 0)                  # RGB black
CAR_COLOR = (0, 0, 200)                 # RGB blue
INTERSECTION_COLOR = (200, 0, 0)        # RGB red
CORNER_COLOR = (72, 72, 72)             # RGB grey
ROAD_COLOR = (82, 82, 82)               # RGB grey


class Game:
    def __init__(self, spawn_rate=1, debug=False):
        pygame.init()
        pygame.font.init()

        # Set variables
        self.debug = debug
        self.car_list = []
        self.road_list = []
        self.intersections_list = []
        self.spawn_rate = spawn_rate
        self.window_width = WINDOW_WIDTH
        self.window_height = WINDOW_HEIGHT
        self.block_size = BlOCK_SIZE
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))  # Setup the display screen.
        self.screen.fill(BACKGROUND_COLOR)                                              # Set the background
        self.draw_grid(self.window_width, self.window_height)                           # Draw the overlaying grid

        # Generate intersection
        for intersection in lights_data.coordinates:
            # Create an intersection on the coordinates specified in lights_data with the corresponding name.
            self.intersections_list.append(lights.Intersection(lights_data.coordinates[intersection], intersection))
        for intersection in self.intersections_list:
            # Check if its an intersection we control, if not we give it the corner color.
            if len(intersection.name) == 1:
                self.draw_intersection(intersection, INTERSECTION_COLOR)
            else:
                self.draw_intersection(intersection, CORNER_COLOR)

        # Generate roads
        # TODO: Generate roads between intersections of a specified length. Likely going to have to be hard coded,
        #       I don't like it any more than you do.

        # Generate cars
        # TODO: Change all of this, only here for debugging purposes.
        for _ in range(random.randint(2, MAX_AMOUNT_CARS-18)):
            self.car_list.append(cars.Car(random.randint(0, 5), random.randint(0, 5), random.randint(-1, 1)))

        self.next_tick()

        while True:
            if debug:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.next_tick()
            else:
                self.next_tick()
                sleep(0.5)

    """
    Game Logic
    """
    def next_tick(self):
        for car in self.car_list:
            self.draw_car(car, BACKGROUND_COLOR)
            brrr = car.drive()              # Sue me
            if brrr == "Arrived":
                self.car_list.remove(car)   # If the car is at its destination we can remove the car from the field.
            self.draw_car(car, CAR_COLOR)
        pygame.display.update()

    # TODO: Create user action, specify the intersection with a tuple (x,y) and specify the direction 1-4
    def action(self, light, direction):
        pass

    """
    Visual Logic (I.E drawing)
    """
    # Borrowed/stolen from https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame
    def draw_grid(self, window_width, window_height):
        for x in range(window_width):
            for y in range(window_height):
                rect = pygame.Rect(x * self.block_size, y * self.block_size, self.block_size, self.block_size)
                pygame.draw.rect(self.screen, GRID_COLOR, rect, 1)

    def draw_car(self, car, color):
        x, y = car.coordinates
        rect = pygame.Rect(x * self.block_size, y * self.block_size, self.block_size, self.block_size)
        pygame.draw.rect(self.screen, color, rect)          # Draw the car.
        pygame.draw.rect(self.screen, GRID_COLOR, rect, 1)  # Redraw the grid on top. Looks better when erasing.

    def draw_road(self, road, color):
        for x, y in road.coordinate_range():    # Takes a list of tuples which contain the road path section coordinates
            rect = pygame.Rect(x * self.block_size, y * self.block_size, self.block_size, self.block_size)
            pygame.draw.rect(self.screen, color, rect)  # Draw the road section.
            pygame.draw.rect(self.screen, GRID_COLOR, rect, 1)  # Redraw the grid on top for consistency.

    def draw_intersection(self, intersection, color):
        x, y = intersection.coordinates
        rect = pygame.Rect(x * self.block_size, y * self.block_size, self.block_size, self.block_size)
        pygame.draw.rect(self.screen, color, rect)  # Draw the intersection.
        pygame.draw.rect(self.screen, GRID_COLOR, rect, 1)  # Redraw the grid on top for consistency.
        if self.debug:
            myfont = pygame.font.SysFont('Comic Sans MS', 25)
            textsurface = myfont.render(intersection.name, False, (0, 0, 0))
            self.screen.blit(textsurface, (x * self.block_size, y * self.block_size))


Game()
