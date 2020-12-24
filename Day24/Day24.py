#!/usr/bin/env python

import os
import re
import sys
import math
import requests

from typing import List, Tuple, Dict, Set
from copy import deepcopy


sys.path.append("..")
from utils import download_input

INPUT_URL = "https://adventofcode.com/2020/day/24/input"
INPUT_FILENAME = "input.txt"
# INPUT_FILENAME = "example_input.txt"

nw = "nw"
ne = "ne"
w = "w"
e = "e"
sw = "sw"
se = "se"

DIRECTIONS = {  nw: (0,-1),
                ne: (1,-1),
                w: (-1,0),
                e: (1,0),
                sw: (-1,1),
                se: (0,1)}

COLOURS = {"black": 1,
            "white": 0}

Tile = Tuple[int,int]

##################################################
def parse_input(filename: str) -> Dict:
    with open(filename, "r") as f:
        rules = [re.findall("nw|ne|sw|se|e|w", l) for l in f.read().strip().split("\n")]

    return rules

def follow_rules(rules: List[List[str]]) -> Set[Tile]:
    current_tile = (0,0)
    # tiles = {current_tile: COLOURS["white"]}
    tiles = set()

    for tile in rules:
        current_tile = (0,0)
        for direction in tile:
            increment = DIRECTIONS[direction]
            current_tile = tuple([t+i for t,i in zip(current_tile, increment)])
            # if current_tile in tiles and tiles[current_tile] == COLOURS["black"]:
            #     print(f"{current_tile} was black, now white")
            # if current_tile not in tiles:
            #     tiles[current_tile] = COLOURS["white"]
        # print(f"Flipping {current_tile} to black")
        if current_tile not in tiles:
            tiles.add(current_tile)
        else:
            tiles.remove(current_tile)
        # tiles[current_tile] = COLOURS["black"] if tiles[current_tile] == COLOURS["white"] else COLOURS["white"]
        # print()

    return tiles

def evolve(original_tiles: Dict[Tile, int], n_times: int) -> Dict[Tile, int]:
    tiles = deepcopy(original_tiles)
    return





####################################
if not os.path.exists(INPUT_FILENAME):
    cookie = {"session": os.environ["session"]}
    success = download_input(INPUT_URL, INPUT_FILENAME, cookie)
    if not success: # This should be handled better
        exit(-1)

rules = parse_input(INPUT_FILENAME)
tiles = follow_rules(rules)

# black_tiles = sum([c for c in tiles.values() if c == COLOURS["black"]])
black_tiles = len(tiles)
print(f"The sum of black tiles is {black_tiles}")
