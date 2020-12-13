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

INPUT_URL = "https://adventofcode.com/2020/day/13/input"
INPUT_FILENAME = "input.txt"
# INPUT_FILENAME = "example_input.txt"
cookie = {"session": os.environ["session"]}

def first_multiple_greater(n: int, limit: int) -> int:
    # for i in itertools.count():
    #     multiple = n * i
    #     if multiple >= limit:
    #         return multiple
    return n * math.ceil(limit / n)


def parse_input(filename: str) -> Dict:
    with open(filename, "r") as f:
        raw_input = f.read().strip()

    timestamp, raw_buses = raw_input.split("\n")
    buses = re.findall("\d+", raw_buses)

    timetable = {   "timestamp": int(timestamp),
                    "buses": [int(b) for b in buses],
                    "idx_buses": [raw_buses.split(",").index(b) for b in buses] # Added for Part 2
                }

    return timetable




####################################
if not os.path.exists(INPUT_FILENAME):
    success = download_input(INPUT_URL, INPUT_FILENAME, cookie)
    if not success: # This should be handled better
        exit(-1)

timetable = parse_input(INPUT_FILENAME)

# Part one
timetable["first_buses"] = [first_multiple_greater(b, timetable["timestamp"]) for b in timetable["buses"]]

min_bus = min(zip(timetable["buses"], timetable["first_buses"]), key=lambda x: x[1])
delay = min_bus[1] - timetable["timestamp"]
print(f"The delay is {delay} and the ID is {min_bus[0]} -> {delay * min_bus[0]}")

# Part two
# For every multiple N of the first ID, check if N+offset is multiple of the other buses
first_bus = timetable["buses"][0]
other_bus = timetable["buses"][1:]
idx_other = timetable["idx_buses"][1:]

# The bruteforce solution is not reasonable since
# it takes too long to test all the numbers

# first_multiple = first_multiple_greater(first_bus, limit=100000000000000)
# print(f"First multiple to try: {first_multiple}")
# for i in itertools.count(start=first_multiple):
#     multiple = first_bus * i
#
#     for bus, offset in zip(other_bus, idx_other):
#         if (multiple + offset) % bus != 0:
#             break
#     else:
#         break
# The expected result would be the "multiple" var.

# It seems like a clear clase of the Chinese remainder theorem
# Using the example input:
# 7n + 0 === 0 mod 7
# 7n + 1 === 0 mod 13
# 7n + 4 === 0 mod 59
# 7n + 6 === 0 mod 31
# 7n + 7 === 0 mod 19
#
# We have to find 7n = x so let's write it as
# x === ai  mod ni
# ----------------
# x === 0   mod 7
# x === 12  mod 13
# x === 55  mod 59
# x === 25  mod 31
# x === 12  mod 19
#
# Since all the mods are pairwise coprime we can use the theorem
# Let's define N as the product of the mods N=7·13·59·31·19
# ri and si will be the Bezout's coeffs of ni and N/ni for i=1,...,k=5
# so the solution x will be
# x = sum(ai*si*N/ni) for i=1,...,k=5
# x === 0 mod N
#
# To get Bezout's coeffs we need the Extended Euclidean Algorithm
# https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode
def extended_gcd(a: int, b: int) -> Dict:
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    output = {  "coeffs": (old_s, old_t),
                "gcd": old_r,
                "quotients": (t,s)}
    return output

# Pseudocode from https://rosettacode.org/wiki/Chinese_remainder_theorem
def chinese_remainder_theorem(a: List[int], n: List[int]) -> Tuple[int, int]:
    N = math.prod(n)
    s = []
    for n_i in n:
        result = extended_gcd(n_i, N//n_i)
        s.append(result["coeffs"][1]) # 1 because we are looking for the N//ni coeffs

    x = 0
    for i in range(len(s)):
        x += a[i] * s[i] * (N // n[i])

    return (x % N, N)


n = timetable["buses"]
a = [b - i for b,i in zip(timetable["buses"], timetable["idx_buses"])]

result = chinese_remainder_theorem(a,n)

print(f"The first timestamp is {result}")
