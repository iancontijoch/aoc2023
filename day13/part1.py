from __future__ import annotations

import argparse
import itertools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    total = 0
    patterns = s.split('\n\n')
    for p in patterns:
        coords = {
            (x, y): c
            for y, line in enumerate(p.splitlines())
            for x, c in enumerate(line)
        }
        bx, by = support.bounds(coords)
        cols = tuple(
            ''.join(
                coords[(x, y)]
                for y in by.range
            ) for x in bx.range
        )
        rows = tuple(
            ''.join(
                coords[(x, y)]
                for x in bx.range
            ) for y in by.range
        )
        v_lines, h_lines = [], []

        for i, pair in enumerate(itertools.pairwise(cols)):
            if pair[0] == pair[1]:
                v_reflection_span = len(bx.range) - i - 2
                left = cols[max(0, i - v_reflection_span):i]
                right = cols[i + 2: i + 2 + min(len(left), len(bx.range))]
                if left == right[::-1]:
                    v_lines.append(i)

        for i, pair in enumerate(itertools.pairwise(rows)):
            if pair[0] == pair[1]:
                h_reflection_span = len(by.range) - i - 2
                above = rows[max(0, i - h_reflection_span):i]
                below = rows[i + 2: i + 2 + min(len(above), len(by.range))]
                if above == below[::-1]:
                    h_lines.append(i)

        total += sum(v + 1 for v in v_lines) + \
            sum(h + 1 for h in h_lines) * 100
    return total


INPUT_S = '''\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
'''
EXPECTED = 405


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
