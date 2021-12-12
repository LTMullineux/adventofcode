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

def add_path_to_grid(grid, path):
    print(f'Adding path {path} to grid')
    x1, y1 = path[0]
    x2, y2 = path[1]

    is_horizontal = (y1 == y2)
    if is_horizontal:
        path_len = abs(x1 - x2)
        path_start = min(x1, x2)
        print(f'Horizontal path: row y={y1} going from x={path_start} to x={path_start + path_len}')
        print(y1, path_start, path_start + path_len)
        for i in range(path_len + 1):
            grid[y1][path_start + i] += 1

    else:
        path_len = abs(y1 - y2)
        path_start = min(y1, y2)
        print(f'Vertical path: col x={x1} going from x={path_start} to x={path_start + path_len}')
        print(x1, path_start, path_start + path_len)
        for i in range(path_len + 1):
            grid[path_start + i][x1] += 1

    return grid

def get_overlap_count(grid, threshold):
    return sum([sum(map(lambda x: x >= threshold, row)) for row in grid])

def main():
    with open('input.txt', 'r') as f:
        raw_paths = [l.strip() for l in f.readlines()]

    paths = parse_raw_paths(raw_paths)
    paths = list(filter(
        lambda p: (p[0][0] == p[1][0]) or (p[0][1] == p[1][1]),
        paths
    ))

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