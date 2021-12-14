import re

def parse_input(filename):
    with open(filename, 'r') as f:
        # raw = [l.strip() for l in f.readlines()]
        dots, instructions = f.read().split('\n\n')

    dots = {
        (int(x), int(y)) for x,y in
        re.findall(r'(\d+),(\d+)', dots)
    }

    instructions = [
        (axis, int(fold_point)) for axis, fold_point in
        re.findall(r'fold along ([xy])=(\d+)', instructions)
    ]

    return dots, instructions

def print_grid(dots):
    x_max = max(x for x,y in dots)
    y_max = max(y for x,y in dots)
    for y in range(y_max + 1):
        print(' '.join('#' if (x,y) in dots else '.' for x in range(x_max + 1)))

def fold(dots, axis, fold_point):
    new_dots = set()
    for x,y in dots:
        if axis == 'y' and y > fold_point:
            new_dots.add((x, fold_point * 2 - y))
        elif axis == 'x' and x > fold_point:
            new_dots.add((fold_point * 2 - x, y))
        else:
            new_dots.add((x, y))

    return new_dots


def main():
    dots, instructions = parse_input('input.txt')
    for i, (axis, fold_point) in enumerate(instructions, 1):
        print('-' * 50)
        print(f'Fold {i}: folding along {axis}={fold_point}')
        dots = fold(dots, axis, fold_point)
        print(len(dots))

    print_grid(dots)

if __name__ == '__main__':
    main()