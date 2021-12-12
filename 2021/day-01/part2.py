from collections import deque

def window(seq, n=2, func=None):
    if not func:
        func = lambda x: x
    it = iter(seq)
    win = deque((next(it, None) for _ in range(n)), maxlen=n)
    yield func(tuple(win))
    append = win.append
    for e in it:
        append(e)
        yield func(tuple(win))

def create_increase_list(l):
    return [int(l[i] > l[i-1]) for i in range(1, len(l))]

def main():
    with open('input.txt', 'r') as f:
        depths = [int(line) for line in f.readlines()]

    window_size = 3
    depth_window = list(window(depths, window_size, sum))
    increase = create_increase_list(depth_window)
    print(sum(increase))


if __name__ == '__main__':
    main()