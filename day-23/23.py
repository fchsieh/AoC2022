# Path: day-23/23.py
# Solution for day 23 of Advent of Code
import os

from aoc_tools import Test


def read_data(file):
	pass


def solve(data):
	pass


if __name__ == "__main__":
	os.chdir(os.path.dirname(os.path.abspath(__file__)))
	test, input = read_data("test.txt"), read_data("input.txt")
	Test(test, solve, -1, -1)
	solve(input)
