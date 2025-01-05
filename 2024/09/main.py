from collections import namedtuple
from pathlib import Path

File = namedtuple("File", ["char", "size"])


def part_1(disk_map: str) -> int:
    disk: list[str | int] = []
    for i in range(len(disk_map)):
        char = i // 2 if i % 2 == 0 else "."
        disk.extend([char] * int(disk_map[i]))

    i = 0
    j = len(disk) - 1
    while i < j:
        if disk[i] != ".":
            i += 1
        if disk[j] == ".":
            j -= 1
        if disk[i] == "." and disk[j] != ".":
            disk[i], disk[j] = disk[j], disk[i]

    return sum(i * j if j != "." else 0 for i, j in enumerate(disk))


def find_free_space(disk: list[File], n: int, i: int) -> tuple[bool, int, int]:
    left_idx = -1  # k
    right_idx = -1  # j
    for j in range(n - 1, -1, -1):
        if disk[j].char == i:
            right_idx = j
            break

    if right_idx == -1:
        return False, left_idx, right_idx

    for k in range(j):
        if disk[k].char == "." and disk[k].size >= disk[j].size:
            left_idx = k
            return True, left_idx, right_idx

    return False, left_idx, right_idx


# NOTE: perform swap on original array
def handle_insert(disk: list[File], left_idx: int, right_idx: int) -> None:
    file_left = File(*disk[left_idx])
    file_right = File(*disk[right_idx])

    disk[left_idx] = disk[right_idx]
    disk[right_idx] = File(".", file_right.size)

    if file_right.size != file_left.size:
        new_pos = left_idx + 1
        size_diff = file_left.size - file_right.size
        disk.insert(new_pos, File(".", size_diff))


def part_2(disk_map: str) -> int:
    disk: list[File] = []
    n = len(disk_map)
    for i in range(n):
        char = i // 2 if i % 2 == 0 else "."
        disk.append(File(char, int(disk_map[i])))

    file_count = (n - 1) // 2
    for i in range(file_count, -1, -1):
        is_space, left_idx, right_idx = find_free_space(disk, n, i)
        if is_space:
            handle_insert(disk, left_idx, right_idx)

    checksum = 0
    idx = 0
    for file in disk:
        for _ in range(file.size):
            if file.char != ".":
                checksum += idx * int(file.char)

            idx += 1

    return checksum


def main(filename: Path) -> None:
    with open(filename, "r") as f:
        disk_map = f.read().strip()

    result = part_1(disk_map)
    print("part 1", result)

    result = part_2(disk_map)
    print("part 2", result)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-e", "--example", action="store_true")
    args = parser.parse_args()

    filename = Path("example-input.txt") if args.example else Path("input.txt")
    main(filename)
