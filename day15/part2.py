from __future__ import annotations

import argparse
import os.path
from collections import deque

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def focus_power(box_num: int, slot: int, focal_len: int) -> int:
    return (1 + box_num) * (slot + 1) * focal_len


def hash_algo(s: str) -> int:
    val = 0
    for c in s:
        val += ord(c)
        val *= 17
        val = val % 256
    return val


def compute(s: str) -> int:
    steps = s.strip('\n').split(',')
    boxes: list[deque[tuple[str, str]]] = [deque() for _ in range(256)]
    for step in steps:
        if '-' in step:
            label = step[:-1]
            box_num = hash_algo(label)
            matches = [
                (lbl, lens)
                for lbl, lens in boxes[box_num]
                if lbl == label
            ]
            if matches:
                boxes[box_num].remove(matches[0])
        elif '=' in step:
            label, focal_len = step.split('=')
            box_num = hash_algo(label)
            # add if not in box
            if label not in (lbl for lbl, _ in boxes[box_num]):
                boxes[box_num].append((label, focal_len))
            for i, (lbl, _) in enumerate(boxes[box_num]):
                if lbl == label:
                    boxes[box_num][i] = (label, focal_len)

    return sum(
        focus_power(box_num, i, int(focal_len))
        for box_num, box in enumerate(boxes)
        for i, (_, focal_len) in enumerate(box)
    )


INPUT_S = '''\
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
'''
EXPECTED = 145


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
