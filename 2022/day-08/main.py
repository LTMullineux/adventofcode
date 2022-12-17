from math import prod

def read_trees(filename):
    trees = []
    with open(filename) as f:
        for line in f:
            trees.append(list(map(int, list(line.strip()))))

    return trees

def main():
    trees = read_trees('input.txt')
    trees_T = [*zip(*trees)]

    visible_trees, scenic_score = 0, 0
    for i in range(0, len(trees)):
        row = trees[i]
        for j in range(0, len(trees[0])):

            if (i == 0) or (i == len(trees) - 1) or (j == 0) or (j == len(trees[0]) - 1):
                visible_trees += 1
                continue

            col = trees_T[j]
            tree_height = trees[i][j]

            # views up, left, right, down
            views = (
                col[i - 1::-1],
                row[j - 1::-1],
                row[j + 1:],
                col[i + 1:],
            )

            not_visible = all(any(tree >= tree_height for tree in view) for view in views)
            visible_trees += int(not not_visible)
            scenic_score = max(scenic_score, prod(
                next((v + 1 for v, tree in enumerate(view) if tree >= tree_height), len(view))
                for view in views
            ))

    print('Part 1:')
    print(f'Number of visible trees: {visible_trees}')

    print('Part 2:')
    print(f'Best scenic score: {scenic_score}')


if __name__ == '__main__':
    main()
