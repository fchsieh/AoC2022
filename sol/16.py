"""
disclaimer: mostly copied from https://gist.github.com/berndtj/7aa2dd7a37f02c004d68287b4ba3a0dd
because I had no idea how to solve this one :(
"""

from collections import deque, defaultdict
from itertools import combinations


class Valve:
    def __init__(self, name, rate, nei) -> None:
        self.name = name
        self.rate = rate
        self.nei = nei


def read_data():
    data = {}
    with open("../data/16.txt") as f:
        for line in f:
            line = line.replace(",", "")
            split_line = line.strip().split(" ")
            valve = split_line[1]
            rate = int(split_line[4][5:-1])
            neighbor = split_line[9:]
            data[valve] = Valve(valve, rate, neighbor)
    return data


def shortest_dist_between_two_valves(data, start, end):
    # run bfs
    q = deque([start])
    visited = set([start])
    dist = 0
    while q:
        for _ in range(len(q)):
            current = q.popleft()
            if current == end:
                return dist
            for nei in data[current].nei:
                if nei not in visited:
                    q.append(nei)
                    visited.add(nei)
        dist += 1
    return -1


def dist_table(data):
    all_valves = list(data.keys())
    table = defaultdict(lambda: 0)
    for name, _ in data.items():
        for another in all_valves:
            key = tuple(sorted([name, another]))
            if another != name and key not in table:
                dist = shortest_dist_between_two_valves(data, name, another)
                table[key] = dist
    return table


def part1(
    name,
    data,
    dist_table,
    unvisited,
    turns=0,
    rate=0,
    flow=0,
    path=None,
    time=30,
    paths=None,
):
    if len(unvisited) == 0:
        flow += (time - turns) * rate
        paths.append((path, flow))
        return flow
    for v_name in unvisited:
        valve = data[v_name]
        new_turns = dist_table[tuple(sorted([name, v_name]))] + 1
        if new_turns == 1 or turns + new_turns > time:
            new_flow = (time - turns) * rate
            paths.append((path, flow + new_flow))
            continue
        new_flow = rate * new_turns
        part1(
            v_name,
            data,
            dist_table,
            unvisited=unvisited - {v_name},
            turns=turns + new_turns,
            rate=rate + valve.rate,
            flow=flow + new_flow,
            path=path + [v_name],
            time=time,
            paths=paths,
        )


def best_path(paths):
    max_flow = (None, 0)
    for p in paths:
        if p[1] > max_flow[1]:
            max_flow = p
    return max_flow


def main():
    data = read_data()

    # Part 1
    dist = dist_table(data)
    unvisited = set([valve.name for valve in data.values() if valve.rate != 0])
    paths = []
    part1("AA", data, dist, unvisited=unvisited, path=[], time=30, paths=paths)
    print("Part 1:", best_path(paths))

    # Part 2
    max_flow = (None, None, 0)
    for i in range(len(data.keys())):
        for c in combinations(unvisited, i):
            s1 = set(c)
            s2 = unvisited - s1
            paths = []
            part1("AA", data, dist, unvisited=s1, path=[], time=26, paths=paths)
            best1 = best_path(paths)
            paths = []
            part1("AA", data, dist, unvisited=s2, path=[], time=26, paths=paths)
            best2 = best_path(paths)
            if best1[1] + best2[1] > max_flow[2]:
                max_flow = (best1, best2, best1[1] + best2[1])
    print("Part 2:", max_flow)


if __name__ == "__main__":
    main()
