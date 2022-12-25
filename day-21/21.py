# Path: day-21/21.py
# Solution for day 21 of Advent of Code
import os

from aoc_tools import Test

monkey_map = None


class Monkey:
    op_table = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
        "/": lambda x, y: x // y,
    }

    def __init__(self, expr=""):
        self.val = 0
        self.op = None
        self.left_val: str = ""
        self.right_val: str = ""
        self.name = None

        operands = expr.split()
        self.name = operands[0][:-1]
        if len(operands) == 2:
            self.val = int(operands[-1])
        else:
            _, left_val, op, right_val = operands
            self.op = self.op_table[op]
            self.left_val = left_val
            self.right_val = right_val

    def __str__(self):
        if self.op is None:
            return f"{self.name} := {self.val}"
        return f"{self.name} := left: {self.left_val}, right: {self.right_val}"


def read_data(file):
    monkeys_map = {}
    with open(file) as f:
        for line in f:
            new_monkey = Monkey(line)
            monkeys_map[new_monkey.name] = new_monkey
    return monkeys_map


def calc(name):
    cur_monkey = monkey_map[name]
    if cur_monkey.op is None:  # is a number
        return cur_monkey.val

    left = monkey_map[cur_monkey.left_val]
    right = monkey_map[cur_monkey.right_val]
    return cur_monkey.op(calc(left.name), calc(right.name))


def solve(data):
    # for validation
    is_test = False
    if "is_test" in data:
        is_test = True

    global monkey_map
    monkey_map = data
    root_val = calc("root")
    print(f"Part 1: {root_val}")

    low = -int(1e128)
    high = int(1e128)
    root_left = data["root"].left_val
    root_right = data["root"].right_val

    while low < high:
        mid = low + (high - low) // 2
        monkey_map["humn"].val = mid
        left = calc(root_left)
        right = calc(root_right)
        if left == right:
            print(f"Part 2: {mid}")
            return
        elif left < right:
            # test file has different order
            if is_test:
                low = mid + 1
            else:
                high = mid - 1
        else:
            if is_test:
                high = mid - 1
            else:
                low = mid + 1


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    test, input = read_data("test.txt"), read_data("input.txt")
    test["is_test"] = True  # for validation only
    Test(test, solve, 152, 301)
    solve(input)
