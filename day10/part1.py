from __future__ import annotations

import argparse
import os.path
from collections import deque

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def connected_pipes(
    x: int, y: int, coords: dict[tuple[int, int], str],
) -> tuple[tuple[int, int], tuple[int, int]]:

    c = coords[(x, y)]
    if c == '|':
        return ((x, y - 1), (x, y + 1))
    elif c == '-':
        return ((x - 1, y), (x + 1, y))
    elif c == 'L':
        return ((x, y - 1), (x + 1, y))
    elif c == 'J':
        return ((x - 1, y), (x, y - 1))
    elif c == '7':
        return ((x - 1, y), (x, y + 1))
    elif c == 'F':
        return ((x + 1, y), (x, y + 1))
    elif c == '.':
        return ((x, y), (x, y))
    else:
        raise NotImplementedError(f'Coord {(x, y)} {c} not understood.')


def in_bounds(x: int, y: int, bx: support.Bound, by: support.Bound) -> bool:
    return x in bx.range and y in by.range


def infer_s(x: int, y: int, coords: dict[tuple[int, int], str]) -> str:
    north, east, south, west = (p for p in support.adjacent_4(x, y))
    bounds = support.bounds(coords)

    has_south = in_bounds(*south, *bounds) and (
        x,
        y,
    ) in connected_pipes(*south, coords)
    has_east = in_bounds(*east, *bounds) and (
        x,
        y,
    ) in connected_pipes(*east, coords)
    has_north = in_bounds(*north, *bounds) and (
        x,
        y,
    ) in connected_pipes(*north, coords)
    has_west = in_bounds(*west, *bounds) and (
        x,
        y,
    ) in connected_pipes(*west, coords)

    if has_south and has_north:
        return '|'
    elif has_south and has_east:
        return 'F'
    elif has_south and has_west:
        return '7'
    elif has_north and has_west:
        return 'J'
    elif has_north and has_east:
        return 'L'
    elif has_west and has_east:
        return '-'
    else:
        raise NotImplementedError('could not infer S')


def parse_coords(s: str) -> dict[tuple[int, int], str]:
    coords = {}
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            coords[(x, y)] = c
    return coords


def format_coords_hash(coords: dict[tuple[int, int], str]) -> str:
    min_x = min(x for x, _ in coords)
    max_x = max(x for x, _ in coords)
    min_y = min(y for _, y in coords)
    max_y = max(y for _, y in coords)
    return '\n'.join(
        ''.join(
            coords[(x, y)] if (x, y) in coords else ' '
            for x in range(min_x, max_x + 1)
        )
        for y in range(min_y, max_y + 1)
    )


def print_coords(coords: dict[tuple[int, int], str]) -> None:
    print(format_coords_hash(coords))


def bfs(
    coords: dict[tuple[int, int], str], start: tuple[int, int],
) -> int:
    visited = set()
    queue = deque([(start, 0)])
    distances = {}

    while queue:
        node, distance = queue.popleft()
        if node not in visited:
            visited.add(node)
            distances[node] = distance

            for adj in connected_pipes(*node, coords):
                if adj not in visited:
                    queue.append((adj, distance + 1))

    return max(distances.values())


def compute(s: str) -> int:
    coords = parse_coords(s)
    print_coords(coords)

    s_coords = next(x for x, y in coords.items() if coords.get(x, y) == 'S')
    coords[s_coords] = infer_s(*s_coords, coords)

    return bfs(coords, s_coords)


INPUT_S = '''\
.....
.S-7.
.|.|.
.L-J.
.....
'''
EXPECTED = 4


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
