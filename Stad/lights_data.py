distances = {
    "A": {"B": 775, "K": 1150},
    "B": {"A": 775, "I": 430, "CB": 1275},
    "C": {"D": 570, "CB": 850},
    "D": {"C": 570, "E": 650},
    "E": {"D": 650, "F": 720, "BEH": 400},
    "F": {"E": 720, "G": 880},
    "G": {"F": 880, "O": 390, "H": 75},
    "H": {"G": 75, "BEH": 675, "I": 1160},
    "I": {"B": 430, "IPJ": 430, "H": 1160},
    "J": {"L": 2000, "K": 980, "IPJ": 470},
    "K": {"J": 980, "A": 1150},
    "L": {"J": 2000, "M": 1125},
    "M": {"L": 1125, "P": 440, "N": 475},
    "N": {"O": 195, "M": 475},
    "O": {"G": 390, "P": 275, "N": 195},
    "P": {"O": 275, "M": 440, "IPJ": 1280},
    # Crossings over which we have no control.
    "CB": {"C": 850, "BEH": 575, "B": 1275},
    "BEH": {"CB": 575, "E": 400, "H": 675, "B": 1100},
    "IPJ": {"I": 430, "P": 1280, "J": 470}
}

distances_with_corners = {
    "A": {"B": 19, "A-K_A": 23},
    "B": {"A": 19, "I": 11, "CB-B_A": 9, "B-BEH_A": 5},
    "C": {"D": 14, "CB": 21},
    "D": {"C": 14, "E-D_D": 5},
    "E": {"E-D_A": 3, "F": 18, "BEH": 9}, 
    "F": {"E": 18, "G-F_A": 16},
    "G": {"H": 2, "G-O_A": 4, "G-F_A": 6},
    "H": {"G": 2, "BEH-H_A": 7, "I-H_C": 8},
    "I": {"B": 11, "IPJ": 10, "I-H_A": 9},
    "J": {"K-J_A": 20, "IPJ": 12, "J-L_A": 38},
    "K": {"A-K_A": 6, "K-J_A": 5},
    "L": {"J-L_A": 13, "M-L_A": 15},
    "M": {"M-L_A": 13, "P": 11, "N-M_A": 7},
    "N": {"N-M_A": 5, "O": 5},
    "O": {"N": 5, "P": 7, "G-O_A": 6},
    "P": {"O": 7, "M": 11, "IPJ-P_C": 17},
    "CB": {"C": 21, "BEH": 14, "CB-B_A": 22}, 
    "BEH": {"E": 9, "CB": 14, "BEH-H_A": 10, "B-BEH_B": 17}, 
    "IPJ": {"I": 10, "J": 12, "IPJ-P_A": 8},
    "E-D_A": {"E-D_B": 2, "E": 3}, 
    "E-D_B": {"E-D_C": 4, "E-D_A": 2}, 
    "E-D_C": {"E-D_D": 2, "E-D_B": 4}, 
    "E-D_D": {"D": 5, "E-D_C": 2},
    "BEH-H_A": {"BEH": 10, "H": 7},
    "G-F_A": {"G": 6, "F": 16},
    "G-O_A": {"O": 6, "G": 4},
    "B-BEH_A": {"B": 5, "B-BEH_B": 5},
    "B-BEH_B": {"BEH": 17, "B-BEH_A": 5},
    "I-H_A": {"I": 9, "I-H_A": 7},
    "I-H_B": {"I-H_C": 5, "I-H_A": 7},
    "I-H_C": {"H": 8, "I-H_B": 5},
    "M-L_A": {"L": 15, "M": 13},
    "IPJ-P_A": {"IPJ": 8, "IPJ-P_B": 3},
    "IPJ-P_B": {"IPJ-P_C": 4, "IPJ-P_A": 3},
    "IPJ-P_C": {"P": 17, "IPJ-P_B": 4},
    "CB-B_A": {"CB": 22, "B": 9}, 
    "J-L_A": {"J": 38, "L": 13},
    "A-K_A": {"B": 23, "K": 6},
    "K-J_A": {"K": 5, "J": 20},
    "N-M_A": {"M": 17, "N": 5}
}

coordinates = {
    "A": (9, 62),
    "B": (9, 43),
    "C": (0, 0),
    "D": (14, 0),
    "E": (14, 12),
    "F": (32, 12),
    "G": (26, 28),
    "H": (24, 28),
    "I": (20, 43),
    "J": (20, 65),
    "K": (15, 85),
    "L": (58, 52),
    "M": (43, 39),
    "N": (37, 32),
    "O": (32, 32),
    "P": (32, 39),
    # Crossings over which we have no control.
    "CB": (0, 21),
    "BEH": (14, 21),
    "IPJ": (20, 53)
}

corners = {
    "E-D": {"E-D_A": (14, 9), "E-D_B": (12, 9), "E-D_C": (12, 5), "E-D_D": (14, 5)},
    "BEH-H": {"BEH-H_A": (24, 21)},
    "G-F": {"G-F_A": (32, 28)},
    "G-O": {"G-O_A": (26, 32)},
    "B-BEH": {"B-BEH_A": (9, 38), "B-BEH_B": (14, 38)},
    "I-H": {"I-H_A": (29, 43), "I-H_B": (29, 36), "I-H_C": (24, 36)},
    "M-L": {"M-L_A": (43, 52)},
    "IPJ-P": {"IPJ-P_A": (28, 53), "IPJ-P_B": (28, 56), "IPJ-P_C": (32, 56)},
    "CB-B": {"CB-B_A": (0, 43)},
    "J-L": {"J-L_A": (58, 65)},
    "A-K": {"A-K_A": (9, 85)},
    "K-J": {"K-J_A": (20, 85)},
    "N-M": {"N-M_A": (43, 32)},
    # Roads without corners
    "C-D": {},
    "C-CB": {},
    "E-F": {},
    "E-BEH": {},
    "BEH-CB": {},
    "B-I": {},
    "B-A": {},
    "M-P": {},
    "O-N": {},
    "O-P": {},
    "I-IPJ": {},
    "J-IPJ": {},
    "H-G": {}
}

intersection_and_corner_coordinates = coordinates.copy()
for road in corners:
    for corner in corners[road]:
        intersection_and_corner_coordinates[corner] = corners[road][corner]

starting_points = [
    "A",
    "C",
    "D",
    "F",
    "K",
    "L",
    "N"
]

destinations = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P"
]

light_states = {
    0: (1, 0),
    1: (-1, 0),
    2: (0, 1),
    3: (0, -1)
}

light_states_inverse = dict((v, k) for k, v in light_states.items())
