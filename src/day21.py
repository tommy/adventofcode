from pprint import pprint
from itertools import islice
from collections import Counter, defaultdict, deque
import re


def readlines():
    with open("./input/day21.txt") as f:
        for line in f.readlines():
            yield line.strip()


def parse(lines):
    players = {}
    for line in lines:
        m = re.match(r"^Player (\d+) starting position: (\d+)$", line)
        assert m
        [n, pos] = m.groups()
        players[int(n)] = int(pos)
        yield int(pos)


def deterministic_die():
    n = 0
    while True:
        yield n + 1
        n += 1
        n %= 100


def advance(pos, n):
    return (pos + n - 1) % 10 + 1


assert advance(1, 1) == 2
assert advance(9, 1) == 10
assert advance(10, 1) == 1


def solve_one():
    positions = list(parse(readlines()))
    players = [(0, pos) for pos in positions]
    turn = 0
    die = deterministic_die()
    while all(points < 1000 for (points, _) in players):
        i = turn % len(players)
        (points, pos) = players[i]
        new_pos = advance(pos, sum(islice(die, 3)))
        players[i] = (points + new_pos, new_pos)
        turn += 1
    return min(points for (points, _) in players) * turn * 3


# { (total roll) : (number of universes with this total) }
quantum_die = Counter(
    [sum([x, y, z]) for x in [1, 2, 3] for y in [1, 2, 3] for z in [1, 2, 3]]
)


def solve_two():
    positions = list(parse(readlines()))
    wins = [0] * len(positions)
    players = [(0, pos) for pos in positions]

    # ( number of universese in this state, turn, [ (points, position) ] )
    q = deque([(1, 0, players)])

    while q:
        (n, turn, players) = q.pop()

        i = turn % len(players)
        (points, pos) = players[i]

        for roll, universes in quantum_die.items():
            new_pos = advance(pos, roll)
            if points + new_pos >= 21:
                wins[i] += n * universes
            else:
                new_players = players[:]
                new_players[i] = (points + new_pos, new_pos)
                q.append((n * universes, turn + 1, new_players))

    print(wins)

    return max(wins)


if __name__ == "__main__":
    pprint(solve_one())
    pprint(solve_two())
