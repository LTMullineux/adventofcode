import string

PRIORITIES = dict(zip(string.ascii_letters, range(1, 53)))

def get_rucksacks(filename):
    rucksacks = []
    with open(filename, 'r') as f:
        for line in f:
            items = list(line.strip())
            rucksacks.append(items)
    return rucksacks

def get_overlapping_item_priorities(rucksacks):
    overlap_priorities = []
    for rucksack in rucksacks:
        rucksack_size = len(rucksack)
        compartment_size = int(rucksack_size / 2)
        c1, c2 = set(rucksack[:compartment_size]), set(rucksack[compartment_size:])

        overlap = list(c1 & c2)
        priority = sum([PRIORITIES[item] for item in overlap])
        overlap_priorities.append((overlap, priority))

    return overlap_priorities

def get_chunks(seq, size):
    for i in range(0, len(seq), size):
        yield seq[i:i + size]

def get_badge(rucksacks):
    return set.intersection(*[set(r) for r in rucksacks])

def main():
    rucksacks = get_rucksacks('input.txt')

    print('Part 1')
    overlap_priorities = get_overlapping_item_priorities(rucksacks)
    total_priority = sum([priority for _, priority in overlap_priorities])
    print(f'Total priority: {total_priority}')

    print('Part 2')
    group_badges = [get_badge(g) for g in get_chunks(rucksacks, 3)]
    group_badge_priorities = [sum([PRIORITIES[item] for item in badge]) for badge in group_badges]
    print(f'Total group badge priority: {sum(group_badge_priorities)}')


if __name__=='__main__':
    main()