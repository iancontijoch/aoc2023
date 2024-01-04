from __future__ import annotations

import argparse
import itertools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
EXPANSION_RATE = 2


def compute(s: str) -> int:
    coords = {
        (x, y): c
        for y, line in enumerate(s.splitlines())
        for x, c in enumerate(line)
    }
    galaxies = {coord for coord in coords if coords[coord] == '#'}
    bx, by = support.bounds(coords)

    space_rows = [
        y for y in by.range
        if all(coords[(x, y)] == '.' for x in bx.range)
    ]

    space_cols = [
        x for x in bx.range
        if all(coords[(x, y)] == '.' for y in by.range)
    ]

    expanded_galaxies = set()

    for x, y in galaxies:
        x_offset = len([c for c in space_cols if c < x]) * (EXPANSION_RATE - 1)
        y_offset = len([r for r in space_rows if r < y]) * (EXPANSION_RATE - 1)
        expanded_galaxies.add((x + x_offset, y + y_offset))

    total = 0
    for start, end in itertools.combinations(expanded_galaxies, 2):
        x1, y1 = start
        x2, y2 = end
        total += (abs(y2 - y1) + abs(x2 - x1))

    return total


INPUT_S = '''\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
'''
EXPECTED = 374


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
