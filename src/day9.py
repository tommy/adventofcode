from functools import reduce
from pprint import pprint
from collections import deque


def readlines():
    with open("./input/day9.txt") as f:
        for line in f.readlines():
            yield line.strip()


def parse(lines):
    return [[int(x) for x in l] for l in lines]


def indices_of_local_minima(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if is_local_minima(matrix, i, j):
                yield (i, j)


def is_local_minima(matrix, i, j):
    return all(
        map(
            lambda p: matrix[p[0]][p[1]] > matrix[i][j],
            neighbors(i, j, len(matrix), len(matrix[i])),
        )
    )


def neighbors(i, j, width, height):
    if i > 0:
        yield (i - 1, j)
    if i < width - 1:
        yield (i + 1, j)
    if j > 0:
        yield (i, j - 1)
    if j < height - 1:
        yield (i, j + 1)


def solve_one():
    matrix = parse(readlines())
    return sum(map(lambda p: matrix[p[0]][p[1]] + 1, indices_of_local_minima(matrix)))


def solve_two():
    matrix = parse(readlines())
    q = deque(indices_of_local_minima(matrix))
    ds = DisjointSet(
        [(i, j) for i in range(len(matrix)) for j in range(len(matrix[i]))]
    )

    while q:
        i, j = q.popleft()
        for n in neighbors(i, j, len(matrix), len(matrix[i])):
            if matrix[n[0]][n[1]] == 9:
                continue
            if matrix[i][j] < matrix[n[0]][n[1]]:
                ds.union((i, j), n)
                q.append(n)

    basins = {p: ds.size[p] for p in ds.find_roots() if matrix[p[0]][p[1]] != 9}
    return reduce(lambda a, b: a * b, sorted(basins.values())[-3:])


class DisjointSet:
    def __init__(self, ps):
        self.parent = {p: p for p in ps}
        self.size = {p: 1 for p in ps}
        self.rank = {p: 0 for p in ps}

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        xr = self.find(x)
        yr = self.find(y)
        if xr == yr:
            return
        if self.rank[xr] > self.rank[yr]:
            self.parent[yr] = xr
            self.size[xr] = self.size[xr] + self.size[yr]
        else:
            self.parent[xr] = yr
            self.size[yr] = self.size[xr] + self.size[yr]
            if self.rank[xr] == self.rank[yr]:
                self.rank[yr] += 1

    def find_roots(self):
        roots = []
        for p in self.parent:
            if self.parent[p] == p:
                roots.append(p)
        return roots


if __name__ == "__main__":
    pprint(solve_one())
    pprint(solve_two())

    s = DisjointSet([(i, j) for i in range(5) for j in range(5)])
