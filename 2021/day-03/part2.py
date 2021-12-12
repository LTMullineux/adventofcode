def get_params(report):
    report_items, item_length = len(report), len(report[0])
    counter = dict(zip(range(item_length), [0] * item_length))
    for bits in report:
        for i, bit in enumerate(bits):
            if bit == '1':
                counter[i] += 1

    gamma = ''.join([str(int((v / report_items) >= 0.5)) for v in counter.values()])
    epsilon = ''.join([ str((int(g) + 1) % 2) for g in list(gamma) ])
    return gamma, epsilon

def create_reverse_index(report):
    item_length = len(report[0])
    index = {k: {'0': set(), '1': set()} for k in range(item_length)}
    for bits in report:
        for i, bit in enumerate(bits):
            index[i][bit].add(bits)

    return index

def get_rating(report, init_bits, gamma_or_epsilon):
    reverse_index = create_reverse_index(report)
    rating = set(report)
    init_bits_ = init_bits
    i = 0

    while len(rating) > 1:

        bit = init_bits_[i]
        rating = reverse_index[i][bit]
        reverse_index = create_reverse_index(list(rating))

        gamma, epsilon = get_params(list(rating))
        if gamma_or_epsilon == 'gamma':
            init_bits_ = gamma
        else:
            init_bits_ = epsilon

        i += 1
        if len(rating) == 1:
            break

    return rating


def main():
    report = ('00100', '11110', '10110', '10111', '10101', '01111', '00111', '11100', '10000', '11001', '00010', '01010',)

    with open('input.txt', 'r') as f:
        report = [l.strip() for l in f.readlines()]

    gamma, epsilon = get_params(report)

    print('gamma:', gamma)
    print('epsilon:', epsilon)
    print('score: ', f'{int(gamma, 2)} * {int(epsilon, 2)} = {int(gamma, 2) * int(epsilon, 2)}')

    oxygen_rating = get_rating(report, gamma, 'gamma').pop()
    co2_rating = get_rating(report, epsilon, 'epsilon').pop()

    print('oxygen_rating: ', oxygen_rating)
    print('co2_rating: ', co2_rating)
    print('score: ', f'{int(oxygen_rating, 2)} * {int(co2_rating, 2)} = {int(oxygen_rating, 2) * int(co2_rating, 2)}')


if __name__ == '__main__':
    main()