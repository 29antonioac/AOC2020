#!/usr/bin/env python

import os
import re
import sys
import math
import requests
import itertools

from timeit import default_timer as timer
from typing import List, Tuple, Dict, DefaultDict
from collections import Counter
from copy import deepcopy


sys.path.append("..")
from utils import download_input

INPUT_URL = "https://adventofcode.com/2020/day/17/input"
INPUT_FILENAME = "input.txt"
INPUT_FILENAME = "example_input.txt"


INACTIVE = "."
ACTIVE = "#"
O_INACTIVE = "0"
O_ACTIVE = "%"

Point = Tuple[int, int, int]
Space = Set[Point]
def parse_input(filename: str) -> Space:
    with open(filename, "r") as f:
        raw_input = [list(l.strip()) for l in f.readlines()]

    space = Space(lambda: INACTIVE)
    # Assuming the input is just 2-D
    for y, row in enumerate(raw_input):
        for x, element in enumerate(row):
            space[(x,y,0)] = element
            space[(x,y,-1)] = INACTIVE
            space[(x,y,1)] = INACTIVE

    return space

def draw(space: Space) -> str:
    drawing = ""

    all_x = sorted(list(set([x for x,y,z in space.keys()])))
    all_y = sorted(list(set([y for x,y,z in space.keys()])))
    all_z = sorted(list(set([z for x,y,z in space.keys()])))
    for z in all_z:
        drawing += f"{z=}\n\n"
        for y in all_y:
            for x in all_x:
                p = (x,y,z)
                if x != 0 or y != 0:
                    drawing += space[p]
                else:
                    if space[p] == INACTIVE:
                        drawing += O_INACTIVE
                    else:
                        drawing += O_ACTIVE
            drawing += "\n"
        drawing += "\n\n"
    return drawing

def total_active(space: Space) -> int:
    n_active = 0
    for p, state in space.items():
        if state == ACTIVE:
            n_active += 1
    return n_active

def adjacent_active(space: Space, p: Point, distance: bool=False) -> int:
    n_active = 0
    check_space = deepcopy(space)

    for increment in itertools.product([0,1,-1], repeat=len(p)):
        if not any(increment):
            continue

        q = tuple([i + inc for i, inc in zip(p, increment)])
        # This should have been handled better!
        if not distance:
            # print(f"{q} -> {check_space[q]}")
            if check_space[q] == ACTIVE:
                n_active += 1
        # else:
        #     multiplier = 1
        #     while 0 <= check_x < len(space) and 0 <= check_y < len(space[check_x]):
        #         # print(f"Multiplier {multiplier}")
        #         # print(f"Checking {check_x},{check_y}")
        #         # print()
        #         if space[check_x][check_y] == ACTIVE:
        #             n_active += 1
        #             break # To get just the closest one
        #         elif space[check_x][check_y] == INACTIVE:
        #             break # To get just the closest one
        #         elif check_x == 0 and check_y == 0:
        #             break
        #         else:
        #             multiplier += 1
        #             check_x = x + inc_x * multiplier
        #             check_y = y + inc_y * multiplier

    return n_active, check_space

def iteration(space: Space, distance: bool=False, max_active: int=4) -> Space:
    to_change = dict()

    # All the comparisons will be made in the original one,
    # but the changes will be made in the new one

    for p, element in space.items():
        adj_active, new_space = adjacent_active(space, p, distance)
        if element == INACTIVE and adj_active == 3:
            # print(f"{x},{y} being ACTIVE")
            to_change[p] = ACTIVE
        elif element == ACTIVE and adj_active not in [2,3]:
            # print(f"{x},{y} being INACTIVE")
            to_change[p] = INACTIVE
    print(to_change)
    for p, element in to_change.items():
        new_space[p] = element

    return new_space

####################################
if not os.path.exists(INPUT_FILENAME):
    cookie = {"session": os.environ["session"]}
    success = download_input(INPUT_URL, INPUT_FILENAME, cookie)
    if not success: # This should be handled better
        exit(-1)

# # Part one: no distance criteria and 4 as max occupancy
# # Result: 2481
layouts = []
original_space = parse_input(INPUT_FILENAME)
space = deepcopy(original_space)
layouts.append(original_space)

print(draw(space))

print("-----")

n_iterations = 1
new_space = iteration(space)
layouts.append(new_space)

print(draw(new_space))


# for i in range(6):
#     space = deepcopy(new_space)
#     new_space = iteration(space)
#     n_iterations += 1
#     layouts.append(new_space)
#
# n_active = total_active(space)
# print(f"First active after 6 cycles are {n_active}")
#
# # Part two: distance criteria and 5 as max occupancy
# # Result: 2227
# layouts = []
# space = deepcopy(original_space)
# layouts.append(space)
#
# n_iterations = 1
# new_space = iteration(space, distance=True, max_active=5)
# layouts.append(new_space)
#
# while space != new_space:
#     space = deepcopy(new_space)
#     new_space = iteration(space, distance=True, max_active=5)
#     n_iterations += 1
#     layouts.append(new_space)
#
# n_active = total_active(space)
# print(f"Second Steady occupations are {n_active}")
