import re
from pathlib import Path

Coord = tuple[int, int]
Robot = dict[str, int]
pattern = re.compile(r"p=(?P<x>-?\d+),(?P<y>-?\d+)\s*v=(?P<dx>-?\d+),(?P<dy>-?\d+)")


def solve(robots: list[Robot], steps: int, max_x: int, max_y: int) -> list[Coord]:
    positions: list[Coord] = []
    for r in robots:
        x = (r["x"] + r["dx"] * steps) % max_x
        y = (r["y"] + r["dy"] * steps) % max_y
        positions.append((x, y))

    return positions


def part_1(positions: list[Coord], max_x: int, max_y: int) -> int:
    counts = [[0, 0], [0, 0]]
    mid_x = max_x // 2
    mid_y = max_y // 2
    for x, y in positions:
        if x != mid_x and y != mid_y:
            counts[int(y > mid_y)][int(x > mid_x)] += 1

    return counts[0][0] * counts[0][1] * counts[1][0] * counts[1][1]


def part_2(robots: list[Robot], max_steps: int, max_x: int, max_y: int) -> int:
    seconds = 0
    while True:
        seconds += 1
        if seconds > max_steps:
            return -1

        positions = solve(robots, seconds, max_x, max_y)
        if len(positions) == len(set(positions)):
            return seconds


def main(filename: Path) -> None:
    with open(filename, "r") as f:
        robots: list[Robot] = (m.groupdict() for m in pattern.finditer(f.read()))

    robots = [dict(zip(r.keys(), map(int, r.values()))) for r in robots]

    max_x = 101
    max_y = 103
    positions = solve(robots, 100, max_x, max_y)
    print("part 1", part_1(positions, max_x, max_y))
    print("part 2", part_2(robots, 1_000_000, max_x, max_y))


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-e", "--example", action="store_true")
    args = parser.parse_args()

    filename = Path("example-input.txt") if args.example else Path("input.txt")
    main(filename)
