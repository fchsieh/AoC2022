from collections import deque


def read_data():
    data = []
    with open("../data/18.txt") as f:
        for line in f:
            x, y, z = map(int, line.split(","))
            data.append((x, y, z))
    return data


def part1(cubes):
    cubes_map = {}
    for x, y, z in cubes:
        cubes_map[(x, y, z)] = 6  # surface
    for i in range(len(cubes)):
        for j in range(i + 1, len(cubes)):
            x1, y1, z1 = cubes[i]
            x2, y2, z2 = cubes[j]
            if abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2) == 1:  # adjacent
                # two cubes are adjacent, so they share 2 surface
                # both cubes' surface -= 1
                cubes_map[(x1, y1, z1)] -= 1
                cubes_map[(x2, y2, z2)] -= 1
    return sum(cubes_map.values())


def part2(cubes):
    lava_cubes = {}
    # find range of x, y, z
    x_min, x_max = min(cubes, key=lambda x: x[0])[0], max(cubes, key=lambda x: x[0])[0]
    y_min, y_max = min(cubes, key=lambda x: x[1])[1], max(cubes, key=lambda x: x[1])[1]
    z_min, z_max = min(cubes, key=lambda x: x[2])[2], max(cubes, key=lambda x: x[2])[2]
    for c in cubes:
        lava_cubes[c] = True

    # find trapped air cubes
    trapped_cubes = []
    for x in range(x_min - 1, x_max + 2):
        for y in range(y_min - 1, y_max + 2):
            for z in range(z_min - 1, z_max + 2):
                if (x, y, z) not in cubes:
                    trapped_cubes.append((x, y, z))  # potential trapped air cube
    # find connected components outside the lava
    # run BFS from (x_min - 1, y_min - 1, z_min - 1)
    queue = deque([(x_min - 1, y_min - 1, z_min - 1)])
    seen = set()
    seen.add((x_min - 1, y_min - 1, z_min - 1))
    while queue:
        x, y, z = queue.popleft()
        trapped_cubes.remove((x, y, z))  # not a trapped air cube
        for neighbor in [
            (x + 1, y, z),
            (x - 1, y, z),
            (x, y + 1, z),
            (x, y - 1, z),
            (x, y, z + 1),
            (x, y, z - 1),
        ]:
            if neighbor not in seen and neighbor in trapped_cubes:
                queue.append(neighbor)
                seen.add(neighbor)

    return part1(cubes) - part1(trapped_cubes)


def main():
    cubes = read_data()
    print("Part 1:", part1(cubes))
    print("Part 2:", part2(cubes))


if __name__ == "__main__":
    main()
