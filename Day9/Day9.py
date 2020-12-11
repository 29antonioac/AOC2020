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


sys.path.append("..")
from utils import download_input

INPUT_URL = "https://adventofcode.com/2020/day/9/input"
INPUT_FILENAME = "input.txt"
# INPUT_FILENAME = "example_input.txt"
cookie = {"session": os.environ["session"]}

#https://stackoverflow.com/questions/6822725/rolling-or-sliding-window-iterator
def window(seq, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(itertools.islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result

# Trying to get a dict
# {"light red bags": {"bright white bag": 1, "muted yellow bags": 2}}
def parse_input(filename: str) -> List:
    with open(filename, "r") as f:
        raw_input = [int(l) for l in f.readlines()]

    return raw_input

def first_bad_number(numbers: List, preamble_size: int=5) -> int:
    def check(number: int, preamble: List, n: int=2) -> bool:
        # print(f"Checking {number} and {preamble}")
        for c in itertools.combinations(preamble, n):
            # print(c)
            if sum(c) == number:
                return True
        return False

    first_bad = preamble_size
    good = True
    while first_bad < len(numbers) and good:
        # print(first_bad)
        good = check(numbers[first_bad], numbers[first_bad - preamble_size:first_bad])
        if not good:
            print(f"{first_bad} -> {numbers[first_bad]} is not the sum of {numbers[first_bad - preamble_size:first_bad]}")
        else:
            first_bad += 1

    return first_bad

def sum_limits_contiguous_sum(numbers: List, number: int) -> int:
    window_size = range(2, len(numbers))
    for ws in window_size:
        for w in window(numbers, n=ws):
            if sum(w) == number:
                print(f"Window size = {ws}, window = {w}")
                return min(w) + max(w)
    return None


####################################
if not os.path.exists(INPUT_FILENAME):
    success = download_input(INPUT_URL, INPUT_FILENAME, cookie)
    if not success: # This should be handled better
        exit(-1)

numbers = parse_input(INPUT_FILENAME)
first_bad = first_bad_number(numbers, preamble_size=25)
print(f"The first bad is {first_bad} -> {numbers[first_bad]}")

sum_limits = sum_limits_contiguous_sum(numbers, numbers[first_bad])
print(f"The sum limit is {sum_limits}")
