import os
from aoc_tools import Test


class Grid:
    def __init__(self, width):
        self.width = width
        self.grid = set([(x, 0) for x in range(width)])

    def __str__(self) -> str:
        s = "\n"
        max_height = 20
        max_y = max([y for _, y in self.grid])
        min_y = max(0, max_y - max_height)

        for y in range(max_y, min_y - 1, -1):
            s += "|" if y != 0 else "+"
            for x in range(self.width):
                if (x, y) in self.grid:
                    if y != 0:
                        s += "#"
                    else:
                        s += "-"
                else:
                    s += "."
            s += "| %d\n" % y if y != 0 else "+\n"
        return s

    def add(self, rock):
        self.grid.add(rock)


class Rock:
    def __init__(self, top, type) -> None:
        self.rocks = []
        self.type = type
        self.add(top)

    def add(self, top) -> None:
        rocks_table = {
            "-": lambda x, y: [
                [x + 2, y + 0],
                [x + 3, y + 0],
                [x + 4, y + 0],
                [x + 5, y + 0],
            ],
            "+": lambda x, y: [
                [x + 2, y + 1],
                [x + 3, y],
                [x + 3, y + 1],
                [x + 3, y + 2],
                [x + 4, y + 1],
            ],
            "J": lambda x, y: [
                [x + 2, y + 0],
                [x + 3, y + 0],
                [x + 4, y + 0],
                [x + 4, y + 1],
                [x + 4, y + 2],
            ],
            "|": lambda x, y: [
                [x + 2, y + 0],
                [x + 2, y + 1],
                [x + 2, y + 2],
                [x + 2, y + 3],
            ],
            "o": lambda x, y: [
                [x + 2, y + 0],
                [x + 3, y + 0],
                [x + 2, y + 1],
                [x + 3, y + 1],
            ],
        }

        self.rocks = rocks_table[self.type](0, top + 4)

    def move(self, direction) -> None:
        if direction == "<":
            self.rocks = [(x - 1, y) for x, y in self.rocks]
        elif direction == ">":
            self.rocks = [(x + 1, y) for x, y in self.rocks]
        elif direction == "v":
            self.rocks = [(x, y - 1) for x, y in self.rocks]

    def rest(self, grid) -> int:
        # add rock to grid and return max height of current rocks
        max_height = 0
        for r in self.rocks:
            grid.add(r)
            max_height = max(max_height, r[1])
        return max_height

    def simulate(self, grid, direction) -> bool:
        # return true if rocks has come to rest
        def can_move(direction):
            for r in self.rocks:
                x, y = r
                if direction == "<":
                    if x == 0 or (x - 1, y) in grid.grid:
                        return False
                elif direction == ">":
                    if x == grid.width - 1 or (x + 1, y) in grid.grid:
                        return False
            return True

        def can_fall():
            for r in self.rocks:
                x, y = r
                if (x, y - 1) in grid.grid:
                    return False
            return True

        if can_move(direction):
            self.move(direction)

        if can_fall():
            self.move("v")
            return False  # can continue falling

        return True  # has come to rest


def read_data(file):
    with open(file) as f:
        data = list(f.read())
    return data


def part1(data, rock_type, max_rocks=2022):
    grid = Grid(7)
    rocks_idx = 0
    dir_idx = 0
    tower_height = 0

    while rocks_idx < max_rocks:
        rock = Rock(tower_height, rock_type[rocks_idx % len(rock_type)])
        while True:
            dir = data[dir_idx % len(data)]
            rest = rock.simulate(grid, dir)
            dir_idx += 1
            if rest:
                # rock has stopped
                break

        rocks_height = rock.rest(grid)
        tower_height = max(tower_height, rocks_height)
        rocks_idx += 1

    return tower_height


def part2(data, rock_type, max_rocks=1000000000000):
    """
    disclaimer: mostly copied from https://github.com/terminalmage/adventofcode/blob/main/2022/day17.py
    """
    grid = Grid(7)
    rocks_idx = 0
    dir_idx = 0
    tower_height = 0
    seen = {}

    for rocks_idx in range(max_rocks):
        rock = Rock(tower_height, rock_type[rocks_idx % len(rock_type)])
        while True:
            if rocks_idx > 1000:
                key = (rocks_idx % len(rock_type), dir_idx % len(data))
                if key in seen:  # same rock type and direction found
                    prev_rocks_idx, prev_height = seen[key]
                    period = rocks_idx - prev_rocks_idx
                    if rocks_idx % period == max_rocks % period:
                        cycle_height = tower_height - prev_height
                        rocks_remain = max_rocks - rocks_idx
                        cycles_remain = rocks_remain // period + 1
                        return prev_height + cycle_height * cycles_remain
                else:
                    seen[key] = (rocks_idx, tower_height)

            dir = data[dir_idx % len(data)]
            rest = rock.simulate(grid, dir)
            dir_idx += 1
            if rest:
                # rock has stopped
                break

        rocks_height = rock.rest(grid)
        tower_height = max(tower_height, rocks_height)
        rocks_idx += 1

    return tower_height


def solve(data):
    # Part 1
    rock_type = ["-", "+", "J", "|", "o"]
    print("Part 1:", part1(data, rock_type, max_rocks=2022))

    print("Part 2:", part2(data, rock_type, max_rocks=1000000000000))


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    test, data = read_data("test.txt"), read_data("input.txt")
    Test(test, solve, 3068, 1514285714288)
    solve(data)
