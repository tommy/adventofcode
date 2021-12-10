from collections import deque
from pprint import pprint


def readlines():
    with open("./input/day10.txt") as f:
        for line in f.readlines():
            yield line.strip()


m = {"{": "}", "(": ")", "[": "]", "<": ">"}
inv = {v: k for k, v in m.items()}


def solve_one():
    s = {"}": 1197, ")": 3, "]": 57, ">": 25137}
    score = 0
    for line in readlines():
        q = deque()
        for c in line:
            if c in set("({[<"):
                q.append(c)
            elif not q or q.pop() != inv[c]:
                score += s[c]
    return score


def solve_two():
    s = {"{": 3, "(": 1, "[": 2, "<": 4}
    scores = []
    for line in readlines():
        q = deque()
        for c in line:
            if c in set("({[<"):
                q.append(c)
            elif q and q[-1] == inv[c]:
                q.pop()
            else:
                break
        else:
            score = 0
            while q:
                score *= 5
                score += s[q.pop()]
            scores.append(score)
    return sorted(scores)[len(scores) // 2]


if __name__ == "__main__":
    pprint(solve_one())
    pprint(solve_two())
