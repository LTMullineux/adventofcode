def create_increase_list(l):
    return [int(l[i] > l[i-1]) for i in range(1, len(l))]

def main():
    with open('input.txt', 'r') as f:
        depths = [int(line) for line in f.readlines()]

    increase = create_increase_list(depths)
    print(sum(increase))


if __name__ == '__main__':
    main()