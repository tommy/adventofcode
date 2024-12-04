from itertools import islice
from pprint import pprint
import re
from collections import defaultdict, Counter


def readlines():
    with open("./input/day19-example.txt") as f:
        for line in f.readlines():
            yield line.strip()


def parse(lines):
    data = defaultdict(list)
    s = None
    for line in lines:
        if line == "":
            continue
        m = re.match(r"^--- scanner (\d)+ ---$", line)
        if m:
            s = int(m.group(1))
        else:
            point = [int(x) for x in line.split(",")]
            data[s].append(point)
    return data


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


def minus(a, b):
    return [x - y for x, y in zip(a, b)]


assert minus([1, 2, 1], [3, 4, 5]) == [-2, -2, -4]


def roll(v):
    return (v[0], v[2], -v[1])


def turn(v):
    return (-v[1], v[0], v[2])


def sequence(v):
    for cycle in range(2):
        for step in range(3):  # Yield RTTT 3 times
            v = roll(v)
            yield (v)  #    Yield R
            for i in range(3):  #    Yield TTT
                v = turn(v)
                yield (v)
        v = roll(turn(roll(v)))  # Do RTR


def transforms(a):
    return list(zip(*[sequence(x) for x in a]))


def pairwise_diffs(a):
    return [(x, y, minus(x, y)) for x in a for y in a if x != y]


def count_diffs(a, b):
    return Counter([tuple(d) for _, _, d in pairwise_diffs(a) + pairwise_diffs(b)])


def similarity(a, b):
    return sum(
        [
            1
            for v in Counter(
                [tuple(d) for _, _, d in pairwise_diffs(a) + pairwise_diffs(b)]
            ).values()
            if v > 1
        ]
    )


def rotate_to_match(a, b):
    return max((bb for bb in transforms(b)), key=lambda x: (similarity(a, x)))


def solve_one():
    data = parse(readlines())
    for k, v in data.items():
        data[k] = max(
            [bb for bb in transforms(v)],
            key=lambda x: max(
                (similarity(x, xx) for k2, xx in data.items() if k != k2)
            ),
        )

    s = DisjointSet([(k, p) for k, v in data.items() for p in v])
    pprint(len(s.find_roots()))
    for k, v in data.items():
        for k2, v2 in data.items():
            if k == k2:
                continue
            pw = pairwise_diffs(v)
            pw2 = pairwise_diffs(v2)
            for x, y, d in pw:
                for x2, y2, d2 in pw2:
                    if d == d2:
                        s.union((k, x), (k2, x2))
                        s.union((k, y), (k2, y2))

    pprint(len(s.find_roots()))
    # pprint(list(similarity(data[k], xx) for k2, xx in data.items() if k != k2))


def solve_two():
    pass


if __name__ == "__main__":
    print(solve_one())
    pprint(solve_two())
