from os import remove


def readlines():
    with open("./input/day5.txt") as f:
        for line in f.readlines():
            yield line.strip()


def parse():
    for l in readlines():
        s, _, e = l.split()
        yield (
            list(map(int, s.split(","))),
            list(map(int, e.split(","))),
        )


def diagonal(s, e):
    (x1, y1), (x2, y2) = s, e
    return x1 != x2 and y1 != y2


def step(x1, x2):
    if x1 == x2:
        return 0
    if x1 < x2:
        return 1
    return -1


def points_on_line(vent):
    s, e = vent

    dx = step(s[0], e[0])
    dy = step(s[1], e[1])

    x, y = s
    while x != e[0] or y != e[1]:
        yield (x, y)
        x += dx
        y += dy
    yield (x, y)


def max_coord(vents):
    mx, my = (0, 0)
    for (s, e) in vents:
        for x, y in [s, e]:
            mx = max(mx, x)
            my = max(my, y)
    return mx + 1, my + 1


def flatten(xxs):
    for xs in xxs:
        for x in xs:
            yield x


def solve_one():
    vents = parse()
    vents = list(filter(lambda v: not diagonal(v[0], v[1]), vents))
    mx, my = max_coord(vents)
    counts = [[0] * my for _ in range(mx)]
    for v in vents:
        for i, j in points_on_line(v):
            counts[i][j] = counts[i][j] + 1

    # for xs in counts:
    #     print(xs)

    return len(list(filter(lambda x: x > 1, flatten(counts))))


def solve_two():
    vents = list(parse())
    mx, my = max_coord(vents)
    counts = [[0] * my for _ in range(mx)]
    for v in vents:
        for i, j in points_on_line(v):
            counts[i][j] = counts[i][j] + 1

    # for xs in counts:
    #     print(xs)

    return len(list(filter(lambda x: x > 1, flatten(counts))))


def main():
    print(solve_one())
    print(solve_two())


if __name__ == "__main__":
    main()
