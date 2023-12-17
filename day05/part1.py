from __future__ import annotations

import argparse
import itertools
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
CATEGORIES = (
    'seed', 'soil', 'fertilizer',
    'water', 'light', 'temperature',
    'humidity', 'location',
)


def get_location(
    src_num: int,
    src: str,
    maps: dict[tuple[str, str], list[tuple[range, range]]],
) -> int:
    if src == 'location':
        return src_num
    else:
        dest = [v for k, v in maps if k == src][0]
        try:
            from_rng, to_rng = [
                (from_rng, to_rng)
                for from_rng, to_rng in maps[(src, dest)]
                if src_num in from_rng
            ][0]
            # find distance between src_num and rng start
            next_src_num = to_rng.start + (src_num - from_rng.start)
        except IndexError:
            next_src_num = src_num
        return get_location(next_src_num, dest, maps)


def compute(s: str) -> int:

    seeds_match = re.search(r'seeds: (.+)', s)
    assert seeds_match is not None
    seeds = tuple(
        int(x)
        for x in seeds_match.group(1).split()
    )
    maps: dict[tuple[str, str], list[tuple[range, range]]] = {}

    for source, destination in itertools.pairwise(CATEGORIES):
        maps[(source, destination)] = []
        rng_s_match = re.search(
            rf'{source}-to-{destination} map:([\s\d]+)', s,
        )
        assert rng_s_match is not None
        rng_s = rng_s_match.group(1).strip().split('\n')
        rng_lst = tuple(tuple(map(int, r.split())) for r in rng_s)

        for r in rng_lst:
            dest_rng_start, src_rng_start, rng_len = r
            dest_rng = range(dest_rng_start, dest_rng_start + rng_len)
            src_rng = range(src_rng_start, src_rng_start + rng_len)
            maps[(source, destination)].append((src_rng, dest_rng))

    return min(get_location(s, 'seed', maps) for s in seeds)


INPUT_S = '''\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
'''
EXPECTED = 35


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
