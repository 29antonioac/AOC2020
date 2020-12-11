#!/usr/bin/env python

import os
import re
import sys
import math
import requests
import itertools

from timeit import default_timer as timer
from typing import List, Tuple, Dict
from collections import Counter
from copy import deepcopy


sys.path.append("..")
from utils import download_input

INPUT_URL = "https://adventofcode.com/2020/day/11/input"
INPUT_FILENAME = "input.txt"
# INPUT_FILENAME = "example_input.txt"
cookie = {"session": os.environ["session"]}

EMPTY = "L"
OCCUPIED = "#"
FLOOR = "."

Seat_Layout = List[List[str]]
def parse_input(filename: str) -> Seat_Layout:
    with open(filename, "r") as f:
        raw_input = [list(l.strip()) for l in f.readlines()]

    return raw_input

def total_occupations(seat_layout: Seat_Layout) -> int:
    n_occupations = 0
    for row in range(len(seat_layout)):
        for col in range(len(seat_layout[row])):
            if seat_layout[row][col] == OCCUPIED:
                n_occupations += 1
    return n_occupations

def adjacent_occupations(seat_layout: Seat_Layout, row: int, col: int, distance: bool=False) -> int:
    n_occupations = 0

    for inc_row, inc_col in itertools.product([0,1,-1], repeat=2):
        if inc_row == 0 and inc_col == 0:
            continue

        check_row = row + inc_row
        check_col = col + inc_col
        # This should have been handled better!
        if not distance:
            if 0 <= check_row < len(seat_layout) and 0 <= check_col < len(seat_layout[check_row]):
                if seat_layout[check_row][check_col] == OCCUPIED:
                    n_occupations += 1
        else:
            multiplier = 1
            while 0 <= check_row < len(seat_layout) and 0 <= check_col < len(seat_layout[check_row]):
                # print(f"Multiplier {multiplier}")
                # print(f"Checking {check_row},{check_col}")
                # print()
                if seat_layout[check_row][check_col] == OCCUPIED:
                    n_occupations += 1
                    break # To get just the closest one
                elif seat_layout[check_row][check_col] == EMPTY:
                    break # To get just the closest one
                elif check_row == 0 and check_col == 0:
                    break
                else:
                    multiplier += 1
                    check_row = row + inc_row * multiplier
                    check_col = col + inc_col * multiplier

    return n_occupations

def iteration(seat_layout: Seat_Layout, distance: bool=False, max_occupied: int=4) -> Seat_Layout:
    new_seat_layout = deepcopy(seat_layout)

    # All the comparisons will be made in the original one,
    # but the changes will be made in the new one

    for row in range(len(seat_layout)):
        for col in range(len(seat_layout[row])):
            if seat_layout[row][col] == EMPTY and adjacent_occupations(seat_layout, row, col, distance) == 0:
                # print(f"{row},{col} being occupied")
                new_seat_layout[row][col] = OCCUPIED
            elif seat_layout[row][col] == OCCUPIED and adjacent_occupations(seat_layout, row, col, distance) >= max_occupied:
                # print(f"{row},{col} being empty")
                new_seat_layout[row][col] = EMPTY

    return new_seat_layout

####################################
if not os.path.exists(INPUT_FILENAME):
    success = download_input(INPUT_URL, INPUT_FILENAME, cookie)
    if not success: # This should be handled better
        exit(-1)

# Part one: no distance criteria and 4 as max occupancy
# Result: 2481
layouts = []
original_seat_layout = parse_input(INPUT_FILENAME)
seat_layout = deepcopy(original_seat_layout)
layouts.append(seat_layout)

n_iterations = 1
new_seat_layout = iteration(seat_layout)
layouts.append(new_seat_layout)

while seat_layout != new_seat_layout:
    seat_layout = deepcopy(new_seat_layout)
    new_seat_layout = iteration(seat_layout)
    n_iterations += 1
    layouts.append(new_seat_layout)

n_occupations = total_occupations(seat_layout)
print(f"First Steady occupations are {n_occupations}")

# Part two: distance criteria and 5 as max occupancy

layouts = []
seat_layout = deepcopy(original_seat_layout)
layouts.append(seat_layout)

n_iterations = 1
new_seat_layout = iteration(seat_layout, distance=True, max_occupied=5)
layouts.append(new_seat_layout)

while seat_layout != new_seat_layout:
    seat_layout = deepcopy(new_seat_layout)
    new_seat_layout = iteration(seat_layout, distance=True, max_occupied=5)
    n_iterations += 1
    layouts.append(new_seat_layout)

n_occupations = total_occupations(seat_layout)
print(f"Second Steady occupations are {n_occupations}")
