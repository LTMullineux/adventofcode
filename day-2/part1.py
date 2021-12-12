def read_data():
    cmds = []
    with open('input.txt', 'r') as f:
        for l in f.readlines():
            cmd, value = l.strip().split(' ')
            cmds.append((cmd, int(value)))
    return cmds

def parse_cmd(cmd, value, x, y):
    if cmd == 'forward':
        x += value
    elif cmd == 'up':
        y -= value
    elif cmd == 'down':
        y += value
    else:
        raise ValueError('Invalid command')

    return x, y

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
    x, y = 0, 0
    for cmd, value in cmds:
        x, y = parse_cmd(cmd, value, x, y)

    print(f'Final position: {x}, {y}')
    print(f'Final multiply: {x * y}')


if __name__ == '__main__':
    main()