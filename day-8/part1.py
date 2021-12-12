
digits = {
    0: {'a', 'b', 'c',      'e', 'f', 'g'},
    1: {          'c',           'f'     },
    2: {'a',      'c', 'd', 'e',      'g'},
    3: {'a',      'c', 'd',      'f', 'g'},
    4: {     'b', 'c', 'd',      'f'     },
    5: {'a', 'b',      'd',      'f', 'g'},
    6: {'a', 'b',      'd', 'e', 'f', 'g'},
    7: {'a',      'c',           'f'     },
    8: {'a', 'b', 'c', 'd', 'e', 'f', 'g'},
    9: {'a', 'b', 'c', 'd',      'f', 'g'},
}

digit_lens = {}
for d, displays in digits.items():
    display_len = len(displays)
    if display_len not in digit_lens:
        digit_lens[display_len] = {d}
        continue
    digit_lens[display_len].add(d)

def main():
    with open('input.txt') as f:
        raw_entries = f.read().splitlines()

    entries = [list(map(lambda x: x.split(' '), e.split(' | '))) for e in raw_entries]

    # for signals, outputs in entries:
    #     print(signals, ' -> ', outputs)

    unique_digits = {k:0 for k in (1,4,7,8,)}
    count = 0
    for signals, outputs in entries:
        for output in outputs:
            output_len = len(output)
            if len(digit_lens[output_len]) == 1:
                digit = list(digit_lens[output_len])[0]
                unique_digits[digit] += 1
                count += 1

    print(count)
    print(unique_digits)
    print(sum(unique_digits.values()))


if __name__ == '__main__':
    main()