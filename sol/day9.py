import matplotlib.pyplot as plt


def read_data():
    with open("../data/day9.txt", "r") as f:
        data = f.read().splitlines()
    return data


def add(a, b):
    return [sum(x) for x in zip(a, b)]


def main():
    data = read_data()
    # Part 1
    visited = set()
    head = [0, 0]
    tail = [0, 0]
    dist = lambda h, t: abs(h[0] - t[0]) ** 2 + abs(h[1] - t[1]) ** 2
    for steps in data:
        dir = [0, 0]
        if steps[0] == "R":
            dir[0] = 1
        elif steps[0] == "L":
            dir[0] = -1
        elif steps[0] == "U":
            dir[1] = 1
        elif steps[0] == "D":
            dir[1] = -1
        for _ in range(int(steps[1:])):
            # simulate movement of head and tail
            # move head
            head = add(head, dir)
            # check if tail should move
            d = dist(head, tail)
            if d < 4:
                continue
            else:
                if tail[0] == head[0] - 2:  # move to left of head
                    tail = add(head, [-1, 0])
                elif tail[0] == head[0] + 2:
                    tail = add(head, [1, 0])
                elif tail[1] == head[1] - 2:
                    tail = add(head, [0, -1])
                elif tail[1] == head[1] + 2:
                    tail = add(head, [0, 1])
            visited.add(tuple(tail))

    print("Part 1:", len(visited) + 1)

    # Part 2

    track = set([(0, 0)])
    knots = [[0, 0] for _ in range(10)]
    for steps in data:
        if steps[0] == "R":
            dir = [1, 0]
        elif steps[0] == "L":
            dir = [-1, 0]
        elif steps[0] == "U":
            dir = [0, 1]
        elif steps[0] == "D":
            dir = [0, -1]
        for _ in range(int(steps[1:])):
            knots[0] = add(knots[0], dir)
            for k, ((headx, heady), (tailx, taily)) in enumerate(zip(knots, knots[1:])):
                if abs(headx - tailx) > 1:
                    if headx > tailx:
                        tailx += 1
                    else:
                        tailx -= 1
                    if abs(heady - taily) >= 1:
                        if heady > taily:
                            taily += 1
                        else:
                            taily -= 1
                elif abs(heady - taily) > 1:
                    if heady > taily:
                        taily += 1
                    else:
                        taily -= 1
                    if abs(headx - tailx) >= 1:
                        if headx > tailx:
                            tailx += 1
                        else:
                            tailx -= 1
                knots[k + 1][0] = tailx
                knots[k + 1][1] = taily
            track.add(tuple(knots[-1]))

    print("Part 2:", len(track))


if __name__ == "__main__":
    main()
