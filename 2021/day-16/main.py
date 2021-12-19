from functools import reduce
from operator import mul

ops = {
    0: lambda v: sum(v),
    1: lambda v: reduce(mul, v, 1),
    2: lambda v: min(v),
    3: lambda v: max(v),
    5: lambda v: int(v[0] > v[1]),
    6: lambda v: int(v[0] < v[1]),
    7: lambda v: int(v[0] == v[1]),
}

def hex_to_bin(hex_str):
    return ''.join(f'{int(c, 16):04b}' for c in hex_str)

def get_packet_info(bin_str):
    version = int(bin_str[:3], 2)
    type_id = int(bin_str[3:6], 2)
    packets = bin_str[6:]
    return version, type_id, packets

def parse_literal(bin_str):
    values = []
    pointer = 0
    new_bin_str = bin_str
    while True:
        chunk = new_bin_str[pointer:pointer + 5]
        new_bin_str = new_bin_str[5:]
        values.append(chunk[1:])
        if chunk[0] == '0':
            break

    return int(''.join(values), 2), new_bin_str

def parse_operator(bin_str, type_id, versions):
    values = []
    length_type_id = int(bin_str[0], 2)

    if length_type_id:
        count = int(bin_str[1:12], 2)
        new_bin_str = bin_str[12:]
        for _ in range(count):
            value, new_bin_str = parse(new_bin_str, versions)
            values.append(value)

    else:
        length = int(bin_str[1:16], 2)
        new_bin_str = bin_str[16:]
        size = len(new_bin_str)
        while len(new_bin_str) + length > size:
            value, new_bin_str = parse(new_bin_str, versions)
            values.append(value)

    return ops[type_id](values), new_bin_str

def parse(bin_str, versions):
    version, type_id, next_bin_str = get_packet_info(bin_str)
    versions.append(version)
    if type_id == 4:
        return parse_literal(next_bin_str)
    else:
        return parse_operator(next_bin_str, type_id, versions)

def main():
    with open('input.txt', 'r') as f:
        bin_str = hex_to_bin(f.read().strip())

    versions = []
    value, bin_str = parse(bin_str, versions)
    print(sum(versions), value)


if __name__ == '__main__':
    main()