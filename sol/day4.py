def read_data():
    with open("../data/day4.txt") as f:
        raw_data = f.read().splitlines()
        parsed = [x.split(",") for x in raw_data]
    return parsed


def main():
    data = read_data()
    # Part 1
    count = 0
    for pair in data:
        elf1 = [int(x) for x in pair[0].split("-")]
        elf2 = [int(x) for x in pair[1].split("-")]
        # check if one is fully contained in the other
        # elf1 is fully contained in elf2
        if elf1[0] >= elf2[0] and elf1[1] <= elf2[1]:
            count += 1
        # elf2 is fully contained in elf1
        elif elf2[0] >= elf1[0] and elf2[1] <= elf1[1]:
            count += 1
    print("Part 1: ", count)

    # Part 2
    count = 0
    for pair in data:
        elf1 = [int(x) for x in pair[0].split("-")]
        elf2 = [int(x) for x in pair[1].split("-")]
        # check if one is overlapping the other
        range_1 = range(elf1[0], elf1[1] + 1)
        range_2 = range(elf2[0], elf2[1] + 1)
        # check if there is an overlap between the two ranges
        if len(set(range_1).intersection(range_2)) > 0:
            count += 1

    print("Part 2: ", count)


if __name__ == "__main__":
    main()
