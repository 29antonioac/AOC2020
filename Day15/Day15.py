#!/usr/bin/env python

import os
import re
import sys
import math
import requests
import itertools
import functools

from timeit import default_timer as timer
from typing import List, Tuple, Dict
from collections import Counter


sys.path.append("..")
from utils import download_input

INPUT_URL = "https://adventofcode.com/2020/day/15/input"
INPUT_FILENAME = "input.txt"
# INPUT_FILENAME = "example_input.txt"
# INPUT_FILENAME = "example_input_2.txt"

def parse_input(filename: str) -> Dict:
    with open(filename, "r") as f:
        raw_input = [int(i) for i in f.read().strip().split(",")]

    return raw_input
####################################

# This modifies the input list and returns the last one
# This could have been done better, maybe we just need to store the last
# one and not the two previous? The last one should be the current one...
def memory_game(numbers: List[int], limit: int=2020) -> int:
    indexes = {n: [idx] for idx, n in enumerate(numbers)}
    new_number = numbers[-1]

    for turn in range(len(numbers), limit):
        current_number = new_number
        current_indexes = indexes[current_number]
        if len(current_indexes) >= 2:
            new_number = current_indexes[-1] - current_indexes[-2]
            if new_number in indexes:
                indexes[new_number].append(turn)
                indexes[new_number] = indexes[new_number][-2:]
            else:
                indexes[new_number] = [turn]
        else:
            new_number = 0
            indexes[new_number].append(turn)
            indexes[new_number] = indexes[new_number][-2:]

    return new_number


####################################
if not os.path.exists(INPUT_FILENAME):
    cookie = {"session": os.environ["session"]}
    success = download_input(INPUT_URL, INPUT_FILENAME, cookie)
    if not success: # This should be handled better
        exit(-1)

numbers = parse_input(INPUT_FILENAME)
last_number = memory_game(numbers, limit=2020)
print(f"The 2020th number is {numbers[-1]} == {last_number}")

last_number = memory_game(numbers, limit=30000000)
print(f"The 30000000th number is {numbers[-1]} == {last_number}")
