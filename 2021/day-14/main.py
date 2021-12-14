from collections import deque, Counter

def read_input(filename):
    with open(filename, 'r') as f:
        template, pairs = f.read().split('\n\n')

    rules = {a:b for a,b in [p.split(' -> ') for p in pairs.split('\n')]}
    pair_counter = {p:0 for p in rules.keys()}
    base_counter = {p:0 for p in rules.values()}
    for b in template:
        base_counter[b] += 1
    return template, rules, pair_counter, base_counter

def new_inserts(pair, rules):
    v = rules[pair]
    return v, pair[0] + v, v + pair[1]

def main():
    template, rules, pair_counter, base_counter = read_input('input.txt')
    for pair in [template[i:i+2] for i in range(len(template) - 1)]:
        pair_counter[pair] += 1

    print('Template:', template)
    i, rounds = 0, 40
    while i < rounds:
        i += 1
        new_pair_counter = {k:0 for k,v in pair_counter.items()}
        for pair, count in pair_counter.items():
            if count == 0:
                continue

            middle, left_insert, right_insert = new_inserts(pair, rules)
            base_counter[middle] += count
            new_pair_counter[left_insert] += count
            new_pair_counter[right_insert] += count

        pair_counter = new_pair_counter
        score = max(base_counter.values()) - min(base_counter.values())

        print('-' * 50)
        print('Round', i)
        print('Polymer length:', sum(base_counter.values()))
        print('Score:', score)


if __name__ == '__main__':
    main()
