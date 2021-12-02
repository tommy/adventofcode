def main():
    print(solve_one())
    print(solve_two())


def readlines():
    with open("./input/day2.txt") as f:
        for line in f.readlines():
            yield line.strip()


def parse(line):
    [dir, v] = line.split()
    if dir == "forward":
        return [int(v), 0]
    elif dir == "down":
        return [0, int(v)]
    elif dir == "up":
        return [0, -int(v)]


def solve_one():
    [horizontal, depth] = [0, 0]
    for line in readlines():
        [dh, dd] = parse(line)
        horizontal += dh
        depth += dd
    return horizontal * depth


def solve_two():
    [horizontal, aim, depth] = [0, 0, 0]
    for line in readlines():
        [dh, da] = parse(line)
        horizontal += dh
        aim += da
        depth += dh * aim

    return horizontal * depth


if __name__ == "__main__":
    main()
