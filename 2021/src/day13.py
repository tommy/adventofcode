from pprint import pprint
import re


def readlines():
    with open("./input/day13.txt") as f:
        for line in f.readlines():
            yield line.strip()


def parse(lines):
    dots = set()
    for line in lines:
        if line == "":
            break
        x, y = line.split(",")
        dots.add((int(x), int(y)))

    p = re.compile("fold along (x|y)=(\d+)")
    folds = []
    for line in lines:
        m = p.match(line)
        if not m:
            raise Exception("Could not parse line: {}".format(line))
        folds.append((m.group(1), int(m.group(2))))

    return (dots, folds)


def fold_x(dots, fold_value):
    for x, y in dots:
        if fold_value > x:
            yield (x, y)
        elif fold_value < x:
            dist = x - fold_value
            yield (x - 2 * dist, y)


def fold_y(dots, fold_value):
    for x, y in dots:
        if fold_value > y:
            yield (x, y)
        elif fold_value < y:
            dist = y - fold_value
            yield (x, y - 2 * dist)


def fold_once(dots, fold):
    fold_axis, fold_line = fold
    if fold_axis == "x":
        return set(fold_x(dots, fold_line))
    elif fold_axis == "y":
        return set(fold_y(dots, fold_line))
    else:
        raise Exception("Unknown axis: {}".format(fold_axis))


def print_dots(dots):
    w = max(x for x, y in dots) + 1
    h = max(y for x, y in dots) + 1
    for y in range(h):
        for x in range(w):
            if (x, y) in dots:
                print("#", end="")
            else:
                print(".", end="")
        print()


def solve_one():
    dots, folds = parse(readlines())
    dots = fold_once(dots, folds[0])
    print(len(dots))


def solve_two():
    dots, folds = parse(readlines())

    for fold in folds:
        dots = fold_once(dots, fold)

    print_dots(dots)


if __name__ == "__main__":
    pprint(solve_one())
    pprint(solve_two())
