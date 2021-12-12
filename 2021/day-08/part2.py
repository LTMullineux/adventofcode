def main():

    with open('input.txt') as f:
        raw_entries = [e.split(' | ') for e in f.read().splitlines()]
        entries = [(ins.split(), outs.split()) for ins, outs in raw_entries]

    output_sums = []
    for inputs, outputs in entries:

        digits = [set()] * 10
        digits[1] = next(set(input_) for input_ in inputs if len(input_) == 2)
        digits[4] = next(set(input_) for input_ in inputs if len(input_) == 4)
        digits[7] = next(set(input_) for input_ in inputs if len(input_) == 3)
        digits[8] = next(set(input_) for input_ in inputs if len(input_) == 7)

        len_fives = (set(input_) for input_ in inputs if len(input_) == 5)
        for len_five in len_fives:
            if digits[1].issubset(len_five):
                digits[3] = len_five
            elif len(digits[4] & len_five) == 3:
                digits[5] = len_five
            else:
                digits[2] = len_five

        len_sixes = (set(input_) for input_ in inputs if len(input_) == 6)
        for len_six in len_sixes:
            if len(len_six & digits[4]) == 4:
                digits[9] = len_six
            elif len(len_six & digits[5]) == 5:
                digits[6] = len_six
            else:
                digits[0] = len_six

        str_output = ''
        for output in outputs:
            mod_10_value = 0
            digit_idx = digits.index(set(output))
            str_output += str(digit_idx)

        output_sums.append(int(str_output))

    print(output_sums)
    print(f'Sum of output codes: {sum(output_sums)}')


if __name__ == '__main__':
    main()
