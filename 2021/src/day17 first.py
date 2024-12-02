from enum import Enum
from pprint import pprint
import re


def readlines():
    with open("./input/day17.txt") as f:
        for line in f.readlines():
            yield line.strip()


def parse(lines):
    line = next(lines)
    p = re.compile(
        "target area: x=(?P<xmin>-?\d+)..(?P<xmax>-?\d+), y=(?P<ymin>-?\d+)..(?P<ymax>-?\d+)"
    )
    m = p.match(line)
    return {k: int(v) for k, v in m.groupdict().items()}


def sign(x):
    return 1 if x > 0 else -1 if x < 0 else 0


class Probe:
    def __init__(self, vel, target):
        self.pos = (0, 0)
        self.vel = vel
        self.target = target
        self.path = [self.pos]
        self.x_ans = None
        self.y_ans = None
        self.hits = None

    def step(self):
        self.pos = (self.pos[0] + self.vel[0], self.pos[1] + self.vel[1])
        self.vel = (self.vel[0] - sign(self.vel[0]), self.vel[1] - 1)
        self.path.append(self.pos)
        return self.pos

    def within(self):
        return (
            self.pos[0] >= self.target["xmin"]
            and self.pos[0] <= self.target["xmax"]
            and self.pos[1] >= self.target["ymin"]
            and self.pos[1] <= self.target["ymax"]
        )

    def analyze(self):
        if self.within():
            self.hits = True
            self.x_ans = "hits"
            self.y_ans = "hits"

        if self.pos[0] >= self.target["xmin"] and self.pos[0] <= self.target["xmax"]:
            self.x_ans = "hits"
        if self.pos[1] >= self.target["ymin"] and self.pos[1] <= self.target["ymax"]:
            self.y_ans = "hits"

        (x, y) = self.pos
        (dx, dy) = self.vel

        if y < self.target["ymin"] and dy <= 0 and self.y_ans is None:
            self.y_ans = "misses up"
        if x < self.target["xmin"] and dx <= 0 and self.x_ans is None:
            self.x_ans = "misses left"
        if x > self.target["xmax"] and dx >= 0 and self.x_ans is None:
            self.x_ans = "misses right"

        if self.x_ans is None or self.y_ans is None:
            return None
        else:
            return (self.x_ans, self.y_ans)

    def simulate(self):
        while self.analyze() is None:
            self.step()
        return self.analyze()

    def best(self):
        return max(y for x, y in self.path)

    def print_grid(self):
        # start
        grid = {(0, 0): "S"}

        # target
        for x in range(self.target["xmin"], self.target["xmax"] + 1):
            for y in range(self.target["ymin"], self.target["ymax"] + 1):
                grid[(x, y)] = "T"

        # path
        for x, y in self.path:
            grid[(x, y)] = "#"

        # print
        lox = min(x for x, y in grid)
        w = max(x for x, y in grid)
        loy = min(y for x, y in grid)
        h = max(y for x, y in grid)
        for y in range(h, loy - 1, -1):
            for x in range(lox, w + 1):
                if (x, y) in grid:
                    print(grid[(x, y)], end="")
                else:
                    print(".", end="")
            print()


def solve_one():
    target = parse(readlines())

    hits = {}
    vel = (0, 1)
    y_ans = None

    while vel[1] <= 100:
        probe = Probe(vel, target)
        (x_ans, y_ans) = probe.simulate()
        if y_ans != "misses up":
            print(x_ans, y_ans, vel)
            hits[vel] = probe
        vel = (vel[0], vel[1] + 1)

    for (_, y_vel) in sorted(hits, key=lambda p: p[1], reverse=True):
        x_vel = 1
        x_ans = None
        print("vel", (x_vel, y_vel))
        while x_ans != "misses right":
            probe = Probe((x_vel, y_vel), target)
            (x_ans, y_ans) = probe.simulate()
            if probe.hits:
                return probe.best()
            x_vel += 1

    best = max(hits.values(), key=lambda p: p.best())
    print([y for x, y in best.path])
    print(best.target)
    # best.print_grid()
    return best.best()


def solve_two():
    pass


if __name__ == "__main__":
    pprint(solve_one())
    pprint(solve_two())
