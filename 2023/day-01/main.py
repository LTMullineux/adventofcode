INTS = set(map(str, range(10)))
NUMBERS = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]


def first_digit(line: list[str], reverse=False) -> str | None:
    line_length = len(line)
    window_line = line if not reverse else line[::-1]
    for i in range(len(window_line)):
        int_candidate = window_line[i]
        if int_candidate in INTS:
            return int_candidate

        for j, number in enumerate(NUMBERS):
            number_length = len(number)
            if i + number_length > line_length:
                continue

            candidate_str = "".join(window_line[i : i + number_length])
            if reverse:
                candidate_str = candidate_str[::-1]

            if candidate_str == number:
                return str(j)

    return None


def main(filename: str) -> None:
    with open(filename, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    digits = []
    for line in lines:
        tens = first_digit(line)
        ones = first_digit(line, reverse=True)
        if tens is not None and ones is not None:
            digits.append(int(tens + ones))

    print(sum(digits))


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-e", "--example", action="store_true")
    args = parser.parse_args()

    filename = "example-input.txt" if args.example else "input.txt"
    main(filename)
