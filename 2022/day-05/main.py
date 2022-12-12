from collections import deque

def get_chunks(seq, size):
    for i in range(0, len(seq), size):
        yield seq[i:i + size]

def parse_creates_and_steps(filename):
    crate_positions = []
    rules = []
    with open(filename, 'r') as f:
        for line in f:
            # if breaker line or index line, next
            if line == '' or line[:2] == ' 1':
                continue

            # if line is a crate position, add to crate_positions
            if '[' in line:
                for stack_idx, crate_str in enumerate(get_chunks(line, 4), 1):
                    crate_str = crate_str.strip()
                    if not crate_str:
                        continue

                    crate_name = crate_str[1]
                    crate_positions.append((crate_name, stack_idx))
                    continue

            # if line is a rule, add to rules
            if line[:4] == 'move':
                _, count, _, source, _, target = line.strip().split(' ')
                rules.append((int(count), int(source), int(target)))

    stacks = {}
    for crate_name, stack_idx in crate_positions:
        if stack_idx not in stacks:
            stacks[stack_idx] = deque()
        stacks[stack_idx].appendleft(crate_name)  # appending top down

    stacks = {k:v for k,v in sorted(stacks.items(), key=lambda i: i[0])}
    return stacks, rules

def rearrange_CrateMover9000(stacks, rules):
    for rule in rules:
        count, source, target = rule
        if source == target:
            continue

        for _ in range(count):
            crate = stacks[source].pop()
            stacks[target].append(crate)

def rearrange_CrateMover9001(stacks, rules):
    for rule in rules:
        count, source, target = rule
        if source == target:
            continue

        multi_crates = []
        for _ in range(count):
            crate = stacks[source].pop()
            multi_crates.append(crate)
        for crate in multi_crates[::-1]:
            stacks[target].append(crate)

def main():
    print('Part 1')
    stacks, rules = parse_creates_and_steps('input.txt')
    rearrange_CrateMover9000(stacks, rules)
    top_crates = ''.join([s.pop() for s in stacks.values()])
    print(f'top_crates: {top_crates}')

    print('Part 2')
    stacks, rules = parse_creates_and_steps('input.txt')
    rearrange_CrateMover9001(stacks, rules)
    top_crates = ''.join([s.pop() for s in stacks.values()])
    print(f'top_crates: {top_crates}')

if __name__ == '__main__':
    main()
