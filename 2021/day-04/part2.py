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

def get_score(board, marker):
    unmarked_sum = 0
    for row, mask in zip(board, marker):
        anti_mask = [not m for m in mask]
        unmarked_sum += sum(compress(map(int, row), anti_mask))

    return unmarked_sum


def main():

    board_size = 5
    draws, boards = read_input('input.txt')
    markers = [create_marker(board_size) for _ in range(len(boards))]

    markers, winning_draws, rnds = [], [], []
    for board in boards:

        has_won = False
        marker = create_marker(board_size)
        for rnd, draw in enumerate(draws):

            new_marker = update_marker(board, marker, draw)
            if marker_wins(new_marker):
                has_won = True
                markers.append(new_marker)
                winning_draws.append(draw)
                rnds.append(rnd)
                break

            if has_won: break
            marker = copy.deepcopy(new_marker)

        if not has_won:
            markers.append(marker)
            winning_draws.append(-1)
            rnds.append(-1)

    last_winner = max(rnds)
    max_index = rnds.index(last_winner)
    board, marker, draw, rnd = boards[max_index], markers[max_index], winning_draws[max_index], rnds[max_index]

    print(f'board {max_index} wins last on round {rnd} with draw {draw}')
    print(f'with a score of {get_score(board, marker)} * {draw} = {get_score(board, marker) * int(draw)}')


if __name__ == '__main__':
    main()