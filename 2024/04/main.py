import itertools as it
from pathlib import Path as PPath
from typing import Generator

Grid = list[list[str]]
Coord = tuple[int, int]
Path = tuple[Coord, ...]
Window = tuple[tuple[Coord, ...]]


def pprint(
    grid: Grid, mask_char: str = ".", keep_coords: set[Coord] | None = None
) -> None:
    for y, row in enumerate(grid):
        new_row = []
        for x, char in enumerate(row):
            if keep_coords and (x, y) in keep_coords:
                new_row.append(char)
            else:
                new_row.append(mask_char)

        print(" ".join(new_row))


def is_within_grid(i: int, j: int, max_x: int, max_y: int) -> bool:
    return 0 <= i < max_x and 0 <= j < max_y


def iter_paths(
    max_x: int,
    max_y: int,
    path_len: int,
) -> Generator[Path, None, None]:
    """Generate all the possible paths of length `path_len` in a grid of size
    `max_x` * `max_y`, which can go horizontal, vertical, diagonal, written backwards,
    or even overlapping other words"""
    for x in range(max_x):
        for y in range(max_y):
            for dx, dy in it.product((-1, 0, 1), repeat=2):
                if dx == dy == 0:
                    continue

                path = []
                for i in range(path_len):
                    new_x, new_y = x + i * dx, y + i * dy
                    if is_within_grid(new_x, new_y, max_x, max_y):
                        path.append((new_x, new_y))
                    else:
                        break

                if len(path) == path_len:
                    yield tuple(path)


def is_xmas_path(path: Path, grid: Grid) -> bool:
    word = "".join([grid[y][x] for x, y in path])
    return word == "XMAS"


def iter_windows(
    grid: Grid,
    max_x: int,
    max_y: int,
    window_size: int,
) -> Generator[Window, None, None]:
    """Generate all the possible windows of size `window_size` in a grid of size `max_x`
    * `max_y`
    """
    for y in range(max_y - window_size + 1):
        for x in range(max_x - window_size + 1):
            window = [
                grid[j][i]
                for j in range(y, y + window_size)
                for i in range(x, x + window_size)
            ]

            yield tuple(
                window[i : i + window_size] for i in range(0, len(window), window_size)
            )


def is_xmas_window(window: Window) -> bool:
    if window[1][1] != "A":
        return False

    pos_diag = window[0][0] + window[2][2]
    neg_diag = window[0][2] + window[2][0]
    if pos_diag not in {"SM", "MS"} or neg_diag not in {"SM", "MS"}:
        return False

    return True


def main(filename: PPath) -> None:
    with open(filename, "r") as f:
        grid: list[list[str]] = [list(line.strip()) for line in f.readlines()]

    max_x, max_y = len(grid[0]), len(grid)
    path_len = 4

    counter = 0
    valid_locations: set[Coord] = set()
    for path in iter_paths(max_x, max_y, path_len):
        if is_xmas_path(path, grid):
            counter += 1
            valid_locations.update(path)

    print("part 1:", counter)

    window_size = 3
    counter = 0
    for w in iter_windows(grid, max_x, max_y, window_size):
        if is_xmas_window(w):
            counter += 1

    print("part 2:", counter)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-e", "--example", action="store_true")
    args = parser.parse_args()

    filename = PPath("example-input.txt") if args.example else PPath("input.txt")
    main(filename)
