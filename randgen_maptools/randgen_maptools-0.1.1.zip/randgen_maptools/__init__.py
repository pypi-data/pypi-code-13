# -*- coding: utf-8 -*-
import random


__author__ = 'Dan Alexander'
__email__ = 'lxndrdagreat@gmail.com'
__version__ = '0.1.1'


def coord_to_1d_index(x, y, width):
    """
    Returns the 1 dimensional array index for the given x/y coordinate and
    map width.
    """
    return y * width + x


def generate_square(width, height, wall=1, floor=0):
    data = [floor] * (width * height)

    for y in range(0, height):
        for x in range(0, width):
            if y == 0 or y == height - 1 or x == 0 or x == width - 1:
                data[coord_to_1d_index(x, y, width)] = wall

    return data


def default_map_ascii(value):

    # wall
    if value == 1:
        return "#"

    # road
    elif value == 2:
        return "%"

    # tree
    elif value == 3:
        return "T"

    # water
    elif value == 4:
        return "~"

    # stair up
    elif value == 5:
        return "<"

    # stair down
    elif value == 6:
        return ">"

    # default is floor (empty)
    return "."


def print_map_data(width, height, map_data):
    for y in range(0, height):
        row = ""
        for x in range(0, width):
            tile = map_data[coord_to_1d_index(x, y, width)]
            row += default_map_ascii(tile)
        print(row)


# Creates a clump ;)
def generate_clump(max_width, max_height, iterations):

    clump = generate_square(max_width, max_height, 0, 0)

    center_x = int(max_width / 2)
    center_y = int(max_height / 2)

    i = center_x
    j = center_y

    for k in range(0, iterations):
        n = random.randint(1, 6)
        e = random.randint(1, 6)
        s = random.randint(1, 6)
        w = random.randint(1, 6)

        if n == 1 and i > 0:
            i = i - 1
            clump[coord_to_1d_index(i, j, max_width)] = 1
        if s == 1 and i < max_height - 1:
            i = i + 1
            clump[coord_to_1d_index(i, j, max_width)] = 1
        if e == 1 and j < max_width - 1:
            j = j + 1
            clump[coord_to_1d_index(i, j, max_width)] = 1
        if w == 1 and j > 0:
            j = j - 1
            clump[coord_to_1d_index(i, j, max_width)] = 1    

    return clump


# Returns True if given x/y is within two other points
def coord_is_within(x, y, bx, by, bx2, by2):
    return x >= bx and x <= bx2 and y >= by and y <= by2