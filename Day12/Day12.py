#!/usr/bin/env python

import os
import re
import sys
import math
import requests
import itertools
import numpy as np

from timeit import default_timer as timer
from typing import List, Tuple, Dict
from collections import Counter

from scipy.special import comb
from functools import lru_cache

sys.path.append("..")
from utils import download_input

INPUT_URL = "https://adventofcode.com/2020/day/12/input"
INPUT_FILENAME = "input.txt"
# INPUT_FILENAME = "example_input.txt"
cookie = {"session": os.environ["session"]}


NORTH = "N"
SOUTH = "S"
EAST = "E"
WEST = "W"
LEFT = "L"
RIGHT = "R"
FORWARD = "F"

# First coordinate is X, second is Y, like in a map, not like in a matrix!
SLOPES = {
    EAST: [1,0],
    NORTH: [0,1],
    WEST: [-1,0],
    SOUTH: [0,-1]
}

# Directions in degrees
DIRECTIONS = {
    0: EAST,
    90: NORTH,
    180: WEST,
    270: SOUTH
}

DIRECTIONS_LR = {
    LEFT: 1,
    RIGHT: -1
}

def parse_input(filename: str) -> List:
    with open(filename, "r") as f:
        raw_input = [l.strip() for l in f.readlines()]

    instructions = [{"instruction": i[:1], "argument": int(i[1:])} for i in raw_input]

    return instructions


def manhattan_distance(p: List[int], q: List[int]) -> int:
    distance = 0
    for pn, qn in zip(p, q):
        distance += math.fabs(pn - qn)
    return distance

####################################
if not os.path.exists(INPUT_FILENAME):
    success = download_input(INPUT_URL, INPUT_FILENAME, cookie)
    if not success: # This should be handled better
        exit(-1)

instructions = parse_input(INPUT_FILENAME)

# Part one
starting_position = [0,0]
current_position = [0,0]
current_direction = 0

for i in instructions:
    instruction = i["instruction"]
    argument = i["argument"]

    if instruction in [LEFT, RIGHT]:
        current_direction = (current_direction + DIRECTIONS_LR[instruction] * argument) % 360 # It's a circle
        # print(f"New direction: {current_direction} -> {DIRECTIONS[current_direction]}")
    else:
        if instruction == FORWARD:
            instruction = DIRECTIONS[current_direction] # Change the instruction to the needed one
        if instruction in [NORTH, SOUTH, EAST, WEST]:
            # print(f"Going {instruction} by {argument} units")
            for idx in range(len(current_position)):
                current_position[idx] += argument * SLOPES[instruction][idx]
            # print(f"Current: {current_position}")

distance = manhattan_distance(starting_position, current_position)
print(f"First Manhattan distance is {distance}")

# Part two
starting_ship_position = [0,0]
current_ship_position = [0,0]

starting_waypoint_position = [10, 1]
current_waypoint_position = [10, 1]

COS = {
    0: 1,
    90: 0,
    180: -1,
    270: 0
}

SIN = {
    0: 0,
    90: 1,
    180: 0,
    270: -1
}

for i in instructions:
    instruction = i["instruction"]
    argument = i["argument"]

    if instruction in [LEFT, RIGHT]:
        theta = (DIRECTIONS_LR[instruction] * argument) % 360

        # Usual formulae to rotate a 2D vector
        px = current_waypoint_position[0] * COS[theta] - current_waypoint_position[1] * SIN[theta]
        py = current_waypoint_position[0] * SIN[theta] + current_waypoint_position[1] * COS[theta]
        current_waypoint_position = [px, py]

        # print(f"New waypoint position: {current_waypoint_position}")
    elif instruction == FORWARD:
        for idx in range(len(current_ship_position)):
            current_ship_position[idx] += argument * current_waypoint_position[idx]

        # print(f"New position: {current_ship_position}")
    elif instruction in [NORTH, SOUTH, EAST, WEST]:
        # print(f"Moving waypoint {instruction} by {argument} units")
        for idx in range(len(current_ship_position)):
            current_waypoint_position[idx] += argument * SLOPES[instruction][idx]
        # print(f"Current: {current_position}")

distance = manhattan_distance(starting_ship_position, current_ship_position)
print(f"Second Manhattan distance is {distance}")
