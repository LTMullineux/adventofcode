from collections import deque
from pathlib import Path

Map = list[list[int]]
Coord = tuple[int, int]
Trail = tuple[Coord, ...]
DELTAS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def is_within_grid(i: int, j: int, max_x: int, max_y: int) -> bool:
    return 0 <= i < max_x and 0 <= j < max_y


def bfs(m: Map, pos: Coord) -> list[Coord]:
    max_x, max_y = len(m[0]), len(m)
    queue = deque([(pos, [pos])])
    trails = []

    while queue:
        (x, y), path = queue.popleft()
        if m[y][x] == 9:
            trails.append(path)
            continue

        for dx, dy in DELTAS:
            nx = x + dx
            ny = y + dy

            # check within bounds and not already in the path (dont want loops)
            if not is_within_grid(nx, ny, max_x, max_y):
                continue

            current_value = m[y][x]
            next_value = m[ny][nx]
            if next_value - current_value != 1:
                continue

            if (nx, ny) not in path:
                queue.append(((nx, ny), path + [(nx, ny)]))

    return trails


def get_longest_trails(trails: list[Trail]) -> list[Trail]:
    # get longest trail per (start, end) pairs
    longest_trails = {}

    for trail in trails:
        start, end = trail[0], trail[-1]
        current_length = len(trail)
        if (start, end) not in longest_trails or current_length > len(
            longest_trails[(start, end)]
        ):
            longest_trails[(start, end)] = trail

    return list(longest_trails.values())


def main(filename: Path) -> None:
    with open(filename, "r") as f:
        m: Map = [tuple(map(int, tuple(line.strip()))) for line in f.readlines()]

    starts: list[Coord] = [
        (x, y) for y in range(len(m)) for x in range(len(m[0])) if m[y][x] == 0
    ]

    trails = []
    for start in starts:
        trails.extend(bfs(m, start))

    longest_trails = get_longest_trails(trails)
    print("part 1", len(longest_trails))

    distinct_trails = set(tuple(trail) for trail in trails)
    print("part 2", len(distinct_trails))


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-e", "--example", action="store_true")
    args = parser.parse_args()

    filename = Path("example-input.txt") if args.example else Path("input.txt")
    main(filename)
