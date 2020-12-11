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

class Passport(object):
    def __init__(self, passport: Dict[str,str]):
        self.passport = passport
        self.valid = False
    def __str__(self):
        return str(self.valid) + "\n" + str(self.passport)

    def check_weak(self, needed_fields) -> bool:
        self.valid = True
        for k in needed_fields:
            if k not in self.passport:
                self.valid = False
                break
        return self.valid
    def check_strong(self, needed_fields) -> bool:
        self.valid = self.check_weak(needed_fields)
        if self.valid:
            try:
                byr = int(self.passport["byr"])
                iyr = int(self.passport["iyr"])
                eyr = int(self.passport["eyr"])
                hgt = self.passport["hgt"]
                hcl = hex(int(self.passport["hcl"].replace("#", "0x"), 16))
                ecl = self.passport["ecl"]
                pid = self.passport["pid"]

                self.valid =    1920 <= byr <= 2002 and \
                                2010 <= iyr <= 2020 and \
                                2020 <= eyr <= 2030 and \
                                ((hgt.endswith("cm") and 150 <= int(hgt[:-2]) <= 193) or
                                 (hgt.endswith("in") and 59  <= int(hgt[:-2]) <= 76)) and \
                                "#" in self.passport["hcl"] and \
                                ecl in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"] and \
                                len(pid) == 9
            except ValueError as e:
                # print(f"Something is not in the format needed: {e}")
                self.valid = False

        return self.valid

def parse_input(filename: str) -> List[Passport]:
    with open(filename, "r") as f:
        input_list = [i.replace("\n", " ").strip() for i in f.read().split("\n\n")]

    passport_list = [Passport(dict([p.split(":") for p in ii.split(" ")])) for ii in input_list]
    return passport_list



if not os.path.exists(INPUT_FILENAME):
    success = download_input(INPUT_URL, INPUT_FILENAME, cookie)
    if not success: # This should be handled better
        exit(-1)

passport_list = parse_input(INPUT_FILENAME)

needed_fields = ["byr",
                 "iyr",
                 "eyr",
                 "hgt",
                 "hcl",
                 "ecl",
                 "pid"]#,
                 # "cid"]

valid_passports_weak = [p.check_weak(needed_fields) for p in passport_list]
valid_passports_strong = [p.check_strong(needed_fields) for p in passport_list]
print(f"Valid passports with weak criteria: {sum(valid_passports_weak)}/{len(passport_list)}")
print(f"Valid passports with strong criteria: {sum(valid_passports_strong)}/{len(passport_list)}")
