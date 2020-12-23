#!/usr/bin/env python

import os
import regex as re # This allows recursion
import sys
import math
import requests
import itertools

from timeit import default_timer as timer
from typing import List, Tuple, Dict, Set
from collections import Counter
from copy import deepcopy


sys.path.append("..")
from utils import download_input

INPUT_URL = "https://adventofcode.com/2020/day/19/input"
INPUT_FILENAME = "input.txt"
# INPUT_FILENAME = "example_input.txt"
# INPUT_FILENAME = "example_input_2.txt"

##################################################
def parse_input(filename: str) -> List[List[str]]:
    with open(filename, "r") as f:
        raw_rules, messages = f.read().strip().split("\n\n")

    # rules = dict(l.replace('"','').split(": ") for l in raw_rules.split("\n"))
    # rules = {k: v.split(" | ") for k,v in rules.items()}
    # rules = {k: (lambda x: [y.split(" ") for y in x])(v) for k,v in rules.items()}
    # rules = {k: (v if len(v[0]) > 1 else v[0][0]) for k,v in rules.items()}
    rules = {l.split(": ")[0]: l.split(": ")[1] for l in raw_rules.replace('"', '').split("\n")}
    rules = {k: "   " + v.replace(" ", "   ") + "   " for k, v in rules.items()}
    messages = messages.split("\n")

    return rules, messages


def process_rules_one(rules: str) -> Dict:
    def clean(r: str) -> str:
        return r.replace(" ", "").replace("|", "").replace("(","").replace(")", "")
    new_rules = deepcopy(rules)

    # First attempt
    while not clean(new_rules["0"]).isalpha():
        # print(new_rules)
        for r, _ in rules.items():
            letter = new_rules[r]
            if clean(letter).isalpha():
                for new_r, _ in rules.items():
                    if r != new_r and r in new_rules[new_r]:
                        replacement = ("(" + letter + ")") if "|" in letter else letter
                        new_rules[new_r] = new_rules[new_r].replace(" " + r + " ", replacement)

    new_rules["0"] = new_rules["0"] + "$"
    for k, _ in new_rules.items():
        new_rules[k] = new_rules[k].replace(" ", "")
    return new_rules

# def process_rules_two(rules: Dict) -> Dict:
#     def condition(r: List[List[str]]) -> str:
#         return True
#
#     new_rules = deepcopy(rules)
#
#     # First attempt
#     while not clean(new_rules["0"]).isalpha():
#         # print(new_rules)
#         for r, _ in rules.items():
#             letter = new_rules[r]
#             print(f"{letter}")
#             if condition(letter):
#                 for new_r, inner_rules in rules.items():
#                     for rule in inner_rules:
#                         if r != new_r and rule == r:
#                             replacement = ("(" + letter + ")") if "|" in letter else letter
#                             new_rules[new_r] = new_rules[new_r].replace(r, replacement)
#
#     new_rules["0"] = new_rules["0"] + r"$"
#     return new_rules

####################################
if not os.path.exists(INPUT_FILENAME):
    cookie = {"session": os.environ["session"]}
    success = download_input(INPUT_URL, INPUT_FILENAME, cookie)
    if not success: # This should be handled better
        exit(-1)


rules, messages = parse_input(INPUT_FILENAME)
raw_rules, messages = parse_input(INPUT_FILENAME)
rules_one = process_rules_one(raw_rules)

first_pattern = re.compile(rules_one["0"])
first_valid_messages = [m for m in messages if first_pattern.match(m) is not None]
print(f"First number of valid messages: {len(first_valid_messages)}")

# Part 2
raw_rules_two = deepcopy(raw_rules)
raw_rules_two["8"] = "  42   |   42   8   "
raw_rules_two["11"] = "   42       31      |     42       11      31    "
rules_two = deepcopy(rules_one)
rules_two["8"] = "(" + rules_two["42"] + ")" + "+"
rules_two["11"] = "(" + "|".join([f'(({rules_two["42"]}){{{n}}}({rules_two["31"]}){{{n}}})' for n in range(1, 12)]) + ")"
rules_two["0"] =  rules_two["8"] + rules_two["11"] + "$"

second_pattern = re.compile(rules_two["0"])
second_valid_messages = [m for m in messages if second_pattern.match(m) is not None]
print(f"Second number of valid messages: {len(second_valid_messages)}")
