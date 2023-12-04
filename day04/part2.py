from __future__ import annotations

import argparse
import os.path

import pytest
from typing import Generator

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def count_cards(card_num: int, card_matches_dct: dict[int, set[int]], card_num_copies: dict[int, int]):
    neighbors = card_matches_dct[card_num]
    if not neighbors:
        return
    
    for n in neighbors:
        card_num_copies[n] += 1
        count_cards(n, card_matches_dct, card_num_copies)

def compute(s: str) -> int:
    total = 0
    card_matches, card_num_matches, card_num_copies = {}, {}, {}
    lines = s.splitlines()
    total = len(lines)
    print(len(lines))
    for line in lines:
        card_s, rest = line.split(': ')
        card_num = int(card_s.split()[1])
        winning_s, nums_s = rest.split(' | ')

        num_matches = len(set(winning_s.split()).intersection(set(nums_s.split())))
        card_num_matches[card_num] = num_matches
        card_matches[card_num] = set(range(card_num + 1, card_num + num_matches + 1))
        card_num_copies[card_num] = 1  # assign original copy

    for card_num in card_matches:
        count_cards(card_num, card_matches, card_num_copies)

    return sum(card_num_copies.values())


INPUT_S = '''\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
'''
EXPECTED = 30


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
