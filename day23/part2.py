from __future__ import annotations

import argparse
import os.path
from collections import defaultdict
from collections import deque

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    coords = {
        (x, y): c
        for y, line in enumerate(lines)
        for x, c in enumerate(line)
    }

    _, by = support.bounds(coords)

    start = next(
        (x, y) for (x, y) in coords
        if coords[(x, y)] == '.' and y == 0
    )
    end = next(
        (x, y) for (x, y) in coords
        if coords[(x, y)] == '.' and y == by.max
    )

    junctions = [start]

    # find all the junctions in the graph (more than 2 adjacent valid spaces)
    for pos in coords:
        if coords[pos] != '#':
            neighbors = [
                n for n in support.adjacent_4(
                    *pos,
                ) if n in coords and coords[n] != '#'
            ]
            if len(neighbors) > 2:
                junctions.append(pos)

    junctions.append(end)

    def bfs(
        start: tuple[int, int], end: tuple[int, int],
        coords: dict[tuple[int, int], str],
    ) -> list[int]:
        dists = []
        seen = {start}
        q = deque([(start, [start], seen)])
        while q:
            pos, path, seen = q.popleft()
            if pos in junctions and pos not in (start, end):
                continue
            if pos == end:
                dists.append(len(path))
                continue
            neighbors = [
                n for n in support.adjacent_4(
                    *pos,
                ) if n in coords and coords[n] != '#' and n not in seen
            ]
            for n in neighbors:
                seen.add(n)
                q.append((n, path + [n], seen.copy()))

        return dists

    trails = defaultdict(list)

    # apply bfs to junctions to get distances between them
    for j in junctions:
        for other in junctions:
            ret = bfs(j, other, coords)
            if ret and ret != [1]:
                trails[j].append((other, ret[0] - 1))

    def dfs(
        start: tuple[int, int], end: tuple[int, int],
        trails: dict[tuple[int, int], list[tuple[tuple[int, int], int]]],
    ) -> list[list[int]]:
        dists, paths = [], []
        seen = {start}
        todo = [(start, [0], [start], seen)]
        while todo:
            pos, dist, path, seen = todo.pop()
            if pos == end:
                paths.append(path)
                dists.append(dist)
                continue
            for n, d in trails[pos]:
                if n not in seen:
                    seen.add(pos)
                    todo.append((n, dist + [d], path + [n], seen.copy()))
        return dists

    # apply dfs to junctions to get the max path length
    dists = dfs(start, end, trails)
    return max([sum(d) for d in dists])


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
EXPECTED = 154


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
