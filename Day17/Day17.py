#!/usr/bin/env python

import os
import re
import sys
import math
import requests
import itertools

from timeit import default_timer as timer
from typing import List, Tuple, Dict, Set
from collections import Counter
from copy import deepcopy


sys.path.append("..")
from utils import download_input

INPUT_URL = "https://adventofcode.com/2020/day/17/input"
INPUT_FILENAME = "input.txt"
# INPUT_FILENAME = "example_input.txt"


INACTIVE = "."
ACTIVE = "#"

Point = Tuple[int, int, int]
Space = Set[Point]
def parse_input(filename: str, ndim: int=3) -> Space:
    with open(filename, "r") as f:
        raw_input = [list(l.strip()) for l in f.readlines()]

    space = set()
    # Assuming the input is just 2-D
    for x, row in enumerate(raw_input):
        for y, element in enumerate(row):
            if element == ACTIVE:
                space.add(tuple([x,y] + [0] * (ndim - 2)))

    return space

def total_active(space: Space) -> int:
    return len(space)

def iteration(space: Space) -> Space:
    to_add = set()
    to_keep = set()
    neighbour_counter = Counter()

    for p in space:
        for increment in itertools.product([0,1,-1], repeat=len(p)):
            if not any(increment):
                continue

            # Since being neighbour_counter is reflexive, I can count
            # how many neighbours have my neighbours
            q = tuple([i + inc for i, inc in zip(p, increment)])
            neighbour_counter[q] += 1
    to_keep = set([p for p in space if neighbour_counter[p] in [2,3]])
    to_add = set([p for p, count in neighbour_counter.items() if p not in space and count == 3])

    return to_add | to_keep

####################################
if not os.path.exists(INPUT_FILENAME):
    cookie = {"session": os.environ["session"]}
    success = download_input(INPUT_URL, INPUT_FILENAME, cookie)
    if not success: # This should be handled better
        exit(-1)

# # Part one
# # Result: 375
layouts = []
original_space = parse_input(INPUT_FILENAME)
space = deepcopy(original_space)
layouts.append(original_space)

for _ in range(6):
    new_space = iteration(layouts[-1])
    layouts.append(new_space)

n_active = total_active(layouts[-1])
print(f"First number of actives after 6 cycles are {n_active}")


# # Part two: same but 4-D
# # Result: 2227
layouts = []
original_space = parse_input(INPUT_FILENAME, ndim=4)
space = deepcopy(original_space)
layouts.append(original_space)

for _ in range(6):
    new_space = iteration(layouts[-1])
    layouts.append(new_space)

n_active = total_active(layouts[-1])
print(f"Second number of actives after 6 cycles are {n_active}")
