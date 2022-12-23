from itertools import pairwise, count

def read_rocks(filename):
    rocks = set()
    with open(filename) as f:
        for line in f.readlines():
            rock_paths = line.strip().split(' -> ')

            for start, stop in pairwise(rock_paths):
                start_x, start_y = map(int, start.split(','))
                stop_x, stop_y = map(int, stop.split(','))

                if start_y == stop_y:
                    min_x, max_x = min(start_x, stop_x), max(start_x, stop_x)
                    for x in range(min_x, max_x + 1):
                        rocks.add((x, start_y))

                elif start_x == stop_x:
                    min_y, max_y = min(start_y, stop_y), max(start_y, stop_y)
                    for y in range(min_y, max_y + 1):
                        rocks.add((start_x, y))

    return rocks

def print_cave(rocks, sand_at_rest, floor=False):
    min_x, max_x = min(x for x, y in rocks), max(x for x, y in rocks)
    min_y, max_y = min(y for x, y in rocks), max(y for x, y in rocks)

    for y in range(max_y + 4):
        row = []
        for x in range(min_x - 4, max_x + 5):
            if (x, y) in rocks:
                row.append('#')
            elif (x, y) in sand_at_rest:
                row.append('o')
            else:
                row.append('.')
        print(''.join(row))


def drop_grain(x, y, deepest_y, blockers):
    if (500, 0) in blockers:
        return None

    for new_y in range(y, deepest_y + 1):
        if (x, new_y) in blockers:
            if (x - 1, new_y) not in blockers:
                return drop_grain(x - 1, new_y, deepest_y, blockers)
            elif (x + 1, new_y) not in blockers:
                return drop_grain(x + 1, new_y, deepest_y, blockers)
            else:
                return x, new_y - 1

def drop_sand(rocks):
    sand_at_rest = set()
    deepest_y = max(y for x, y in rocks)
    while True:

        blockers = rocks | sand_at_rest
        grain_resting_place = drop_grain(500, 0, deepest_y, blockers)
        if not grain_resting_place:
            return sand_at_rest

        sand_at_rest.add(grain_resting_place)

def main():
    rocks = read_rocks('input.txt')

    sand_at_rest_part_1 = drop_sand(rocks)
    print_cave(rocks, sand_at_rest_part_1)

    inf_floor_y = 2 + max(y for x, y in rocks)
    floored_rocks = rocks | set((x, inf_floor_y) for x in range(500 - inf_floor_y, 501 + inf_floor_y))
    sand_at_rest_part_2 = drop_sand(floored_rocks)
    print_cave(floored_rocks, sand_at_rest_part_2)

    print('Part 1:', len(sand_at_rest_part_1))
    print('Part 2:', len(sand_at_rest_part_2))

if __name__ == '__main__':
    main()
