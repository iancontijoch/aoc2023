from __future__ import annotations

import argparse
import itertools
import os.path
from collections import Counter
from collections import namedtuple
from enum import auto
from enum import Enum
from typing import Iterator

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class HandType(Enum):
    HIGH_CARD = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    FIVE_OF_A_KIND = auto()


CARD_VALS = {
    'T': 10,
    'J': 1,
    'Q': 12,
    'K': 13,
    'A': 14,
}


Hand = namedtuple('Hand', ('value', 'type', 'bid'))


def find_type(hand: str) -> HandType:
    c = Counter(hand)
    pairs = {card for card, count in c.most_common() if count == 2}
    threes = {card for card, count in c.most_common() if count == 3}
    fours = {card for card, count in c.most_common() if count == 4}
    fives = {card for card, count in c.most_common() if count == 5}

    if len(c.values()) == 5:
        return HandType.HIGH_CARD
    elif len(pairs) == 1 and not threes:
        return HandType.ONE_PAIR
    elif len(pairs) == 2:
        return HandType.TWO_PAIR
    elif threes and not pairs:
        return HandType.THREE_OF_A_KIND
    elif threes and pairs:
        return HandType.FULL_HOUSE
    elif fours:
        return HandType.FOUR_OF_A_KIND
    elif fives:
        return HandType.FIVE_OF_A_KIND
    else:
        raise NotImplementedError(f'could not identify hand type: {hand}')


def insert_joker(hand_value: str, replacement_options: list[str]) -> HandType:
    max_hand_type = HandType.HIGH_CARD
    count_j = hand_value.count('J')
    for comb in itertools.combinations(replacement_options * count_j, count_j):
        new_hand_value = hand_value
        for c in comb:
            new_hand_value = new_hand_value.replace('J', c, 1)

        new_hand_type = find_type(new_hand_value)
        if new_hand_type.value > max_hand_type.value:
            max_hand_type = new_hand_type

    return max_hand_type


def rank_ties(tied_hands: Iterator[Hand]) -> list[Hand]:
    tie_values = {
        h: tuple(
            map(
                int, (
                    CARD_VALS.get(c, c)
                    for c in h.value
                ),
            ),
        ) for h in tied_hands
    }
    return sorted(tie_values, key=lambda x: tie_values.get(x) or -1)


def compute(s: str) -> int:
    hands = set()
    replacement_options = [str(x) for x in range(2, 10)] + ['T', 'Q', 'K', 'A']
    lines = s.splitlines()
    for line in lines:
        hand, bid = line.split()
        hand_type = insert_joker(
            hand, replacement_options,
        ) if 'J' in hand else find_type(hand)
        hands.add(Hand(hand, hand_type, int(bid)))

    ranked_hands = []
    for x in range(1, len(HandType) + 1):
        compare_lst = (h for h in hands if h.type.value == x)
        ranked_hands.extend(rank_ties(compare_lst))

    return sum(x * (i+1) for i, x in enumerate(r.bid for r in ranked_hands))


INPUT_S = '''\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
'''
EXPECTED = 5905


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
