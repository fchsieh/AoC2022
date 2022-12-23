import sys
import os
import subprocess


try:
    from aocd.models import Puzzle
except ImportError:
    print("Please install aocd: pip install aocd")
    sys.exit(1)


def download(day, year, path):
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


def main(args):
    if len(args) != 3:
        print("Usage: python setup.py <year> <day>")
        sys.exit(1)
    # setup a new day for aoc
    year = int(args[1])
    day = int(args[2])
    print("Creating new day of AoC: {}-12-{}".format(year, day))
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
    # download input and test
    print("Downloading input and test...")
    download(day, year, folder)
    print("Done! Happy coding!")


if __name__ == "__main__":
    main(sys.argv)
