def main():
    # print(solve_one())
    print(solve_two())


def readlines():
    with open("./input/day3.txt") as f:
        for line in f.readlines():
            yield line.strip()


def parse(line):
    return int(line, 2)


def bits(i):
    bits = []
    while i:
        bits.insert(0, i & 1)
        i >>= 1
    return bits


def transpose(xxs):
    xxs = list(xxs)
    print(list(map(len, xxs)))
    for i in range(0, len(xxs[0])):
        yield list(map(lambda xs: xs[i], xxs))


def frequencies(num_digits, measurements):
    num_measurements = 0
    ones = [0] * num_digits
    for n in measurements:
        num_measurements += 1
        for i in range(num_digits - 1, 0 - 1, -1):
            ones[num_digits - 1 - i] += 1 if n & (1 << i) else 0

    gamma = 0
    epsilon = 0
    for i in range(num_digits):
        gamma <<= 1
        epsilon <<= 1
        if ones[i] * 2 >= num_measurements:
            gamma += 1
        else:
            epsilon += 1

    # print(gamma, epsilon)
    return (gamma, epsilon)


def solve_one():
    lines = list(readlines())
    num_digits = len(lines[0])
    measurements = map(parse, lines)
    gamma, epsilon = frequencies(num_digits, measurements)
    return gamma * epsilon


def most_common_bit(i, xs):
    num_measurements = 0
    ones = 0
    for x in xs:
        num_measurements += 1
        ones += 1 if x & (1 << i) else 0
    return 1 if ones * 2 >= num_measurements else 0


def filter_by_digit(digit, i, xs):
    return filter(lambda x: x & (1 << i) == digit << i, xs)


def find_rating(select_common, num_digits, i, xs):
    xs = list(xs)
    print(select_common, num_digits, i, list(map(bin, xs)))

    if len(xs) == 0:
        return None
    if len(xs) == 1:
        return xs[0]
    else:
        common = most_common_bit(i, xs)
        print("Common:", common)
        return find_rating(
            select_common,
            num_digits,
            i - 1,
            filter_by_digit(common if select_common else 1 - common, i, xs),
        )


# def find_rating(select_common, num_digits, i, xs):
#     print(select_common, num_digits, i, list(map(bin, xs)))
#     f = frequencies(num_digits, xs)
#     print(list(map(bin, f)))
#     bit_criteria = f[0] if select_common else f[1]

#     if len(xs) == 0:
#         return None
#     if len(xs) == 1:
#         return xs[0]
#     return find_rating(
#         select_common,
#         num_digits,
#         i + 1,
#         filter_by_digit(bit_criteria & (1 << i), i, xs),
#     )


def solve_two():
    lines = list(readlines())
    num_digits = len(lines[0])
    measurements = list(map(parse, lines))
    oxy = find_rating(True, num_digits, num_digits - 1, measurements)
    co2 = find_rating(False, num_digits, num_digits - 1, measurements)
    print(oxy, co2)
    return oxy * co2


if __name__ == "__main__":
    main()
