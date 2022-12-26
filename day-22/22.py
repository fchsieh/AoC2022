# Path: day-22/22.py
# Solution for day 22 of Advent of Code
import copy
import os
import re
from collections import deque

from aoc_tools import Test


def read_data(file):
    data = {"path": [], "map": {}, "start": None, "warp": {}}
    with open(file) as f:
        raw_data = f.read().splitlines()
        path = raw_data[-1]
        # split path into (steps, direction) tuples
        path_data = re.findall(r"([0-9]+)([A-Z]*)", path)
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
        neighbors = [n.coord for n in self.nei.values() if n is not None]
        return f"({self.r}, {self.c}) -> {neighbors if neighbors else 'None'}"

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


class Face:
    def __init__(self, data=None, start=None, side=-1):
        self.data = data
        self.nodes = []

        # build face
        self.build_face(start, side)
        self.set_boundary()
        self.connect_inner_nodes()

        # check if face is built correctly
        assert len(self.nodes) == side**2, "Not all nodes are in face"

    def build_face(self, start, side):
        for r in range(start[0], start[0] + side):
            for c in range(start[1], start[1] + side):
                if (r, c) in self.data["map"]:
                    self.nodes.append(self.data["map"][(r, c)])

    def set_boundary(self):
        min_r = min(node.r for node in self.nodes)
        max_r = max(node.r for node in self.nodes)
        min_c = min(node.c for node in self.nodes)
        max_c = max(node.c for node in self.nodes)
        self.row_range = (min_r, max_r)
        self.col_range = (min_c, max_c)
        self.left_nodes = sorted(
            [node for node in self.nodes if node.c == min_c], key=lambda x: x.r
        )
        self.right_nodes = sorted(
            [node for node in self.nodes if node.c == max_c], key=lambda x: x.r
        )
        self.up_nodes = sorted(
            [node for node in self.nodes if node.r == min_r], key=lambda x: x.c
        )
        self.down_nodes = sorted(
            [node for node in self.nodes if node.r == max_r], key=lambda x: x.c
        )

    def connect_inner_nodes(self):
        for r in range(self.row_range[0] + 1, self.row_range[1]):
            for c in range(self.col_range[0] + 1, self.col_range[1]):
                node = self.data["map"][(r, c)]
                node.left = self.data["map"][(r, c - 1)]
                node.right = self.data["map"][(r, c + 1)]
                node.up = self.data["map"][(r - 1, c)]
                node.down = self.data["map"][(r + 1, c)]

    def connect(self, face, my="", their="", rev=False, warp_dir=""):
        my_nodes = getattr(self, f"{my}_nodes")
        their_nodes = getattr(face, f"{their}_nodes")
        if rev:
            their_nodes = their_nodes[::-1]

        for my_node, their_node in zip(my_nodes, their_nodes):
            # connect nodes between faces
            setattr(my_node, f"{my}", their_node)
            setattr(their_node, f"{their}", my_node)

            # moving to another face needs to change direction
            self.data["warp"][(my_node.coord, their_node.coord)] = warp_dir

        if my == "up" or my == "down":
            for i, node in enumerate(my_nodes):
                if my == "up":
                    down_node = self.data["map"][(node.r + 1, node.c)]
                    node.down = down_node
                elif my == "down":
                    up_node = self.data["map"][(node.r - 1, node.c)]
                    node.up = up_node
                # connect left and right of current row
                if 0 < i < len(my_nodes) - 1:
                    left_node = self.data["map"][(node.r, node.c - 1)]
                    right_node = self.data["map"][(node.r, node.c + 1)]
                    node.left = left_node
                    node.right = right_node
                elif i == 0:
                    right_node = self.data["map"][(node.r, node.c + 1)]
                    node.right = right_node
                elif i == len(my_nodes) - 1:
                    left_node = self.data["map"][(node.r, node.c - 1)]
                    node.left = left_node
        elif my == "left" or my == "right":
            for i, node in enumerate(my_nodes):
                if my == "left":
                    right_node = self.data["map"][(node.r, node.c + 1)]
                    node.right = right_node
                elif my == "right":
                    left_node = self.data["map"][(node.r, node.c - 1)]
                    node.left = left_node
                # connect up and down of current col
                if 0 < i < len(my_nodes) - 1:
                    up_node = self.data["map"][(node.r - 1, node.c)]
                    down_node = self.data["map"][(node.r + 1, node.c)]
                    node.up = up_node
                    node.down = down_node
                elif i == 0:
                    down_node = self.data["map"][(node.r + 1, node.c)]
                    node.down = down_node
                elif i == len(my_nodes) - 1:
                    up_node = self.data["map"][(node.r - 1, node.c)]
                    node.up = up_node

    def __str__(self):
        return f"Face {self.id} -> {[x.coord for x in self.nodes]}"


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


