#!/usr/bin/env python

import os
import re
import sys
import math
import requests
import itertools
import numpy as np

from timeit import default_timer as timer
from typing import List, Tuple, Dict, Set
from collections import Counter, defaultdict
from copy import deepcopy
from operator import add, mul
from scipy.ndimage import correlate

from constraint import *


sys.path.append("..")
from utils import download_input

INPUT_URL = "https://adventofcode.com/2020/day/21/input"
INPUT_FILENAME = "input.txt"
# INPUT_FILENAME = "example_input.txt"

##################################################
def parse_input(filename: str) -> Dict:
    with open(filename, "r") as f:
        raw_input = f.read().strip().replace(")", "").split("\n")

    all_ingredients = set()
    all_allergens = set()
    ingredient_count = Counter()
    possible = {}
    whole_rules = []
    raw_input = [l.split(" (contains ") for l in raw_input]
    for i, a in raw_input:
        ingredient_list = i.split(" ")
        for ingredient in ingredient_list:
            all_ingredients.add(ingredient)
            ingredient_count[ingredient] += 1
            for allergen in a.split(", "):
                all_allergens.add(allergen)
                if allergen in possible:
                    possible[allergen] &= set(ingredient_list)
                else:
                    possible[allergen] = set(ingredient_list)
        whole_rules.append([i.split(" "), a.split(", ")])
    return whole_rules, all_ingredients, all_allergens, ingredient_count, possible




####################################
if not os.path.exists(INPUT_FILENAME):
    cookie = {"session": os.environ["session"]}
    success = download_input(INPUT_URL, INPUT_FILENAME, cookie)
    if not success: # This should be handled better
        exit(-1)

whole_rules, all_ingredients, all_allergens, ingredient_count, possible = parse_input(INPUT_FILENAME)


# I tried to go to the overkill solution, using a Contraint Satisfaction Problem
# Too overkill, it doesn't end, but I learned how to use the module!
#
#
# def custom_constraint(*arguments):
#     for ingredients, allergens in whole_rules:
#         for variable, value in zip(all_allergens, arguments):
#             if variable in allergens:
#                 if value not in ingredients:
#                     return False
#
#     return True

# problem = Problem()
# for i, a in other_rules.items():
#     problem.addVariable(i, list(a))
# problem.addConstraint(AllDifferentConstraint())
# problem.addConstraint(custom_constraint, all_allergens)

# solutions = problem.getSolutions()
# ingredients_with_allergens = set([v for k,v in solutions[0].items()])
# ingredients_to_check = all_ingredients - ingredients_with_allergens

# The easy solution is like one of the previous problems: take the ones with
# just one possibility and solve the others
definitive = {}
while possible:
    allergen = [k for k,v in possible.items() if len(v) == 1][0]
    ingredient = possible.pop(allergen)
    ingredient_name = list(ingredient)[0]
    definitive[ingredient_name] = allergen
    for a, i in possible.items():
        possible[a] -= ingredient

allergic_ingredients = set([k for k,v in definitive.items()])
non_allergic_ingredients = all_ingredients - allergic_ingredients

n_times = 0
for i, c in ingredient_count.items():
    if i in non_allergic_ingredients:
        n_times += c

print(f"Number of times ingredients with no allergies appear: {n_times}")

# Part 2: sorting
sorted_ingredients = dict(sorted(definitive.items(), key=lambda v: v[1]))
canonical_list = ",".join(sorted_ingredients.keys())
print(f"The canonical list is {canonical_list}")
