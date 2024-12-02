def readlines():
    with open("./input/day7.txt") as f:
        for line in f.readlines():
            yield line.strip()


def parse():
    l = next(readlines())
    return map(int, l.split(","))


def fuel_to_align(n, crabs):
    return sum(map(lambda x: abs(n - x), crabs))


def solve_one():
    crabs = list(parse())
    low = min(crabs)
    hi = max(crabs)

    return min(fuel_to_align(n, crabs) for n in range(low, hi + 1))


def revised_fuel_to_align(n, crabs):
    tri = lambda n: n * (n + 1) // 2
    return sum(map(lambda x: tri(abs(n - x)), crabs))


def solve_two():
    crabs = list(parse())
    low = min(crabs)
    hi = max(crabs)

    return min(revised_fuel_to_align(n, crabs) for n in range(low, hi + 1))


if __name__ == "__main__":
    print(solve_one())
    print(solve_two())
