from pprint import pprint
from collections import defaultdict, Counter
from functools import cache


def readlines():
    with open("./input/day14.txt") as f:
        for line in f.readlines():
            yield line.strip()


def pairs(s):
    for i in range(len(s)):
        yield s[i : i + 2]


def step(template, rules):
    ps = (s[0] + rules[s] + s[0] for s in pairs(template))
    return "".join((p[:-1] for p in ps))


def parse(lines):
    template = next(lines)
    next(lines)
    rules = defaultdict(str)
    for line in lines:
        pair, insertion = line.split(" -> ")
        rules[pair] = insertion
    return template, rules


def solve_one():
    template, rules = parse(readlines())
    for _ in range(10):
        template = step(template, rules)
    counts = Counter(template)
    low = min(counts.values())
    high = max(counts.values())
    return high - low


def expand_counts(template, rules, n):
    @cache
    def expand_pair(pair, n):
        if n == 0 or pair not in rules:
            return Counter()
        else:
            return (
                expand_pair(pair[0] + rules[pair], n - 1)
                + Counter({rules[pair]: 1})
                + expand_pair(rules[pair] + pair[1], n - 1)
            )

    def full_expand(template, n):
        counts = Counter()
        prev = next(template)
        for c in template:
            counts += Counter({prev: 1})
            counts += expand_pair(prev + c, n)
            prev = c
        counts += Counter({prev: 1})
        return counts

    return full_expand((c for c in template), n)


def solve_two():
    template, rules = parse(readlines())
    counts = expand_counts(template, rules, 40)
    low = min(counts.values())
    high = max(counts.values())
    return high - low


if __name__ == "__main__":
    pprint(solve_one())
    pprint(solve_two())
