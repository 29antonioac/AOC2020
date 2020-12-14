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

INPUT_URL = "https://adventofcode.com/2020/day/14/input"
INPUT_FILENAME = "input.txt"
# INPUT_FILENAME = "example_input.txt"
# INPUT_FILENAME = "example_input_2.txt"
cookie = {"session": os.environ["session"]}

def parse_input(filename: str) -> Dict:
    with open(filename, "r") as f:
        raw_input = f.read().strip()

    return raw_input

# https://wiki.python.org/moin/BitManipulation
def int2bits(i: int, nbits: int=36) -> str:
    return format(i, "b").zfill(nbits)

def bits2int(b: str) -> int:
    return int(b, 2)

def changebits(bytes: str, bitmask: str) -> str:
    byte_as_list = list(bytes)
    for idx, bit in enumerate(bitmask):
        if bit != "X":
            byte_as_list[idx] = bit

    return "".join(byte_as_list)


def process_program_one(program: str) -> Dict:
    mem = {}
    mask = None

    for line in program.split("\n"):
        if line.startswith("mask"):
            _, mask = line.split(" = ")
        elif line.startswith("mem"):
            address, value = [int(i) for i in re.findall("\d+", line)]
            bits_value = int2bits(value)
            new_value = bits2int(changebits(bits_value, mask))
            mem[address] = new_value

    return mem

def mask_to_address_list(address: str, bitmask: str) -> List[str]:
    address_as_list = list(address)
    n_floating = bitmask.count("X")

    for idx, bit in enumerate(bitmask):
        if bit == "1":
            address_as_list[idx] = "1"
        elif bit == "X":
            address_as_list[idx] = "{}"
    new_address_template = "".join(address_as_list)

    address_list = [new_address_template.format(*i) for i in itertools.product([1,0], repeat=n_floating)]
    return address_list

def process_program_two(program: str) -> Dict:
    mem = {}
    mask = None

    for line in program.split("\n"):
        if line.startswith("mask"):
            _, mask = line.split(" = ")
        elif line.startswith("mem"):
            address, value = [int(i) for i in re.findall("\d+", line)]
            all_addresses = mask_to_address_list(int2bits(address), mask)
            for current_address in all_addresses:
                mem[bits2int(current_address)] = value

    return mem


####################################
if not os.path.exists(INPUT_FILENAME):
    success = download_input(INPUT_URL, INPUT_FILENAME, cookie)
    if not success: # This should be handled better
        exit(-1)

program = parse_input(INPUT_FILENAME)

mem = process_program_one(program)
sum_values = sum([v for k,v in mem.items()])
print(f"The sum of the values in memory with first version is {sum_values}")

mem = process_program_two(program)
sum_values = sum([v for k,v in mem.items()])
print(f"The sum of the values in memory with second version is {sum_values}")
