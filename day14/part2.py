from __future__ import annotations

import argparse
import os.path

import pytest

import support
from support import Direction4

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
CYCLES = 1_000_000_000


def move(
    coords: dict[tuple[int, int], str], start: tuple[int, int],
    dir: Direction4,
) -> tuple[int, int]:
    end = start
    nxt = dir.apply(*start)
    while nxt in coords and coords[nxt] == '.':
        end = nxt
        nxt = dir.apply(*nxt)
    return end


def cycle(
    coords: dict[tuple[int, int], str],
    bx: support.Bound, by: support.Bound,
) -> dict[tuple[int, int], str]:

    dirs = (
        Direction4.UP,
        Direction4.LEFT,
        Direction4.DOWN,
        Direction4.RIGHT,
    )
    for d in dirs:
        if d in (Direction4.UP, Direction4.LEFT):
            for x in bx.range:
                for y in by.range:
                    if coords[(x, y)] == 'O':
                        end = move(coords, (x, y), d)
                        coords[(x, y)] = '.'
                        coords[end] = 'O'
        else:
            for x in reversed(bx.range):
                for y in reversed(by.range):
                    if coords[(x, y)] == 'O':
                        end = move(coords, (x, y), d)
                        coords[(x, y)] = '.'
                        coords[end] = 'O'
    return coords


def compute(s: str) -> int:
    lines = s.splitlines()
    coords = {
        (x, y): c
        for y, line in enumerate(lines)
        for x, c in enumerate(line)
    }
    states = set()
    cy_states: dict[frozenset[tuple[tuple[int, int], str]], int] = {}
    loads = []
    cy_start = cy_end = -1
    bx, by = support.bounds(coords)

    for i in range(CYCLES):
        state = frozenset(coords.items())
        rows = tuple(
            ''.join(
                coords[(x, y)]
                for x in bx.range
            )
            for y in by.range
        )
        loads.append(
            sum(
                (i + 1) * r.count('O')
                for i, r in enumerate(reversed(rows))
            ),
        )
        if state in states:
            cy_start = cy_states[state]
            cy_end = i
            break
        else:
            cy_states[state] = i
            states.add(state)
        coords = cycle(coords, bx, by)

    return loads[cy_start:][(CYCLES - cy_start) % (cy_end - cy_start)]


INPUT_S = '''\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
'''
EXPECTED = 64


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
