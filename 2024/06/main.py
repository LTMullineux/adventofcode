from pathlib import Path

Coord = tuple[int, int]
State = tuple[int, int, int, int]
Grid = list[list[str]]

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def find_path(grid: Grid, x: int, y: int, dir_index: int) -> list[State]:
    max_x, max_y = len(grid[0]), len(grid)
    dx, dy = DIRS[dir_index]
    path: list[State] = []

    while True:
        state = (x, y, dir_index)
        path.append(state)
        if not (-1 < x + dx < max_x and -1 < y + dy < max_y):
            break
        elif grid[y + dy][x + dx] == "#":
            dir_index = (dir_index + 1) % 4
            dx, dy = DIRS[dir_index]
        else:
            x += dx
            y += dy

    return path


def is_loop(grid: Grid, x: int, y: int, dir_index: int) -> bool:
    max_x, max_y = len(grid[0]), len(grid)
    dx, dy = DIRS[dir_index]
    states: set[State] = set()

    while True:
        state = (x, y, dir_index)
        if state in states:
            return True

        states.add(state)
        if not (-1 < x + dx < max_x and -1 < y + dy < max_y):
            return False
        elif grid[y + dy][x + dx] == "#":
            dir_index = (dir_index + 1) % 4
            dx, dy = DIRS[dir_index]
        else:
            x += dx
            y += dy


def main(filename: Path) -> None:
    with open(filename, "r") as f:
        grid: Grid = [list(i.strip()) for i in f.readlines()]

    x: int = 0
    y: int = 0
    max_x, max_y = len(grid[0]), len(grid)
    for j in range(max_y):
        for i in range(max_x):
            if grid[j][i] == "^":
                x, y = i, j
                break

    dir_index: int = 0
    path = find_path(grid, x, y, dir_index)
    visited = set([(x, y) for x, y, _ in path])
    print("part 1", len(visited))

    loop_counter = 0
    seen_obstacles = set()
    for path_last_state in path[2:]:
        i, j, _ = path_last_state
        if grid[j][i] == "#" or grid[j][i] == "^":
            continue

        if (i, j) in seen_obstacles:
            continue

        seen_obstacles.add((i, j))
        grid[j][i] = "#"
        if is_loop(grid, x, y, dir_index):
            loop_counter += 1

        grid[j][i] = "."

    print("part 2", loop_counter)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-e", "--example", action="store_true")
    args = parser.parse_args()

    filename = Path("example-input.txt") if args.example else Path("input.txt")
    main(filename)
