def load_program(filename):
    instructions = []
    with open(filename) as f:
        for line in f:
            l = line.strip()
            if l == 'noop':
                instructions.append(('noop'))
            else:
                instr, value = l.split(' ')
                instructions.append((instr, int(value)))

    return instructions

def main():
    instructions = load_program('input.txt')

    X = [1, 1]
    for args in instructions:
        match args:
            case ('noop'):
                X.append(X[-1])
            case ('addx', v):
                X.append(X[-1])
                X.append(X[-1] + v)

    indexes = [20, 60, 100, 140, 180, 220]
    strength_score = sum([X[i] * i for i in indexes])
    print('Part 1')
    print(f'Strength score: {strength_score}')

    CRT = []
    for row in range(6):
        pos, CRT_row = 0, []
        for cycle in range(40 * row + 1, 40 * (row + 1) + 1):
            sprite = X[cycle]
            if sprite - 1 <= pos <= sprite + 1:
                CRT_row.append('#')
            else:
                CRT_row.append('.')

            pos += 1

        CRT.append(CRT_row)

    print('Part 2')
    print('\n'.join(''.join(r) for r in CRT))


if __name__ == '__main__':
    main()