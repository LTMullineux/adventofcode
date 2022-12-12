def get_section_pairs(filename):
    sections = []
    with open(filename, 'r') as f:
        for line in f:
            range_1, range_2 = line.strip().split(',')
            x1, x2 = range_1.split('-')
            x3, x4 = range_2.split('-')
            sections.append(((int(x1), int(x2)), (int(x3), int(x4))))

    return sections

def is_fully_contained_pair(range1, range2):
    x1, x2 = range1
    x3, x4 = range2
    return (x1 <= x3 and x4 <= x2) or (x3 <= x1 and x2 <= x4)

def is_overlapping_pair(range1, range2):
    x1, x2 = range1
    x3, x4 = range2
    return (x1 <= x3 and x3 <= x2) \
        or (x1 <= x4 and x4 <= x2) \
        or (x3 <= x1 and x1 <= x4) \
        or (x3 <= x2 and x2 <= x4)

def main():
    section_pairs = get_section_pairs('input.txt')

    print('Part 1')
    fully_contained_pairs = sum([
        is_fully_contained_pair(range1, range2)
        for range1, range2 in section_pairs
    ])
    print(f'Fully contained pairs: {fully_contained_pairs}')

    print('Part 2')
    overlapping_pairs = sum([
        is_overlapping_pair(range1, range2)
        for range1, range2 in section_pairs
    ])
    print(f'Overlapping pairs: {overlapping_pairs}')

if __name__=='__main__':
    main()
