#!/usr/bin/env python


import abc

from timeit import default_timer as timer
from typing import List, Tuple
from collections import Counter

INPUT_FILENAME = "input.txt"

class PasswordChecker(metaclass=abc.ABCMeta):
    def __init__(self, firstnum: int, secondnum: int, letter: str, password: str):
        self.firstnum = firstnum
        self.secondnum = secondnum
        self.letter = letter
        self.password = password
        self.valid = False

    @abc.abstractmethod
    def condition(self) -> bool:
        pass

    def check(self) -> bool:
        if self.condition():
            self.valid = True
        else:
            self.valid = False
        return self.valid

class PasswordChecker_one(PasswordChecker):
    def __init__(self, firstnum: int, secondnum: int, letter: str, password: str):
        super().__init__(firstnum, secondnum, letter, password)
        self.letter_count = Counter(password)

    def condition(self) -> bool:
        return self.firstnum <= self.letter_count[self.letter] <= self.secondnum

class PasswordChecker_two(PasswordChecker):
    def __init__(self, firstnum: int, secondnum: int, letter: str, password: str):
        super().__init__(firstnum, secondnum, letter, password)


    def condition(self) -> bool:
        return  (self.password[self.firstnum - 1] == self.letter) ^ \
                (self.password[self.secondnum - 1] == self.letter)


def parse_input(filename: str) -> Tuple[List[PasswordChecker], List[PasswordChecker]]:
    password_list_first = []
    password_list_second = []
    with open(filename, "r") as f:
        for line in f:
            limits, letter, password = line.replace(":", "").split(" ")
            firstnum, secondnum = limits.split("-")
            password_list_first.append(PasswordChecker_one(int(firstnum), int(secondnum), letter, password))
            password_list_second.append(PasswordChecker_two(int(firstnum), int(secondnum), letter, password))
    return password_list_first, password_list_second



password_list_first, password_list_second = parse_input(INPUT_FILENAME)
good_passwords_first = [p.check() for p in password_list_first]
good_passwords_second = [p.check() for p in password_list_second]
print(f"Good passwords first criteria = {sum(good_passwords_first)}/{len(good_passwords_first)}")
print(f"Good passwords second criteria = {sum(good_passwords_second)}/{len(good_passwords_second)}")
