from itertools import compress

def main():
    with open('input.txt') as f:
        raw_lanterns = f.read().splitlines()

    modulus = 7
    lanterns = list(map(int, raw_lanterns[0].split(',')))
    lanterns = [(l, modulus) for l in lanterns]
    # print(f'Initial state: {tuple(map(lambda x: x[0], lanterns))}')

    days = 80
    new_borns = []
    for day in range(1, days + 1):
        lanterns = [((l - 1) % m, max(m-1, modulus)) for l,m in lanterns]
        lanterns += new_borns

        pregnant_lanterns = map(lambda x: x[0] == 0, lanterns)
        n_new_lanterns = sum(pregnant_lanterns)
        new_borns = [(8, modulus + 2)] * n_new_lanterns

        # print(f'Day {day}: {tuple(map(lambda x: x[0], lanterns))}')

    print(f'Final population: {len(lanterns)}')

if __name__ == '__main__':
    main()