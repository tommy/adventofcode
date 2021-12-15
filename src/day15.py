from pprint import pprint
from heapq import heappush, heappop


def readlines():
    with open("./input/day15.txt") as f:
        for line in f.readlines():
            yield line.strip()


def parse(lines):
    m = {(i, j): int(c) for i, line in enumerate(lines) for j, c in enumerate(line)}
    return (
        m,
        max((i for i, j in m), default=0) + 1,
        max((j for i, j in m), default=0) + 1,
    )


def neighbors(p, rows, cols):
    i, j = p
    return (
        (ii, jj)
        for ii in range(i - 1, i + 2)
        for jj in range(j - 1, j + 2)
        if (ii != i or jj != j)
        and (ii == i or jj == j)
        and (ii >= 0 and ii < rows)
        and (jj >= 0 and jj < cols)
    )


def dist(p):
    return -(p[0] + p[1])


def solve_one():
    m, rows, cols = parse(readlines())
    h = []
    its = 0
    heappush(h, (0, 0, [(0, 0)]))
    seen = {(0, 0)}
    while h:
        its += 1
        cost, _, path = heappop(h)
        # if its % 1000 == 0:
        #     print(its, len(h), len(path), cost)
        if path[-1] == (rows - 1, cols - 1):
            return cost
        for p in neighbors(path[-1], rows, cols):
            if p not in seen:
                seen.add(p)
                heappush(h, (cost + m[p], dist(p), path + [p]))
    else:
        return "no Path!"


def cell_cost(m, size, p):
    i, j = p
    rows, cols = size
    iq, ii = divmod(i, rows)
    jq, jj = divmod(j, cols)
    if iq >= 5 or jq >= 5:
        raise f"out of bounds: {p} {size}"
    cost = m[(ii, jj)] + iq + jq
    if cost < 10:
        return cost
    else:
        return cost - 9


def neighbors_2(p, size):
    i, j = p
    rows, cols = size
    return (
        (ii, jj)
        for ii in range(i - 1, i + 2)
        for jj in range(j - 1, j + 2)
        if (ii != i or jj != j)
        and (ii == i or jj == j)
        and (ii >= 0 and ii < rows)
        and (jj >= 0 and jj < cols)
    )


def solve_two():
    m, rows, cols = parse(readlines())
    size = (rows, cols)
    full_size = (rows * 5, cols * 5)
    end = (full_size[0] - 1, full_size[1] - 1)
    h = []
    its = 0
    heappush(h, (0, 0, [(0, 0)]))
    seen = {(0, 0)}
    # print_costs(m, size, full_size)
    while h:
        its += 1
        cost, _, path = heappop(h)
        # if its % 10 == 0:
        #     print(its, len(h), len(path), cost)
        if path[-1] == end:
            # print_path(path)
            # print([cell_cost(m, size, p) for p in path])
            return cost
        for p in neighbors_2(path[-1], full_size):
            if p not in seen:
                seen.add(p)
                heappush(h, (cost + cell_cost(m, size, p), dist(p), path + [p]))
    else:
        return "no Path!"


def print_costs(m, size, full_size):
    w, h = full_size
    for y in range(h):
        for x in range(w):
            print(cell_cost(m, size, (x, y)), end="")
        print()


def print_path(path):
    w = max(x for x, y in path) + 1
    h = max(y for x, y in path) + 1
    for y in range(h):
        for x in range(w):
            if (x, y) in path:
                print("#", end="")
            else:
                print(".", end="")
        print()


if __name__ == "__main__":
    pprint(solve_one())
    pprint(solve_two())
