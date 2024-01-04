from __future__ import annotations

import argparse
import os.path

import pytest

import support
from support import Direction4

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def move(
    coords: dict[tuple[int, int], str],
    by: support.Bound, start: tuple[int, int],
) -> tuple[int, int]:
    end = start
    nxt = Direction4.UP.apply(*start)
    while nxt[1] in by.range and coords[nxt] == '.':
        end = nxt
        nxt = Direction4.UP.apply(*nxt)
    return end


def compute(s: str) -> int:
    lines = s.splitlines()
    coords = {
        (x, y): c
        for y, line in enumerate(lines)
        for x, c in enumerate(line)
    }
    bx, by = support.bounds(coords)
    for x in bx.range:
        for y in by.range:
            if coords[(x, y)] == 'O':
                end = move(coords, by, (x, y))
                coords[(x, y)] = '.'
                coords[end] = 'O'
    rows = tuple(
        ''.join(
            coords[(x, y)]
            for x in bx.range
        )
        for y in by.range
    )

    return sum(
        (i + 1) * r.count('O')
        for i, r in enumerate(reversed(rows))
    )


INPUT_S = '''\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
'''
EXPECTED = 136


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
