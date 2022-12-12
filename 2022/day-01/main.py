def read_inventory(filename):
    inventory = []
    elf_inventory = []
    with open(filename, 'r') as f:
        for line in f:
            item = line.strip()
            if item == '':
                inventory.append(elf_inventory)
                elf_inventory = []
            else:
                elf_inventory.append(int(item))

    if elf_inventory:
        inventory.append(elf_inventory)

    return inventory

def get_most_calorific_elves(inventory, top_n=1):
    total_calories = [sum(i) for i in inventory]
    return sorted(
        ((e, c) for e, c in enumerate(total_calories, 1)),
        key=lambda x: x[1],
        reverse=True
    )[:top_n]

def main():
    inventory = read_inventory('input.txt')

    print('Part 1')
    calorific_elf, max_calories_value = get_most_calorific_elves(inventory, top_n=1)[0]
    print(f'Elf', calorific_elf + 1, ', with a total of ', max_calories_value, ' calories')

    print('Part 2')
    top_3_calorific_elves = get_most_calorific_elves(inventory, top_n=3)
    top_3_total_calories = sum([c for _, c in top_3_calorific_elves])
    print('Top 3 total Calories: ', top_3_total_calories)
    for elf, calories in top_3_calorific_elves:
        print(f'Elf', elf + 1, ', with a total of ', calories, ' calories')

if __name__ == '__main__':
    main()
