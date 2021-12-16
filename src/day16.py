from pprint import pprint
from itertools import islice, chain


def readlines():
    with open("./input/day16.txt") as f:
        for line in f.readlines():
            yield line.strip()


def parse(hex_string):
    for c in hex_string:
        for dig in bin(int(c, 16))[2:].zfill(4):
            yield dig


def peek(iterable):
    try:
        first = next(iterable)
    except StopIteration:
        return None
    return first, chain([first], iterable)


def parse_bin(digits, n):
    s = "".join(islice(digits, n))
    if len(s) != n:
        raise StopIteration(f"Expected {n} digits: {s}")
    return int(s, 2)


def parse_version(digits):
    return parse_bin(digits, 3)


def parse_type(digits):
    return parse_bin(digits, 3)


def parse_literal(digits):
    more = True
    v = 0
    while more:
        more = next(digits) == "1"
        for d in islice(digits, 4):
            v *= 2
            v += int(d)
    return v


def parse_length_type(digits):
    return "TOTAL_LENGTH" if next(digits) == "0" else "NUM_PACKETS"


def parse_length(digits, length_type):
    if length_type == "TOTAL_LENGTH":
        return parse_bin(digits, 15)
    if length_type == "NUM_PACKETS":
        return parse_bin(digits, 11)
    raise f"unexpected length_type {length_type}"


def parse_operator(digits):
    length_type = parse_length_type(digits)
    length = parse_length(digits, length_type)

    packets = []
    if length_type == "TOTAL_LENGTH":
        ds = islice(digits, length)
        try:
            while True:
                packets.append(parse_packet(ds))
        except StopIteration as e:
            pass

    if length_type == "NUM_PACKETS":
        for _ in range(length):
            packets.append(parse_packet(digits))

    return {"length_type": length_type, "length": length, "packets": packets}


def parse_packet(digits):
    packet = {"version": parse_version(digits), "type": parse_type(digits)}
    if packet["type"] == 4:
        packet["literal"] = parse_literal(digits)
    else:
        packet["operator"] = parse_operator(digits)

    return packet


def traverse(packet):
    yield packet
    if packet["type"] != 4:
        for p in packet["operator"]["packets"]:
            yield from traverse(p)


def solve_one():
    # digits = parse("D2FE28")
    # digits = parse("A0016C880162017C3686B18A3D4780")
    # digits = parse("8A004A801A8002F478")
    digits = parse(next(readlines()))
    root = parse_packet(digits)
    # pprint(root)
    return sum([p["version"] for p in (traverse(root))])


def eval_sum(packet):
    return sum(eval(p) for p in packet["operator"]["packets"])


def eval_product(packet):
    ans = 1
    for p in packet["operator"]["packets"]:
        ans *= eval(p)
    return ans


def eval_min(packet):
    return min(eval(p) for p in packet["operator"]["packets"])


def eval_max(packet):
    return max(eval(p) for p in packet["operator"]["packets"])


def eval_literal(packet):
    return packet["literal"]


def eval_greater_than(packet):
    a, b = packet["operator"]["packets"]
    return 1 if eval(a) > eval(b) else 0


def eval_less_than(packet):
    a, b = packet["operator"]["packets"]
    return 1 if eval(a) < eval(b) else 0


def eval_equal_to(packet):
    a, b = packet["operator"]["packets"]
    return 1 if eval(a) == eval(b) else 0


types = {
    0: eval_sum,
    1: eval_product,
    2: eval_min,
    3: eval_max,
    4: eval_literal,
    5: eval_greater_than,
    6: eval_less_than,
    7: eval_equal_to,
}


def eval(packet):
    # pprint(packet)
    f = types[packet["type"]]
    return f(packet)


def solve_two():
    # digits = parse("D2FE28")
    # digits = parse("A0016C880162017C3686B18A3D4780")
    # digits = parse("D8005AC2A8F0")
    digits = parse(next(readlines()))
    root = parse_packet(digits)
    # pprint(root)
    return eval(root)


if __name__ == "__main__":
    pprint(solve_one())
    pprint(solve_two())
