from pprint import pprint
import re


def readlines():
    with open("./input/day22.txt") as f:
        for line in f.readlines():
            yield line.strip()


def parse(lines):
    for line in lines:
        m = re.match(
            r"(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)", line
        )
        assert m, line
        assert m.group(1) in ["on", "off"]
        yield (m.group(1), tuple([int(x) for x in m.groups()[1:]]))


def within_cube(cube, point):
    (xmin, xmax, ymin, ymax, zmin, zmax) = cube
    (x, y, z) = point

    return xmin <= x <= xmax and ymin <= y <= ymax and zmin <= z <= zmax


def solve_one():
    data = parse(readlines())
    cube = set()
    for (action, (xmin, xmax, ymin, ymax, zmin, zmax)) in data:
        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                for z in range(zmin, zmax + 1):
                    if (
                        xmin < -50
                        or xmax > 50
                        or ymin < -50
                        or ymax > 50
                        or zmin < -50
                        or zmax > 50
                    ):
                        continue
                    if action == "on":
                        cube.add((x, y, z))
                    elif action == "off":
                        cube.discard((x, y, z))
    return len(cube)


def solve_one_2():
    reverse_ops = list(reversed(list(parse(readlines()))))
    count = 0
    for x in range(-50, 50 + 1):
        for y in range(-50, 50 + 1):
            for z in range(-50, 50 + 1):
                on = 0
                for (action, cube) in reverse_ops:
                    if within_cube(cube, (x, y, z)):
                        if action == "on":
                            on = 1
                        else:
                            on = 0
                        break
                count += on
    return count


def intersect_range(min1, max1, min2, max2):
    return ((a, b) for (a, b) in [(max(min1, min2), min(max1, max2))] if a <= b)


assert list(intersect_range(1, 4, 2, 3)) == [(2, 3)]
assert list(intersect_range(1, 10, 10, 15)) == [(10, 10)]
assert list(intersect_range(1, 10, -1, 5)) == [(1, 5)]
assert list(intersect_range(1, 10, 20, 30)) == []


def divide_range(min1, max1, min2, max2):
    return (
        (a, b)
        for (a, b) in [(min1, min2 - 1), (min2, max2), (max2 + 1, max1)]
        if a <= b
    )


assert list(divide_range(1, 4, 2, 3)) == [(1, 1), (2, 3), (4, 4)]
assert list(divide_range(1, 4, 3, 4)) == [(1, 2), (3, 4)]
assert list(divide_range(1, 4, 1, 2)) == [(1, 2), (3, 4)]


def intersect_cube(a, b):
    (xmin, xmax, ymin, ymax, zmin, zmax) = a
    (xmin2, xmax2, ymin2, ymax2, zmin2, zmax2) = b
    return [
        (xm, xx, ym, yx, zm, zx)
        for (xm, xx) in intersect_range(xmin, xmax, xmin2, xmax2)
        for (ym, yx) in intersect_range(ymin, ymax, ymin2, ymax2)
        for (zm, zx) in intersect_range(zmin, zmax, zmin2, zmax2)
    ]


assert list(intersect_cube((0, 10, 0, 10, 0, 10), (5, 6, 5, 6, 5, 6))) == [
    (5, 6, 5, 6, 5, 6)
]
assert list(intersect_cube((0, 10, 0, 10, 0, 10), (11, 12, 11, 12, 11, 12))) == []
assert list(intersect_cube((0, 10, 0, 10, 0, 10), (2, 4, 3, 5, 8, 20))) == [
    (2, 4, 3, 5, 8, 10)
]


def subtract_cube(a, b):
    intersection = intersect_cube(a, b)
    if len(intersection) == 0:
        return [a]
    assert len(intersection) == 1

    (xmin, xmax, ymin, ymax, zmin, zmax) = a
    [(xmin2, xmax2, ymin2, ymax2, zmin2, zmax2)] = intersection
    return (
        (xm, xx, ym, yx, zm, zx)
        for (xm, xx) in divide_range(xmin, xmax, xmin2, xmax2)
        for (ym, yx) in divide_range(ymin, ymax, ymin2, ymax2)
        for (zm, zx) in divide_range(zmin, zmax, zmin2, zmax2)
        if (xm, xx, ym, yx, zm, zx) != (xmin2, xmax2, ymin2, ymax2, zmin2, zmax2)
    )


# pprint(list(divide_range(0, 10, 5, 6)))
# pprint(list(subtract_cube((0, 10, 0, 10, 0, 10), (5, 6, 5, 6, 5, 6))))
# pprint(list(subtract_cube((0, 10, 0, 10, 0, 10), (0, 10, 0, 6, 5, 6))))
# pprint(list(subtract_cube((0, 10, 0, 10, 0, 10), (5, 6, 5, 6, 5, 6))))
# pprint(list(subtract_cube((0, 10, 0, 10, 0, 10), (11, 12, 11, 12, 11, 12))))
# pprint(list(subtract_cube((18, 30, -20, -8, -3, 13), (-41, 9, -7, 43, -33, 15))))
# pprint(list(subtract_range(18, 30, -41, 9)))
# pprint(list(subtract_range(-20, -8, -7, 43)))
# pprint(list(subtract_range(-3, 13, -33, 15)))


def size_cube(cube):
    (xmin, xmax, ymin, ymax, zmin, zmax) = cube
    return (xmax - xmin + 1) * (ymax - ymin + 1) * (zmax - zmin + 1)


def solve_two():
    reverse_ops = list(reversed(list(parse(readlines()))))
    count = 0
    processed = set()
    for (action, cube) in reverse_ops:
        # print(action, cube)
        q = [cube]
        for processed_cube in processed:
            qq = []
            for cube2 in q:
                sub = subtract_cube(cube2, processed_cube)
                qq.extend(sub)
            q = qq
        if action == "on":
            for c in q:
                count += size_cube(c)
        processed.add(cube)
    return count


if __name__ == "__main__":
    # # pprint(solve_one())
    pprint(solve_one_2())
    pprint(solve_two())
    pass
