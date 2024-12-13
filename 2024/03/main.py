import re
from itertools import pairwise
from pathlib import Path


def create_dont_ranges(s: str) -> list[tuple[int, int]]:
    cond_pattern = r"(do\(\))|(don't\(\))"
    positions: list[tuple[bool, int, int]] = [
        (m.group(1) is not None, m.start(), m.end())
        for m in re.finditer(cond_pattern, s)
    ]

    ranges: list[tuple[int, int]] = []
    for left, right in pairwise(positions):
        left_is_do, left_start, _ = left
        _, right_start, _ = right

        if not left_is_do:
            ranges.append((left_start, right_start))

    return ranges


def main(filename: Path) -> None:
    with open(filename, "r") as f:
        memory: str = f.read().strip()

    mul_pattern = r"mul\(\s*(?P<X>\d+)\s*,\s*(?P<Y>\d+)\s*\)"
    values: list[tuple[int, int]] = [
        (m.start(), m.end(), m.group("X"), m.group("Y"))
        for m in re.finditer(mul_pattern, memory)
    ]
    print("part 1", sum(int(x) * int(y) for _, _, x, y in values))

    dont_ranges = create_dont_ranges(memory)
    filtered_values = [
        (start, end, x, y)
        for start, end, x, y in values
        if not any(
            dont_start < start < dont_end for dont_start, dont_end in dont_ranges
        )
    ]
    print("part 2", sum(int(x) * int(y) for _, _, x, y in filtered_values))


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-e", "--example", action="store_true")
    args = parser.parse_args()

    filename = Path("example-input.txt") if args.example else Path("input.txt")
    main(filename)
