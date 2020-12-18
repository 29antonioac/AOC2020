#!/usr/bin/env python

import os
import re
import sys
import math
import requests
import itertools

from timeit import default_timer as timer
from typing import List, Tuple, Dict, Set
from collections import Counter
from copy import deepcopy
from operator import add, mul


sys.path.append("..")
from utils import download_input

INPUT_URL = "https://adventofcode.com/2020/day/18/input"
INPUT_FILENAME = "input.txt"
# INPUT_FILENAME = "example_input.txt"
# INPUT_FILENAME = "example_input_2.txt"

##################################################
def parse_input(filename: str) -> List[List[str]]:
    with open(filename, "r") as f:
        homework = [list(l.strip().replace(" ", "")) for l in f.readlines()]

    return homework


def process_expression_one(expression: List[str]) -> int:
    result = 0
    current_operation = add
    pos = 0

    # Just accumulating the result with the next operator, no precedence
    while pos < len(expression):
        term = expression[pos]
        if term.isdigit():
            result = current_operation(result, int(term))
            pos += 1
        elif term == "*":
            current_operation = mul
            pos += 1
        elif term == "+":
            pos += 1
            current_operation = add
        elif term == "(":
            # Look for its matching bracket, sublist and call the function itself
            ending_pos = pos
            brackets = ["("]
            while brackets and ending_pos < len(expression) - 1:
                ending_pos += 1
                new_term = expression[ending_pos]
                if new_term == "(":
                    brackets.append("(")
                elif new_term == ")":
                    brackets.pop()
            # We are assuming there will be matching brackets, no input errors here
            # Avoid the brackets in the new call!
            result = current_operation(result, process_expression_one(expression[pos+1:ending_pos]))
            pos = ending_pos + 1

        else:
            raise ValueError(f"Term {term} not defined!")

    return result

def process_expression_two(expression: List[str]) -> int:
    results = []
    current_result = 0
    current_operation = add
    pos = 0

    # Same as before, but just accumulating sums
    # Each sum will be stored to be multiplied in the end
    while pos < len(expression):
        term = expression[pos]
        if term.isdigit():
            current_result = current_operation(current_result, int(term))
            pos += 1
        elif term == "*":
            results.append(current_result)
            current_result = 0
            pos += 1
        elif term == "+":
            pos += 1
            current_operation = add
        elif term == "(":
            # Look for its matching bracket, sublist and call the function itself
            ending_pos = pos
            brackets = ["("]
            while brackets and ending_pos < len(expression) - 1:
                ending_pos += 1
                new_term = expression[ending_pos]
                if new_term == "(":
                    brackets.append("(")
                elif new_term == ")":
                    brackets.pop()
            current_result = current_operation(current_result, process_expression_two(expression[pos+1:ending_pos]))
            pos = ending_pos + 1

        else:
            raise ValueError(f"Term {term} not defined!")

    # Add the last one
    results.append(current_result)
    return math.prod(results)


####################################
if not os.path.exists(INPUT_FILENAME):
    cookie = {"session": os.environ["session"]}
    success = download_input(INPUT_URL, INPUT_FILENAME, cookie)
    if not success: # This should be handled better
        exit(-1)


homework = parse_input(INPUT_FILENAME)

results_one = [process_expression_one(expression) for expression in homework]
print(f"First results: {sum(results_one)}")

results_two = [process_expression_two(expression) for expression in homework]
print(f"Second results: {sum(results_two)}")
