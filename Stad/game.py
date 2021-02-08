from . import roads, cars, lights, lights_data    # Local python modules, each controlling their respective game aspect.
from termcolor import colored
import numpy as np
from time import sleep
import itertools
import pygame
import random


# Variables
WINDOW_WIDTH = 650                      # Window dimensions
WINDOW_HEIGHT = 900                     # Window dimensions
BlOCK_SIZE = 10                         # Size of each block in the grid.
MAX_AMOUNT_CARS = 200                   # Maximum cars allowed to exist at once.
CAR_SPAWN_SIZE = 5                      # Amount of spawning attempts per tick.
CAR_SPAWN_CHANCE = 4                    # Chance of car spawning successfully, notation: 1/number
WIN_REWARD = 1                          # Reward value for letting a car drive
LOSE_PUNISHMENT = 2                     # Punishment value for making a car stop

# Colors                                # Welcome to 50 shades of colors
BACKGROUND_COLOR = (200, 200, 200)      # RGB white(ish)
GRID_COLOR = (0, 0, 0)                  # RGB black
CAR_COLOR = (0, 200, 200)               # RGB blue/cyan
INTERSECTION_COLOR = (200, 0, 0)        # RGB red
CROSSING_COLOR = (255, 180, 12)         # RGB orange
CORNER_COLOR = (25, 25, 25)             # RGB grey
ROAD_COLOR = (82, 82, 82)               # RGB grey
TEXT_COLOR = (0, 200, 0)                # RGB green

# Verbosity toggles
verbose_collisions = False              # Print a message every time a car crashes.


