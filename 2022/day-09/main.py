DIRECTIONS = {
    'U': ( 0,  1),
    'D': ( 0, -1),
    'L': (-1,  0),
    'R': ( 1,  0),
}

def read_motions(filename):
    motions = []
    with open(filename) as f:
        for line in f:
            direction, distance = line.strip().split()
            motions.append((direction, int(distance)))
    return motions

def simulate_rope_tail(head_positions, rope_len):
    for _ in range(rope_len - 1):
        # all tails start from origin
        tail_positions = [(0, 0)]

        for hx, hy in head_positions[1:]:
            tx, ty = tail_positions[-1]
            dx, dy = hx - tx, hy - ty
            if max(abs(dx), abs(dy)) > 1:
                dx, dy = max(-1, min(1, dx)), max(-1, min(1, dy))
                tail_positions.append((tx + dx, ty + dy))

        # overwrite head_positions with the previous tail positions
        head_positions = tail_positions

    return tail_positions

def main():
    motions = read_motions('input.txt')
    head_positions = [(0, 0)]
    for direction, distance in motions:
        (x, y), (dx, dy) = head_positions[-1], DIRECTIONS[direction]
        head_positions.extend((x + dx * i, y + dy * i) for i in range(1, distance + 1))

    print('Part 1')
    tail_positions = simulate_rope_tail(head_positions, 2)
    unique_tail_position_count = len(set(tail_positions))
    print(f'Unique tail positions: {unique_tail_position_count}')

    print('Part 2')
    tail_positions = simulate_rope_tail(head_positions, 10)
    unique_tail_position_count = len(set(tail_positions))
    print(f'Unique tail positions: {unique_tail_position_count}')


if __name__ == '__main__':
    main()
