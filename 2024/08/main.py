import itertools as it
from collections import defaultdict
from pathlib import Path
from typing import Iterable

Coord = tuple[int, int]


def dist(left: Coord, right: Coord) -> Coord:
    return right[0] - left[0], right[1] - left[1]


def is_in_map(coord: Coord, bound: Coord) -> bool:
    return 0 <= coord[0] <= bound[0] and 0 <= coord[1] <= bound[1]


def find_antinodes(
    ants: dict[str, list[Coord]], bounds: Coord, iterable: Iterable[int]
) -> set[Coord]:
    antinodes: set[Coord] = set()
    for _, freq_ants in ants.items():
        for left, right in it.permutations(freq_ants, 2):
            d_to_right = dist(left, right)
            for i in iterable:
                antinode = (right[0] + i * d_to_right[0], right[1] + i * d_to_right[1])
                if not is_in_map(antinode, bounds):
                    break

                antinodes.add(antinode)

            d_to_left = dist(right, left)
            for i in iterable:
                antinode = (left[0] + i * d_to_left[0], left[1] + i * d_to_left[1])
                if not is_in_map(antinode, bounds):
                    break

                antinodes.add(antinode)

    return antinodes


class Counter(Iterable[int]):
    def __iter__(self) -> int:
        return it.count(1)


def main(filename: Path) -> None:
    ants = defaultdict(list)
    max_x, max_y = 0, 0
    with open(filename, "r") as f:
        for y, line in enumerate(f.readlines()):
            for x, char in enumerate(line.strip()):
                max_x = max(max_x, x)
                max_y = max(max_y, y)
                if char == ".":
                    continue

                ants[char].append((x, y))

    bounds = (max_x, max_y)
    part_1 = find_antinodes(ants, bounds, (1,))
    print("part 1", len(part_1))

    part_2 = find_antinodes(ants, bounds, Counter())
    for ant_positions in ants.values():
        part_2.update(ant_positions)

    print("part 2", len(part_2))


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-e", "--example", action="store_true")
    args = parser.parse_args()

    filename = Path("example-input.txt") if args.example else Path("input.txt")
    main(filename)
