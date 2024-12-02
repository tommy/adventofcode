from pprint import pprint
from collections import Counter, defaultdict


def readlines():
    with open("./input/day8.txt") as f:
        for line in f.readlines():
            yield line.strip()


def parse(lines):
    for l in lines:
        (control, questions) = l.strip().split("|")

        yield {
            "control": [c.strip() for c in control.strip().split(" ")],
            "questions": [q.strip() for q in questions.strip().split(" ")],
        }


def solve_one():
    return len(
        [
            q
            for l in parse(readlines())
            for q in l["questions"]
            if len(q) in [2, 4, 3, 7]
        ]
    )


# 1:   c  f  (2)

# 7: a c  f  (3)

# 4:  bcd f  (4)

# 2: a cde g (5)
# 3: a cd fg
# 5: ab d fg

# 1b, 2c, 3d, 1e, 2f

# 0: abc efg (6)
# 6: ab defg
# 9: abcd fg

# 3b, 2c, 2d, 2e, 3f

# 8: abcdefg (7)


def analyze(control):
    fives = Counter([c for n in control for c in n if len(n) == 5])
    sixes = Counter([c for n in control for c in n if len(n) == 6])

    mapped = defaultdict(lambda: "")
    for c in "abcdefg":
        (f, s) = (fives[c], sixes[c])
        if (f, s) == (1, 3):
            mapped[c] = "b"
        elif (f, s) == (2, 2):
            mapped[c] = "c"
        elif (f, s) == (3, 2):
            mapped[c] = "d"
        elif (f, s) == (1, 2):
            mapped[c] = "e"
        elif (f, s) == (2, 3):
            mapped[c] = "f"

    return mapped


def identify(i, mapping):
    if len(i) == 2:
        return "1"
    if len(i) == 3:
        return "7"
    if len(i) == 4:
        return "4"
    if len(i) == 7:
        return "8"

    rel = set("bcdef") & set("".join([mapping[c] for c in i]))
    if rel == set("cde"):
        return "2"
    if rel == set("cdf"):
        return "3"
    if rel == set("bdf"):
        return "5"
    if rel == set("bcef"):
        return "0"
    if rel == set("bdef"):
        return "6"
    if rel == set("bcdf"):
        return "9"


def solve_two():
    s = 0
    for l in parse(readlines()):
        mapping = analyze(l["control"])
        v = int("".join([identify(i, mapping) for i in l["questions"]]))
        s += v
    return s


if __name__ == "__main__":
    pprint(solve_one())
    pprint(solve_two())
