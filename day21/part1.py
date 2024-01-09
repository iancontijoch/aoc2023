from __future__ import annotations

import argparse
import collections
import os.path

import pytest

import support
from support import Direction4

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
DIRS = {Direction4.UP, Direction4.DOWN, Direction4.LEFT, Direction4.RIGHT}


def compute(s: str, remaining_steps: int = 64) -> int:
    lines = s.splitlines()
    coords = {
        (x, y): c
        for y, line in enumerate(lines)
        for x, c in enumerate(line)
    }
    start = next(pos for pos, c in coords.items() if c == 'S')
    ans, seen = set(), set()

    todo = collections.deque([(start, remaining_steps)])
    while todo:
        pos, i = todo.popleft()
        if i % 2 == 0:
            ans.add(pos)
        if i == 0:
            continue
        for d in DIRS:
            pos_d = d.apply(*pos)
            if (
                (pos_d) not in seen
                and pos_d in coords and coords[pos_d] != '#'
            ):
                seen.add(pos_d)
                todo.append((pos_d, i - 1))
    return len(ans)


INPUT_S = '''\
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
'''

REMAINING_STEPS_T = 6
EXPECTED = 16


@pytest.mark.parametrize(
    ('input_s', 'expected', 'remaining_steps'),
    (
        (INPUT_S, EXPECTED, REMAINING_STEPS_T),
    ),
)
def test(input_s: str, expected: int, remaining_steps: int) -> None:
    assert compute(input_s, remaining_steps) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
    # test(INPUT_S, EXPECTED)
