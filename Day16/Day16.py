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
from copy import deepcopy


sys.path.append("..")
from utils import download_input

INPUT_URL = "https://adventofcode.com/2020/day/16/input"
INPUT_FILENAME = "input.txt"
# INPUT_FILENAME = "example_input.txt"
# INPUT_FILENAME = "example_input_2.txt"

def parse_input(filename: str) -> Dict:
    with open(filename, "r") as f:
        raw_rules, yours, nearby = f.read().strip().split("\n\n")

    notes = {}

    # First parse the rules
    rules = {}
    for rule in raw_rules.split("\n"):
        rule_name, constraints = rule.split(": ")
        rules[rule_name] = [[int(i) for i in re.findall("\d+", c)] for c in constraints.split("or")]

    yours = [int(i) for i in yours.replace("your ticket:\n", "").split(",")]
    nearby = [[int(i) for i in n.split(",")] for n in nearby.replace("nearby tickets:\n", "").split("\n")]

    notes["rules"] = rules
    notes["yours"] = yours
    notes["nearby"] = nearby
    # Added for Part 2
    notes["rules_idx"] = {idx: k for idx, k in enumerate(notes["rules"].keys())}
    return notes

####################################
def completely_invalid_digits(notes: Dict) -> Tuple[List[int], List[int]]:
    invalid_digits = []
    # Added for part 2
    invalid_tickets = []
    for idx_ticket, ticket in enumerate(notes["nearby"]):
        for digit in ticket:
            valid_digit = False
            for rule_name, rule in notes["rules"].items():
                for lower, upper in rule:
                    if lower <= digit <= upper:
                        valid_digit = True
                        break
                if valid_digit:
                    break
            else: # If you don't find any break is because this digit was not valid for any rule
                invalid_digits.append(digit)
                invalid_tickets.append(idx_ticket)
                # break # Break the digit loop, one is enough to check
    return invalid_digits, invalid_tickets

def discard_tickets(tickets: List[int], idx_invalid_tickets: List[int]) -> Dict:
    return [ticket for idx_ticket, ticket in enumerate(tickets) if idx_ticket not in idx_invalid_tickets]


# Compute the valid fields for every digit in the ticket
def get_fields_sorted(notes: Dict, tickets: str="yours") -> List[int]:
    def digit_in_rule(digit: int, rule: Dict) -> bool:
        for lower, upper in rule:
            if lower <= digit <= upper:
                return True
        return False

    # This will store a list of lists of lists: the outer list is len(tickets)
    # the inner one is len(digits) and the most inner one will contain the
    # valid fields for each digit in the ticket
    valid_fields = []
    for ticket in notes["nearby"]:
        inner_ticket_list = []
        for digit in ticket:
            valid = set([i for i, r in notes["rules"].items() if digit_in_rule(digit, r)])
            inner_ticket_list.append(valid)
        valid_fields.append(inner_ticket_list)

    # Compute intersection of all sets for the same digit
    final_fields = [functools.reduce(lambda x,y: x&y,i) for i in zip(*[ticket for ticket in valid_fields])]

    # For every digit, check if there is only one possible index.
    # If that's the case, delete it from the others until nothing changes
    new_fields = deepcopy(final_fields)
    changing = True
    while changing:
        changing = False
        for field_i in new_fields:
            if len(field_i) == 1:
                for idx_j, field_j in enumerate(new_fields):
                    if len(field_j) > 1:
                        new_fields[idx_j] -= field_i
                        changing = True

    # This assumes the search was perfect and there aren't any digit with
    # more than one field
    return [x for y in new_fields for x in y]

####################################
if not os.path.exists(INPUT_FILENAME):
    cookie = {"session": os.environ["session"]}
    success = download_input(INPUT_URL, INPUT_FILENAME, cookie)
    if not success: # This should be handled better
        exit(-1)

notes = parse_input(INPUT_FILENAME)
invalid_digits, invalid_tickets = completely_invalid_digits(notes)
print(f"Sum of bad digits is {sum(invalid_digits)}")

# Part 2
notes["nearby"] = discard_tickets(notes["nearby"], invalid_tickets)
valid_indexes = get_fields_sorted(notes)
departure_digits = [notes["yours"][idx] for idx, key in enumerate(valid_indexes) if "departure" in key]
print(f"The product of the departure digits is {math.prod(departure_digits)}")
