from pprint import pprint
import sys


def readlines():
    with open("./input/day11.txt") as f:
        for line in f.readlines():
            yield line.strip()


def parse(lines):
    m = {}
    for i, l in enumerate(lines):
        for j, c in enumerate(l):
            m[(i, j)] = int(c)
    return m


def neighbors(p):
    rows, cols = 10, 10
    i, j = p
    return (
        (ii, jj)
        for ii in range(i - 1, i + 2)
        for jj in range(j - 1, j + 2)
        if (ii != i or jj != j) and (ii >= 0 and ii < rows) and (jj >= 0 and jj < cols)
    )


def step(m):
    flashed = set([p for p in m if m[p] == 9])
    flashing = [p for p in flashed]
    m = {k: (v + 1) % 10 for k, v in m.items()}
    while flashing:
        p = flashing.pop()
        for n in neighbors(p):
            if n not in flashed:
                m[n] += 1
                if m[n] == 10:
                    m[n] = 0
                    flashed.add(n)
                    flashing.append(n)

    return m, flashed


def solve_one():
    m = parse(readlines())
    count = 0
    for _ in range(100):
        m, flashed = step(m)
        count += len(flashed)
    return count


def solve_two():
    m = parse(readlines())
    for n in range(1, sys.maxsize):
        m, flashed = step(m)
        if len(flashed) == 100:
            return n


if __name__ == "__main__":
    pprint(solve_one())
    pprint(solve_two())