class Game:
    def __init__(self,
                 spawn_rate=1, tick_cap=0, tick_speed=10,
                 debug=False, manual=False, stats=True,
                 max_cars=MAX_AMOUNT_CARS, headless=False):
        # Pygame initialisations
        if not headless:
            pygame.init()
            pygame.font.init()

        # Set variables
        self.max_cars = max_cars
        self.debug = debug
        self.headless = headless
        self.statistics = stats             # If this is true we track statistics and write them to a file
        self.tick_cap = tick_cap            # Maximum amount of ticks per game, 0 means the game will go on forever
        self.manual = manual                # If manual is true the user may change the lights and the clock is disabled
        self.tick_number = 0                # Keep track of our tick number
        self.score = 0                      # Score to measure how well the A.I is doing.
        self.car_list = []                  # List of all car objects
        self.road_dict = {}                 # List of all road objects
        self.intersections_dict = {}        # List of all intersection objects
        self.road_coordinates_list = []     # List of all road coordinates, used for visual logic
        self.corner_coordinates_list = []   # List of all corner coordinates, used for visual logic
        self.spawn_rate = spawn_rate
        self.tick_offset = 0                # Tick offset to persist stats across resets
        # Extremely resource intensive, uncomment at your own risk. Also uncomment as appropriate in self.action()
        # self.possible_actions = list(itertools.product([0, 1, 2, 3], repeat=16))
        self.possible_actions = []
        if not self.headless:
            self.window_width = WINDOW_WIDTH
            self.window_height = WINDOW_HEIGHT
            self.block_size = BlOCK_SIZE
            self.screen = pygame.display.set_mode((self.window_width, self.window_height))  # Setup the display screen.
            self.screen.fill(BACKGROUND_COLOR)                                              # Set the background
            self.draw_grid(self.window_width, self.window_height)                           # Draw the overlaying grid

        # Statistics variables
        if self.statistics:
            self.tick_history = []
            self.score_history = []
            self.car_amount_history = []
            self.score_per_tick_history = []

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
            if self.headless:
                break
            else:
                self.draw_road(self.road_dict[road], ROAD_COLOR)

        # Generate intersection
        for intersection in lights_data.coordinates:
            # Create an intersection on the coordinates specified in lights_data with the corresponding name.
            self.intersections_dict[intersection] = lights.Intersection(lights_data.coordinates[intersection],
                                                                        intersection)
        for intersection in self.intersections_dict:
            if self.headless:
                break
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

        # If the game is set to automatic we need to do the ticks ourself.
        if not self.manual:
            if self.tick_cap != 0:
                debug_tick_index = 0
                while debug_tick_index < self.tick_cap:
                    if debug:
                        events = pygame.event.get()
                        for event in events:
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    self.next_tick()
                                    debug_tick_index += 1
                                if event.key == pygame.K_w:
                                    self.max_cars = 0      
                    else:
                        self.next_tick()
                        debug_tick_index += 1
                        if tick_speed != 0:
                            sleep(1 / tick_speed)
                pygame.display.quit()
            else:
                while True:
                    if debug:
                        events = pygame.event.get()
                        for event in events:
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    self.next_tick()
                                if event.key == pygame.K_w:
                                    self.max_cars = 0
                    else:
                        self.next_tick()
                        if tick_speed != 0:  # If its zero there will be no delay
                            sleep(1/tick_speed)

    """
    Game Logic
    """
    def next_tick(self):
        self.tick_number += 1
        # Changing the traffic lights if the users doesn't wish to do it themselves, it loops through the states each
        # tick.
        if not self.manual:
            for intersection in self.intersections_dict:
                intersection_state_index = lights_data.light_states_inverse[
                    self.intersections_dict[intersection].direction
                ]
                # Highest state is 3, loop back to 0 if we reach it.
                intersection_state_index = (1 + intersection_state_index) % len(lights_data.light_states)
                self.intersections_dict[intersection].direction = lights_data.light_states[intersection_state_index]
        for car in self.car_list:
            if not self.headless:
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
                    # TODO: Fix this, cars hang randomly around corners, backing up and stacking.
                    #       Currently there is a hotfix in place. If you have time make sure this is fixed properly
                    # If the cars are going in opposite directions they may faze through each other.
                    if other_car.projected_x_direction * car.x_direction == -1 or \
                            other_car.projected_y_direction * car.y_direction == -1:
                        drive = True
                    # Some weird bug causes cars to hang and somehow this fixes it.
                    # I'll look into it if I have the time but for now this seems to work.
                    elif other_car.x_direction * car.x_direction == -1 or other_car.y_direction * car.y_direction == -1:
                        drive = True
                    elif car.projected_x_direction * other_car.x_direction == -1 \
                            or car.projected_y_direction * other_car.y_direction == -1:
                        drive = True
                    else:
                        if verbose_collisions:
                            print(colored("Collision on:", "blue"), colored(car.next_position(), "red"))
                            print(colored("Score:", "blue"), self.score)
                        drive = False
                        break
            if drive:
                for intersection in self.intersections_dict:    # Check if the car is approaching an intersection.
                    if len(intersection) > 1:
                        pass
                    elif car.next_position() == self.intersections_dict[intersection].coordinates:
                        if car.x_direction == self.intersections_dict[intersection].direction[0] and \
                           car.y_direction == self.intersections_dict[intersection].direction[1]:
                            drive = True
                        else:
                            drive = False
            if drive:
                self.score += WIN_REWARD
                brrr = car.drive()              # Sue me
                if brrr == "Arrived":
                    self.car_list.remove(car)   # If the car is at its destination we can remove the car from the field.
                else:
                    if not self.headless:
                        self.draw_car(car, CAR_COLOR)
            else:
                self.score -= LOSE_PUNISHMENT
                if not self.headless:
                    self.draw_car(car, CAR_COLOR)
        # Generate new cars.
        for _ in range(CAR_SPAWN_SIZE):
            if len(self.car_list) >= self.max_cars:
                break
            if random.randint(1, CAR_SPAWN_CHANCE) == 1:
                self.car_list.append(cars.Car())
        # Render application
        if not self.headless:
            pygame.event.get()                  # Prevents the application from freezing up on Windows.
            pygame.display.update()
        # Update statistics
        if self.statistics:
            self.tick_history.append(self.tick_number + self.tick_offset)
            self.score_history.append(self.score)
            self.car_amount_history.append(len(self.car_list))
            self.score_per_tick_history.append(self.score/self.tick_number)

    def action(self, light=None, direction=None, number=None):
        # Uncomment if your using itertools and have a better pc than me
        # if number is not None:
        #     action = list(self.possible_actions[number])    # get the traffic positions for that action
        #     for i in action:
        #         self.intersections_dict[lights_data.coordinates_keys[i]] = lights_data.light_states[i]
        if number is not None:
            light = number // 4
            position = number % 4
            self.intersections_dict[lights_data.coordinates_keys[light]].direction = lights_data.light_states[position]
        else:
            assert light is not None and direction is not None
            self.intersections_dict[light].direction = lights_data.light_states[direction]

    def reset(self):
        # remove cars from screen
        for car in self.car_list:
            if not self.headless:
                current_car_pos_x, current_car_pos_y = car.coordinates
                if (current_car_pos_x, current_car_pos_y) in [lights_data.coordinates["CB"],  # Crossings over which
                                                              lights_data.coordinates["BEH"],  # we have no control.
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
        # reset intersection direction
        for intersection in self.intersections_dict:
            self.intersections_dict[intersection].direction = lights_data.light_states[0]
        # Reset variables and update tick offset for statistics reasons
        self.tick_offset = self.tick_number + self.tick_offset
        self.tick_number = 0
        self.car_list = []
        self.score = 0

    """
    Statistics
    """
    def get_stats(self):
        if not self.statistics:
            print(colored("Error, statistics not enabled.", "red"))
            return None
        return {
            "Score": (self.tick_history, self.score_history),
            "Cars": (self.tick_history, self.car_amount_history),
            "Average score": (self.tick_history, self.score_per_tick_history)
        }
    """
    Game data
    """
    def get_game_data(self):
        data_list = []
        for car in self.car_list:
            # data_list.append(car.x_position, car.y_position, car.x_direction, car.y_direction)
            # This is a really, really bad solution. We need to represent the coordinates and direction in a single num
            data_list.append(np.dot(np.dot(car.x_position, car.y_position), np.dot(car.x_direction, car.y_direction)))
        while len(data_list) < self.max_cars:
            data_list.append(np.dot(np.dot(0, 0), np.dot(0, 0)))
        return np.array(data_list)

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
