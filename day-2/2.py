from aoc_tools import Test
import os


def read_input(file):
    with open(file) as f:
        raw_data = f.read().splitlines()
        parsed = [x.split() for x in raw_data]  # split on whitespace
    return parsed


def choice(C):
    if C == "X" or C == "A":  # rock
        return 1
    elif C == "Y" or C == "B":  # paper
        return 2
    elif C == "Z" or C == "C":  # scissors
        return 3


def score_of_round(opponent, my_choice):
    my = choice(my_choice)
    op = choice(opponent)

    if my == op:
        return 3  # tie

    # scissors beats paper and paper beats rock
    if my - op == 1:  # 3 > 2 and 2 > 1
        return 6  # win
    if my == 1 and op == 3:  # rock beats scissors
        return 6  # win

    return 0  # lose


def score_part_two(opponent, my_choice):
    op = choice(opponent)
    if my_choice == "X":  # we need to lose
        if op == 1:  # op plays rock
            return score_of_round(opponent, "Z") + choice("Z")  # we play scissors
        elif op == 2:  # op plays paper
            return score_of_round(opponent, "X") + choice("X")  # we play rock
        elif op == 3:  # op plays scissors
            return score_of_round(opponent, "Y") + choice("Y")  # we play paper

    elif my_choice == "Y":  # we need to draw
        # we play the same as opponent
        return score_of_round(opponent, opponent) + choice(opponent)

    else:  # we need to win
        if op == 1:  # op plays rock
            return score_of_round(opponent, "Y") + choice("Y")  # we play paper
        elif op == 2:  # op plays paper
            return score_of_round(opponent, "Z") + choice("Z")  # we play scissors
        elif op == 3:  # op plays scissors
            return score_of_round(opponent, "X") + choice("X")  # we play rock


def solve(data):
    # Part 1
    score = 0
    for round in data:
        opponent = round[0]
        my_move = round[1]
        score += score_of_round(opponent, my_move) + choice(my_move)
    print("Part 1:", score)

    # Part 2
    score = 0
    for round in data:
        opponent = round[0]
        my_move = round[1]
        score += score_part_two(opponent, my_move)
    print("Part 2:", score)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    test, data = read_input("test.txt"), read_input("input.txt")
    Test(test, solve, 15, 12)
    solve(data)
