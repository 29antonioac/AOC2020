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

INPUT_URL = "https://adventofcode.com/2020/day/7/input"
INPUT_FILENAME = "input.txt"
# INPUT_FILENAME = "example_input.txt"
# INPUT_FILENAME = "example_input_2.txt"
cookie = {"session": os.environ["session"]}

# Trying to get a dict
# {"light red bags": {"bright white bag": 1, "muted yellow bags": 2}}
def parse_input(filename: str) -> Dict:
    with open(filename, "r") as f:
        raw_input = [l.strip() for l in f.readlines()]

    rules = dict()
    for line in raw_input:
        bag, contains = re.sub(" ?bags?", "", line).split(" contain ")
        contains_list = [c.split(" ", 1) for c in contains.replace(".", "").split(", ") if contains != "no other."]
        rules[bag] = {b: int(v) for v,b in contains_list}
    return rules

def check_bag(rules: Dict, bag_to_check: str) -> int:
    def inner_check(inner_rule: Dict, inner_bag_to_check: str) -> bool:
        for inner_bag, capacity in inner_rule.items():
            if inner_bag == bag_to_check:
                # print(f"{bag_to_check} found!")
                return True
            else:
                # print(f"Looking for {bag_to_check} in {inner_bag}")
                found = inner_check(rules[inner_bag], inner_bag_to_check)
                if found:
                    return True

    n_contains = 0
    for outer_bag, outer_rule in rules.items():
        # print(f"Looking for {bag_to_check} in {outer_bag}")
        found = bag_to_check != outer_bag and inner_check(outer_rule, bag_to_check)
        if found:
            n_contains += 1
        # print()
    return n_contains

def number_bags (rules: Dict, bag_to_check: str) -> int:
    def inner_number(inner_rule: Dict) -> int:
        inner_number_ret = 0
        if not inner_rule:
            # print("Returning 1")
            return 1
        for inner_bag, inner_capacity in inner_rule.items():
            # print(f"Returning {inner_capacity}*inner_number[{inner_bag}]")
            inner_number_ret += inner_capacity * inner_number(rules[inner_bag])
        return inner_number_ret + 1 # The bag itself

    return inner_number(rules[bag_to_check]) - 1 # Substract the one that's being checked

if not os.path.exists(INPUT_FILENAME):
    success = download_input(INPUT_URL, INPUT_FILENAME, cookie)
    if not success: # This should be handled better
        exit(-1)

rules = parse_input(INPUT_FILENAME)

checked = check_bag(rules, "shiny gold")
print(f"Shiny gold in {checked} bags")

n_bags = number_bags(rules, "shiny gold")
print(f"n_bags = {n_bags}")
