def parse_raw_paths(raw_paths):
     split_coord = lambda x: tuple(map(int, x.split(',')))
     return [tuple(map(split_coord, p.split(' -> '))) for p in raw_paths]

def create_grid(x, y):
    print(f'Creating {x}x{y} grid')
    grid = []
    for i in range(x):
        inner = []
        for j in range(y):
            inner.append(0)
        grid.append(inner)
    return grid

def print_grid(grid):
    for row in grid:
        print(row)

def add_horizontal_path(grid, x1, x2, y):
    path_len = abs(x1 - x2)
    path_start = min(x1, x2)
    print(f'Horizontal path: row y={y} going from x={path_start} to x={path_start + path_len}')
    for i in range(path_len + 1):
        grid[y][path_start + i] += 1

    return grid

def add_vertical_path(grid, x, y1, y2):
    path_len = abs(y1 - y2)
    path_start = min(y1, y2)
    print(f'Vertical path: col x={x} going from y={path_start} to y={path_start + path_len}')
    for i in range(path_len + 1):
        grid[path_start + i][x] += 1

    return grid

def add_diagonal_path(grid, x1, y1, x2, y2):
    x_path_len = abs(x1 - x2)
    print(f'Diagnoal path of length ({abs(x1 - x2)}, {abs(y1 - y2)})')
    for _ in range(x_path_len + 1):
        grid[y1][x1] += 1
        x1 += 1 if x2 > x1 else -1
        y1 += 1 if y2 > y1 else -1

    return grid

def add_path_to_grid(grid, path):
    print(f'Adding path {path} to grid')
    x1, y1 = path[0]
    x2, y2 = path[1]

    is_diagonal = (x1 != x2) and (y1 != y2)
    is_horizontal = (y1 == y2)
    if is_diagonal:
        grid = add_diagonal_path(grid, x1, y1, x2, y2)
    elif is_horizontal:
        grid = add_horizontal_path(grid, x1, x2, y1)

    else:
        grid = add_vertical_path(grid, x1, y1, y2)

    return grid

def get_overlap_count(grid, threshold):
    return sum([sum(map(lambda x: x >= threshold, row)) for row in grid])

def main():
    with open('input.txt', 'r') as f:
        raw_paths = [l.strip() for l in f.readlines()]

    paths = parse_raw_paths(raw_paths)
    max_x = max(p[0][0] for p in paths) + 1
    max_y = max(p[0][1] for p in paths) + 1
    size = max(max_x, max_y)
    grid = create_grid(size, size)

    for p in paths:
        print('-' * 20)
        grid = add_path_to_grid(grid, p)
        # print_grid(grid)

    overlap_count = get_overlap_count(grid, threshold=2)
    print(f'Overlap count: {overlap_count}')

if __name__ == '__main__':
    main()