def readlines():
    with open("./input/day4.txt") as f:
        for line in f.readlines():
            yield line.strip()


def parse_draws(lines):
    line = next(lines)
    return map(int, line.split(","))


def parse_board(lines):
    b = []
    for _ in range(5):
        l = next(lines)
        b.append(list(map(int, l.split())))
    return b


def parse(lines):
    draws = parse_draws(lines)
    boards = []

    while True:
        try:
            _ = next(lines)
            b = parse_board(lines)
            boards.append(b)
        except StopIteration:
            break

    return (list(draws), boards)


def index_of(x, board):
    for i in range(5):
        for j in range(5):
            if board[i][j] == x:
                return (i, j)
    return None


def winning_lines():
    lines = []
    for i in range(5):
        row = []
        col = []
        for j in range(5):
            row.append((i, j))
            col.append((j, i))
        lines.append(row)
        lines.append(col)
    return lines


def has_won(marked):
    for l in winning_lines():
        if all(map(lambda x: x in marked, l)):
            return True
    return False


def when_does_it_win(draws, board):
    score = sum([board[i][j] for i in range(5) for j in range(5)])
    marked = []
    for n, x in enumerate(draws):
        for i in range(5):
            for j in range(5):
                if board[i][j] == x:
                    marked.append((i, j))
                    score -= x
                    if has_won(marked):
                        return (n, score * x)

    return marked


def solve_one():
    draws, boards = parse(readlines())
    scores = [when_does_it_win(draws, b) for b in boards]
    return min(scores, key=lambda s: s[0])


def solve_two():
    draws, boards = parse(readlines())
    scores = [when_does_it_win(draws, b) for b in boards]
    return max(scores, key=lambda s: s[0])


def main():
    print(solve_one())
    print(solve_two())


if __name__ == "__main__":
    main()
