from collections import defaultdict
from uuid import uuid4

DIGITS = set(map(str, range(10)))
Grid = defaultdict[int, defaultdict[int, int]]


def create_grid_reference(
    raw_grid: list[str],
) -> tuple[Grid, list[tuple[int, int]], int, int]:
    # return grid reference to numbers, list of symbol positions, max_x, max_y
    max_y = len(raw_grid)
    max_x = len(raw_grid[0])

    grid = defaultdict(lambda: defaultdict(tuple))
    symbols = []
    for y, row in enumerate(raw_grid):
        number_str = []
        number_indexes = []
        for x, char in enumerate(row + "x"):
            if char in DIGITS:
                number_str.append(char)
                number_indexes.append(x)
                continue

            else:
                if number_str:
                    number = int("".join(number_str))
                    number_hash = uuid4().hex[:16]
                    for index in number_indexes:
                        grid[y][index] = (number, number_hash)

                    number_str = []
                    number_indexes = []

                if char != "." and char != "x":
                    symbols.append((y, x, char))

    return grid, symbols, max_x, max_y


def get_neighbors(x: int, y: int, max_x: int, max_y: int) -> tuple[int, int]:
    for d_x in (-1, 0, 1):
        for d_y in (-1, 0, 1):
            if d_x == 0 and d_y == 0:
                continue

            n_x, n_y = x + d_x, y + d_y
            if 0 <= n_x < max_x and 0 <= n_y < max_y:
                yield n_x, n_y


def main(filename: str) -> None:
    with open(filename, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    grid, symbols, max_x, max_y = create_grid_reference(lines)

    engine_sum = 0
    seen_numbers = set()
    gears = []
    for y, x, symbol in symbols:
        neighbor_count = []
        for n_x, n_y in get_neighbors(x, y, max_x, max_y):
            neighbor = grid[n_y][n_x]
            if not neighbor:
                continue

            number, number_hash = neighbor
            if number_hash not in seen_numbers:
                engine_sum += number
                seen_numbers.add(number_hash)
                neighbor_count += [number]

        if symbol == "*" and len(neighbor_count) == 2:
            gears.append(neighbor_count)

    gear_ratio = sum([i * j for i, j in gears])
    print(engine_sum)
    print(gear_ratio)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-e", "--example", action="store_true")
    args = parser.parse_args()

    filename = "example-input.txt" if args.example else "input.txt"
    main(filename)
