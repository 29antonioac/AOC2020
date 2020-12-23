#!/usr/bin/env python

from typing import List, Tuple, Dict, Set

INPUT_URL = "https://adventofcode.com/2020/day/22/input"
INPUT_STR = "389547612"
# INPUT_STR = "389125467"

##################################################
class Cup(object):
    def __init__(self, label, next=None):
        self.label = label
        self.next = next

    def change_next(self, next):
        self.next = next

    def __str__(self):
        return str(self.label) + "->" + (str(self.next.label) if self.next else "None")

    def __repr__(self):
        return str(self.label) + "->" + (str(self.next.label) if self.next else "None")

def parse_input(numbers: str) -> Dict[int, Cup]:
    number_list = [int(i) for i in numbers]
    cup_list = {i: Cup(i) for i in number_list}
    number_list.append(number_list.pop(0))
    for idx, idx_next in zip(cup_list.keys(), number_list):
        cup_list[idx].change_next(cup_list[idx_next])
    return cup_list

def move(cup_list: Dict[int, Cup], cup: Cup) -> Cup:

    picked_cups = [cup.next, cup.next.next, cup.next.next.next]
    picked_numbers = [c.label for c in picked_cups]

    destination_number = cup.label - 1
    destination_cup = cup_list.get(destination_number, None)

    while (destination_cup is None) or destination_number in picked_numbers:
        if destination_number <= 0:
            destination_number = max(cup_list.keys())
        else:
            destination_number = destination_number - 1
        destination_cup = cup_list.get(destination_number, None)

    cup.change_next(picked_cups[-1].next)
    picked_cups[-1].change_next(destination_cup.next)
    destination_cup.change_next(picked_cups[0])

    new_current = cup.next
    return new_current

def play(cup_list: List[Cup], times: int) -> List[int]:
    current_cup = cup_list[3]
    for _ in range(times):
        current_cup = move(cup_list, current_cup)

    return cup_list



####################################

cup_list_one = parse_input(INPUT_STR)

# Part one
final_numbers_one = play(cup_list_one, 100)

cup = final_numbers_one[1].next
final_numbers_sorted = []
while cup.label != 1:
    final_numbers_sorted.append(cup.label)
    cup = cup.next

final_result = "".join([str(i) for i in final_numbers_sorted])
print(f"Result after 100 moves is {final_result}")

# Part two
n_moves = 10000000
size = 1000000

cup_list_two = parse_input(INPUT_STR)
existent = max(cup_list_two.keys())
for i in range(existent + 1, size + 1):
    cup_list_two[i] = Cup(i)

cup_list_two[int(INPUT_STR[-1])].change_next(cup_list_two[existent+1])

for i in range(existent+1, size):
    cup_list_two[i].change_next(cup_list_two[i+1])
cup_list_two[size].change_next(cup_list_two[3])

final_numbers_two = play(cup_list_two, n_moves)

cup_one = cup_list_two[1]

final_result_two = cup_one.next.label * cup_one.next.next.label
print(f"Result after {n_moves} moves is {final_result_two}")
