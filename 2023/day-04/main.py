import re
from collections import defaultdict
from math import log

Game = tuple[set[int], set[int]]


def parse_pile(lines: list[str]) -> list[Game]:
    games = []
    for line in lines:
        _, cards_str = line.split(":")
        winners_str, numbers_str = cards_str.split(" | ")
        winners = set([int(card) for card in re.split(r"\s+", winners_str.strip())])
        numbers = set([int(card) for card in re.split(r"\s+", numbers_str.strip())])
        games.append((winners, numbers))

    return games


def get_game_points(game: Game) -> int:
    overlap = set.intersection(*game)
    overlap_size = len(overlap)
    if overlap_size <= 1:
        return overlap_size
    else:
        return 2 ** (overlap_size - 1)


def get_copied_counts(points: list[int]) -> dict[int, int]:
    copy_counts = defaultdict(lambda: 0)
    for i, game_point in enumerate(points, 1):
        print("-" * 80)
        print(f"Game {i} has {game_point} winners, with {copy_counts[i]} copies")

        if game_point >= 1:
            original_overlap = int(1 + log(game_point, 2))
            start_index = i + 1
            end_index = i + original_overlap

            print("original_overlap", original_overlap)
            for j in range(next_index, next_index + original_overlap):
                print(f"Game {j} is a copy of game {i}")
                copy_counts[j] += 1

    return copy_counts


def main(filename: str) -> None:
    with open(filename, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    games = parse_pile(lines)
    points = [get_game_points(game) for game in games]
    print(f"Total points: {sum(points)}")

    print(points)
    # copy_counts = get_copied_counts(points)
    # for k, v in copy_counts.items():
    #     print(f"Game {k}: {v}")


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-e", "--example", action="store_true")
    args = parser.parse_args()

    filename = "example-input.txt" if args.example else "input.txt"
    main(filename)
