from ast import literal_eval
from functools import cmp_to_key

def get_pairs(seq, size):
    for i in range(0, len(seq), size):
        yield seq[i:i + size - 1]

def read_packet_pairs(filename):
    with open(filename, 'r') as f:
        packets = [
            tuple(map(lambda p: literal_eval(p.strip()), pair))
            for pair in get_pairs(f.readlines(), 3)
        ]

    return packets

def compare_packets(l, r):
    if isinstance(l, int) and isinstance(r, int):
        return r - l
    elif isinstance(l, int):
        l = [l]
    elif isinstance(r, int):
        r = [r]

    if len(l) == 0 or len(r) == 0:
        return len(r) - len(l)

    return compare_packets(l[0], r[0]) or compare_packets(l[1:], r[1:])

def main():
    packet_pairs = read_packet_pairs('input.txt')

    order_index_sum = sum((i for i, p in enumerate(packet_pairs, 1) if compare_packets(*p) > 0))
    print(f'Part 1: {order_index_sum}')

    all_packets = [p for pair in packet_pairs for p in pair] + [[[2]], [[6]]]
    sorted_packets = sorted(all_packets, key=cmp_to_key(compare_packets), reverse=True)
    two = sorted_packets.index([[2]]) + 1
    six = sorted_packets.index([[6]]) + 1
    print(f'Part 2: {two * six}')


if __name__ == '__main__':
    main()
