from functools import lru_cache
from collections import Counter
from itertools import product
import copy

def parse_input(filename):
    with open(filename, 'r') as f:
        positions = [int(l.split()[-1]) for l in f.read().splitlines()]

    return positions

def part1(positions):
    scores = [0] * len(positions)
    dice, rolls = 0, 0

    while True:
        player_idx = rolls % len(positions)
        rolls_str = []
        for r in range(3):
            dice = dice % 100 + 1
            positions[player_idx] = 1 + (positions[player_idx] + dice - 1) % 10
            rolls += 1
            rolls_str.append(str(dice))

        scores[player_idx] += positions[player_idx]

        if scores[player_idx] >= 1000:
            winning_score = scores[1 - player_idx] * rolls
            print(f'Player {player_idx + 1} wins with {winning_score} points')
            break

# the sum of rolls in a turn and the count of the number of ways it can occur
DIRAC_DICE = Counter([sum(x) for x in product(range(1, 4), range(1, 4), range(1, 4))])

@lru_cache(maxsize=None)
def quantum(p1, p2, s1, s2, player_to_roll):
    if s1 >= 21: return 1
    if s2 >= 21: return 0

    wins = 0
    for roll_sum, ways_to_roll in DIRAC_DICE.items():
        if player_to_roll == 1:
            p = 1 + (p1 + roll_sum - 1) % 10
            s = s1 + p
            wins += ways_to_roll * quantum(p, p2, s, s2, 2)
        else:
            p = 1 + (p2 + roll_sum - 1) % 10
            s = s2 + p
            wins += ways_to_roll * quantum(p1, p, s1, s, 1)

    return wins

def part2(positions):
    print(quantum(*positions, 0, 0, 1))


if __name__ == '__main__':
    positions = parse_input('input.txt')
    part1(copy.deepcopy(positions))
    part2(copy.deepcopy(positions))
