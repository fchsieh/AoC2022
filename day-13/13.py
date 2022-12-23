import ast
import functools
import itertools
import os

from aoc_tools import Test


def read_data(file):
    with open(file) as f:
        return [line.split("\n") for line in f.read().split("\n\n")]


def compare(left, right):
    # For part2, customized compare function for sorting
    ret = {
        "cont": 0,
        "true": -1,
        "false": 1,
    }
    if right is None:
        return 1

    # If both values are integers, compare their values
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return ret["true"]
        elif left == right:
            return ret["cont"]
        else:
            return ret["false"]

    # If both values are lists, compare their elements recursively
    elif isinstance(left, list) and isinstance(right, list):
        for a, b in itertools.zip_longest(left, right):
            if a is None:
                return ret["true"]
            elif b is None:
                return ret["false"]
            compared = compare(a, b)
            if compared != ret["cont"]:
                return compared

    # One value is a list and the other is an integer
    else:
        if isinstance(left, list):
            return compare(left, [right])
        else:
            return compare([left], right)
    return ret["cont"]


def solve(data):
    # Part 1
    ans = 0  # number of right order
    for i, line in enumerate(data):
        left = ast.literal_eval(line[0])
        right = ast.literal_eval(line[1])
        if compare(left, right) <= 0:
            ans += i + 1

    print("Part 1:", ans)
    # Part 2
    # flatten data
    data = [ast.literal_eval(d) for sublist in data for d in sublist]
    data.extend([[[2]], [[6]]])
    data.sort(key=functools.cmp_to_key(compare))
    print("Part 2:", (data.index([[2]]) + 1) * (data.index([[6]]) + 1))


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    test, data = read_data("test.txt"), read_data("input.txt")
    Test(test, solve, 13, 140)
    solve(data)
