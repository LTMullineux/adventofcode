


def main():
    report = [
        '00100',
        '11110',
        '10110',
        '10111',
        '10101',
        '01111',
        '00111',
        '11100',
        '10000',
        '11001',
        '00010',
        '01010',
    ]

    with open('input.txt', 'r') as f:
        report = [l.strip() for l in f.readlines()]

    report_items, item_length = len(report), len(report[0])
    counter = dict(zip(range(item_length), [0] * item_length))
    for bits in report:
        for i, bit in enumerate(bits):
            if bit == '1':
                counter[i] += 1

    gamma = ''.join([str(int(round(v / report_items))) for v in counter.values()])
    epsilon = ''.join([ str((int(g) + 1) % 2) for g in list(gamma) ])

    print(gamma, int(gamma, 2))
    print(epsilon, int(epsilon, 2))
    print(int(epsilon, 2) * int(gamma, 2))


if __name__ == '__main__':
    main()