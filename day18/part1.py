from __future__ import annotations

import argparse
import os.path
from collections import deque

import pytest

import support
from support import Direction4

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

DIRS = {
    'L': Direction4.LEFT,
    'R': Direction4.RIGHT,
    'U': Direction4.UP,
    'D': Direction4.DOWN,
}


def bfs(
    pos: tuple[int, int],
    coords: dict[tuple[int, int], str],
    visited: set[tuple[int, int]] | None = None,
) -> set[tuple[int, int]]:
    if visited is None:
        visited = set()

    q = deque([pos])
    visited.add(pos)

    while q:
        pos = q.popleft()
        if pos not in coords:
            continue
        for adj in support.adjacent_4(*pos):
            if adj not in visited:
                visited.add(adj)
                q.append(adj)
    return visited


def compute(s: str) -> int:
    lines = s.splitlines()
    pos = (0, 0)
    seen = set()
    for line in lines:
        d_s, n, _ = line.split()
        for _ in range(int(n)):
            pos = DIRS[d_s].apply(*pos)
            seen.add(pos)

    min_x = min(k[0] for k in seen)
    max_x = max(k[0] for k in seen)
    min_y = min(k[1] for k in seen)
    max_y = max(k[1] for k in seen)

    seen = {
        (x + abs(min_x), y + abs(min_y))
        for x, y in seen
    }

    coords = {
        (x, y): '#' if (x, y) in seen else '.'
        for y in range(abs(min_y) + abs(max_y) + 1)
        for x in range(abs(min_x) + abs(max_x) + 1)
    }

    for space in (pos for pos in coords if coords[pos] == '.'):
        f = bfs(space, coords, seen.copy())
        break
    return len(f)


INPUT_S = '''\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
'''
EXPECTED = 62


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
