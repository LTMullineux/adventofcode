from itertools import product
from collections import deque
from math import inf

class Map:
    def __init__(self, filename):
        self.map = []
        self.base_char = ord('a')
        self.deltas = ((-1, 0), (1, 0), (0, -1), (0, 1))
        self.start = None
        self.end = None
        self.width = 0
        self.height = 0
        self.read_map(filename)

    def read_map(self, filename):
        S, E, z = (ord(c) - self.base_char for c in 'SEz')
        grid = []
        with open(filename) as f:
            self.map = [[ord(c) - self.base_char for c in line.strip()] for line in f]

        self.height = len(self.map)
        self.width = len(self.map[0])

        self.start = next((i, j) for i, j in product(range(self.height), range(self.width)) if self.map[i][j] == S)
        self.end = next((i, j) for i, j in product(range(self.height), range(self.width)) if self.map[i][j] == E)

        self.map[self.start[0]][self.start[1]] = 0
        self.map[self.end[0]][self.end[1]] = z

    def print(self):
        for r in self.map:
            print(''.join(chr(c + self.base_char) for c in r))

    def solve(self):
        '''
        Solve from end to start, using BFS.
        First `a` seen while working back is the best spot, else the start is the best spot.
        '''
        distance = 0
        q = deque([(self.end, 0)])
        seen = {self.end}
        best_starting_dist = None

        while q:
            (i, j), dist = q.popleft()
            if (i, j) == self.start:
                distance = dist
                break

            # first `a` found while working backwards
            if self.map[i][j] == 0 and best_starting_dist is None:
                best_starting_dist = dist

            candidates = ((i + di, j + dj) for di, dj in self.deltas)
            neighbors = {(ii, jj) for ii, jj in candidates if (
                0 <= ii < self.height and
                0 <= jj < self.width and
                self.map[i][j] - self.map[ii][jj] <= 1
            )}
            q.extend((n, dist + 1) for n in neighbors if n not in seen)
            seen.update(neighbors)

        return distance, best_starting_dist or distance

def main():
    m = Map('input.txt')
    distance, best_starting_dist = m.solve()

    print(f'Part 1: {distance}')
    print(f'Part 2: {best_starting_dist}')


if __name__ == '__main__':
    main()