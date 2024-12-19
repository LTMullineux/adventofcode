import itertools as it
import operator as op
from pathlib import Path
from typing import Callable

Operator = Callable[[int, int], int]


def concat(a: int, b: int) -> int:
    return int(str(a) + str(b))


def operate(numbers: tuple[int, ...], operators: list[Operator]) -> int:
    assert len(numbers) == len(operators) + 1
    total = numbers[0]
    for num, op_ in zip(numbers[1:], operators):
        total = op_(total, num)

    return total


def operate_all(
    target: int, numbers: tuple[int, ...], operators: list[Operator]
) -> int:
    for operators_ in it.product(operators, repeat=len(numbers) - 1):
        result = operate(numbers, operators_)
        if result == target:
            return target

    return 0


def main(filename: Path) -> None:
    with open(filename, "r") as f:
        raw = [i.strip().split(": ") for i in f.readlines()]
        equations = [(int(i), tuple(map(int, j.split(" ")))) for i, j in raw]

    total = 0
    for target, numbers in equations:
        total += operate_all(target, numbers, (op.add, op.mul))

    print("part 1", total)

    total = 0
    for target, numbers in equations:
        total += operate_all(target, numbers, (op.add, op.mul, concat))

    print("part 2", total)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-e", "--example", action="store_true")
    args = parser.parse_args()

    filename = Path("example-input.txt") if args.example else Path("input.txt")
    main(filename)
