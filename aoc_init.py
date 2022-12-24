import sys
import os
import subprocess


try:
    from aocd.models import Puzzle
except ImportError:
    print("Please install aocd: pip install aocd")
    sys.exit(1)


def build_folder(day):
    # create folder
    folder = "day-{}".format(day)
    print("Creating folder: {}".format(folder))
    # create files
    files = ["test.txt", "input.txt", "{}.py".format(day)]
    try:
        os.mkdir(folder)
    except FileExistsError:
        print("Folder {} already exists".format(folder))
    for file in files:
        try:
            open(os.path.join(folder, file), "w")
        except FileExistsError:
            print("File {} already exists".format(file))
    return folder


def download(day, year, path):
    print("Downloading input and example data...")
    # check if session key is set
    if "AOC_SESSION" not in os.environ:
        token = subprocess.check_output(["aocd-token".format(day, year)])
        token = token.decode("utf-8").split(" ")[0].strip()
        os.environ["AOC_SESSION"] = token

    puzzle = Puzzle(year=year, day=day)
    # download test
    test_location = os.path.join(path, "test.txt")
    with open(test_location, "w") as f:
        f.write(puzzle.example_data)

    # download input
    input_location = os.path.join(path, "input.txt")
    with open(input_location, "w") as f:
        f.write(puzzle.input_data)


def write_default_code(day):
    with open("day-{}/{}.py".format(day, day), "w") as f:
        f.write("# Path: day-{}/{}.py\n".format(day, day))
        f.write("# Solution for day {} of Advent of Code\n".format(day))
        f.write("import os\n\nfrom aoc_tools import Test\n\n\n")
        f.write("def read_data(file):\n\tpass\n\n\n")
        f.write("def solve(data):\n\tpass\n\n\n")
        f.write('if __name__ == "__main__":\n')
        f.write("\tos.chdir(os.path.dirname(os.path.abspath(__file__)))\n")
        f.write('\ttest, input = read_data("test.txt"), read_data("input.txt")\n')
        f.write("\tTest(test, solve, -1, -1)\n")
        f.write("\tsolve(input)\n")


def main(args):
    if len(args) != 3:
        print("Usage: python setup.py <year> <day>")
        sys.exit(1)
    # setup a new day for aoc
    year = int(args[1])
    day = int(args[2])
    # Check if folder exists
    if os.path.exists("day-{}".format(day)):
        print("Day {} already exists".format(day))
        sys.exit(1)
    print("Creating new day of AoC: {}-12-{}".format(year, day))

    # Create folder
    folder = build_folder(day)
    # Download input and test data
    download(day, year, folder)
    # write default code for day
    write_default_code(day)

    print("Done! Happy coding!")


if __name__ == "__main__":
    main(sys.argv)
