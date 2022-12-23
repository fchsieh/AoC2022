from aoc_tools import Test
import os


def read_data(file):
    data = []
    with open("{}.txt".format(file)) as f:
        cur_list = []
        for line in f:
            if line == "\n":
                data.append(cur_list)
                cur_list = []
            else:
                cur_list.append(int(line.strip()))
        data.append(cur_list)
    return data


def solve(data):
    # Part 1
    # find max sum sub-array
    sum_arr = [sum(x) for x in data]
    print("Part 1:", max(sum_arr))

    # Part 2
    # sort the array in descending order
    sum_arr.sort(reverse=True)
    # get the sum of the top 3 elements
    print("Part 2:", sum_arr[0] + sum_arr[1] + sum_arr[2])


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    test, data = read_data("test"), read_data("input")
    Test(test, solve, 24000, 45000)
    solve(data)
