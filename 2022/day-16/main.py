from math import inf
from collections import defaultdict
from functools import cache
import re

VALVE_PATTERN = r'Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z]+[, [A-Z]+]*)'

def read_valve_report(filename):
    with open(filename) as f:
        return [
            (valve, int(flow_rate), set(tunnels.strip().split(', ')))
            for valve, flow_rate, tunnels in re.findall(VALVE_PATTERN, f.read())
        ]

def main():
    valves = read_valve_report('input.txt')

    # floyd-warshall
    # ... set up matrices
    flows = {valve: flow_rate for valve, flow_rate, _ in valves}
    vertices = []
    D = defaultdict(lambda: defaultdict(lambda: inf))

    for valve, flow_rate, tunnels in valves:
        D[valve][valve] = 0
        for next_tunnel in tunnels:
            D[valve][next_tunnel] = 1

        if flow_rate > 0:
            vertices.append(valve)

    for k in flows:
        for i in flows:
            for j in flows:
                D[i][j] = min(D[i][j], D[i][k] + D[k][j])

    # ... embed function for closure over D and flows
    def find_most_pressure(opened_valves, t_step):
        max_pressure, ignore_valves = 0, set(opened_valves)
        for v in filter(lambda v: v not in ignore_valves, vertices):
            t_left = t_step - (1 + D[opened_valves[-1]][v])
            if t_left >= 0:
                max_pressure = max(
                    max_pressure,
                    t_left * flows[v] + find_most_pressure((*opened_valves, v), t_left)
                )

        return max_pressure

    max_pressure = find_most_pressure(('AA',), 30)
    print(max_pressure)


if __name__ == '__main__':
    main()
