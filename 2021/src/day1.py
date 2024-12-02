def main():
    print(solve_one())
    print(solve_two())


def readlines():
    with open("./input/day1.txt") as f:
        for line in f.readlines():
            yield line.strip()


def window(xs, n):
    window = []
    for x in xs:
        window.append(x)
        if len(window) == n:
            break

    yield window

    for x in xs:
        window = window[1:] + [x]
        yield window


def solve_one():
    return len(list([[x, y] for [x, y] in window(map(int, readlines()), 2) if x < y]))


def solve_two():
    ms = map(int, readlines())
    ws = window(ms, 3)
    sums = map(sum, ws)
    pairs_of_sums = window(sums, 2)
    increases = [[x, y] for [x, y] in pairs_of_sums if x < y]
    return len(list(increases))


if __name__ == "__main__":
    main()
