import json

def get_blank_population():
    return dict(
        old=dict(zip(range(0, 7), [0] * 8)),
        new=dict(zip(range(7, 9), [0] * 2))
    )

def pretty_print(population):
    p = dict(zip(range(0, 9), [0] * 9))
    for k,v in population['old'].items():
        p[k] += v
    for k,v in population['new'].items():
        p[k] += v
    print(json.dumps(p, indent=4))

def main():
    with open('input.txt') as f:
        raw_lanterns = f.read().splitlines()

    lanterns = get_blank_population()
    for l in raw_lanterns[0].split(','):
        lanterns['old'][int(l)] += 1

    modulus = 7
    days = 256
    for day in range(1, days + 1):

        # print('-' * 100)
        next_lanterns = get_blank_population()

        # old population
        for age in range(0, modulus):
            next_lanterns['old'][age] = lanterns['old'][(age + 1) % modulus]

        # new population
        next_lanterns['new'][8] = next_lanterns['old'][6]
        next_lanterns['new'][7] = lanterns['new'][8]

        next_lanterns['old'][6] += lanterns['new'][7]

        lanterns = next_lanterns
        lantern_count = sum(lanterns['old'].values()) + sum(lanterns['new'].values())
        print(f'day {day} -> {lantern_count}')
        # pretty_print(lanterns)


if __name__ == '__main__':
    main()