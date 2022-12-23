import os
from aoc_tools import Test


def read_data(file):
    with open(file) as f:
        return f.readlines()[0]


def solve(data):
    # Part 1
    window = []
    for i in range(len(data)):
        window.append(data[i])
        if len(window) == 5:
            # remove previous element
            window.remove(data[i - 4])
            if len(set(window)) == 4:
                print("Part 1:", i + 1)
                break
    # Part 2
    window = []
    for i in range(len(data)):
        window.append(data[i])
        if len(window) == 15:
            # remove previous element
            window.remove(data[i - 14])
            if len(set(window)) == 14:
                print("Part 2:", i + 1)
                break


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    test, data = read_data("test.txt"), read_data("input.txt")
    Test(test, solve, 7, 19)
    solve(data)
