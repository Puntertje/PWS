class Road:
    def __init__(self, intersection_dict, corner_dict, name=""):
        self.intersection_coordinate_dict = intersection_dict
        self.corner_coordinate_dict = corner_dict
        self.name = name
        self.road_coordinate_list = []
        self.generate_road_coordinates()

    def generate_road_coordinates(self):
        total_list = {**self.intersection_coordinate_dict, **self.corner_coordinate_dict}   # Wack
        for corner in total_list:
            x, y = total_list[corner]
            for corner_candidate in total_list:
                if corner_candidate != corner:  # Don't want a road to itself.
                    x_can, y_can = total_list[corner_candidate]
                    # Yes, I know this is spaget, if you have an alternative suggestion please lmk
                    if x_can == x and y_can != y:
                        if y_can < y:
                            road_coordinate = y_can + 1
                            while True:
                                self.road_coordinate_list.append(tuple((x, road_coordinate)))
                                road_coordinate += 1
                                if road_coordinate == y:
                                    break
                        if y < y_can:
                            road_coordinate = y + 1
                            while True:
                                self.road_coordinate_list.append(tuple((x, road_coordinate)))
                                road_coordinate += 1
                                if road_coordinate == y_can:
                                    break
                    if x_can != x and y_can == y:
                        if x_can < x:
                            road_coordinate = x_can + 1
                            while True:
                                self.road_coordinate_list.append(tuple((road_coordinate, y)))
                                road_coordinate += 1
                                if road_coordinate == x:
                                    break
                        if x < x_can:
                            road_coordinate = x + 1
                            while True:
                                self.road_coordinate_list.append(tuple((road_coordinate, y)))
                                road_coordinate += 1
                                if road_coordinate == x_can:
                                    break
