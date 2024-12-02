from pprint import pprint
import itertools
import functools
import math
import re
import zipper


def readlines():
    with open("./input/day18.txt") as f:
        for line in f.readlines():
            yield line.strip()


def parse(lines):
    for line in lines:
        if not re.match(r"^[\s\d\[\],]+$", line):
            raise Exception("Invalid line: {}".format(line))
        yield eval(line)


def is_pair(n):
    return type(n) == list and len(n) == 2 and type(n[0]) == int and type(n[1]) == int


assert is_pair([1, 2]), "should be pair"
assert not is_pair([[1, 2], 2]), "should not be pair"
assert not is_pair([1, [2, 2]]), "should not be pair"


def must_split(n):
    if type(n) == zipper.Loc:
        n = n.node()
    return type(n) == int and n >= 10


assert must_split(10), "should be split"
assert not must_split(9), "should not be split"
assert not must_split([10, 1]), "not an int"


def split(n):
    top = zipper.list(n)
    node = top.find(must_split)
    if node:
        x = node.node()
        return node.replace([math.floor(x / 2), math.ceil(x / 2)]).root()
    else:
        return None


assert split([[10, 1], 2]) == [[[5, 5], 1], 2]
assert split([[9, 1], 2]) is None
assert split([[[[0, 7], 4], [15, [0, 13]]], [1, 1]]) == [
    [[[0, 7], 4], [[7, 8], [0, 13]]],
    [1, 1],
]


def depth(n):
    depth = 0
    while n.up():
        n = n.up()
        depth += 1
    return depth


assert depth(zipper.list([10, 1])) == 0
assert depth(zipper.list([[10, 1]]).down()) == 1


def must_explode(n):
    if type(n) != zipper.Loc:
        raise TypeError("must be a Loc")
    return is_pair(n.node()) and depth(n) >= 4


assert must_explode(
    zipper.list([[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]])
    .leftmost_descendant()
    .up()
)


def explode(n):
    top = zipper.list(n)
    node = top.find(must_explode)
    if node:
        # print(node.root())
        # print(node.node())
        l, r = regular_left(node), regular_right(node)
        # print("left", l)
        # print("right", r)
        lx, rx = node.node()
        node = node.replace(0)
        if l:
            node = node.move_to(l).edit(lambda x: x + lx)
        if r:
            node = node.move_to(r).edit(lambda x: x + rx)
        return node.root()
    else:
        return None


def regular_left(n):
    if type(n) != zipper.Loc:
        raise TypeError("must be a Loc")

    while n.left() or n.up():
        if n.left():
            return n.left().rightmost_descendant()
        else:
            n = n.up()
    else:
        return None


def regular_right(n):
    if type(n) != zipper.Loc:
        raise TypeError("must be a Loc")

    while n.right() or n.up():
        if n.right():
            return n.right().leftmost_descendant()
        else:
            n = n.up()
    else:
        return None


four_three = (
    zipper.list([[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]])
    .down()
    .down()
    .down()
    .down()
)

assert regular_left(four_three) is None
assert regular_left(four_three.right()).node() == 3
assert regular_right(four_three).node() == 4

assert explode([[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]) == [
    [[[0, 7], 4], [7, [[8, 4], 9]]],
    [1, 1],
]
assert explode([[[[4, 3], 4], 4], [7, [[8, 4], 9]]]) is None


def split_or_explode(n):
    n_explode = explode(n)
    if n_explode:
        return n_explode
    n_split = split(n)
    if n_split:
        return n_split
    return None


def reduce(n):
    next = split_or_explode(n)
    if next:
        return reduce(next)
    else:
        return n


assert reduce([[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]) == [
    [[[0, 7], 4], [[7, 8], [6, 0]]],
    [8, 1],
]


def add(x, y):
    return [x, y]


def magnitude(n):
    if type(n) == int:
        return n
    else:
        return 3 * magnitude(n[0]) + 2 * magnitude(n[1])


assert magnitude([[9, 1], [1, 9]]) == 129


def solve_one():
    ns = parse(readlines())
    return magnitude(functools.reduce(lambda x, y: reduce(add(x, y)), ns))


def solve_two():
    ns = list(parse(readlines()))
    return max([magnitude(reduce(add(x, y))) for x in ns for y in ns if x != y])


if __name__ == "__main__":
    pprint(solve_one())
    pprint(solve_two())
