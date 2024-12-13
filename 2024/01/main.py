import re
from collections import Counter
from pathlib import Path


def main(filename: Path) -> None:
    left: list[int] = []
    right: list[int] = []
    with open(filename, "r") as f:
        for line in f.readlines():
            i, j = re.split(r"\s+", line.strip())
            left.append(int(i))
            right.append(int(j))

    left = sorted(left)
    right = sorted(right)

    dist = sum([abs(i - j) for i, j in zip(left, right)])
    print("part 1:", dist)

    right_counts = Counter(right)
    sim = sum([i * right_counts.get(i, 0) for i, j in zip(left, right)])
    print("part 2:", sim)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-e", "--example", action="store_true")
    args = parser.parse_args()

    filename = Path("example-input.txt") if args.example else Path("input.txt")
    main(filename)