def test_part2_warp(data, side=4):
    # Just a lot of hardcoding...
    face1 = Face(data, (0, 8), side)
    face2 = Face(data, (4, 0), side)
    face3 = Face(data, (4, 4), side)
    face4 = Face(data, (4, 8), side)
    face5 = Face(data, (8, 8), side)
    face6 = Face(data, (8, 12), side)
    # face1
    face1.connect(face2, my="up", their="up", rev=True, warp_dir="down")
    face1.connect(face3, my="left", their="up", rev=False, warp_dir="down")
    face1.connect(face4, my="down", their="up", rev=False, warp_dir="down")
    face1.connect(face6, my="right", their="right", rev=True, warp_dir="left")
    # face2
    face2.connect(face1, my="up", their="up", rev=True, warp_dir="down")
    face2.connect(face6, my="left", their="down", rev=True, warp_dir="up")
    face2.connect(face3, my="right", their="left", rev=False, warp_dir="right")
    face2.connect(face5, my="down", their="down", rev=True, warp_dir="up")
    # face3
    face3.connect(face1, my="up", their="left", rev=False, warp_dir="right")
    face3.connect(face2, my="left", their="right", rev=False, warp_dir="left")
    face3.connect(face4, my="right", their="left", rev=False, warp_dir="right")
    face3.connect(face5, my="down", their="left", rev=True, warp_dir="right")
    # face4
    face4.connect(face1, my="up", their="down", rev=False, warp_dir="up")
    face4.connect(face3, my="left", their="right", rev=False, warp_dir="left")
    face4.connect(face6, my="right", their="up", rev=True, warp_dir="down")
    face4.connect(face5, my="down", their="up", rev=False, warp_dir="down")
    # face5
    face5.connect(face4, my="up", their="down", rev=False, warp_dir="up")
    face5.connect(face3, my="left", their="down", rev=True, warp_dir="up")
    face5.connect(face6, my="right", their="left", rev=False, warp_dir="right")
    face5.connect(face2, my="down", their="down", rev=True, warp_dir="up")
    # face6
    face6.connect(face4, my="up", their="right", rev=True, warp_dir="left")
    face6.connect(face5, my="left", their="right", rev=False, warp_dir="left")
    face6.connect(face1, my="right", their="right", rev=True, warp_dir="left")
    face6.connect(face2, my="down", their="left", rev=True, warp_dir="right")


def input_part2_warp(data):
    face1 = Face(data, (0, 50), 50)
    face2 = Face(data, (0, 100), 50)
    face3 = Face(data, (50, 50), 50)
    face4 = Face(data, (100, 0), 50)
    face5 = Face(data, (100, 50), 50)
    face6 = Face(data, (150, 0), 50)
    # face1
    face1.connect(face6, my="up", their="left", rev=False, warp_dir="right")
    face1.connect(face4, my="left", their="left", rev=True, warp_dir="right")
    face1.connect(face2, my="right", their="left", rev=False, warp_dir="right")
    face1.connect(face3, my="down", their="up", rev=False, warp_dir="down")
    # face2
    face2.connect(face1, my="left", their="right", rev=False, warp_dir="left")
    face2.connect(face6, my="up", their="down", rev=False, warp_dir="up")
    face2.connect(face5, my="right", their="right", rev=True, warp_dir="left")
    face2.connect(face3, my="down", their="right", rev=False, warp_dir="left")
    # face3
    face3.connect(face1, my="up", their="down", rev=False, warp_dir="up")
    face3.connect(face4, my="left", their="up", rev=False, warp_dir="down")
    face3.connect(face2, my="right", their="down", rev=False, warp_dir="up")
    face3.connect(face5, my="down", their="up", rev=False, warp_dir="down")
    # face4
    face4.connect(face3, my="up", their="left", rev=False, warp_dir="right")
    face4.connect(face1, my="left", their="left", rev=True, warp_dir="right")
    face4.connect(face5, my="right", their="left", rev=False, warp_dir="right")
    face4.connect(face6, my="down", their="up", rev=False, warp_dir="down")
    # face5
    face5.connect(face3, my="up", their="down", rev=False, warp_dir="up")
    face5.connect(face4, my="left", their="right", rev=False, warp_dir="left")
    face5.connect(face2, my="right", their="right", rev=True, warp_dir="left")
    face5.connect(face6, my="down", their="right", rev=False, warp_dir="left")
    # face6
    face6.connect(face4, my="up", their="down", rev=False, warp_dir="up")
    face6.connect(face1, my="left", their="up", rev=False, warp_dir="down")
    face6.connect(face5, my="right", their="down", rev=False, warp_dir="up")
    face6.connect(face2, my="down", their="up", rev=False, warp_dir="down")


def print_map(data, route):
    max_col = max(len(row) for row in data["raw_map"])
    for r in range(len(data["raw_map"])):
        for c in range(max_col):
            if (r, c) in route:
                dir = route[(r, c)]
                if dir == "up":
                    print("^", end="")
                elif dir == "down":
                    print("v", end="")
                elif dir == "left":
                    print("<", end="")
                elif dir == "right":
                    print(">", end="")
            elif (r, c) in data["map"]:
                print("#" if data["map"][(r, c)].wall else ".", end="")
            else:
                print(" ", end="")
        print()


def move(data):
    path = data["path"]
    start = data["start"]
    route = {}
    DIRECTION = deque(["right", "down", "left", "up"])
    for steps, direction in path:
        dir = DIRECTION[0]
        # move by steps
        for _ in range(steps):
            route[start.coord] = dir
            destination = start.nei[dir]
            # if moved into a wall, stop
            if destination.wall:
                break
            # check if is crossing a warp, if so, change direction
            if (start.coord, start.nei[dir].coord) in data["warp"]:
                # rotate until match the warp direction
                dir = data["warp"][(start.coord, start.nei[dir].coord)]
                while DIRECTION[0] != dir:
                    DIRECTION.rotate(1)
            start = destination

        # turn direction
        if direction == "L":  # counter-clockwise
            DIRECTION.rotate(1)
        elif direction == "R":  # clockwise
            DIRECTION.rotate(-1)
    # print_map(data, route)
    return start.password + ["right", "down", "left", "up"].index(DIRECTION[0])


def solve(data):
    part1_data = copy.deepcopy(data)
    part1_warp(part1_data)
    print(f"Part 1: {move(part1_data)}")

    part2_data = copy.deepcopy(data)
    if "test" in data:
        test_part2_warp(part2_data)
    else:
        input_part2_warp(part2_data)
    print(f"Part 2: {move(part2_data)}")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    test, input = read_data("test.txt"), read_data("input.txt")
    test["test"] = True
    Test(test, solve, 6032, 5031)
    solve(input)
