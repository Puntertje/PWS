from . import roads, cars, lights, lights_data    # Local python modules, each controlling their respective game aspect.
from time import sleep
import pygame
import random
from termcolor import colored


# Variables
WINDOW_WIDTH = 650                      # Window dimensions
WINDOW_HEIGHT = 900                     # Window dimensions
BlOCK_SIZE = 10                         # Size of each block in the grid.
MAX_AMOUNT_CARS = 20                    # Maximum cars allowed to exist at once.
CAR_SPAWN_SIZE = 5                      # Amount of spawning attempts per tick.
CAR_SPAWN_CHANCE = 4                    # Chance of car spawning successfully, notation: 1/number

# Colors                                # Welcome to 50 shades of colors
BACKGROUND_COLOR = (200, 200, 200)      # RGB white(ish)
GRID_COLOR = (0, 0, 0)                  # RGB black
CAR_COLOR = (0, 0, 200)                 # RGB blue
INTERSECTION_COLOR = (200, 0, 0)        # RGB red
CROSSING_COLOR = (255, 180, 12)         # RGB orange
CORNER_COLOR = (25, 25, 25)             # RGB grey
ROAD_COLOR = (82, 82, 82)               # RGB grey
TEXT_COLOR = (0, 200, 0)                # RGB green


class Game:
    def __init__(self, spawn_rate=1, debug=False, tick_speed=10):
        # pygame initialisations
        pygame.init()
        pygame.font.init()

        # Set variables
        self.debug = debug
        self.car_list = []                  # List of all car objects
        self.road_dict = {}                 # List of all road objects
        self.intersections_dict = {}        # List of all intersection objects
        self.road_coordinates_list = []     # List of all road coordinates, used for visual logic
        self.corner_coordinates_list = []   # List of all corner coordinates, used for visual logic
        self.spawn_rate = spawn_rate
        self.window_width = WINDOW_WIDTH
        self.window_height = WINDOW_HEIGHT
        self.block_size = BlOCK_SIZE
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))  # Setup the display screen.
        self.screen.fill(BACKGROUND_COLOR)                                              # Set the background
        self.draw_grid(self.window_width, self.window_height)                           # Draw the overlaying grid

        # Generate roads
        for corner in lights_data.corners:
            corner_intersections = {}
            for intersection in corner.split("-"):
                corner_intersections[intersection] = lights_data.coordinates[intersection]
            self.road_dict[corner] = roads.Road(corner_intersections, lights_data.corners[corner], corner)
        # Remove edge case
        road_cord_edge_case = [(14, 6), (14, 7), (14, 8)]
        self.road_dict["E-D"].road_coordinate_list = [
            road_cord for road_cord in self.road_dict["E-D"].road_coordinate_list
            if road_cord not in road_cord_edge_case
        ]
        for road in self.road_dict:
            self.draw_road(self.road_dict[road], ROAD_COLOR)

        # Generate intersection
        for intersection in lights_data.coordinates:
            # Create an intersection on the coordinates specified in lights_data with the corresponding name.
            self.intersections_dict[intersection] = lights.Intersection(lights_data.coordinates[intersection], intersection)
        for intersection in self.intersections_dict:
            # Check if its an intersection we control, if not we give it the crossing color.
            if len(self.intersections_dict[intersection].name) == 1:
                self.draw_intersection(self.intersections_dict[intersection], INTERSECTION_COLOR)
            else:
                self.draw_intersection(self.intersections_dict[intersection], CROSSING_COLOR)

        # Add road and corner coordinates
        for corner_dict_key in lights_data.corners:
            for corner_value in lights_data.corners[corner_dict_key]:
                self.corner_coordinates_list.append(lights_data.corners[corner_dict_key][corner_value])
        for road_obj in self.road_dict:
            self.road_coordinates_list.extend(self.road_dict[road_obj].road_coordinate_list)
        # Generate cars
        # TODO: Change all of this, only here for debugging purposes.
        for _ in range(random.randint(2, MAX_AMOUNT_CARS)):
            self.car_list.append(cars.Car())
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
                sleep(1/tick_speed)

    """
    Game Logic
    """
    def next_tick(self):
        for car in self.car_list:
            current_car_pos_x, current_car_pos_y = car.coordinates
            if (current_car_pos_x, current_car_pos_y) in [lights_data.coordinates["CB"],    # Crossings over which
                                                          lights_data.coordinates["BEH"],   # we have no control.
                                                          lights_data.coordinates["IPJ"]]:
                self.draw_car(car, CROSSING_COLOR)
            elif (current_car_pos_x, current_car_pos_y) in lights_data.coordinates.values():
                self.draw_car(car, INTERSECTION_COLOR)
            elif (current_car_pos_x, current_car_pos_y) in self.corner_coordinates_list:
                self.draw_car(car, CORNER_COLOR)
            elif (current_car_pos_x, current_car_pos_y) in self.road_coordinates_list:
                self.draw_car(car, ROAD_COLOR)
            else:
                self.draw_car(car, BACKGROUND_COLOR)
            drive = True
            for other_car in self.car_list:
                if other_car.coordinates == car.next_position():
                    if other_car.x_direction * car.x_direction == -1 or other_car.y_direction * car.y_direction == -1:
                        drive = True
                    else:
                        print(colored("Collission on:", "blue"), colored(car.next_position(), "red"))
                        drive = False
                        break
            if drive:
                brrr = car.drive()              # Sue me
                if brrr == "Arrived":
                    self.car_list.remove(car)   # If the car is at its destination we can remove the car from the field.
                else:
                    self.draw_car(car, CAR_COLOR)
            else:
                self.draw_car(car, CAR_COLOR)
        for _ in range(CAR_SPAWN_SIZE):
            if len(self.car_list) >= MAX_AMOUNT_CARS:
                break
            if random.randint(1, CAR_SPAWN_CHANCE) == 1:
                self.car_list.append(cars.Car())
        pygame.event.get()                  # Prevents the application from freezing up on Windows.
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
        for x, y in road.road_coordinate_list:  # Road coordinates
            rect = pygame.Rect(x * self.block_size, y * self.block_size, self.block_size, self.block_size)
            pygame.draw.rect(self.screen, color, rect)  # Draw the road section.
            pygame.draw.rect(self.screen, GRID_COLOR, rect, 1)
        self.draw_corner(road)

    def draw_corner(self, road):
        for corner in road.corner_coordinate_dict:          # Corners
            x, y = road.corner_coordinate_dict[corner]
            rect = pygame.Rect(x * self.block_size, y * self.block_size, self.block_size, self.block_size)
            pygame.draw.rect(self.screen, CORNER_COLOR, rect)  # Draw the corner section.
            pygame.draw.rect(self.screen, GRID_COLOR, rect, 1)  # Redraw the grid on top for consistency.
            if self.debug:
                font = pygame.font.SysFont('Comic Sans MS', 25)
                text = font.render(corner, False, TEXT_COLOR)
                self.screen.blit(text, (x * self.block_size, y * self.block_size))

    def draw_intersection(self, intersection, color):
        x, y = intersection.coordinates
        rect = pygame.Rect(x * self.block_size, y * self.block_size, self.block_size, self.block_size)
        pygame.draw.rect(self.screen, color, rect)  # Draw the intersection.
        pygame.draw.rect(self.screen, GRID_COLOR, rect, 1)  # Redraw the grid on top for consistency.
        if self.debug:
            font = pygame.font.SysFont('Comic Sans MS', 25)
            text = font.render(intersection.name, False, TEXT_COLOR)
            self.screen.blit(text, (x * self.block_size, y * self.block_size))
