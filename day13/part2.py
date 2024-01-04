from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def reflection_row(block: list[str], distance_to_match: int) -> int:
    for idx in range(len(block)):
        if idx == 0:
            continue
        if (
            sum(
                distance(left, right)
                for left, right in zip(reversed(block[:idx]), block[idx:])
            )
                == distance_to_match
        ):
            return idx
    return 0


def distance(left: str, right: str) -> int:
    return sum(a != b for a, b in zip(left, right))


def score_block(rows: list[str], distance_to_match: int) -> int:
    if row := reflection_row(rows, distance_to_match):
        return 100 * row
    if col := reflection_row(
        [''.join(x) for x in list(zip(*rows))],
        distance_to_match,
    ):
        return col
    return 0


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
        rows = list(
            ''.join(coords[(x, y)] for x in bx.range)
            for y in by.range
        )
        total += score_block(rows, 1)

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
EXPECTED = 400


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
