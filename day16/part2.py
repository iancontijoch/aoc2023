from __future__ import annotations

import argparse
import os.path

import pytest

import support
from support import Direction4

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def move(
    d: Direction4, x: int, y: int,
    coords: dict[tuple[int, int], str],
    visited: set[tuple[Direction4, int, int]] | None = None,
) -> set[tuple[Direction4, int, int]]:

    if visited is None:
        visited = set()

    x, y = d.apply(x, y)
    if (x, y) not in coords or (d, x, y) in visited:
        return visited
    c = coords[(x, y)]
    visited.add((d, x, y))
    if c == '.':
        visited = move(d, x, y, coords, visited)
    elif c == '|':
        if d in (Direction4.DOWN, Direction4.UP):
            visited = move(d, x, y, coords, visited)
        else:
            visited = move(Direction4.UP, x, y, coords, visited)
            visited = move(Direction4.DOWN, x, y, coords, visited)
    elif c == '-':
        if d in (Direction4.LEFT, Direction4.RIGHT):
            visited = move(d, x, y, coords, visited)
        else:
            visited = move(Direction4.LEFT, x, y, coords, visited)
            visited = move(Direction4.RIGHT, x, y, coords, visited)
    elif c == '\\':
        if d is Direction4.UP:
            visited = move(Direction4.LEFT, x, y, coords, visited)
        elif d is Direction4.RIGHT:
            visited = move(Direction4.DOWN, x, y, coords, visited)
        elif d is Direction4.LEFT:
            visited = move(Direction4.UP, x, y, coords, visited)
        elif d is Direction4.DOWN:
            visited = move(Direction4.RIGHT, x, y, coords, visited)
        else:
            raise NotImplementedError
    elif c == '/':
        if d is Direction4.UP:
            visited = move(Direction4.RIGHT, x, y, coords, visited)
        elif d is Direction4.RIGHT:
            visited = move(Direction4.UP, x, y, coords, visited)
        elif d is Direction4.LEFT:
            visited = move(Direction4.DOWN, x, y, coords, visited)
        elif d is Direction4.DOWN:
            visited = move(Direction4.LEFT, x, y, coords, visited)
        else:
            raise NotImplementedError
    else:
        raise RuntimeError
    return visited


def compute(s: str) -> int:
    lines = s.splitlines()
    lines = lines[1:] if not lines[0] else lines
    coords = {
        (x, y): c
        for y, line in enumerate(lines)
        for x, c in enumerate(line)
    }
    bx, by = support.bounds(coords)

    top = [(Direction4.DOWN, x, y) for x, y in coords if y == by.min]
    left = [(Direction4.RIGHT, x, y) for x, y in coords if x == bx.min]
    bottom = [(Direction4.UP, x, y) for x, y in coords if y == by.max]
    right = [(Direction4.LEFT, x, y) for x, y in coords if x == bx.max]

    all_ds = top + left + bottom + right

    all_maxs = [
        (
            (x, y), len(
                {
                    (mx, my)
                    for _, mx, my in move(d, x, y, coords)
                },
            ),
        )
        for d, x, y in all_ds
    ]

    return max(all_maxs, key=lambda x: x[1])[1]


INPUT_S = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""
EXPECTED = 51


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
