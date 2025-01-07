import re
from pathlib import Path

pattern = re.compile(
    r"Button A: X\+(?P<a_x>\d+), Y\+(?P<a_y>\d+)\n"
    r"Button B: X\+(?P<b_x>\d+), Y\+(?P<b_y>\d+)\n"
    r"Prize: X=(?P<x>\d+), Y=(?P<y>\d+)"
)


def determinant(a: int, b: int, c: int, d: int) -> int:
    return a * d - b * c


def solve(rule: dict[str, int]) -> tuple[int, int]:
    # NOTE: solve via cramers rule, only if det(A) != 0 for linear system Ax = b
    det_A = determinant(rule["a_x"], rule["b_x"], rule["a_y"], rule["b_y"])
    assert det_A != 0, "Determinant is zero"

    # determinants of A1 (replace col 1 of A with b) and A2 (replace col 2 of A with b)
    det_A1 = determinant(rule["x"], rule["b_x"], rule["y"], rule["b_y"])
    det_A2 = determinant(rule["a_x"], rule["x"], rule["a_y"], rule["y"])

    x1 = det_A1 / det_A
    x2 = det_A2 / det_A
    return x1, x2


def main(filename: Path) -> None:
    with open(filename, "r") as f:
        rules = [m.groupdict() for m in pattern.finditer(f.read())]

    rules = [dict(zip(r.keys(), map(int, r.values()))) for r in rules]

    total = 0
    for r in rules:
        a, b = solve(r)
        if a.is_integer() and b.is_integer():
            total += int(a) * 3 + int(b) * 1

    print("part 1", total)

    total = 0
    for r in rules:
        r["x"] = r["x"] + 10_000_000_000_000
        r["y"] = r["y"] + 10_000_000_000_000
        a, b = solve(r)
        if a.is_integer() and b.is_integer():
            total += int(a) * 3 + int(b) * 1

    print("part 2", total)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-e", "--example", action="store_true")
    args = parser.parse_args()

    filename = Path("example-input.txt") if args.example else Path("input.txt")
    main(filename)
