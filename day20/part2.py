from __future__ import annotations

import argparse
import collections
import math
import os.path
from typing import NamedTuple
from typing import Protocol

import pytest

import support

"""
Credit to anthonywritescode.
"""

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Signalable(Protocol):
    def process(self, src: str, high: bool) -> list[tuple[str, str, bool]]: ...


class Broadcaster(NamedTuple):
    name: str
    targets: tuple[str, ...]

    def process(self, src: str, high: bool) -> list[tuple[str, str, bool]]:
        return [(self.name, target, high) for target in self.targets]


class F(NamedTuple):
    name: str
    state: list[bool]
    targets: tuple[str, ...]

    def process(self, src: str, high: bool) -> list[tuple[str, str, bool]]:
        if high:
            return []
        else:
            val = self.state[0] = not self.state[0]
            return [(self.name, target, val) for target in self.targets]


class C(NamedTuple):
    name: str
    inputs: dict[str, bool]
    targets: tuple[str, ...]

    def process(self, src: str, high: bool) -> list[tuple[str, str, bool]]:
        self.inputs[src] = high
        val = not all(self.inputs.values())
        return [(self.name, target, val) for target in self.targets]


class Placeholder(NamedTuple):
    def process(self, src: str, high: bool) -> list[tuple[str, str, bool]]:
        return []


def compute(s: str) -> int:
    kjs = {}
    cs = {}
    signals: dict[str, Signalable] = collections.defaultdict(Placeholder)
    for line in s.splitlines():
        src, target_s = line.split(' -> ')
        targets = tuple(target_s.split(', '))
        if src[0] == '%':
            srcname = src[1:]
            signals[srcname] = F(srcname, [False], targets)
        elif src[0] == '&':
            srcname = src[1:]
            signals[srcname] = cs[srcname] = C(srcname, {}, targets)
        elif src == 'broadcaster':
            srcname = src
            signals[src] = Broadcaster(srcname, targets)
        else:
            signals[src] = Placeholder()

    for line in s.splitlines():
        src, target_s = line.split(' -> ')
        targets = tuple(target_s.split(', '))
        if src.startswith(('%', '&')):
            srcname = src[1:]
        else:
            srcname = src

        for target in targets:
            c = cs.get(target, None)
            if c is not None:
                c.inputs[srcname] = False
            if target == 'kj':
                kjs[srcname] = -1

    freq = {}

    i = 0
    while True:
        i += 1
        todo = collections.deque([('button', 'broadcaster', False)])
        while todo:
            src, dest, signal = todo.popleft()
            todo.extend(signals[dest].process(src, high=signal))

            if src in kjs and signal is True:
                if kjs[src] == -1:
                    kjs[src] = i
                elif src not in freq:
                    freq[src] = i - kjs[src]
                    if len(freq) == len(kjs):
                        return math.lcm(*freq.values())


INPUT_S = '''\
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
'''
EXPECTED = 32000000

INPUT_2_S = '''\
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
'''
INPUT_2_EXPECTED = 11687500


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
        (INPUT_2_S, INPUT_2_EXPECTED),
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
