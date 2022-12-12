from itertools import chain


def read_input(filename):
    with open(filename) as f:
        algo, img = f.read().split('\n\n')

    transform = lambda line: map(lambda x: 0 if x == '.' else 1, line)
    algo = list(transform(algo))
    img = [list(transform(row)) for row in img.split('\n')]

    lit_pixels = set()
    for y, line in enumerate(img):
        for x, pixel in enumerate(line):
            if pixel:
                lit_pixels.add((x, y))

    return algo, lit_pixels

def get_image_bounds(lit_pixels, padding):
    min_x = min(x for x, y in lit_pixels) - padding
    max_x = max(x for x, y in lit_pixels) + padding
    min_y = min(y for x, y in lit_pixels) - padding
    max_y = max(y for x, y in lit_pixels) + padding
    return min_x, max_x, min_y, max_y

def plot(lit_pixels, padding=5):
    min_x, max_x, min_y, max_y = get_image_bounds(lit_pixels, padding=padding)
    for y in range(min_y, max_y + 1):
        row = []
        for x in range(min_x, max_x + 1):
            if (x, y) in lit_pixels:
                row.append('#')
            else:
                row.append('.')
        print(''.join(row))

def enhance(lit_pixels, algo, outer_lit):
    new_lit_pixels = set()
    min_x, max_x, min_y, max_y = get_image_bounds(lit_pixels, padding=0)

    for y in range(min_y - 1, max_y + 2):
        for x in range(min_x - 1, max_x + 2):

            bin_num = 0
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    px, py = x + dx, y + dy
                    bin_num <<= 1
                    bin_num |= ((px, py) in lit_pixels) or (
                        outer_lit and not (min_x <= px <= max_x and min_y <= py <= max_y)
                    )

            if algo[bin_num] == 1:
                new_lit_pixels.add((x, y))

    return new_lit_pixels, algo[-outer_lit] == 1

def main():

    algo, lit_pixels = read_input('input.txt')
    outer_lit = False

    plot(lit_pixels)
    for _ in range(2):
        print('-' * 50)
        lit_pixels, outer_lit = enhance(lit_pixels, algo, outer_lit)
        print(f'Number of lit pixels = {len(lit_pixels)}')
        plot(lit_pixels)

    print('#' * 50)
    print(f'Number of lit pixels = {len(lit_pixels)}')
    print('#' * 50)

    for _ in range(48):
        lit_pixels, outer_lit = enhance(lit_pixels, algo, outer_lit)

    print('#' * 50)
    print(f'Number of lit pixels = {len(lit_pixels)}')
    print('#' * 50)


if __name__ == '__main__':
    main()