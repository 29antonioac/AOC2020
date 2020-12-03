#!/usr/bin/env python

import os
import abc
import math
import requests
import itertools

from timeit import default_timer as timer
from typing import List, Tuple
from collections import Counter

INPUT_URL = "https://adventofcode.com/2020/day/3/input"
INPUT_FILENAME = "input.txt"
# INPUT_FILENAME = "example_input.txt"
cookie = {"session": os.environ["session"]}

class TravelMap(object):
    def __init__(self, travelmap: List[List[bool]]):
        self.map = travelmap

    def shape(self) -> Tuple[int, int]:
        return len(self.map), len(self.map[0])

    def check(self, row: int, col: int) -> bool:
        return self.map[row][col]

def download_input(url: str, filename: str) -> bool:
    try:
        r = requests.get(url, cookies=cookie)
        with open(filename, "w") as f:
            f.write(r.text)
    except:
        print(f"Something happened")
        return False
    return True

def parse_input(filename: str) -> TravelMap:
    with open(filename, "r") as f:
        travelmap = [[(True if s == "#" else False) for s in list(line)] for line in f]
    return TravelMap(travelmap)


if not os.path.exists(INPUT_FILENAME):
    success = download_input(INPUT_URL, INPUT_FILENAME)
    if not success: # This should be handled better
        exit(-1)

travelmap = parse_input(INPUT_FILENAME)
map_shape = travelmap.shape()

# Part one: single slope
slope = (1, 3)
coordinates_generator = ((y, x % (map_shape[1] - 1)) for y, x in zip(range(0, travelmap.shape()[0], slope[0]), itertools.count(step=slope[1])) )

is_tree = [travelmap.check(row, col) for row, col in coordinates_generator]
n_trees = sum(is_tree)
print(f"Number of trees: {n_trees}")

# Part two: list of slopes, multiplying all the results
slopes = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]
total_n_trees = []
for slope in slopes:
    coordinates_generator = ((y, x % (map_shape[1] - 1)) for y, x in zip(range(0, travelmap.shape()[0], slope[0]), itertools.count(step=slope[1])) )

    is_tree = [travelmap.check(row, col) for row, col in coordinates_generator]
    n_trees = sum(is_tree)
    total_n_trees.append(n_trees)
    print(f"Number of trees with slope {slope}: {n_trees}")
print(f"Product of all number of trees: {math.prod(total_n_trees)}")
