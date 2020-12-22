#!/usr/bin/env python

import os
import re
import sys
import math
import requests

from typing import List, Tuple, Dict, Set
from copy import deepcopy


sys.path.append("..")
from utils import download_input

INPUT_URL = "https://adventofcode.com/2020/day/22/input"
INPUT_FILENAME = "input.txt"
# INPUT_FILENAME = "example_input.txt"

##################################################
def parse_input(filename: str) -> Dict:
    with open(filename, "r") as f:
        decks = [p.split(":\n")[-1] for p in f.read().strip().split("\n\n")]

    decks = [[int(n) for n in d.split("\n") ] for d in decks]
    return decks

def score(winner: List[int]) -> int:
    return sum([c*v for c,v in zip(reversed(winner),range(1,len(winner)+1))])

def combat(original_player_one: List[int], original_player_two: List[int], recursive: bool) -> Tuple[List[int], List[int]]:
    player_one = deepcopy(original_player_one)
    player_two = deepcopy(original_player_two)
    decks_history = set()

    while player_one and player_two:
        state = (tuple(player_one), tuple(player_two))
        if state in decks_history:
            return player_one, None
        else:
            decks_history.add(state)

        card_one = player_one.pop(0)
        card_two = player_two.pop(0)

        if recursive and len(player_one) >= card_one and len(player_two) >= card_two:
            result_one, result_two = combat(player_one[:card_one], player_two[:card_two], recursive=True)
            if result_one:
                player_one.append(card_one)
                player_one.append(card_two)
            else:
                player_two.append(card_two)
                player_two.append(card_one)

        elif card_one > card_two:
            player_one.append(card_one)
            player_one.append(card_two)
        elif card_two > card_one:
            player_two.append(card_two)
            player_two.append(card_one)
        else:
            raise ValueError(f"What should I do with similar values? {card_one}-{card_two}")

    return player_one, player_two

####################################
if not os.path.exists(INPUT_FILENAME):
    cookie = {"session": os.environ["session"]}
    success = download_input(INPUT_URL, INPUT_FILENAME, cookie)
    if not success: # This should be handled better
        exit(-1)

player_one, player_two = parse_input(INPUT_FILENAME)

result_one, result_two = combat(player_one, player_two, recursive=False)
score_normal = score(result_one) if result_one else score(result_two)
print(f"The score of the winner is {score_normal}")

result_one, result_two = combat(player_one, player_two, recursive=True)
score_recursive = score(result_one) if result_one else score(result_two)
print(f"The score of the recursive_combat winner is {score_recursive}")
