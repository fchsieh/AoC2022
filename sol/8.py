def read_data():
    with open("../data/8.txt") as f:
        return f.read().splitlines()


def part1(data):
    # build tree map
    forest = []
    for line in data:
        forest.append([])
        for tree in line:
            forest[-1].append(int(tree))

    # mark visible trees
    ans = 0
    for row in range(1, len(forest) - 1):
        for col in range(1, len(forest[0]) - 1):
            cur = forest[row][col]
            visible = False
            # visible if left, right, up, down are strictly less than current
            visible_left = all(cur > forest[row][i] for i in range(0, col))
            visible_right = all(
                cur > forest[row][i] for i in range(col + 1, len(forest[0]))
            )
            visible_up = all(cur > forest[i][col] for i in range(0, row))
            visible_down = all(
                cur > forest[i][col] for i in range(row + 1, len(forest))
            )

            visible = visible_left or visible_right or visible_up or visible_down
            if visible:
                ans += 1
    # add four edges
    ans += len(forest[0]) * 2 + len(forest) * 2 - 4
    return ans


def part2(data):
    # build tree map
    forest = []
    for line in data:
        forest.append([])
        for tree in line:
            forest[-1].append(int(tree))

    # find highest scenic score
    scenic_score = -(10**9)
    for row in range(len(forest)):
        for col in range(len(forest[0])):
            cur = forest[row][col]
            score_left = 0
            for left in range(col - 1, -1, -1):
                if forest[row][left] < cur:
                    score_left += 1
                else:
                    score_left += 1
                    break
            score_right = 0
            for right in range(col + 1, len(forest[0])):
                if forest[row][right] < cur:
                    score_right += 1
                else:
                    score_right += 1
                    break
            score_up = 0
            for up in range(row - 1, -1, -1):
                if forest[up][col] < cur:
                    score_up += 1
                else:
                    score_up += 1
                    break
            score_down = 0
            for down in range(row + 1, len(forest)):
                if forest[down][col] < cur:
                    score_down += 1
                else:
                    score_down += 1
                    break
            score = score_left * score_right * score_up * score_down
            scenic_score = max(scenic_score, score)

    return scenic_score


def main():
    data = read_data()
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))


if __name__ == "__main__":
    main()
