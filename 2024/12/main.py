import itertools as it
from collections import deque
from pathlib import Path

Map = list[list[int]]
Coord = tuple[int, int]
Region = set[Coord]
Fence = tuple[int, int, int, int]
RegionInfo = tuple[str, int, int, Region, Fence]
DELTAS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def is_within_grid(i: int, j: int, max_x: int, max_y: int) -> bool:
    return 0 <= i < max_x and 0 <= j < max_y


def find_regions(m: Map) -> list[RegionInfo]:
    max_x, max_y = len(m[0]), len(m)
    regions: list[RegionInfo] = []
    visited: set[Coord] = set()

    for j in range(max_y):
        for i in range(max_x):
            if (i, j) in visited:
                continue

            visited.add((i, j))

            # bfs region
            region = set([(i, j)])
            queue = deque([(i, j)])
            area = 0
            perimeter = 0
            fences: set[Fence] = set()
            char = m[j][i]

            while queue:
                x, y = queue.popleft()
                area += 1
                for dx, dy in DELTAS:
                    nx = x + dx
                    ny = y + dy

                    if is_within_grid(nx, ny, max_x, max_y) and m[ny][nx] == char:
                        if (nx, ny) not in visited:
                            region.add((nx, ny))
                            visited.add((nx, ny))
                            queue.append((nx, ny))
                    else:
                        perimeter += 1
                        fences.add((x, y, dx, dy))

            if region:
                regions.append((char, area, perimeter, region, fences))

    return regions


def count_fences(fences: set[Fence]) -> int:
    c = 0
    while fences:
        x, y, dx, dy = fences.pop()
        c += 1
        for d in (1, -1):
            for i in it.count(d, d):
                # handle moving parallel to existing fence either way
                fence = (x + i * dy, y + i * dx, dx, dy)
                if fence in fences:
                    fences.remove(fence)
                else:
                    break
    return c


def main(filename: Path) -> None:
    with open(filename, "r") as f:
        m: Map = [tuple(line.strip()) for line in f.readlines()]

    regions = find_regions(m)
    price = sum(r[1] * r[2] for r in regions)
    print("part 1", price)

    price = sum(r[1] * count_fences(r[4]) for r in regions)
    print("part 2", price)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-e", "--example", action="store_true")
    args = parser.parse_args()

    filename = Path("example-input.txt") if args.example else Path("input.txt")
    main(filename)
