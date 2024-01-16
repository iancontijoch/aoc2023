from __future__ import annotations

import argparse
import os.path
from typing import Iterator

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def chunks(lst: list[int], n: int) -> Iterator[list[int]]:
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def parse_line(s: str) -> tuple[tuple[int, ...], tuple[int, ...]]:
    s_s, e_s = s.split('~')
    start = tuple(map(int, s_s.split(',')))
    end = tuple(map(int, e_s.split(',')))
    return start, end


def overlap(s1: int, e1: int, s2: int, e2: int) -> bool:
    return e1 >= s2 and e2 >= s1


def fall(
    bricks: list[tuple[tuple[int, int], ...]],
) -> tuple[
    list[tuple[tuple[int, int], ...]],
    dict[int, list[int]],
]:
    ret: list[tuple[tuple[int, int], ...]] = []
    overlaps = {}
    for i, brick in enumerate(bricks):
        x, y, z = brick
        # above ground and doesn't overlap with any other pieces
        while z[0] > 0 and (
            not ret or
            not any(
                all(c)
                for c in chunks(
                    [
                        overlap(*a, *b)
                        for other in ret
                        for a, b in zip(brick, other)
                    ], 3,
                )
            )
        ):
            z = (z[0] - 1, z[1] - 1)
            brick = x, y, z
        overlaps[i] = [
            i for i, c in enumerate(
                chunks(
                    [
                        overlap(*a, *b)
                        for other in ret
                        for a, b in zip(brick, other)
                    ], 3,
                ),
            ) if all(c)
        ]
        ret.append((x, y, (z[0] + 1, z[1] + 1)))
    return ret, overlaps


def compute(s: str) -> int:

    bricks = []
    lines = s.splitlines()
    for line in lines:
        start, end = parse_line(line)
        bricks.append(tuple((a, b) for a, b in zip(start, end)))

    bricks = sorted(bricks, key=lambda x: x[2][0])  # sort by z-value
    bricks, overlaps = fall(bricks)

    # safe to disintegrate if not unique support for above or is at top
    n_at_top = len(
        [
            k for k in overlaps
            if k not in [
                item for v in overlaps.values()
                for item in v
            ]
        ],
    )

    # if A and B support C, but A is only support for D, A cannot be removed
    n_in_tower = len(
        {
            item for v in overlaps.values()
            for item in v
            if len(v) > 1 and [item] not in overlaps.values()
        },
    )

    return n_at_top + n_in_tower


INPUT_S = '''\
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
'''
EXPECTED = 5


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
    # raise SystemExit(main())
    test(INPUT_S, EXPECTED)
