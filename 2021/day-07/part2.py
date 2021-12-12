def argmin(iterable):
    return min(enumerate(iterable), key=lambda x: x[1])[0]

def gauss_sum(n):
    return n * (n + 1) // 2

def main():
    with open('input.txt') as f:
        crabs = tuple(map(int, f.read().strip().split(',')))

    max_position = max(crabs)
    costs = [0] * (max_position + 1)

    for crab in crabs:
        for i in range(max_position + 1):
            distance = abs(crab - i)
            if distance == 0:
                continue
            costs[i] += gauss_sum(distance)

    min_cost_position = argmin(costs)
    min_cost = costs[min_cost_position]
    print(f'Position {min_cost_position}: {min_cost} fuel')


if __name__ == '__main__':
    main()