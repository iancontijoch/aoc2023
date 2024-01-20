from __future__ import annotations

import argparse
import itertools
import operator
import os.path
from typing import NamedTuple

import numpy as np
import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
LO, HI = 200000000000000, 400000000000000


class Stone(NamedTuple):
    x: int
    y: int
    z: int
    vx: int
    vy: int
    vz: int


def in_past(a: Stone, b: Stone, sol: np.array) -> bool:
    a_x_comp = operator.gt if a.vx < 0 else operator.le
    b_x_comp = operator.gt if b.vx < 0 else operator.le

    a_y_comp = operator.gt if a.vy < 0 else operator.le
    b_y_comp = operator.gt if b.vy < 0 else operator.le

    ax = a_x_comp(sol[0], a.x)
    bx = b_x_comp(sol[0], b.x)
    ay = a_y_comp(sol[1], a.y)
    by = b_y_comp(sol[1], b.y)

    return (ax or ay) or (bx or by)


def compute(s: str, lo: int = LO, hi: int = HI) -> int:
    lines = s.splitlines()
    total = 0
    stones = []
    for line in lines:
        p_s, v_s = line.split(' @ ')
        p, v = map(int, p_s.split(', ')), map(int, v_s.split(', '))
        stones.append(Stone(*p, *v))

    for a, b in itertools.combinations(stones, 2):
        m_a, m_b = (a.vy / a.vx), (b.vy / b.vx)
        M = np.array([[-m_a, 1], [-m_b, 1]])
        C_a = a.y - (m_a * a.x)
        C_b = b.y - (m_b * b.x)
        C = np.array([C_a, C_b])

        if m_a == m_b:
            continue
        else:
            sol = np.linalg.solve(M, C)
            if in_past(a, b, sol):
                continue
            if lo <= sol[0] <= hi and lo <= sol[1] <= hi:
                total += 1
    return total


INPUT_S = '''\
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
'''
EXPECTED = 2


@pytest.mark.parametrize(
    ('input_s', 'lo', 'hi', 'expected'),
    (
        (INPUT_S, 7, 27, EXPECTED),
    ),
)
def test(input_s: str, lo: int, hi: int, expected: int) -> None:
    assert compute(input_s, lo, hi) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
