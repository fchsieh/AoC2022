# Path: day-22/22.py
# Solution for day 22 of Advent of Code
import copy
import os
import re
from collections import deque

from aoc_tools import Test


class Node:
    def __init__(self, row, col):
        self.r = row
        self.c = col
        self.left = None
        self.right = None
        self.up = None
        self.down = None
        self.wall = False

    def __str__(self):
        return f"({self.r}, {self.c})"

    @property
    def coord(self):
        return (self.r, self.c)

    @property
    def password(self):
        return (self.r + 1) * 1000 + (self.c + 1) * 4

    @property
    def nei(self):
        return {
            "left": self.left,
            "right": self.right,
            "up": self.up,
            "down": self.down,
        }


def read_data(file):
    data = {"path": [], "map": {}, "start": None}
    with open(file) as f:
        raw_data = f.read().splitlines()
        path = raw_data[-1]
        # split path into (steps, direction) tuples
        path_data = re.findall(r"([0-9]+)([A-Z])", path)
        # convert steps to ints
        path_data = [(int(steps), direction) for steps, direction in path_data]
        data["path"] = path_data

        # create map
        map_data = raw_data[:-2]
        data["raw_map"] = map_data
        for r, row in enumerate(map_data):
            for c, char in enumerate(row):
                if char != " ":
                    # build coordinate system
                    node = Node(r, c)
                    data["map"][node.coord] = node
                    if char == "#":
                        node.wall = True
                    elif char == ".":
                        if data["start"] is None:
                            data["start"] = node

        return data


def part1_warp(data):
    # connect nodes by row
    for r, _ in enumerate(data["raw_map"]):
        sorted_row = sorted(
            [node for node in data["map"].values() if node.r == r],
            key=lambda x: x.c,
        )
        for i, node in enumerate(sorted_row):
            node.left = sorted_row[(i - 1) % len(sorted_row)]
            node.right = sorted_row[(i + 1) % len(sorted_row)]
    # connect nodes by column
    max_col = max(len(row) for row in data["raw_map"])
    for c in range(max_col):
        sorted_col = sorted(
            [node for node in data["map"].values() if node.c == c],
            key=lambda x: x.r,
        )
        for i, node in enumerate(sorted_col):
            node.up = sorted_col[(i - 1) % len(sorted_col)]
            node.down = sorted_col[(i + 1) % len(sorted_col)]


def move(data):
    path = data["path"]
    start = data["start"]
    DIRECTION = deque(["right", "down", "left", "up"])
    for steps, direction in path:
        dir = DIRECTION[0]
        # move by steps
        for _ in range(steps):
            # if moved into a wall, stop
            if start.nei[dir].wall:
                break
            start = start.nei[dir]
        # turn direction
        if direction == "L":  # counter-clockwise
            DIRECTION.rotate(1)
        elif direction == "R":  # clockwise
            DIRECTION.rotate(-1)

    return start.password + ["right", "down", "left", "up"].index(DIRECTION[0])


def solve(data):
    part1_data = copy.deepcopy(data)
    part1_warp(part1_data)
    print(f"Part 1: {move(part1_data)}")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    test, input = read_data("test.txt"), read_data("input.txt")
    # Test(test, solve, 6032, -1)
    solve(test)
    # solve(input)
