from pprint import pprint
from collections import defaultdict


def readlines():
    with open("./input/day12.txt") as f:
        for line in f.readlines():
            yield line.strip()


def parse(lines):
    adj = defaultdict(list)
    for line in lines:
        s, e = line.split("-")
        if s != "end" and e != "start":
            adj[s].append(e)
        if e != "end" and s != "start":
            adj[e].append(s)
    return adj


def paths(adj, path):
    s = path[-1]
    if s == "end":
        yield path
    else:
        for e in adj[s]:
            if e.islower() and e in path:
                continue
            yield from paths(adj, path + [e])


def solve_one():
    adj = parse(readlines())
    return len(list(paths(adj, ["start"])))


def paths_two(adj, path, used_twice):
    s = path[-1]
    if s == "end":
        yield path
    else:
        for e in adj[s]:
            if e.islower() and e in path:
                if used_twice:
                    continue
                else:
                    yield from paths_two(adj, path + [e], True)
            else:
                yield from paths_two(adj, path + [e], used_twice)


def solve_two():
    adj = parse(readlines())
    return len(list(paths_two(adj, ["start"], False)))


if __name__ == "__main__":
    pprint(solve_one())
    pprint(solve_two())
