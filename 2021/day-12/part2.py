from collections import Counter

def parse_connections(filename):
    with open(filename, 'r') as f:
        data = f.read().splitlines()

    connections_ = {}
    for link in data:
        a, b = link.split('-')
        if a not in connections_:
            connections_[a] = [b]
        else:
            connections_[a].append(b)

        if b not in connections_:
            connections_[b] = [a]
        else:
            connections_[b].append(a)

    connections_.pop('end')
    connections = {}
    for k, v in connections_.items():
        connections[k] = [vv for vv in v if vv != 'start']
    return connections

def main():

    connections = parse_connections('input.txt')
    small_caves = set([k for k in connections.keys() if k.islower()])
    candidate_paths = [['start']]
    paths = []

    while True:
        paths_to_explore = [p for p in candidate_paths if p[-1] != 'end']

        if not paths_to_explore:
            break

        candidate_paths = []
        for path in paths_to_explore:
            for next_cave in connections[path[-1]]:

                candidate_path = path[:]
                candidate_path.append(next_cave)
                small_cave_count = Counter([
                    c for c in candidate_path
                    if c.islower() and c not in {'start', 'end'}
                ]).values()

                if next_cave == 'start':
                    continue

                elif next_cave == 'end':
                    paths.append(candidate_path)

                # a single small cave can be visited at most twice
                # ... and the remaining small caves can be visited at most once
                elif next_cave.islower():
                    max_small_cave_vists = max(small_cave_count)

                    if max_small_cave_vists == 1:
                        candidate_paths.append(candidate_path)

                    elif sum(small_cave_count) - 1 == len(small_cave_count):
                        candidate_paths.append(candidate_path)

                    else:
                        continue
                else:
                    candidate_paths.append(candidate_path)

    print(len(paths))


if __name__ == '__main__':
    main()