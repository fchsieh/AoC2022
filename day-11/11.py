import copy
import os
from functools import reduce
from aoc_tools import Test


class Monkey:
    def __init__(
        self, items=[], op=None, mod=None, true_to=None, false_to=None, test=None
    ):
        self.items = items
        self.op = op
        self.true_to = true_to  # if test = true, send item to true_to
        self.false_to = false_to  # if test = false, send item to false_to
        self.inspect_times = 0
        self.mod = mod
        self.test = lambda item: item % self.mod == 0 if test is None else test

    def inspect(self, monkeys, mods=None):
        while self.items:
            self.inspect_times += 1
            item = self.items.pop(0)
            worry = self.op(item)  # perform operation
            if not mods:
                worry //= 3
            else:
                worry %= mods
            if self.test(worry):
                monkeys[self.true_to].items.append(worry)
            else:
                monkeys[self.false_to].items.append(worry)


def read_data(file):
    with open(file) as f:
        data = map(lambda s: s.split("\n"), f.read().split("\n\n"))
    return data


def solve(data):
    monkeys = {}
    for i, monkey in enumerate(data):
        items = list(map(int, monkey[1].split(": ")[-1].split(", ")))
        mod = int(monkey[3].split(" ")[-1])
        op = lambda old, monkey=monkey: eval(monkey[2].split("= ")[-1])
        true_to = int(monkey[4].split(" ")[-1])
        false_to = int(monkey[5].split(" ")[-1])
        monkeys[i] = Monkey(items, op, mod, true_to, false_to)

    # Part 1
    part1_monkeys = copy.deepcopy(monkeys)
    for i in range(20):
        for monkey in part1_monkeys.values():
            monkey.inspect(part1_monkeys)

    ans = [monkey.inspect_times for monkey in part1_monkeys.values()]
    ans.sort(reverse=True)
    print("Part 1:", ans[0] * ans[1])

    # Part 2
    part2_monkeys = copy.deepcopy(monkeys)
    mods = reduce(lambda x, y: x * y, [m.mod for m in part2_monkeys.values()])
    for i in range(10000):
        for monkey in part2_monkeys.values():
            monkey.inspect(part2_monkeys, mods=mods)

    ans = [monkey.inspect_times for monkey in part2_monkeys.values()]
    ans.sort(reverse=True)
    print("Part 2:", ans[0] * ans[1])


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    test, data = read_data("test.txt"), read_data("input.txt")
    Test(test, solve, 10605, 2713310158)
    solve(data)
