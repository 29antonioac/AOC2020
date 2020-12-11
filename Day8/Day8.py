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
from copy import deepcopy

sys.path.append("..")
from utils import download_input

INPUT_URL = "https://adventofcode.com/2020/day/8/input"
INPUT_FILENAME = "input.txt"
# INPUT_FILENAME = "example_input.txt"
cookie = {"session": os.environ["session"]}


def parse_input(filename: str) -> str:
    with open(filename, "r") as f:
        raw_input = f.read().strip()

    code = {"code": [{"operation": op, "argument": int(argument), "times": 0} for command in raw_input.split("\n") for op, argument, in [command.split(" ")]  ], "accumulator": 0}

    return code


def run(program: Dict) -> bool:
    code = program["code"]
    instruction_pointer = 0
    infinite_loop = False
    n_instructions = len(code)
    while instruction_pointer < n_instructions and not infinite_loop:
        instruction = code[instruction_pointer]
        operation = instruction["operation"]
        argument = instruction["argument"]
        instruction["times"] += 1

        if instruction["times"] > 1:
            infinite_loop = True
            break

        if operation == "nop":
            instruction_pointer += 1
        elif operation == "acc":
            program["accumulator"] += argument
            instruction_pointer += 1
        elif operation == "jmp":
            instruction_pointer += argument
        else:
            raise ValueError(f"Operation {operation} does not exist")


    return infinite_loop

if not os.path.exists(INPUT_FILENAME):
    success = download_input(INPUT_URL, INPUT_FILENAME, cookie)
    if not success: # This should be handled better
        exit(-1)

program_original = parse_input(INPUT_FILENAME)
program = deepcopy(program_original)

# Part one: run once until an infinit loop
infinite_loop = run(program)
print(f'Accumulator is {program["accumulator"]}')

# Part two: run several times changing nop to jmp and viceversa to find the good accumulator
program = deepcopy(program_original)
for instruction_pointer in range(len(program_original["code"])):
    code = program["code"]
    instruction = code[instruction_pointer]
    if instruction["operation"] == "jmp":
        instruction["operation"] = "nop"
    elif instruction["operation"] == "nop":
        instruction["operation"] = "jmp"
    else:
        continue
    infinite_loop = run(program)
    if not infinite_loop:
        break
    else:
        program = deepcopy(program_original)

# program = program_original.copy()
# program["code"][-2]["operation"] = "nop"

print(f'Accumulator after fixing is {program["accumulator"]}')
