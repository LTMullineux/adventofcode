from collections import Counter
from pathlib import Path


def solve(stones: Counter, n: int) -> int:
    stones_ = stones.copy()
    for _ in range(n):
        new_stones = Counter()
        for i in stones_:
            # rule 1: 0 -> 1
            if i == 0:
                new_stones[1] += stones_[i]
            else:
                stone_str = str(i)
                stone_len = len(stone_str)
                # rule 2: even digits -> 2 stones split down the middle
                if stone_len % 2 == 0:
                    halfway = stone_len // 2
                    left = int(stone_str[:halfway])
                    right = int(stone_str[halfway:])
                    new_stones[left] += stones_[i]
                    new_stones[right] += stones_[i]
                # rule 3: old number * 2024
                else:
                    new_stones[i * 2024] += stones_[i]

        stones_ = new_stones

    return stones_.total()


def main(filename: Path) -> None:
    with open(filename, "r") as f:
        stones = Counter(int(i) for i in f.read().strip().split(" "))

    print("part 1", solve(stones, 25))
    print("part 2", solve(stones, 75))


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-e", "--example", action="store_true")
    args = parser.parse_args()

    filename = Path("example-input.txt") if args.example else Path("input.txt")
    main(filename)
