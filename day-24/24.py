# Path: day-24/24.py
# Solution for day 24 of Advent of Code
import copy
import os
from collections import deque
from functools import lru_cache

import numpy as np
from aoc_tools import Test


def read_data(file):
    blizzards = []
    with open(file, "r") as f:
        raw_data = f.read().splitlines()
        map_width, map_height = len(raw_data[0]), len(raw_data)
        for r, line in enumerate(raw_data):
            for c, char in enumerate(line):
                if char != "#" and char != ".":
                    blizzards.append((r, c, char))

    return blizzards, map_width, map_height


class TimedMap(list):
    def __init__(self, map_width=-1, map_height=-1, blizzards=[]):
        # default map
        map = np.array([[True for _ in range(map_width)] for _ in range(map_height)])
        # set boundaries
        for r, row in enumerate(map):
            for c, _ in enumerate(row):
                if r == 0 or r == map_height - 1 or c == 0 or c == map_width - 1:
                    map[r][c] = False
        map[0][1] = map[len(map) - 1][-2] = True  # set entrance and exit
        self.default_map = copy.deepcopy(map)

        # global settings
        self.map_width = map_width
        self.map_height = map_height

        # build initial map
        self.map = {0: map}
        # build initial blizzards
        self.blizzards = {}
        self.set_blocked_area(0, blizzards)

    def set_blocked_area(self, time=0, blizzards=[]):
        self.blizzards[time] = blizzards
        for r, c, dir in blizzards:
            self.map[time][r][c] = False

    def move(self):
        # build next map
        next_map = copy.deepcopy(self.default_map)
        # get last map time and blizzards
        last_time = max(self.map.keys())
        last_blizzards = self.blizzards[last_time]
        # build next blizzards
        next_blizzards = []
        for r, c, dir in last_blizzards:
            new_r, new_c = r, c
            if dir == "<":
                new_c = new_c - 1 if c > 1 else self.map_width - 2
            elif dir == ">":
                new_c = new_c + 1 if c < self.map_width - 2 else 1
            elif dir == "^":
                new_r = new_r - 1 if r > 1 else self.map_height - 2
            elif dir == "v":
                new_r = new_r + 1 if r < self.map_height - 2 else 1
            next_blizzards.append((new_r, new_c, dir))

        self.map[last_time + 1] = next_map
        self.set_blocked_area(last_time + 1, next_blizzards)

    def get_opened_cells(self, time=0):
        # find all true cells
        return np.argwhere(self.map[time] == True)

    def pprint(self, time=0):
        s = []
        for r, row in enumerate(self.default_map):
            s.append(["." if cell else "#" for cell in row])

        for r, c, dir in self.blizzards[time]:
            if s[r][c] == ".":  # no blizzard yet
                s[r][c] = dir
            elif s[r][c] != ".":  # already has a blizzard
                s[r][c] = "2"
            elif s[r][c].isnumeric():
                s[r][c] = str(int(s[r][c]) + 1)

        print("\n".join(["".join(row) for row in s]))

    def __getitem__(self, time):
        return self.map[time]

    def __hash__(self):
        return hash(tuple(self.map.keys()))

    def keys(self):
        return self.map.keys()


visited = set()


def bfs(map, map_height, map_width, start, end, start_time=0):
    time = start_time
    deq = deque([start])
    visited.add((start[0], start[1], start_time))
    while deq:
        while time not in map.keys():
            map.move()
        qlen = len(deq)
        for _ in range(qlen):
            cur_r, cur_c = deq.popleft()
            for next_r, next_c in [
                (cur_r, cur_c + 1),
                (cur_r, cur_c - 1),
                (cur_r + 1, cur_c),
                (cur_r - 1, cur_c),
                (cur_r, cur_c),  # stay
            ]:
                if (next_r, next_c) == end:
                    return time
                if (
                    0 <= next_r < map_height
                    and 0 <= next_c < map_width
                    and (next_r, next_c, time + 1) not in visited
                    and map[time][next_r][next_c] == True
                ):
                    # is a valid cell
                    visited.add((next_r, next_c, time + 1))
                    deq.append((next_r, next_c))
        time += 1


def solve(data):
    # build map
    blizzards, map_width, map_height = data
    timed_map = TimedMap(map_width, map_height, blizzards)
    # Part 1
    start = (0, 1)
    end = (map_height - 1, map_width - 2)
    part1 = bfs(timed_map, map_height, map_width, start, end, 0)
    print(f"Part 1: {part1}")

    # Part 2
    back_to_start = bfs(timed_map, map_height, map_width, end, start, part1)
    back_to_end = bfs(timed_map, map_height, map_width, start, end, back_to_start)
    print(f"Part 2: {back_to_end}")

    visited.clear()  # for test validation


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    test, input = read_data("test.txt"), read_data("input.txt")
    Test(test, solve, 18, 54)
    solve(input)
