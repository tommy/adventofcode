from collections import Counter


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


def simulate(n):
    fish = Counter(parse())
    print("Initial: ", fish)
    for _ in range(n):
        fish = sum(step(fish), Counter({}))
    print("After: ", fish)
    return sum([c for _, c in fish.items()])


def solve_one():
    return simulate(80)


def solve_two():
    return simulate(265)


if __name__ == "__main__":
    print(solve_one())
    print(solve_two())
