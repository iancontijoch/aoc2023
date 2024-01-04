from __future__ import annotations

import argparse
import functools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


@functools.cache
def calc(record: str, groups: tuple[int]) -> int:

    if not groups:
        return 1 if '#' not in record else 0
    if not record:
        return 0

    next_char = record[0]
    next_group = groups[0]

    def dot() -> int:
        return calc(record[1:], groups)

    def pound() -> int:
        this_group = record[:next_group]
        this_group = this_group.replace('?', '#')

        if this_group != next_group * '#':
            return 0
        if len(record) == next_group:
            return 1 if len(groups) == 1 else 0
        if record[next_group] in '?.':
            return calc(record[next_group + 1:], groups[1:])
        return 0

    if next_char == '.':
        total = dot()
    elif next_char == '#':
        total = pound()
    elif next_char == '?':
        total = dot() + pound()
    else:
        raise RuntimeError
    return total


def compute(s: str) -> int:
    total = 0
    lines = s.splitlines()
    for line in lines:
        line, groups = line.split()
        gs = tuple(map(int, groups.split(',')))
        line = (line + '?') * 4 + line
        gs *= 5
        total += calc(line, gs)
    return total


INPUT_S = '''\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
'''
EXPECTED = 525152


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
