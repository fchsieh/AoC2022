# Path: day-23/23.py
# Solution for day 23 of Advent of Code
import os

from collections import defaultdict, deque

from aoc_tools import Test


class Coord(tuple):
    def __new__(cls, *args):
        if len(args) == 1:
            args = args[0]
        return super().__new__(cls, args)

    def __add__(self, other):
        return Coord([a + b for a, b in zip(self, other)])


class Elves:
    def __init__(self, data):
        self.elves = [Coord(c) for c in data]
        self.DIRS = {
            "N": Coord(-1, 0),
            "S": Coord(1, 0),
            "W": Coord(0, -1),
            "E": Coord(0, 1),
            "NE": Coord(-1, 1),
            "NW": Coord(-1, -1),
            "SE": Coord(1, 1),
            "SW": Coord(1, -1),
        }
        self.CHECK = deque(
            [
                (self.DIRS["N"], self.DIRS["NE"], self.DIRS["NW"]),
                (self.DIRS["S"], self.DIRS["SE"], self.DIRS["SW"]),
                (self.DIRS["W"], self.DIRS["NW"], self.DIRS["SW"]),
                (self.DIRS["E"], self.DIRS["NE"], self.DIRS["SE"]),
            ]
        )

    def next_round(self):
        proposals = self.get_proposals()
        for location, elf in proposals.items():
            if len(elf) > 1:
                continue
            self.elves.append(location)
            self.elves.remove(elf.pop())
        self.CHECK.rotate(-1)

    def get_proposals(self):
        proposals = defaultdict(list)
        for elf in self.elves:
            if all(elf + dir not in self.elves for dir in self.DIRS.values()):
                continue
            for to, nei1, nei2 in self.CHECK:
                if all(
                    nei not in self.elves for nei in (elf + to, elf + nei1, elf + nei2)
                ):
                    proposals[elf + to].append(elf)
                    break

        return proposals

    def empty_ground(self):
        max_x, max_y = (
            max(self.elves, key=lambda x: x[0])[0],
            max(self.elves, key=lambda x: x[1])[1],
        )
        min_x, min_y = (
            min(self.elves, key=lambda x: x[0])[0],
            min(self.elves, key=lambda x: x[1])[1],
        )
        # calculate empty ground
        empty_ground = 0
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if Coord(x, y) not in self.elves:
                    empty_ground += 1
        return empty_ground

    def __str__(self):
        max_x, max_y = (
            max(self.elves, key=lambda x: x[0])[0],
            max(self.elves, key=lambda x: x[1])[1],
        )
        min_x, min_y = (
            min(self.elves, key=lambda x: x[0])[0],
            min(self.elves, key=lambda x: x[1])[1],
        )
        elves = set(self.elves)
        s = ""
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                s += "#" if Coord(x, y) in elves else "."
            s += "\n"
        return s


def read_data(file):
    elves = []
    with open(file, "r") as f:
        # get position of elves
        # for line in f.readlines():
        # elves.append(line.strip())
        for row, line in enumerate(f.readlines()):
            line = line.strip()
            for col, c in enumerate(line):
                if c == "#":
                    elves.append((row, col))
    return elves


def solve(data):
    # Part 1
    elves_map = Elves(data)
    prev_state = str(elves_map)
    for i in range(1000):
        elves_map.next_round()
        cur_state = str(elves_map)
        if i == 10:
            print(f"Part 1: {elves_map.empty_ground()}")
        if cur_state == prev_state:
            print(f"Part 2: {i+1}")
            break
        prev_state = cur_state


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    test, input = read_data("test.txt"), read_data("input.txt")
    Test(test, solve, 110, 20)
    solve(input)
