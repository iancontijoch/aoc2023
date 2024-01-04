from __future__ import annotations

import argparse
import math
import os.path

import pytest

import support
from support import Direction4

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

DIRS = {
    '2': Direction4.LEFT,
    '0': Direction4.RIGHT,
    '3': Direction4.UP,
    '1': Direction4.DOWN,
}


def area(vertices: list[tuple[int, int]]) -> int:
    nom = 0
    for (x1, y1), (x2, y2) in zip(vertices, vertices[1:]):
        nom += (x1 * y2) - (y1 * x2)
    return abs(nom // 2)


def distance(x1: int, y1: int, x2: int, y2: int) -> int:
    return int(math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2)))


def compute(s: str) -> int:
    lines = s.splitlines()
    pos = (0, 0)
    p = 0
    vertices = [pos]
    for line in lines:
        _, _, hx = line.split()
        hx = hx.replace('(', '').replace(')', '')
        n = int(hx[1:-1], 16)
        d_s = hx[-1]

        x, y = pos
        pos = DIRS[d_s].apply(x=x, y=y, n=int(n))

        p += distance(x, y, *pos)
        vertices.append(pos)

    return area(vertices) + p // 2 + 1


INPUT_S = '''\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
'''
EXPECTED = 952408144115


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
