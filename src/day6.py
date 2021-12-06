from collections import Counter
from functools import reduce


def readlines():
    with open("./input/day6.txt") as f:
        for line in f.readlines():
            yield line.strip()


def parse():
    l = next(readlines())
    return map(int, l.split(","))


def step(fishes):
    for timer in fishes:
        c = fishes[timer]
        if timer == 0:
            yield Counter({8: c, 6: c})
        else:
            yield Counter({(timer - 1): c})


def solve_one():
    fish = Counter(parse())
    print("Initial: ", fish)
    for _ in range(80):
        fish = reduce(lambda x, y: x + y, step(fish))
    print("After: ", fish)
    return sum([c for _, c in fish.items()])


def solve_two():
    fish = Counter(parse())
    print("Initial: ", fish)
    for _ in range(256):
        fish = reduce(lambda x, y: x + y, step(fish))
    print("After: ", fish)
    return sum([c for _, c in fish.items()])


if __name__ == "__main__":
    print(solve_one())
    print(solve_two())
