def print_grid(max_x, max_y, grid):
    for y in range(max_y + 1):
        row = []
        for x in range(max_x + 1):
            row.append(grid[(x, y)])
        print(row)

def get_neighbours(grid, x, y):
    for d_x in (-1, 0, 1):
        for d_y in (-1, 0, 1):
            if d_x == 0 and d_y == 0:
                continue

            neighbour = (x + d_x, y + d_y)
            if neighbour in grid:
                yield neighbour

def reset_energy(grid):
    for k,v in grid.items():
        if v > 9:
            grid[k] = 0

def next_step(grid):
    new_flashes = 0
    to_be_flashed = set()
    has_been_flashed = set()
    for point in grid:
        grid[point] += 1
        if grid[point] > 9:
            to_be_flashed.add(point)

    while to_be_flashed:
        point = to_be_flashed.pop()
        has_been_flashed.add(point)
        new_flashes += 1

        for neighbour in get_neighbours(grid, *point):
            grid[neighbour] += 1
            if grid[neighbour] > 9 and neighbour not in has_been_flashed:
                to_be_flashed.add(neighbour)

    reset_energy(grid)
    return new_flashes

def main():
    grid = {}
    with open('input.txt') as f:
        for y, c in enumerate(f.read().splitlines()):
            for x, energy in enumerate(c):
                grid[(x, y)] = int(energy)

    max_x = max(x for x, y in grid)
    max_y = max(y for x, y in grid)

    flashes = 0
    step = 0
    while step <= 100:

        new_flashes = next_step(grid)
        flashes += new_flashes
        print('Step:', step, 'Flashes:', flashes)
        step += 1


if __name__ == '__main__':
    main()