from collections import defaultdict
import copy

""" Init stack
                        [Z] [W] [Z]
        [D] [M]         [L] [P] [G]
    [S] [N] [R]         [S] [F] [N]
    [N] [J] [W]     [J] [F] [D] [F]
[N] [H] [G] [J]     [H] [Q] [H] [P]
[V] [J] [T] [F] [H] [Z] [R] [L] [M]
[C] [M] [C] [D] [F] [T] [P] [S] [S]
[S] [Z] [M] [T] [P] [C] [D] [C] [D]
 1   2   3   4   5   6   7   8   9 
"""


def read_input():
    with open("../data/day5.txt") as f:
        data = []
        for line in f.readlines():
            cur_line = line.strip().split(" ")
            from_stack = cur_line[3]
            to_stack = cur_line[5]
            moved_crates = int(cur_line[1])
            data.append((from_stack, to_stack, moved_crates))
        return data


def main():
    # build table of each stack
    default_table = defaultdict(list)
    default_table["1"] = list("SCVN")
    default_table["2"] = list("ZMJHNS")
    default_table["3"] = list("MCTGJND")
    default_table["4"] = list("TDFJWRM")
    default_table["5"] = list("PFH")
    default_table["6"] = list("CTZHK")
    default_table["7"] = list("DPRQFSLZ")
    default_table["8"] = list("CSLHDFPW")
    default_table["9"] = list("DSMPFNGZ")
    # Part 1
    table = copy.deepcopy(default_table)
    data = read_input()
    for from_stack, to_stack, moved_crates in data:
        for _ in range(moved_crates):
            table[to_stack].append(table[from_stack].pop())

    # fetch all top crates
    top_crates = []
    for stack in table.values():
        top_crates.append(stack[-1])
    top_crates = "".join(top_crates)
    print("Part 1: ", top_crates)

    # Part 2
    # reset table
    table = copy.deepcopy(default_table)
    for from_stack, to_stack, moved_crates in data:
        to_moved = []
        for _ in range(moved_crates):
            to_moved.append(table[from_stack].pop())
        table[to_stack].extend(to_moved[::-1])

    # fetch all top crates
    top_crates = []
    for stack in table.values():
        top_crates.append(stack[-1])
    top_crates = "".join(top_crates)
    print("Part 2: ", top_crates)


if __name__ == "__main__":
    main()
