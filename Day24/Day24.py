#!/usr/bin/env python

import os
import re
import sys
import math
import requests

from collections import Counter
from typing import List, Tuple, Dict, Set
from copy import deepcopy


sys.path.append("..")
from utils import download_input

INPUT_URL = "https://adventofcode.com/2020/day/24/input"
INPUT_FILENAME = "input.txt"
# INPUT_FILENAME = "example_input.txt"

DIRECTIONS = {  "nw": (0,-1),
                "ne": (1,-1),
                "w": (-1,0),
                "e": (1,0),
                "sw": (-1,1),
                "se": (0,1)}


Tile = Tuple[int,int]

##################################################
def parse_input(filename: str) -> Dict:
    with open(filename, "r") as f:
        rules = [re.findall("nw|ne|sw|se|e|w", l) for l in f.read().strip().split("\n")]

    return rules

def follow_rules(rules: List[List[str]]) -> Set[Tile]:
    current_tile = (0,0)
    tiles = set()

    for tile in rules:
        current_tile = (0,0)
        for direction in tile:
            increment = DIRECTIONS[direction]
            current_tile = tuple([t+i for t,i in zip(current_tile, increment)])

        if current_tile not in tiles:
            tiles.add(current_tile)
        else:
            tiles.remove(current_tile)

    return tiles

def evolve(original_tiles: Dict[Tile, int], n_times: int) -> Dict[Tile, int]:
    def get_neighbours(tile: Tile):
        # This could have been done with zip, too, as above
        neighbours = [(tile[0] + inc[0], tile[1] + inc[1]) for inc in DIRECTIONS.values()]
        return neighbours

    tiles = deepcopy(original_tiles)
    for _ in range(n_times):
        neighbour_counter = Counter()

        to_remove = set()
        to_add = set()

        # Same approach as Day17: count the neighbours of my neighbours
        for t in tiles:
            for neighbour in get_neighbours(t):
                neighbour_counter[neighbour] += 1

        to_remove = set([t for t in tiles if neighbour_counter[t] == 0 or neighbour_counter[t] > 2])
        to_add = set([t for t,c in neighbour_counter.items() if t not in tiles and neighbour_counter[t] == 2])

        tiles = tiles.union(to_add) - to_remove

    return tiles

####################################
if not os.path.exists(INPUT_FILENAME):
    cookie = {"session": os.environ["session"]}
    success = download_input(INPUT_URL, INPUT_FILENAME, cookie)
    if not success: # This should be handled better
        exit(-1)

rules = parse_input(INPUT_FILENAME)

# Part one
tiles = follow_rules(rules)

black_tiles = len(tiles)
print(f"The sum of black tiles is {black_tiles}")

# Part two
n_times = 100
final_tiles = evolve(tiles, n_times=n_times)
final_black_tiles = len(final_tiles)
print(f"The sum of black tiles after {n_times} days is {final_black_tiles}")
