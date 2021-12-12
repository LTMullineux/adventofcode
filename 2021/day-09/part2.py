from collections import deque
from itertools import compress
from functools import reduce
import math

def print_grid(data):
    for l in data:
        print(l)

def transpose(data):
    x = list(zip(*data))
    return [list(i) for i in x]

def create_bool_mask(x, y):
    mask = []
    for i in range(y):
        mask.append([])
        for j in range(x):
            mask[i].append(False)
    return mask

def window(seq, n=2, func=None):
    if not func:
        func = lambda x: x
    it = iter(seq)
    win = deque((next(it, None) for _ in range(n)), maxlen=n)
    yield func(tuple(win))
    append = win.append
    for e in it:
        append(e)
        yield func(tuple(win))

def middle_is_lower(l):
    return l[0] > l[1] and l[1] < l[2]

def and_grids(row_mask, col_mask):
    max_x, max_y = len(row_mask[0]), len(row_mask)
    final_mask = create_bool_mask(max_x, max_y)
    for j in range(max_y):
        for i in range(max_x):
            final_mask[j][i] = row_mask[j][i] and col_mask[j][i]

    return final_mask

def get_risk(data, mask):
    risk = 0
    for data_row, mask_row in zip(data, mask):
        row_risk = list(compress(data_row, mask_row))
        risk += sum(map(lambda x: x + 1, row_risk))
    return risk

def get_low_points_mask(data):
    x, y = len(data[0]), len(data)
    row_mask = create_bool_mask(x, y)
    col_mask = transpose(row_mask)

    for y_, row in enumerate(data):
        row_ = [math.inf] + row + [math.inf]
        for x_, w in enumerate(window(row_, 3)):
            lower = middle_is_lower(w)
            if lower:
                row_mask[y_][x_] = True

    for y_, row in enumerate(transpose(data)):
        row_ = [math.inf] + row + [math.inf]
        for x_, w in enumerate(window(row_, 3)):
            lower = middle_is_lower(w)
            if lower:
                col_mask[y_][x_] = True

    return and_grids(row_mask, transpose(col_mask))

def get_low_points(data, low_point_mask):
    low_points = []
    for j in range(len(data)):
        for i in range(len(data[0])):
            if low_point_mask[j][i]:
                low_points.append((j, i))
    return low_points

def bfs_basins(data, low_points):
    basins = []
    max_y, max_x = len(data), len(data[0])
    for low_point in low_points:
        basin_points = set([low_point])
        point_stack = deque([low_point])

        while point_stack:
            y, x = point_stack.popleft()
            neighbours = ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1))
            for y_, x_ in neighbours:

                if y_ < 0 or y_ >= max_y or x_ < 0 or x_ >= max_x:
                    continue

                neighbour_height = data[y_][x_]
                if neighbour_height > data[y][x] and neighbour_height != 9:
                    basin_points.add((y_, x_))
                    point_stack.append((y_, x_))

        basins.append(basin_points)

    return basins


def main():
    with open('input.txt') as f:
        data = [list(map(int, l)) for l in f.read().splitlines()]

    low_point_mask = get_low_points_mask(data)
    low_points = get_low_points(data, low_point_mask)

    basins = bfs_basins(data, low_points)
    basin_sizes = sorted([len(points) for points in basins])
    print(reduce(lambda x, y: x * y, list(sorted(basin_sizes, reverse=True))[0:3]))

if __name__ == '__main__':
    main()