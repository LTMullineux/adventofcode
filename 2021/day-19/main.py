from itertools import combinations
import copy, re

# rotations thru 90, 180, 270 for x, y and z
ROTATIONS = [
    lambda x, y, z: ((-y, x, z), (-x, -y, z), (y, -x, z)),
    lambda x, y, z: ((z, y, -x), (-x, y, -z), (-z, y, x)),
    lambda x, y, z: ((x, -z, y), (x, -y, -z), (x, z, -y)),
]

def read_input(filename):
    with open(filename) as f:
        raw = [i.strip().split('\n')[1:] for i in f.read().split('\n\n')]

    return [
        [tuple(int(i) for i in line.split(',')) for line in scanner]
        for scanner in raw
    ]

class Scanner:
    def __init__(self, i, beacons):
        self.i = i
        self.pos = (0, 0, 0)
        self.beacons = set(beacons)
        self.rotated_beacons = self.get_rotated_beacons()

    def __repr__(self):
        return f'< Scanner {self.i} @ {self.pos} >'

    def get_rotated_beacons(self):
        rotated_beacons = {tuple(copy.deepcopy(self.beacons))}
        for rotation_func in ROTATIONS:

            points = set()
            for beacon in rotated_beacons:

                rotated_beacon = set(zip(*(rotation_func(*b) for b in beacon)))
                points.update(rotated_beacon)

            rotated_beacons.update(points)

        return rotated_beacons

def itersect_scanners(anchor, relative):
    for rotated_beacons in relative.rotated_beacons:
        for x1, y1, z1 in anchor.beacons:
            for x2, y2, z2 in rotated_beacons:
                dx = x1 - x2
                dy = y1 - y2
                dz = z1 - z2
                points = set((x + dx, y + dy, z + dz) for x,y,z in rotated_beacons)
                if len(anchor.beacons & points) >= 12:
                    return points, (dx, dy, dz)

    return None, None


def main():
    scanners = [Scanner(i, p) for i, p in enumerate(read_input('input.txt'))]
    points = copy.deepcopy(scanners[0].beacons)
    anchors = [scanners[0]]
    relatives = scanners[1:]

    while anchors:
        anchor_scanner = anchors.pop()
        matched_scanners = []

        for relative_scanner in relatives:
            abs_points, relative_pos = itersect_scanners(anchor_scanner, relative_scanner)

            if abs_points:
                points.update(abs_points)
                relative_scanner.beacons = abs_points
                anchors.append(relative_scanner)
                relative_scanner.pos = relative_pos
                print(f'{relative_scanner.i} matched with delta {relative_pos}')
            else:
                matched_scanners.append(relative_scanner)

        relatives = matched_scanners

    print(len(points))

    max_dist = 0
    positions = {s.pos for s in scanners}
    for (x1, y1, z1), (x2, y2, z2) in combinations(positions, 2):
        dist = abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)
        if dist > max_dist:
            max_dist = dist

    print(max_dist)


if __name__ == '__main__':
    main()