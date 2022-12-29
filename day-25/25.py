# Path: day-25/25.py
# Solution for day 25 of Advent of Code
import os

from aoc_tools import Test


def read_data(file):
    encoded_data = open(file).read().strip().splitlines()
    return encoded_data


table = {"0": 0, "1": 1, "2": 2, "-": -1, "=": -2}


def decode(encoded):
    encoded = encoded[::-1]
    num = 0
    base = 1
    for i in range(len(encoded)):
        num += table[encoded[i]] * base
        base *= 5
    return num


def snafu(decimal):
    res = []
    while decimal:
        res.append("012=-"[decimal % 5])
        decimal = (2 + decimal) // 5
    return "".join(res[::-1])


def solve(data):
    part1 = 0
    for n in data:
        part1 += decode(n)
    return "Part 1: " + snafu(part1)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    test, input = read_data("test.txt"), read_data("input.txt")
    # there is no part 2 for this one!
    assert solve(test) == "Part 1: 2=-1=0", "Test failed"
    print(solve(input))
