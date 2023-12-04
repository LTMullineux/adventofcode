from collections import defaultdict
from functools import reduce
from math import inf

Game = list[dict[int, str]]


def format_bag_of_cubes(raw_lines: list[str]) -> Game:
    games = []
    for line in raw_lines:
        game = []
        _, cubes_str = line.split(": ")
        for subset_str in cubes_str.split("; "):
            subset = {}
            for cube_str in subset_str.split(", "):
                count, colour = cube_str.split(" ")
                subset[colour] = int(count)

            game.append(subset)

        games.append(game)

    return games


def is_game_possible(game: Game, constraints: dict[str, int]) -> bool:
    for subset in game:
        for colour, count in subset.items():
            if constraints[colour] < count:
                return False

    return True


def get_fewest_cubes(game: Game) -> dict[str, int]:
    fewest = defaultdict(lambda: -inf)
    for subset in game:
        for colour, count in subset.items():
            fewest[colour] = max(fewest[colour], count)

    return fewest


def main(filename: str) -> None:
    with open(filename, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    games = format_bag_of_cubes(lines)
    game_id_sum = 0
    power_sum = 0
    for i, game in enumerate(games, 1):
        is_possible = is_game_possible(game, {"red": 12, "green": 13, "blue": 14})
        fewest = get_fewest_cubes(game)
        power = reduce(lambda a, b: a * b, fewest.values())
        power_sum += power
        if is_possible:
            game_id_sum += i

    print(game_id_sum, power_sum)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-e", "--example", action="store_true")
    args = parser.parse_args()

    filename = "example-input.txt" if args.example else "input.txt"
    main(filename)
