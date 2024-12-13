from itertools import compress, pairwise
from math import copysign
from pathlib import Path
from typing import Generator


def is_valid_report(report: tuple[int]) -> bool:
    scores = [j - i for i, j in pairwise(report)]
    size = len(scores)
    direction = copysign(1, scores[0])
    sign_count = sum([copysign(1, i) == direction for i in scores])
    range_count = sum([abs(i) == 0 or abs(i) > 3 for i in scores])
    return sign_count == size and range_count == 0


def iter_masked_reports(report: tuple[int]) -> Generator[tuple[int], None, None]:
    size = len(report)
    for i in range(size):
        mask = [1] * size
        mask[i] = 0
        yield tuple(compress(report, mask))


def main(filename: Path) -> None:
    with open(filename, "r") as f:
        reports: list[tuple[int]] = [
            tuple(map(int, line.strip().split())) for line in f.readlines()
        ]

    valid = 0
    valid_dampener = 0
    for report in reports:
        is_safe = is_valid_report(report)
        if is_safe:
            valid += 1

        for masked_report in iter_masked_reports(report):
            is_safe = is_valid_report(masked_report)
            if is_safe:
                valid_dampener += 1
                break

    print("part 1:", valid)
    print("part 2:", valid_dampener)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-e", "--example", action="store_true")
    args = parser.parse_args()

    filename = Path("example-input.txt") if args.example else Path("input.txt")
    main(filename)
