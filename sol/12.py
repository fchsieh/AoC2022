from collections import deque


def read_data():
    with open("../data/12.txt", "r") as f:
        return f.read().splitlines()


def parse_data(data, part2=False):
    table = "abcdefghijklmnopqrstuvwxyz"
    matrix = []
    starts = []
    for r, line in enumerate(data):
        row = []
        for c, char in enumerate(line):
            if (char == "S" or char == "a") and part2:
                starts.append((r, c))
            if char == "S":  # start = a
                row.append(table.index("a"))
                start = (r, c)
            elif char == "E":  # end = z
                row.append(table.index("z"))
                end = (r, c)
            else:
                row.append(table.index(char))
        matrix.append(row)

    return matrix, starts if len(starts) > 0 else start, end


def bfs(mat, start, end):
    visited = [[False for _ in range(len(mat[0]))] for _ in range(len(mat))]
    q = deque([(0, start)])
    while q:
        d, pos = q.popleft()
        r, c = pos
        for new_r, new_c in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
            if new_r < 0 or new_r >= len(mat) or new_c < 0 or new_c >= len(mat[0]):
                continue
            if visited[new_r][new_c]:
                continue
            if mat[new_r][new_c] - mat[r][c] > 1:
                continue
            if (new_r, new_c) == end:
                return d + 1
            visited[new_r][new_c] = True
            q.append((d + 1, (new_r, new_c)))
    return float("inf")  # no path found


def main():
    data = read_data()
    matrix, start, end = parse_data(data)
    # Part 1
    dist = bfs(matrix, start, end)
    print("Part 1:", dist)

    # Part 2
    matrix, starts, end = parse_data(data, part2=True)
    min_dist = float("inf")
    for s in starts:
        dist = bfs(matrix, s, end)
        min_dist = min(min_dist, dist)
    print("Part 2:", min_dist)


if __name__ == "__main__":
    main()
