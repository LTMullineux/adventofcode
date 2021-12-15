from queue import PriorityQueue
from copy import deepcopy

def read_input(filename):
    with open(filename, 'r') as f:
        data = [list(map(int, l)) for l in f.read().splitlines()]

    return data

def tile_grid(grid, factor):
    grid = deepcopy(grid)
    old_x_max, old_y_max = len(grid[0]), len(grid)
    new_x_max, new_y_max = old_x_max * factor, old_y_max * factor
    new_grid = []

    for new_y in range(new_y_max):
        new_row = []

        for new_x in range(new_x_max):
            tile_bump = new_x // old_x_max + new_y // old_y_max
            value = grid[new_y % old_y_max][new_x % old_x_max]
            new_row.append(1 + (value + tile_bump - 1) % 9)

        new_grid.append(new_row)

    return new_grid

def print_grid(grid):
    for row in grid:
        print(''.join(str(x) for x in row))

def print_path(grid, dots):
    x_max = len(grid[0])
    y_max = len(grid)
    for y in range(y_max):
        print(' '.join('#' if (x,y) in dots else '.' for x in range(x_max)))

def manhattan_dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbours(grid, point):
    x_max, y_max = len(grid[0]), len(grid)
    deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    return (
        (point[0] + dx, point[1] + dy) for dx, dy in deltas
        if 0 <= point[0] + dx < x_max and 0 <= point[1] + dy < y_max
    )

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]

def a_star(grid, start, goal):
    frontier = PriorityQueue()
    came_from = {}
    cost_so_far = {}

    frontier.put(start, 0)
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            return reconstruct_path(came_from, current)

        for n in get_neighbours(grid, current):
            new_cost = cost_so_far[current] + grid[n[1]][n[0]]

            if n not in cost_so_far or new_cost < cost_so_far[n]:
                cost_so_far[n] = new_cost
                priority = new_cost + manhattan_dist(goal, n)
                frontier.put(n, priority)
                came_from[n] = current

def get_risk(grid, path):
    return sum(grid[y][x] for x, y in path[2:])


def main():

    grid = read_input('input.txt')

    part1_grid = tile_grid(grid, 1)
    start = (0, 0)
    goal = (len(part1_grid[0]) - 1, len(part1_grid) - 1)
    path = a_star(part1_grid, start, goal)
    risk = get_risk(part1_grid, path)
    print(f'Part 1 risk: {risk}')

    part2_grid = tile_grid(grid, 5)
    start = (0, 0)
    goal = (len(part2_grid[0]) - 1, len(part2_grid) - 1)
    path = a_star(part2_grid, start, goal)
    risk = get_risk(part2_grid, path)
    print(f'Part 2 risk: {risk}')


if __name__ == '__main__':
    main()