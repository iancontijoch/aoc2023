from __future__ import annotations

import argparse
import itertools
import math
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    instructions = lines[0].strip()
    graph = {}

    for line in lines[2:]:
        start_s, rem = line.split(' = ')
        m = re.compile(r'[A-Z1-9]{3}')
        graph[start_s] = m.findall(rem)

    zdict = {}
    current_nodes = tuple(node for node in graph if node.endswith('A'))
    for i, dir in enumerate(itertools.cycle(instructions)):
        zdict.update({
            node: i for node in current_nodes if node.endswith(
                'Z',
            ) and node not in zdict
        })
        if len(zdict) == len(current_nodes):
            break

        current_nodes = tuple(
            graph[node][0 if dir == 'L' else 1]
            for node in current_nodes
        )

    return math.lcm(*zdict.values())


INPUT_S = '''\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
'''
EXPECTED = 6


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
