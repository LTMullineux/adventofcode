import re

def parse_input(filename):
    with open(filename, 'r') as f:
        raw_target = f.read().strip()

    return tuple(map(int, re.search(r'x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)', raw_target ).groups()))

def trajectorize(inital_velocity, target):
    min_x, max_x, min_y, max_y = target
    x, y = 0, 0
    v_x, v_y = inital_velocity

    while True:
        # test if trajectory falls within target
        if (min_x <= x <= max_x) and (min_y <= y <= max_y):
            return 1

        # test if trajectory has gone to far
        if (x > max_x) or (y < min_y):
            return 0

        # update position
        x += v_x
        y += v_y
        v_x = max(0, v_x - 1)
        v_y -= 1

def main():
    target = parse_input('input.txt')
    min_x, max_x, min_y, max_y = target

    print(min_x, max_x, min_y, max_y)
    print(min_y * (1 + min_y) // 2)

    # x and y independent
    # x velocity bounded below by sqrt(2 * x_min)
    valid_velocities = 0
    for v_x in range(int((2 * min_x) ** 0.5), max_x + 1):
        for v_y in range(min_y, -min_y + 1):
            valid_velocities += trajectorize((v_x, v_y), target)

    print(valid_velocities)


if __name__ == '__main__':
    main()