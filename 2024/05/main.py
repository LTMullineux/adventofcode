import itertools as it
from collections import defaultdict, deque
from pathlib import Path
from typing import Generator


def parse_rules(filename: Path) -> dict[int, str]:
    with open(filename, "r") as f:
        raw = f.read().strip()

    raw_rules, raw_updates = raw.split("\n\n")

    rules = defaultdict(set)
    for rule in raw_rules.split("\n"):
        x, y = rule.strip().split("|")
        rules[x].add(y)

    updates = [p.split(",") for p in raw_updates.split("\n")]
    return rules, updates


def iter_pages(pages: list[str]) -> Generator[tuple[set[str], str], None, None]:
    for i in range(2, len(pages) + 1):
        yield set(pages[: i - 1]), pages[i - 1]


def get_topological_order(
    pages: list[str], page_orders: list[tuple[str, str]]
) -> list[str] | None:
    page_orders_filtered = [p for p in page_orders if p[0] in pages and p[1] in pages]
    graph = defaultdict(list)
    in_degree = defaultdict(int)

    for x, y in page_orders_filtered:
        graph[x].append(y)
        in_degree[y] += 1

    queue = deque([p for p in pages if in_degree[p] == 0])
    sorted_order = []
    while queue:
        current = queue.popleft()
        sorted_order.append(current)

        for neighbour in graph[current]:
            in_degree[neighbour] -= 1
            if in_degree[neighbour] == 0:
                queue.append(neighbour)

    # cannot sort because of cycle
    if len(sorted_order) != len(pages):
        return None

    return sorted_order


def main(filename: Path) -> None:
    rules, updates = parse_rules(filename)

    valid_updates = []
    for pages in updates:
        is_valid = True
        for sub_pages, query_page in iter_pages(pages):
            bad_rules = rules.get(query_page, set())
            broken_rules = sub_pages & bad_rules
            if broken_rules:
                is_valid = False
                break

        valid_updates.append(is_valid)

    mid_pages = [int(s[len(s) // 2]) for s in it.compress(updates, valid_updates)]
    print("part 1", sum(mid_pages))

    # create rules from bad_rules
    page_orders = []
    for y, xs in rules.items():
        for x in xs:
            page_orders.append((y, x))

    reordered_pages = []
    for invalid_update in it.compress(updates, map(lambda x: not x, valid_updates)):
        order = get_topological_order(invalid_update, page_orders)
        if order is not None:
            reordered_pages.append(order)

    mid_pages = [int(s[len(s) // 2]) for s in reordered_pages]
    print("part 2", sum(mid_pages))


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-e", "--example", action="store_true")
    args = parser.parse_args()

    filename = Path("example-input.txt") if args.example else Path("input.txt")
    main(filename)
