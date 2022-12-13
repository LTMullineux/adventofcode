from itertools import accumulate
from collections import defaultdict

def main():
    with open('input.txt', 'r') as f:
        terminal_output = [l.strip() for l in f.readlines()]

    dir_sizes = defaultdict(int)
    path_stack = []
    for line in terminal_output:
        if line.startswith('dir') or line.startswith('$ ls'):
            continue

        match line.split():
            case '$', 'cd', '..':
                path_stack.pop()
            case '$', 'cd', dir_name:
                path_stack.append(dir_name)
            case file_size, file_name:
                for file_path in accumulate(path_stack, lambda x, y: f'{x}/{y}'):
                    dir_sizes[file_path] += int(file_size)

    print('Part 1')
    part_1 = sum(s for s in dir_sizes.values() if s <= 100_000)
    print(f'Answer: {part_1}')

    print('Part 2')
    part_2 = min(s for s in dir_sizes.values() if s > (dir_sizes['/'] - 40_000_000))
    print(f'Answer: {part_2}')

if __name__ == '__main__':
    main()
