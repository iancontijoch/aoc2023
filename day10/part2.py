from __future__ import annotations

import argparse
import os.path
import sys
from collections import deque

import pytest

import support
from support import Direction4

sys.setrecursionlimit(15000)

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

FLAT_UP = ('7', '-', 'F')
FLAT_DOWN = ('L', '-', 'J')
FLAT_LEFT = ('L', 'F', '|')
FLAT_RIGHT = ('J', '7', '|')


def enhance(
    coords: dict[tuple[int, int], str],
) -> tuple[dict[tuple[int, int], str], dict[tuple[int, int], tuple[int, int]]]:
    enhanced_coords = {}
    enhanced_to_orig = {}
    for (x, y), tile in coords.items():
        # blow up each tile so each one has 8 tiles
        x2, y2 = 3 * x + 1, 3 * y + 1
        for adj in support.adjacent_8(x2, y2):
            enhanced_coords[adj] = '.'
            enhanced_to_orig[adj] = (x, y)

        enhanced_to_orig[(x2, y2)] = (x, y)

        if tile == '.':
            enhanced_coords[x2, y2] = '.'
            continue
        elif tile == 'L':
            pipe_dirs = (Direction4.UP, Direction4.RIGHT)
        elif tile == 'J':
            pipe_dirs = (Direction4.UP, Direction4.LEFT)
        elif tile == '7':
            pipe_dirs = (Direction4.LEFT, Direction4.DOWN)
        elif tile == '|':
            pipe_dirs = (Direction4.UP, Direction4.DOWN)
        elif tile == '-':
            pipe_dirs = (Direction4.LEFT, Direction4.RIGHT)
        elif tile == 'F':
            pipe_dirs = (Direction4.RIGHT, Direction4.DOWN)
        else:
            raise NotImplementedError(f'unxpected tile {tile}')

        # fill center tile and the pipe tiles
        enhanced_coords[x2, y2] = '#'
        enhanced_coords.update((p.apply(x2, y2), '#') for p in pipe_dirs)

    return enhanced_coords, enhanced_to_orig


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
) -> set[tuple[int, int]]:
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

    return visited


def dfs(
    coords: dict[tuple[int, int], str],
        node: tuple[int, int], bx: support.Bound, by: support.Bound,
        visited: set[tuple[int, int]] | None = None,
) -> bool:
    if visited is None:
        visited = set()

    if node[0] not in bx.range or node[1] not in by.range:
        return False

    # print(node, coords[node])
    visited.add(node)

    for neighbor in (
        n for n in support.adjacent_8(*node)
        if coords.get(n, '.') == '.'
    ):
        if coords[node] == '.' and neighbor not in visited:
            if not dfs(coords, neighbor, bx, by, visited):
                return False
    return True


def compute(s: str) -> int:
    coords = parse_coords(s)

    s_coords = next(x for x, y in coords.items() if coords.get(x, y) == 'S')
    coords[s_coords] = infer_s(*s_coords, coords)

    loop_coords = bfs(coords, s_coords)
    coords.update((c, '.') for c in set(coords) - set(loop_coords))

    enhanced_coords, enhanced_to_orig = enhance(coords=coords)
    bx, by = support.bounds(enhanced_coords)

    ground_coords = {k for k, v in enhanced_coords.items() if v == '.'}
    # bfs the enhanced graph
    gc = (g for g in ground_coords if coords[enhanced_to_orig[g]] == '.')
    ret = {
        enhanced_to_orig[g] for g in gc
        if dfs(enhanced_coords, g, bx, by)
    }
    for r in ret:
        coords[r] = 'I'

    print_coords(coords)

    return len(ret)


INPUT_S = '''\
..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........
'''
EXPECTED = 10


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
