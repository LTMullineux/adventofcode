import re
from operator import add, mul
from collections import deque
from copy import deepcopy
from math import lcm

OPS = {'+': add, '*': mul}

monkey_pattern = r'''Monkey (?P<monkey_idx>\d+):
  Starting items: (?P<items>.+)
  Operation: new = (?P<op>.+)
  Test: divisible by (?P<divisor>\d+)
    If true: throw to monkey (?P<true_idx>\d+)
    If false: throw to monkey (?P<false_idx>\d+)'''

def read_notes(filename):
    with open(filename) as f:
        notes = re.finditer(monkey_pattern, f.read())

    notes = [monkey.groupdict() for monkey in notes]
    monkeys = {}
    for monkey in notes:
        match monkey['op'].split():
            case ('old', op, 'old'):
                operation = lambda x, op=OPS[op]: op(x, x)
            case ('old', op, v):
                operation = lambda x, op=OPS[op], v=v: op(x, int(v))

        monkeys[int(monkey['monkey_idx'])] = {
            'items': [int(item) for item in monkey['items'].split(', ')],
            'op': operation,
            'divisor': int(monkey['divisor']),
            'true_idx': int(monkey['true_idx']),
            'false_idx': int(monkey['false_idx']),
        }

    return monkeys

def play_rounds(monkeys, relief_factor, rounds):
    state = {i: {'items': deque(monkeys[i]['items']), 'inspected': 0} for i in monkeys}
    lcm_divisors = lcm(*[monkeys[i]['divisor'] for i in monkeys])

    for r in range(rounds):
        for i in state.keys():
            for _ in range(len(state[i]['items'])):

                item = state[i]['items'].popleft()
                worry_level = monkeys[i]['op'](item) // relief_factor
                worry_level %= lcm_divisors

                if worry_level % monkeys[i]['divisor'] == 0:
                    next_monkey = monkeys[i]['true_idx']
                else:
                    next_monkey = monkeys[i]['false_idx']

                state[next_monkey]['items'].append(worry_level)
                state[i]['inspected'] += 1

    inspected = [v['inspected'] for v in state.values()]
    print(f'Inspected: {inspected}')

    inspected_sorted = sorted(inspected, reverse=True)
    return inspected_sorted[0] * inspected_sorted[1]

def main():
    monkeys = read_notes('input.txt')

    print('Part 1:')
    monkey_business = play_rounds(monkeys, 3, 20)
    print(f'Monkey business: {monkey_business}')

    print('Part 2:')
    monkey_business = play_rounds(monkeys, 1, 10_000)
    print(f'Monkey business: {monkey_business}')


if __name__ == '__main__':
    main()
