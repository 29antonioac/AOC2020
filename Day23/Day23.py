#!/usr/bin/env python

import os
import re
import sys
import math
import requests
import itertools
import functools

from typing import List, Tuple, Dict, Set
from copy import deepcopy


sys.path.append("..")
from utils import download_input

INPUT_URL = "https://adventofcode.com/2020/day/22/input"
INPUT_STR = "389547612"
# INPUT_STR = "389125467"

##################################################
def parse_input(numbers: str) -> Dict:
    return [int(i) for i in numbers]

@functools.cache
def move(original_numbers: Tuple[int], current: int) -> List[int]:
    numbers = list(original_numbers)
    # print(f"cups: {numbers}")
    # print(f"current: {current}")
    current_idx = numbers.index(current)
    picked = [numbers[(current_idx + 1) % len(numbers)],
                numbers[(current_idx + 2) % len(numbers)],
                numbers[(current_idx + 3) % len(numbers)]]
    for p in picked:
        numbers.pop(numbers.index(p))
    # print(f"pick up: {picked}")
    destination_idx = None
    destination_number = current - 1
    # print(f"May I have destination {destination_number}?")
    while (destination_idx is None) or destination_number in picked:
        # print(f"{destination_idx} -> {destination_number}")
        try:
            destination_idx = numbers.index(destination_number)
        except:
            if destination_number < 0:
                destination_number = max(numbers)
            else:
                destination_number = destination_number - 1
            # print(f"May I have destination {destination_number}?")
    # print(f"destination: {destination_number}")

    numbers.insert(destination_idx + 1, picked[0])
    numbers.insert(destination_idx + 2, picked[1])
    numbers.insert(destination_idx + 3, picked[2])
    new_current = numbers[(numbers.index(current) + 1) % len(numbers)]
    return numbers, new_current

def play(numbers: List[int], times: int) -> List[int]:
    new_current = numbers[0]
    for _ in range(times):
        numbers, new_current = move(tuple(numbers), new_current)

    return numbers



####################################

numbers = parse_input(INPUT_STR)

# Part one
final_numbers_one = play(numbers, 100)

idx_n = (final_numbers_one.index(1) + 1) % len(final_numbers_one)
n = final_numbers_one[idx_n]
final_numbers_sorted = []
while n != 1:
    final_numbers_sorted.append(n)
    idx_n = (idx_n + 1) % len(final_numbers_one)
    n = final_numbers_one[idx_n]

final_result = "".join([str(i) for i in final_numbers_sorted])
print(f"Result after 100 moves is {final_result}")

# Part two
n_moves = 10000
# new_numbers = numbers + list(range(max(numbers), 1000000 + 1))
new_numbers = numbers + list(range(max(numbers), 10000 + 1))
final_numbers_two = play(new_numbers, n_moves)

idx_n1 = (final_numbers_two.index(1) + 1) % len(final_numbers_two)
idx_n2 = (idx_n1 + 1) % len(final_numbers_two)

final_result_two = final_numbers_two[idx_n1] * final_numbers_two[idx_n2]
print(f"Result after {n_moves} moves is {final_result_two}")
