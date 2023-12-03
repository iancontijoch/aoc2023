from __future__ import annotations

import argparse
import math
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    ret = 0
    coords = {}
    digits, gears = {}, {}
    seen = set()
    num, nums = [], []
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            coords[(x, y)] = c
            if c == '*':
                gears[(x, y)] = c
            if c.isnumeric():
                digits[(x, y)] = c

    for (x, y) in digits:
        while (x, y) in digits:
            if (x, y) not in seen:
                num.append((x, y))  # add continuous digits to a num
                seen.add((x, y))
            x += 1
        if num:
            nums.append(num)
        num = []

    for g in gears:
        parts = set()
        for x, y in support.adjacent_8(*g):
            neighbor_digits = [n for n in nums if (x, y) in n]
            if neighbor_digits:
                neighbor_num = int(
                    ''.join([
                        coords[c]
                        for n in nums for c in n if (x, y) in n
                    ]),
                )
                parts.add(neighbor_num)
        if len(parts) == 2:
            ret += math.prod(parts)

    return ret


INPUT_S = '''\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
'''
EXPECTED = 467835


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
