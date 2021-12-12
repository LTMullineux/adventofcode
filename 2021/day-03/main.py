def stringify(int_list):
    return ''.join(list(map(str, int_list)))

def get_params(report):
    report_items, item_length = len(report), len(report[0])
    counter = dict(zip(range(item_length), [0] * item_length))
    for bits in report:
        for i, bit in enumerate(bits):
            if bit == '1':
                counter[i] += 1

    gamma = [int((v / report_items) >= 0.5) for v in counter.values()]
    epsilon = [(int(g) + 1) % 2 for g in gamma]
    return stringify(gamma), stringify(epsilon)


def create_inverted_index(report):
    item_length = len(report[0])
    index = {k: {'0': set(), '1': set()} for k in range(item_length)}
    for bits in report:
        for i, bit in enumerate(bits):
            index[i][bit].add(bits)

    return index

def get_rating(report, init_bits, gamma_or_epsilon):
    inverted_index = create_inverted_index(report)
    rating = set(report)
    init_bits_ = init_bits
    i = 0

    while len(rating) > 1:

        bit = init_bits_[i]
        rating = inverted_index[i][bit]
        inverted_index = create_inverted_index(list(rating))

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
    with open('input.txt', 'r') as f:
        report = [l.strip() for l in f.readlines()]

    gamma, epsilon = get_params(report)
    score = int(gamma, 2) * int(epsilon, 2)

    print('--- Part 1 ---')
    print('gamma:', gamma, ' -> ', int(gamma, 2))
    print('epsilon:', epsilon, ' -> ', int(epsilon, 2))
    print('score: ', score)

    oxygen_rating = get_rating(report, gamma, 'gamma').pop()
    co2_rating = get_rating(report, epsilon, 'epsilon').pop()
    score = int(oxygen_rating, 2) * int(co2_rating, 2)

    print('--- Part 2 ---')
    print('oxygen_rating:', oxygen_rating, ' -> ', int(oxygen_rating, 2))
    print('co2_rating:', co2_rating, ' -> ', int(co2_rating, 2))
    print('score: ', score)


if __name__ == '__main__':
    main()