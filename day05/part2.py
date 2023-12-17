from __future__ import annotations

import argparse
import os.path

import pytest
import re
import itertools
import math
from line_profiler import profile
from typing import Generator, NamedTuple
from collections import deque, defaultdict
from enum import Enum, auto
from functools import total_ordering

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

class Category(Enum):
    SEED = auto()
    SOIL = auto()
    FERTILIZER = auto()
    WATER = auto()
    LIGHT = auto()
    TEMPERATURE = auto()
    HUMIDITY = auto()
    LOCATION = auto()

def get_seed_num(loc_num: int, 
                 maps: dict[tuple[Category, Category], list[tuple[range, range]]]) -> int:
    """Get the destination number of a given source."""
    for dst, src in itertools.pairwise(reversed(Category)):
        dst_src_map = maps[(src, dst)]
        loc_num = backpropagate(loc_num, dst_src_map)  
        if loc_num < 0:
            break  
    return loc_num


def binary_search_ranges(src_num: int, rngs: list[range]):
    left, right = 0, len(rngs) - 1
    while left <= right:
        mid = left + (right - left) // 2
        src_rng = rngs[mid]

        if src_num in src_rng:
            return True
        elif src_num < src_rng.start:
            right = mid - 1
        else:
            left = mid + 1
    return False


def percolate(src_num: int, rngs: list[range]):
    left, right = 0, len(rngs) - 1
    while left <= right:
        mid = left + (right - left) // 2
        src_rng, dst_rng = rngs[mid]

        if src_num in src_rng:
            return dst_rng.start + (src_num - src_rng.start)
        elif src_num < src_rng.start:
            right = mid - 1
        else:
            left = mid + 1
    return src_num


def backpropagate(src_num: int, rngs: list[range]):
    left, right = 0, len(rngs) - 1
    while left <= right:
        mid = left + (right - left) // 2
        src_rng, dst_rng = rngs[mid]

        if src_num in dst_rng:
            return src_rng.start + (src_num - dst_rng.start)
        elif src_num < dst_rng.start:
            right = mid - 1
        else:
            left = mid + 1
    return src_num


def add_initial_range(rngs: set[range]):
    smallest = min(r[0].start for r in rngs)
    if smallest != 0:
        rngs.add((range(smallest), range(smallest),))
    else:
        return rngs


def compute(s: str) -> int:
    seeds = tuple(int(x) for x in re.search(r'seeds: (.+)', s).group(1).split())
    seeds_rngs = [
        range(rng_start, rng_start + rng_len) 
        for rng_start, rng_len 
        in tuple(zip(seeds[::2], seeds[1::2]))]

    maps = {}
    
    for source, destination in itertools.pairwise(Category):
        maps[(source, destination)] = set()
        rng_s = re.search(rf'{source.name.lower()}-to-{destination.name.lower()} map:([\s\d]+)', s).group(1).strip().split('\n')
        rng_lst = tuple(tuple(map(int, r.split())) for r in rng_s)

        for r in rng_lst:
            dst_rng_start, src_rng_start, rng_len = r
            dst_rng = range(dst_rng_start, dst_rng_start + rng_len)
            src_rng = range(src_rng_start, src_rng_start + rng_len)
            maps[(source, destination)].add((src_rng, dst_rng,))
        
        add_initial_range(maps[(source, destination)])

    # sort maps by dest
    for k, v in maps.items():
        maps[k] = sorted(v, key=lambda x: x[1].start)

    # sort location and seed ranges
    sorted_location_rngs = sorted((v for _, v in maps[(Category.HUMIDITY, Category.LOCATION)]), key=lambda x: x.start)
    sorted_seeds_rngs = sorted(seeds_rngs, key=lambda x: x[0])

    # start with smallest locations and backpropagate to find their intial seed number.
    for location_rng in sorted_location_rngs:
        for location_num in location_rng:
            seed_num = get_seed_num(loc_num=location_num, maps=maps)
            # return first within the initial ranges
            if binary_search_ranges(seed_num, sorted_seeds_rngs):  
                return location_num  


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
EXPECTED = 46


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

