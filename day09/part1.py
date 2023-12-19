from __future__ import annotations

import argparse
import itertools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    ret = 0
    for line in lines:
        numbers = support.parse_numbers_split(line)
        seqs = [numbers]
        diff = numbers
        while True:
            diff = [(y - x) for x, y in itertools.pairwise(diff)]
            seqs.append(diff)
            if set(diff) == {0}:
                break
        ret += sum(s[-1] for s in seqs)
    return ret


INPUT_S = '''\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
'''
EXPECTED = 114


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
    # raise SystemExit(test(INPUT_S, EXPECTED))
