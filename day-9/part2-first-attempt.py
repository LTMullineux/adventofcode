from collections import deque
from itertools import compress
from functools import reduce


def row_basin_generator(row_idx, row, split=9):
    row_basin, positions = [], set()
    for col_idx, value in enumerate(row):
        if value == split:
            if row_basin:
                yield row_basin, positions
            row_basin, positions = [], set()
        else:
            row_basin.append(value)
            positions.add((row_idx, col_idx - 1))

    if row_basin:
        yield row_basin, positions


def main():
    with open('input.txt') as f:
        data = [list(map(int, l)) for l in f.read().splitlines()]

    x, y = len(data[0]), len(data)

    row_basins = []
    for row_idx, row in enumerate(data):
        row_ = [9] + row + [9]
        row_basins.append([p for _, p in row_basin_generator(row_idx, row_)])

    basins = {k: b for k,b in enumerate(row_basins[0])}
    basin_count = len(basins) - 1

    for row_idx, row in enumerate(row_basins[1:], 1):
        for row_basin in row:

            has_match_above = False
            row_basin_cols = set(map(lambda x: x[1], row_basin))

            # Find matching basins above
            for basin_idx, basin in basins.items():

                above_row_basin_cols = set([x[1] for x in list(basin) if x[0] == row_idx - 1])
                if above_row_basin_cols & row_basin_cols:
                    has_match_above = True
                    basins[basin_idx] = basin | row_basin
                    break

            if not has_match_above:
                basin_count += 1
                basins[basin_count] = row_basin

    basin_sizes = sorted([len(points) for points in basins.values()])
    print(reduce(lambda x, y: x * y, list(sorted(basin_sizes, reverse=True))[0:3]))


if __name__ == '__main__':
    main()