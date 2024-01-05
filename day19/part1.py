from __future__ import annotations

import argparse
import os.path
from collections import defaultdict
from typing import Any
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Rating(NamedTuple):
    x: int
    m: int
    a: int
    s: int


def compute(s: str) -> int:
    wkflows_s, ratings_s = s.split('\n\n')
    total = 0
    ratings = []
    wkflows: dict[str, Any] = defaultdict(list)

    for line in ratings_s.splitlines():
        ratings.append(
            Rating(
                *(
                    int(x.split('=')[1])
                    for x in line[1:-1].split(',')
                ),
            ),
        )

    for line in wkflows_s.splitlines():
        w, rest = line.split('{')
        rules_lst = rest[:-1].split(',')
        rules, default = rules_lst[:-1], rules_lst[-1]
        rs = []
        for rule in rules:
            cond, nxt = rule.split(':')
            r, op, val = cond[0], cond[1], cond[2:]
            rs.append((r, op, val, nxt))
        wkflows[w].extend([rs, default])

    for rating in ratings:
        nxt = 'in'
        while nxt not in {'A', 'R'}:
            rls, dflt = wkflows[nxt]
            flag = False
            for r, op, val, nxt2 in rls:
                if op == '<':
                    if rating.__getattribute__(r) < int(val):
                        nxt = nxt2
                        flag = True
                        break
                elif op == '>':
                    if rating.__getattribute__(r) > int(val):
                        nxt = nxt2
                        flag = True
                        break
                else:
                    raise ValueError(f'{op} unexpected')
            if not flag:
                nxt = dflt
            if nxt == 'A':
                total += sum(rating)

    return total


INPUT_S = '''\
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
'''
EXPECTED = 19114


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
