#!/usr/bin/env python

import os
import sys
import abc
import math
import requests
import itertools

from timeit import default_timer as timer
from typing import List, Tuple, Dict
from collections import Counter


sys.path.append("..")
from utils import download_input

INPUT_URL = "https://adventofcode.com/2020/day/6/input"
INPUT_FILENAME = "input.txt"
# INPUT_FILENAME = "example_input.txt"
cookie = {"session": os.environ["session"]}

def process_boarding_pass(boarding_pass: str, params: Dict) -> None:
    pass


def parse_input(filename: str) -> str:
    with open(filename, "r") as f:
        raw_input = f.read().strip()

    return raw_input



if not os.path.exists(INPUT_FILENAME):
    success = download_input(INPUT_URL, INPUT_FILENAME, cookie)
    if not success: # This should be handled better
        exit(-1)

raw_input = parse_input(INPUT_FILENAME)

# First part: count the sum of different letters for all groups
count_per_group = [len(set(ii)) for ii in raw_input.replace("\n\n", "\t").replace("\n", "").split("\t")]
print(f"The first sum is {sum(count_per_group)}")

# Second part: count the sum of common letters for all groups
groups = [g.split("\n") for g in raw_input.split("\n\n")]
len_groups = [len(g) for g in groups]
groups_processed = ["".join(g) for g in groups]
counters = [list(Counter(g).values()) for g in groups_processed]


count_per_group = [g.count(l) for g, l in zip(counters, len_groups)]
print(f"The second sum is {sum(count_per_group)} ")
