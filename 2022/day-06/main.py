from itertools import islice
from collections import deque

def read_stream(filename):
    with open(filename, 'r') as f:
        return f.read().strip()

def sliding_window(iterable, n):
    it = iter(iterable)
    window = deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)

def get_packet_marker(stream, length):
    for i, w in enumerate(sliding_window(stream, length), 0):
        if len(set(w)) == length:
            return i + length

def main():
    stream = read_stream('input.txt')

    print('Part 1:', get_packet_marker(stream, 4))
    print('Part 2:', get_packet_marker(stream, 14))

if __name__ == '__main__':
    main()
