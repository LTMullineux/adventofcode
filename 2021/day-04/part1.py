import re, copy
from itertools import compress

def read_input(filename):
    with open(filename) as f:
        rows = f.readlines()

    draws, raw_boards = rows[0], rows[2:]
    draws = draws.strip().split(',')

    board_count = (len(raw_boards) - 2) // 5
    boards = [raw_boards[i*6 : i*6 + 5] for i in range(board_count)]
    boards = [[re.split(r'\s+', r.strip()) for r in b] for b in boards]

    return draws, boards

def create_marker(size):
    marker = []
    for i in range(size):
        inner = []
        for j in range(size):
            inner.append(False)
        marker.append(inner)
    return marker

def update_marker(board, marker, value):
    new_marker = copy.deepcopy(marker)
    for row_idx, row in enumerate(board):
        for col_idx, cell in enumerate(row):
            if cell == value:
                new_marker[row_idx][col_idx] = True
    return new_marker

def marker_wins(marker):
    # check rows
    if any([all(r) for r in marker]):
        return True

    # check columns
    marker_transposed = list(zip(*marker))
    if any([all(r) for r in marker_transposed]):
        return True

    return False

def get_score(board, marker, winning_draw):
    score = 0
    for row, mask in zip(board, marker):
        anti_mask = [not m for m in mask]
        score += sum(compress(map(int, row), anti_mask))

    return score * int(winning_draw)


def main():

    board_size = 5
    draws, boards = read_input('input.txt')
    markers = [create_marker(board_size) for _ in range(len(boards))]

    we_have_a_winner = [False] * len(boards)
    winning_draws = [-1] * len(boards)
    for draw in draws:

        new_markers = []
        for board_idx, (board, marker) in enumerate(zip(boards, markers)):

            new_marker = update_marker(board, marker, draw)
            new_markers.append(new_marker)

            if marker_wins(new_marker):
                we_have_a_winner[board_idx] = True
                winning_draws[board_idx] = draw

        markers = copy.deepcopy(new_markers)
        if any(we_have_a_winner):
            break

    print('-' * 100)
    winning_boards = list(compress(boards, we_have_a_winner))
    winning_markers = list(compress(markers, we_have_a_winner))
    winning_draws = list(compress(winning_draws, we_have_a_winner))

    for board, marker, draw in zip(winning_boards, winning_markers, winning_draws):
        print(f'{draw} wins!')
        print(f'with a score of {get_score(board, marker, draw)}')
        print(board)


if __name__ == '__main__':
    main()