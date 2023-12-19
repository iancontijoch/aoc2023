from __future__ import annotations

import argparse
import itertools
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    graph = {}
    lines = s.splitlines()
    instructions = itertools.cycle(lines[0].strip())
    for line in lines[2:]:
        start_s, rem = line.split(' = ')
        m = re.compile(r'[A-Z]{3}')
        graph[start_s] = m.findall(rem)

    steps = 0
    current_node = 'AAA'
    for dir in instructions:
        steps += 1
        current_node = graph[current_node][0 if dir == 'L' else 1]
        if current_node == 'ZZZ':
            break

    return steps


INPUT_S = '''\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
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
