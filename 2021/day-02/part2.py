def read_data():
    cmds = []
    with open('input.txt', 'r') as f:
        for l in f.readlines():
            cmd, value = l.strip().split(' ')
            cmds.append((cmd, int(value)))
    return cmds

def parse_cmd(cmd, value, depth, horizontal, aim):
    if cmd == 'forward':
        horizontal += value
        depth += aim * value
    elif cmd == 'up':
        aim -= value
    elif cmd == 'down':
        aim += value
    else:
        raise ValueError('Invalid command')

    return depth, horizontal, aim

def main():
    # cmds = [
    #     ('forward', 5,),
    #     ('down', 5,),
    #     ('forward', 8,),
    #     ('up', 3,),
    #     ('down', 8,),
    #     ('forward', 2,),
    # ]

    cmds = read_data()
    depth, horizontal, aim = 0, 0, 0
    for cmd, value in cmds:
        depth, horizontal, aim = parse_cmd(cmd, value, depth, horizontal, aim)
        print('cmd:', cmd, ', value:', value, ', depth:', depth, ', horizontal:', horizontal, ', aim:', aim)

    print(f'Final position: {depth}, {horizontal}, {aim}')
    print(f'Final multiply: {depth * horizontal}')


if __name__ == '__main__':
    main()