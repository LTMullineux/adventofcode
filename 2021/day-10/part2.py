from collections import deque

OPPOSITES = { '(': ')', '[': ']', '{': '}', '<': '>'}
SCORES = { ')': 1, ']': 2, '}': 3, '>': 4}

def main():
    with open('input.txt') as f:
        data = f.read().splitlines()

    corrupted_line_chars = []
    openers = []
    for line in data:
        stack = deque()
        corrupted_chars = []

        for char in line:
            if char in OPPOSITES:
                stack.append(char)
            elif char != OPPOSITES[stack.pop()]:
                corrupted_chars.append(char)

        corrupted_line_chars.append(corrupted_chars)
        openers.append(stack)

    scores = []
    for corrupted_chars, opening_chars in zip(corrupted_line_chars, openers):
        if len(corrupted_chars) != 0:
            continue
        score = 0
        for char in list(opening_chars)[::-1]:
            score *= 5
            score += SCORES[OPPOSITES[char]]
        scores.append(score)

    print(sorted(scores)[len(scores) // 2])


if __name__ == '__main__':
    main()