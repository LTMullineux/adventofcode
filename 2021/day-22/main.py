import re
from collections import Counter

def read_input(filename):
    pattern = r'(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)'
    with open(filename) as f:
        steps = re.findall(pattern, f.read())

    steps = [(l[0] == 'on', tuple(map(int, l[1:])),) for l in steps]
    return steps

def intersect_cubes(a, b):
    x1_a, x2_a, y1_a, y2_a, z1_a, z2_a = a
    x1_b, x2_b, y1_b, y2_b, z1_b, z2_b = b

    x1, x2 = max(x1_a, x1_b), min(x2_a, x2_b)
    y1, y2 = max(y1_a, y1_b), min(y2_a, y2_b)
    z1, z2 = max(z1_a, z1_b), min(z2_a, z2_b)
    if x1 <= x2 and y1 <= y2 and z1 <= z2:
        return (x1, x2, y1, y2, z1, z2)

def get_cube_volume(cube):
    x1, x2, y1, y2, z1, z2 = cube
    return (x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1)

def reboot(steps):
    cubes = Counter()
    for is_on, step in steps:
        new_cubes = Counter()
        if is_on:
            new_cubes[step] += 1

        # find overlap and reduce double counting
        for cube, count in cubes.items():
            intersection = intersect_cubes(step, cube)
            if intersection:
                new_cubes[intersection] -= count

        cubes.update(new_cubes)

    return sum(get_cube_volume(cube) * count for cube, count in cubes.items())

def main():
    steps = read_input('input.txt')
    steps_1 = [s for s in steps if all(i <= 50 and i >= -50 for i in s[1])]

    print(reboot(steps_1))
    print(reboot(steps))


if __name__ == '__main__':
    main()