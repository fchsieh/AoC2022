# Path: day-19/19.py
# Solution for day 19 of Advent of Code
import os
from aoc_tools import Test
from functools import lru_cache, reduce

seen = set()


class State:
    def __init__(
        self,
        ore=0,
        clay=0,
        obsidian=0,
        geodes=0,
        ore_robot=1,
        clay_robot=0,
        obsidian_robot=0,
        geodes_robot=0,
        time=24,
    ):
        self.ore = ore
        self.clay = clay
        self.obsidian = obsidian
        self.geodes = geodes
        self.ore_robot = ore_robot
        self.clay_robot = clay_robot
        self.obsidian_robot = obsidian_robot
        self.geodes_robot = geodes_robot
        self.time = time

    def __str__(self):
        return f"State(ore={self.ore}, clay={self.clay}, obs={self.obsidian}, geo={self.geodes}, ore_r={self.ore_robot}, clay_r={self.clay_robot}, obs_r={self.obsidian_robot}, geo_r={self.geodes_robot}, time={self.time})"

    @property
    def val(self):
        return (
            self.ore,
            self.clay,
            self.obsidian,
            self.geodes,
            self.ore_robot,
            self.clay_robot,
            self.obsidian_robot,
            self.geodes_robot,
            self.time,
        )


class Blueprint:
    def __init__(self, line):
        blueprint_id, robots = line[10:-1].split(": ")
        self.id = int(blueprint_id)
        self.cost_table = {}
        for robot in robots.split(". "):
            type, costs = robot[5:].split(" robot costs ")
            costs = costs.split(" and ")
            self.cost_table[type] = {}
            for cost in costs:
                amount, resource = cost.split(" ")
                self.cost_table[type][resource] = int(amount)

        self.max_ore = max(self.cost_table[t]["ore"] for t in self.cost_table)

    def __str__(self):
        return f"Blueprint {self.id}: {self.cost_table}"

    @property
    def cost(self):
        return self.cost_table


@lru_cache(maxsize=1500)
def max_geodes(bp, ore, clay, obs, geo, ore_r, clay_r, obs_r, geo_r, time):
    # recursion based bfs (with lru cache)
    cost = bp.cost
    max_ore = bp.max_ore

    best = geo
    if time == 0:
        return best

    # try to prune the search tree
    # do not need to build more robots than the cost
    ore_r = min(max_ore, ore_r)
    # obsidian robot requires clay
    clay_r = min(cost["obsidian"]["clay"], clay_r)
    # geode robot requires obsidian
    obs_r = min(cost["geode"]["obsidian"], obs_r)

    # resources cannot exceed the maximum amount achievable
    ore = min(ore, time * max_ore - ore_r * (time - 1))
    clay = min(clay, time * cost["obsidian"]["clay"] - clay_r * (time - 1))
    obs = min(obs, time * cost["geode"]["obsidian"] - obs_r * (time - 1))

    state = (ore, clay, obs, geo, ore_r, clay_r, obs_r, geo_r, time)
    if state in seen:
        return best
    seen.add(state)

    # start building robots (or just wait)
    # always buy one geode robot if possible
    if ore >= cost["geode"]["ore"] and obs >= cost["geode"]["obsidian"]:
        buy_geode = max_geodes(
            bp,
            ore + ore_r - cost["geode"]["ore"],
            clay + clay_r,
            obs + obs_r - cost["geode"]["obsidian"],
            geo + geo_r,
            ore_r,
            clay_r,
            obs_r,
            geo_r + 1,
            time - 1,
        )
        best = max(best, buy_geode)
    # buy one ore robot
    if ore >= cost["ore"]["ore"]:
        buy_ore = max_geodes(
            bp,
            ore + ore_r - cost["ore"]["ore"],
            clay + clay_r,
            obs + obs_r,
            geo + geo_r,
            ore_r + 1,
            clay_r,
            obs_r,
            geo_r,
            time - 1,
        )
        best = max(best, buy_ore)

    # buy one clay robot
    if ore >= cost["clay"]["ore"]:
        buy_clay = max_geodes(
            bp,
            ore + ore_r - cost["clay"]["ore"],
            clay + clay_r,
            obs + obs_r,
            geo + geo_r,
            ore_r,
            clay_r + 1,
            obs_r,
            geo_r,
            time - 1,
        )
        best = max(best, buy_clay)
    # buy one obsidian robot
    if ore >= cost["obsidian"]["ore"] and clay >= cost["obsidian"]["clay"]:
        buy_obs = max_geodes(
            bp,
            ore + ore_r - cost["obsidian"]["ore"],
            clay + clay_r - cost["obsidian"]["clay"],
            obs + obs_r,
            geo + geo_r,
            ore_r,
            clay_r,
            obs_r + 1,
            geo_r,
            time - 1,
        )
        best = max(best, buy_obs)
    # idle
    idle = max_geodes(
        bp,
        ore + ore_r,
        clay + clay_r,
        obs + obs_r,
        geo + geo_r,
        ore_r,
        clay_r,
        obs_r,
        geo_r,
        time - 1,
    )
    best = max(best, idle)

    return best


def read_data(file):
    with open(file, "r") as f:
        data = [Blueprint(line.rstrip()) for line in f.readlines()]
    return data


def solve(blueprints):
    # Part 1
    bp_count = 0
    part1 = 0
    part2 = 1
    for bp in blueprints:
        if bp_count < 3:  # for part 2
            # reset seen
            seen.clear()
            part2_max = max_geodes(bp, 0, 0, 0, 0, 1, 0, 0, 0, 32)
            #print(f"(Part 2) ID: {bp.id} max geodes: {part2_max}")
            part2 *= part2_max
        bp_count += 1
        # part 1
        # reset seen
        seen.clear()
        part1_max = max_geodes(bp, 0, 0, 0, 0, 1, 0, 0, 0, 24)
        #print(f"(Part 1) ID: {bp.id} max geodes: {part1_max}")
        part1 += part1_max * bp.id

    print("Part 1:", part1)
    print("Part 2:", part2)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    test, input = read_data("test.txt"), read_data("input.txt")
    Test(test, solve, 33, 3472)
    solve(input)
