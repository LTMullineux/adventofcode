from itertools import chain, pairwise
from collections import defaultdict
import re

def read_signals(filename):
    pattern = r'Sensor at x=(?P<x_s>-?\d+), y=(?P<y_s>-?\d+): closest beacon is at x=(?P<x_b>-?\d+), y=(?P<y_b>-?\d+)'
    with open(filename, 'r') as f:
        return[tuple(map(int, r)) for r in re.findall(pattern, f.read())]

def print_signals(signals):
    xs = [(s[0], s[2]) for s in signals]
    ys = [(s[1], s[3]) for s in signals]
    min_x, max_x = min(chain(*xs)), max(chain(*xs))
    min_y, max_y = min(chain(*ys)), max(chain(*ys))

    sensors = set([s[:2] for s in signals])
    beacons = set([s[2:] for s in signals])

    for y in range(min_y, max_y + 1):
        row = []
        for x in range(min_x, max_x + 1):
            if (x, y) in sensors:
                row.append('S')
            elif (x, y) in beacons:
                row.append('B')
            else:
                row.append('.')
        print(''.join(row))

def print_coverage(intervals, signals):
    def _is_covered(x, left, right):
        if left <= x <= right:
            return True

    xs = [(s[0], s[2]) for s in signals]
    ys = [(s[1], s[3]) for s in signals]
    min_x, max_x = min(chain(*xs)), max(chain(*xs))
    min_y, max_y = min(chain(*ys)), max(chain(*ys))

    sensors = set([s[:2] for s in signals])
    beacons = set([s[2:] for s in signals])

    for y in range(min_y, max_y + 1):
        row = []
        for x in range(min_x, max_x + 1):
            if (x, y) in sensors:
                row.append('S')
            elif (x, y) in beacons:
                row.append('B')
            elif any(_is_covered(x, left, right) for left, right in intervals[y]):
                row.append('#')
            else:
                row.append('.')

        print(''.join(row))

def manhattan_dist(x, y, i, j):
    return abs(x - i) + abs(y - j)

def merge_intervals(intervals):
    intervals.sort()
    stack = [list(intervals[0])]
    for interval in intervals[1:]:
        # check if previous interval overlaps with current interval
        curr_left, curr_right = interval
        prev_left, prev_right = stack[-1]
        if prev_left <= curr_left <= prev_right:
            stack[-1][1] = max(stack[-1][1], curr_right)
        else:
            stack.append(interval)

    return stack

def get_row_intervals(signals, row):
    intervals = []
    for sx, sy, bx, by in signals:
        row_remainder = manhattan_dist(sx, sy, bx, by) - abs(sy - row)
        if row_remainder > 0:
            intervals.append([sx - row_remainder, sx + row_remainder])

    if len(intervals) == 0:
        return []

    return merge_intervals(intervals)

def find_distress_beacon(signals):
    seen_y = set()
    distress_y_min, distress_y_max = 0, 4_000_000
    for sx, sy, bx, by in signals:
        dist = manhattan_dist(sx, sy, bx, by)

        # go from top of bottom of diamond
        # distress beacon must be 1 row outside of perimeter
        # gap must be size 1, else would be more than one beacon
        for y in range(sy - dist - 1, sy + dist + 2):
            if y in seen_y:
                continue

            seen_y.add(y)
            intervals = get_row_intervals(signals, y)
            if not (distress_y_min <= y <= distress_y_max) or (len(intervals) <= 1):
                continue

            for (_, left), (right, _) in pairwise(intervals):
                if right - left == 2:
                    return left + 1, y

    return -1, -1

def main():
    signals = read_signals('input.txt')

    intervals = get_row_intervals(signals, 2_000_000)
    beacons_positions = sum((x2 - x1 for x1, x2 in merge_intervals(intervals)))
    print(f'Part 1: {beacons_positions}')

    distress_x, distress_y = find_distress_beacon(signals)
    tuning_freq = distress_x * 4_000_000 + distress_y
    print(f'Part 2: ({distress_x}, {distress_y}) -> tuning frequency {tuning_freq}')


if __name__ == '__main__':
    main()
