"""
validates if the function prints the correct output for the given input
"""
import sys, io


class Test:
    def __init__(self, data, function, part1, part2):
        stdout = sys.stdout
        sys.stdout = io.StringIO()
        function(data)
        output = sys.stdout.getvalue()
        self.test(output, (part1, part2))
        # reset the stdout
        sys.stdout = stdout
        print("Test passed")

    def test(self, output, expected):
        assert output == "Part 1: {}\nPart 2: {}\n".format(
            expected[0], expected[1]
        ), "Test failed"


if __name__ == "__main__":
    print("testing script of AoC")
