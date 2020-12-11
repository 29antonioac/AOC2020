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

INPUT_URL = "https://adventofcode.com/2020/day/10/input"
INPUT_FILENAME = "input.txt"
# INPUT_FILENAME = "example_input.txt"
cookie = {"session": os.environ["session"]}

def parse_input(filename: str) -> List:
    with open(filename, "r") as f:
        raw_input = [int(l) for l in f.readlines()]

    return raw_input

# I am counting the number of ways to sum "ones" number of ones,
# in a way they don't sum more than 3
# Example for 4 ones:   1 1 1 1     # Just 1 way
#                       2 1 1       # Moving the "2" makes 3 ways
#                       3 1         # Moving the "3" makes 2 ways
#                       2 2         # Just 1 way
# so the inner_count(4) = 1 + 3 + 2 + 1 = 7
#
# I solved this by hand until n=6 but thanks to reddit I found out
# the function is Tribonacci
def count_arrangements(diffs: np.ndarray) -> int:
    @lru_cache(None)
    def inner_count(n: int) -> int:
        if n <= 2:
            return n
        elif n == 3:
            return 4
        else:
            return inner_count(n-1) + inner_count(n-2) + inner_count(n-3)

    # Get the number of contiguous "1" in the diffs of jolts
    # Example: [1,3,1,1,1,3,3]
    # Output: [1,3]
    ones = [len(l) for l in np.split(diffs, np.where(np.diff(diffs))[0] +1) if (l==1).all()]
    arrangements = [inner_count(o) for o in ones]
    return math.prod(arrangements)


####################################
if not os.path.exists(INPUT_FILENAME):
    success = download_input(INPUT_URL, INPUT_FILENAME, cookie)
    if not success: # This should be handled better
        exit(-1)

chargers = sorted(parse_input(INPUT_FILENAME))
np_chargers = np.array([0] + chargers + [chargers[-1] + 3])
diffs = np.diff(np_chargers)
unique, counts = np.unique(diffs, return_counts=True)
print(f"The product of 1-diffs and 3-diffs is {counts.prod()}")

arrangements = count_arrangements(diffs)
print(f"The number of arrangements is {arrangements}")
