def read_data():
    with open("../data/10.txt") as f:
        data = f.read().splitlines()
    return data


def main():
    data = read_data()
    # Part 1
    signals = [1]  # initial signal
    sprites = [1, 1]  # for part 2
    x = 1
    for op in data:
        if op.startswith("noop"):
            signals.append(x)
            sprites.append(x)
        elif op.startswith("addx"):
            val = int(op.split(" ")[1])
            signals.append(x)  # first cycle for addx
            x += val
            signals.append(x)  # second cycle (value added)
            sprites.extend([x, x])  # finished addx, add to sprites

    cycle = 0
    ans = 0
    for sig in signals:
        # starts calculating from 20th cycle
        cycle += 1
        if cycle >= 20:
            if (cycle - 20) % 40 == 0:
                ans += cycle * sig
    print("Part 1:", ans)
    # Part 2
    crt = []

    for c in range(cycle - 1):
        if c % 40 == 0:
            crt.append([])
            draw_pos = 0
        sprite_pos = {sprites[c] - 1, sprites[c], sprites[c] + 1}
        if draw_pos in sprite_pos:
            crt[-1].append("#")
        else:
            crt[-1].append(".")
        draw_pos += 1
    # copy crt to string
    crt_str = ""
    for row in crt:
        crt_str += "".join(row) + "\n"
    print("Part 2:\n" + crt_str)


if __name__ == "__main__":
    main()
