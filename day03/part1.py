from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    ret = 0
    coords = {}
    digits, symbols = {}, {}
    seen = set()
    num, nums = [], []
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            coords[(x, y)] = c
            if not c.isnumeric() and c != '.':
                symbols[(x, y)] = c
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

    for num in nums:
        if any(
            ((x, y) in symbols)
            for n in num
            for x, y in support.adjacent_8(*n)
        ):
            ret += int(''.join([coords[(x, y)] for x, y in num]))

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
EXPECTED = 4361


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
