from __future__ import annotations

import argparse
import math
import os.path
from collections import namedtuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


Race = namedtuple('Race', ('time', 'record_dist'))


def compute(s: str) -> int:
    lines = s.splitlines()
    times = (int(lines[0].split(':')[1].replace(' ', '')),)
    distances = (int(lines[1].split(':')[1].replace(' ', '')),)

    races = tuple(Race(*x) for x in zip(times, distances))
    ways = {r: 0 for r in races}

    for race in races:
        # only need to check up to half
        for hold_time in range((race.time // 2) + 1):
            if (race.time - hold_time) * hold_time > race.record_dist:
                ways[race] += 2  # symmetrical
        if race.time % 2 == 0:  # fix double count
            ways[race] -= 1
    return math.prod(ways.values())


INPUT_S = '''\
Time:      7  15   30
Distance:  9  40  200
'''
EXPECTED = 71503


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
