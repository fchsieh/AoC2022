def read_data():
    with open("../data/3.txt") as f:
        raw_data = f.read().splitlines()
        parsed = [x.split() for x in raw_data]
    return parsed


def main():
    data = read_data()

    alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    table = {x: i + 1 for i, x in enumerate(alpha)}

    # Part 1
    score = 0
    for backpack in data:
        backpack = backpack[0]
        first = backpack[: len(backpack) // 2]
        second = backpack[len(backpack) // 2 :]
        # find the common letter in both first and second half
        set_first = set(list(first))
        set_second = set(list(second))
        common = set_first.intersection(set_second)
        score += table[list(common)[0]]
    print("Part 1:", score)

    # Part 2
    score = 0
    # read three lines at a time
    for i in range(0, len(data), 3):
        cur_data = [x[0] for x in data[i : i + 3]]
        # find common letter in current group
        set_1 = set(list(cur_data[0]))
        set_2 = set(list(cur_data[1]))
        set_3 = set(list(cur_data[2]))
        common = set_1.intersection(set_2, set_3)
        score += table[list(common)[0]]
    print("Part 2:", score)


if __name__ == "__main__":
    main()
