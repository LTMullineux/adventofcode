import copy

def main():
    with open('input.txt') as f:
        data = f.read().splitlines()

    connections = {}
    for link in data:
        a, b = link.split('-')
        if a not in connections:
            connections[a] = [b]
        else:
            connections[a].append(b)

        if b not in connections:
            connections[b] = [a]
        else:
            connections[b].append(a)

    candidate_paths = [['start']]
    paths = []
    counter = 0
    while True:
        paths_to_explore = [p for p in candidate_paths if p[-1] != 'end']
        if not paths_to_explore:
            break

        candidate_paths = []
        for path in paths_to_explore:
            for next_cave in connections[path[-1]]:

                candidate_path = copy.deepcopy(path)
                if next_cave == 'start':
                    continue

                elif next_cave == 'end':
                    candidate_path.append(next_cave)
                    paths.append(candidate_path)

                elif next_cave.islower() and next_cave in candidate_path:
                    continue

                else:
                    candidate_path.append(next_cave)
                    candidate_paths.append(candidate_path)

    print(len(paths))


if __name__ == '__main__':
    main()