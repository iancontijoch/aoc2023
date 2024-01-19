from __future__ import annotations

import argparse
import os.path
from collections import deque

import pytest

import support
from support import Direction4

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
DIRS = {
    '^': Direction4.UP,
    '<': Direction4.LEFT,
    'v': Direction4.DOWN,
    '>': Direction4.RIGHT,
}


def compute(s: str) -> int:
    lines = s.splitlines()
    coords = {
        (x, y): c
        for y, line in enumerate(lines)
        for x, c in enumerate(line)
    }

    _, by = support.bounds(coords)

    paths = []
    start = next(
        (x, y) for (x, y) in coords
        if coords[(x, y)] == '.' and y == 0
    )
    end = next(
        (x, y) for (x, y) in coords
        if coords[(x, y)] == '.' and y == by.max
    )

    seen = {start}
    q = deque([(start, [start], seen)])
    while q:
        pos, path, seen = q.popleft()
        if pos == end:
            paths.append(path)
            continue
        neighbors = (
            support.adjacent_4(*pos)
            if coords[pos] == '.'
            else [DIRS.get(coords[pos], Direction4.UP).apply(*pos)]
        )
        for neighbor in (
            n for n in neighbors
            if n in coords and coords[n] != '#'
        ):
            if neighbor not in seen:
                seen.add(neighbor)
                q.append((neighbor, path + [neighbor], seen.copy()))

    return max(len(p) - 1 for p in paths)


INPUT_S = '''\
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
'''
EXPECTED = 94


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
    # test(INPUT_S, EXPECTED)
