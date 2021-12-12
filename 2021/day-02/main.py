def read_data(filename):
    cmds = []
    with open(filename, 'r') as f:
        for l in f.readlines():
            cmd, value = l.strip().split(' ')
            cmds.append((cmd, int(value)))

    return cmds

def parse_cmd(cmd, value, depth, x, y):
    if cmd == 'forward':
        x += value
        depth += y * value
    elif cmd == 'up':
        y -= value
    elif cmd == 'down':
        y += value
    else:
        raise ValueError(f'Invalid command `{cmd}`')

    return depth, x, y


def main():

    cmds = read_data('input.txt')
    depth, x, y = 0, 0, 0
    for cmd, value in cmds:
        depth, x, y = parse_cmd(cmd, value, depth, x, y)

    print('--- Part 1 ---')
    print(f'Final position: {x}, {y}')
    print(f'Final score: {x * y}')

    print('--- Part 2 ---')
    print(f'Final position: {depth}, {x}, {y}')
    print(f'Final score: {depth * x}')


if __name__ == '__main__':
    main()