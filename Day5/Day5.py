#!/usr/bin/env python

import os
import sys
import abc
import math
import requests
import itertools

from timeit import default_timer as timer
from typing import List, Tuple, Dict


sys.path.append("..")
from utils import download_input

INPUT_URL = "https://adventofcode.com/2020/day/5/input"
INPUT_FILENAME = "input.txt"
# INPUT_FILENAME = "example_invalid_passports.txt"
cookie = {"session": os.environ["session"]}

def process_boarding_pass(boarding_pass: str, params: Dict) -> None:
    def length(lower, upper):
        return upper - lower + 1

    # First part
    lower_limit = 0
    upper_limit = 127
    interval_length = length(lower_limit, upper_limit)
    for letter in boarding_pass[:7]:
        half_interval = interval_length / 2
        if letter == "F":
            upper_limit -= half_interval
        elif letter == "B":
            lower_limit += half_interval
        else:
            raise ValueError(f"[First part] Some letter is not expected: {letter}")
        interval_length = length(lower_limit, upper_limit)

    if lower_limit != upper_limit:
        raise ValueError(f"[First part] Limits are not equal: {lower_limit}-{upper_limit}")

    params["row"] = lower_limit

    # Second part
    lower_limit = 0
    upper_limit = 7
    interval_length = length(lower_limit, upper_limit)
    for letter in boarding_pass[7:]:
        half_interval = interval_length / 2
        if letter == "L":
            upper_limit -= half_interval
        elif letter == "R":
            lower_limit += half_interval
        else:
            raise ValueError(f"[Second part] Some letter is not expected: {letter}")
        interval_length = length(lower_limit, upper_limit)

    if lower_limit != upper_limit:
        raise ValueError(f"[Second part] Limits are not equal: {lower_limit}-{upper_limit}")

    params["column"] = lower_limit
    params["ID"] = params["row"] * 8 + params["column"]


def parse_input(filename: str) -> Dict:
    with open(filename, "r") as f:
        input_list = [i.strip() for i in f.readlines()]

    boarding_pass_dict = {i: {} for i in input_list}
    return boarding_pass_dict



if not os.path.exists(INPUT_FILENAME):
    success = download_input(INPUT_URL, INPUT_FILENAME, cookie)
    if not success: # This should be handled better
        exit(-1)

boarding_pass_dict = parse_input(INPUT_FILENAME)

for boarding_pass, params in boarding_pass_dict.items():
    process_boarding_pass(boarding_pass, params)

ID_list = [params["ID"] for boarding_pass, params in boarding_pass_dict.items()]
print(f"Highest ID is {max(ID_list)}")

my_seat = 0
for ID in sorted(ID_list)[1:-1]:
    if ID+1 not in ID_list:
        my_seat = ID+1

print(f"My seat is {my_seat}")
