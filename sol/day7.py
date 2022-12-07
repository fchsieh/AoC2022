import math
import os
from collections import defaultdict


class Dir:
    def __init__(self, path, parent=None):
        self.path = path
        self.parent = parent
        self.children = []
        self.file_size = 0


def read_data():
    with open("../data/day7.txt") as f:
        data = f.read().splitlines()
    return data


def main():
    data = read_data()
    # Part 1
    dir = defaultdict(list)
    path = "/"
    for line in data:
        if line.startswith("$"):  # is command
            command = line.split(" ")
            if command[1] == "cd":  # build dir path
                cd_dir = command[2]
                if cd_dir == "..":
                    # remove last dir from path
                    path = os.path.dirname(path)
                elif cd_dir != "/":
                    path = os.path.join(path, cd_dir)
        else:
            dir[path].append(line)

    # build dir tree
    root = Dir("/")
    dir_table = {"/": root}  # points to dir object
    # run dfs to build dir tree
    stack = [(root, "/")]
    while stack:
        parent, path = stack.pop()
        cur_dir_size = 0
        for d in dir[path]:
            if d.startswith("dir"):
                child_path = os.path.join(path, d.split(" ")[1])
                if child_path not in dir_table:
                    dir_table[child_path] = Dir(child_path, parent)
                child = dir_table[child_path]
                parent.children.append(child)
                stack.append((child, child_path))
            else:
                cur_dir_size += int(d.split(" ")[0])
        parent.file_size += cur_dir_size

    # start from root, run dfs to count file size
    def count_file_size(node):
        if not node.children:  # leaf node
            return node.file_size
        else:
            for child in node.children:
                node.file_size += count_file_size(child)
            return node.file_size

    count_file_size(root)  # update file size for each dir
    # find sum of file size that is at most 1e5
    ans = 0
    for k, v in dir_table.items():
        if v.file_size <= 1e5:
            ans += v.file_size

    print("Part 1:", ans)

    # Part 2
    min_space_to_del = math.inf
    needed_space = 30000000 - (70000000 - dir_table["/"].file_size)
    for k, v in dir_table.items():
        if v.file_size >= needed_space:
            min_space_to_del = min(min_space_to_del, v.file_size)
    print("Part 2:", min_space_to_del)


if __name__ == "__main__":
    main()
