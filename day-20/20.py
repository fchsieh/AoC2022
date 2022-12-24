# Path: day-20/20.py
# Solution for day 20 of Advent of Code
import os

from aoc_tools import Test
from collections import deque
from copy import deepcopy


class CircularList:
    def __init__(self, init_data: deque):
        self.Q = deepcopy(init_data)

    def __str__(self):
        return str(self.Q)

    def __iter__(self):
        return self.Q.__iter__()

    def __len__(self):
        return len(self.Q)

    def index(self, val):
        return self.Q.index(val)

    def mix(self, cur_idx, move_to, val):
        def euclidean_remainder(x, y):
            return x - y * (x // y)

        # delete original val
        del self.Q[cur_idx]
        # euclidean modulo to wrap around
        to_idx = euclidean_remainder(cur_idx + move_to, len(self.Q))
        # insert val at new position
        if to_idx == 0:  # insert at end
            self.Q.append(val)
        else:
            self.Q.insert(to_idx, val)


def read_data(file):
    data = []
    with open(file, "r") as f:
        for line in f:
            data.append(int(line.strip()))
    return data


def decrypt(data, times, key):
    data = [key * x for x in data]
    idx_list = CircularList(deque(range(len(data))))
    encrypted = CircularList(deque(data))

    for _ in range(times):
        for orig_i, orig_v in enumerate(data):
            cur_idx = idx_list.index(orig_i)
            idx_list.mix(cur_idx, orig_v, orig_i)
            encrypted.mix(cur_idx, orig_v, orig_v)

    zero_idx = encrypted.index(0)
    one_thousand_th = encrypted.Q[(zero_idx + 1000) % len(encrypted)]
    two_thousand_th = encrypted.Q[(zero_idx + 2000) % len(encrypted)]
    three_thousand_th = encrypted.Q[(zero_idx + 3000) % len(encrypted)]

    return one_thousand_th + two_thousand_th + three_thousand_th


def solve(data):
    # Part 1
    part1 = decrypt(data, 1, 1)
    print(f"Part 1: {part1}")

    # Part 2
    key = 811589153
    part2 = decrypt(data, 10, key)
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    test, input = read_data("test.txt"), read_data("input.txt")
    Test(test, solve, 3, 1623178306)
    solve(input)
