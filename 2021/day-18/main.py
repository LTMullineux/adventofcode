from functools import reduce

def read_input(filename):
    with open(filename) as f:
        raw = f.read().splitlines()
    return [eval(r) for r in raw]

def split(snail):
    # return has split, new values
    if isinstance(snail, int):
        if snail <= 9:
            return True, [snail // 2, (snail + 1) // 2]
        else:
            return False, snail

    left, right = snail
    splut, left = split(left)
    if splut:
        return True, [left, right]

    splut, right = split(right)
    if splut:
        return True, [left, right]

def redooce(snail):
    exploded, snail, _, _ = explode(snail)
    if exploded:
        return redooce(snail)

    splut, snail = split(snail)
    if splut:
        return redooce(snail)

    return snail

def snail_sum(snail, snails):
    redooce([snail, snails])

def explode(snail, depth=0):
    # return exploded, new snail, sum to left, sum to right
    if isinstance(snail, int):
        return False, snail, 0, 0

    left, right = snail
    if depth == 4:
        return True, 0, left, right

    exploded, left, left_sum, right_sum = explode(left, depth + 1)
    if exploded:
        return True, [left, add_left(right, right_sum)], left_sum, 0

    exploded, right, left_sum, right_sum = explode(right, depth + 1)
    if exploded:
        return True, [add_right(left, left_sum), right], 0, right_sum

    return False, [left, right], 0, 0

def add_left(snail, value):
    if isinstance(snail, int): return snail + value
    return [add_left(snail[0], value), snail[1]]

def add_right(snail, value):
    if isinstance(snail, int): return snail + value
    return [snail[0], add_right(snail[1], value)]

def magnitude(snail):
    if isinstance(snail, int): return snail
    left, right = snail
    return 3 * magnitude(left) + 2 * magnitude(right)

def main():
    snails = read_input('example-input.txt')

    m1 = magnitude(reduce(snail_sum, snails[1:], snails[0]))
    print(m1)

    m2 = max(magnitude(snail_sum(i, b)) for i in snails for b in snails)
    print(m2)


if __name__ == '__main__':
    main()