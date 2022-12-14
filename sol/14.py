def parse_data(data):
    paths = []
    for line in data.splitlines():
        parts = []
        for part in line.split(" -> "):
            x, y = part.split(",")
            x, y = int(x), int(y)
            parts.append((x, y))
        paths.append(parts)
    return paths


def read_data():
    with open("../data/14.txt") as f:
        input_str = f.read()
    return parse_data(input_str)


def set_rock_structure(data):
    rocks = set()
    for path in data:
        for i, coord in enumerate(path):
            if i == 0:
                continue
            x1, y1 = path[i - 1]
            x2, y2 = coord
            if x1 == x2:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    rocks.add((x1, y))
            elif y1 == y2:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    rocks.add((x, y1))
    return rocks


def flow(rock_structure, max_y, part2=False):
    x = 500
    y = 0
    while y <= max_y and (x, y) not in rock_structure:
        if part2 and y + 1 >= max_y:
            rock_structure.add((x, y))
            return True

        rest = False
        for dx, dy in (0, 1), (-1, 1), (1, 1):
            if (x + dx, y + dy) not in rock_structure:
                x += dx
                y += dy
                rest = True
                break
        if not rest:
            rock_structure.add((x, y))
            return True
    return False


def main():
    data = read_data()
    # Part 1
    rock_structure = set_rock_structure(data)
    max_y = max(y for x, y in rock_structure)
    ans = 0
    while flow(rock_structure, max_y):
        ans += 1
    print("Part 1:", ans)

    # Part 2
    rock_structure = set_rock_structure(data)
    max_y = max(y for x, y in rock_structure) + 2
    ans = 0
    while flow(rock_structure, max_y, part2=True):
        ans += 1
    print("Part 2:", ans)


if __name__ == "__main__":
    main()
