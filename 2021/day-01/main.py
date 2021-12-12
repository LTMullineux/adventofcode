from collections import deque

def window(seq, n=2, func=None):
    '''
    Itertools recipe for creating windows across sequences.
    Option to apply a func to each w upon return.
    '''
    if not func:
        func = lambda x: x
    it = iter(seq)
    win = deque((next(it, None) for _ in range(n)), maxlen=n)
    yield func(tuple(win))
    append = win.append
    for e in it:
        append(e)
        yield func(tuple(win))

def get_increases(l):
    return [int(l[i] > l[i-1]) for i in range(1, len(l))]

def main():
    with open('input.txt', 'r') as f:
        depths = [int(line) for line in f.readlines()]

    part_1_increases = sum(get_increases(list(window(depths, 1, sum))))
    part_2_increases = sum(get_increases(list(window(depths, 3, sum))))
    print(part_1_increases)
    print(part_2_increases)


if __name__ == '__main__':
    main()