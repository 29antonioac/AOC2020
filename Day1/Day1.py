#!/usr/bin/env python

import requests
import numpy as np

from timeit import default_timer as timer
from typing import List

INPUT_FILENAME = "input.txt"

def parse_input(filename: str) -> List[int]:
    with open(filename, "r") as f:
        number_list = [int(s) for s in f.read().split("\n") if s]
    return number_list

# We need to get the product of the two numbers whose sum is 2020
def exercise_one(number_list: List[int]) -> int:
    np_list = np.array(number_list)
    indexes, _ = np.where((np_list + np_list[:, np.newaxis]) == 2020)
    return np_list[indexes].prod()

# We need to get the product of the three numbers whose sum is 2020
def exercise_two(number_list: List[int]) -> int:
    np_list = np.array(number_list)
    indexes, _, _ = np.where(((np_list + np_list[:, np.newaxis]) + np_list[:, np.newaxis][:,np.newaxis]) == 2020)
    return np_list[np.unique(indexes)].prod()

example_list = [1721,979,366,299,675,1456]
number_list = parse_input(INPUT_FILENAME)

start = timer()
result_one = exercise_one(number_list)
end = timer()
print(f"The first result is {result_one}, time spent {(end - start)} seconds")

start = timer()
result_two = exercise_two(number_list)
end = timer()
print(f"The second result is {result_two}, time spent {(end - start)} seconds")
