from collections import deque

OPPOSITES = { '(': ')', '[': ']', '{': '}', '<': '>', }
SCORES = { ')': 3, ']': 57, '}': 1197, '>': 25137, }

def main():
    with open('input.txt') as f:
        data = f.read().splitlines()

    corrupted_line_chars = []
    for line in data:
        stack = deque()
        corrupted_chars = []

        for char in line:
            if char in OPPOSITES:
                stack.append(char)
            elif char != OPPOSITES[stack.pop()]:
                corrupted_chars.append(char)

        corrupted_line_chars.append(corrupted_chars)

    score = 0
    for corrupted_chars in corrupted_line_chars:
        if len(corrupted_chars) == 0:
            continue
        score += SCORES[corrupted_chars[0]]

    print(score)

if __name__ == '__main__':
    main()