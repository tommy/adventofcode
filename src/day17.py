from enum import Enum
from pprint import pprint
import re
from typing import OrderedDict


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


def check_y(dy, target):
    y = 0
    step = 0
    max_y = y
    while y >= target["ymin"]:
        if y > max_y:
            max_y = y
        if y <= target["ymax"]:
            yield (step, max_y)
        step += 1
        y += dy
        dy -= 1


def check_x(dx, target, max_step):
    x = 0
    step = 0
    while (
        (x <= target["xmax"] and dx > 0)
        or (x >= target["xmin"] and dx < 0)
        or (x >= target["xmin"] and x <= target["xmax"] and dx == 0)
    ):
        if x >= target["xmin"] and x <= target["xmax"]:
            yield step
        step += 1
        x += dx
        dx -= sign(dx)
        if step > max_step:
            break


def solve_one():
    target = parse(readlines())
    for dy in range(1, 200):
        ans = list(check_y(dy, target))
        if ans:
            print(dy, ans)


def solve_two():
    target = parse(readlines())
    possible_ys = {}
    max_y_step = 0
    for dy in range(-400, 400):
        ss = {step for step, _ in (check_y(dy, target))}
        if ss:
            max_y_step = max(max_y_step, max(ss))
            possible_ys[dy] = ss
    print(possible_ys)

    possible_xs = {}
    for dx in range(1, 400):
        ss = {step for step in (check_x(dx, target, max_y_step))}
        if ss:
            possible_xs[dx] = ss
    print(possible_xs)

    pprint(
        len(
            [
                (dx, dy)
                for dx, sx in possible_xs.items()
                for dy, sy in possible_ys.items()
                if sx.intersection(sy)
            ]
        )
    )


if __name__ == "__main__":
    pprint(solve_one())
    pprint(solve_two())
