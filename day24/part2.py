from __future__ import annotations

import argparse
import os.path
from typing import NamedTuple

import pytest
from z3 import Int
from z3 import Ints
from z3 import sat
from z3 import simplify
from z3 import Solver

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Stone(NamedTuple):
    x: int
    y: int
    z: int
    vx: int
    vy: int
    vz: int


def compute(s: str) -> int:
    lines = s.splitlines()
    total = 0
    stones = []
    for line in lines:
        p_s, v_s = line.split(' @ ')
        p, v = map(int, p_s.split(', ')), map(int, v_s.split(', '))
        stones.append(Stone(*p, *v))

    sol = Solver()
    sx, sy, sz, svx, svy, svz = Ints('sx sy sz svx svy svz')

    for i, s1 in enumerate(stones):
        t = Int(f't_{i}')
        sol.add(s1.x + s1.vx * t == sx + svx * t)
        sol.add(s1.y + s1.vy * t == sy + svy * t)
        sol.add(s1.z + s1.vz * t == sz + svz * t)

    if sol.check() == sat:
        m = sol.model()
        total = simplify(m[sx] + m[sy] + m[sz])
    return total


INPUT_S = '''\
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
'''
EXPECTED = 47


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
