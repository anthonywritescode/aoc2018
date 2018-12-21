import argparse
from typing import Callable
from typing import Sequence
from typing import Set

import pytest

from support import timing


class opcodes:
    @staticmethod
    def addr(regs: Sequence[int], a: int, b: int) -> int:
        return regs[a] + regs[b]

    @staticmethod
    def addi(regs: Sequence[int], a: int, b: int) -> int:
        return regs[a] + b

    @staticmethod
    def mulr(regs: Sequence[int], a: int, b: int) -> int:
        return regs[a] * regs[b]

    @staticmethod
    def muli(regs: Sequence[int], a: int, b: int) -> int:
        return regs[a] * b

    @staticmethod
    def banr(regs: Sequence[int], a: int, b: int) -> int:
        return regs[a] & regs[b]

    @staticmethod
    def bani(regs: Sequence[int], a: int, b: int) -> int:
        return regs[a] & b

    @staticmethod
    def borr(regs: Sequence[int], a: int, b: int) -> int:
        return regs[a] | regs[b]

    @staticmethod
    def bori(regs: Sequence[int], a: int, b: int) -> int:
        return regs[a] | b

    @staticmethod
    def setr(regs: Sequence[int], a: int, b: int) -> int:
        return regs[a]

    @staticmethod
    def seti(regs: Sequence[int], a: int, b: int) -> int:
        return a

    @staticmethod
    def gtir(regs: Sequence[int], a: int, b: int) -> int:
        return int(a > regs[b])

    @staticmethod
    def gtri(regs: Sequence[int], a: int, b: int) -> int:
        return int(regs[a] > b)

    @staticmethod
    def gtrr(regs: Sequence[int], a: int, b: int) -> int:
        return int(regs[a] > regs[b])

    @staticmethod
    def eqir(regs: Sequence[int], a: int, b: int) -> int:
        return int(a == regs[b])

    @staticmethod
    def eqri(regs: Sequence[int], a: int, b: int) -> int:
        return int(regs[a] == b)

    @staticmethod
    def eqrr(regs: Sequence[int], a: int, b: int) -> int:
        return int(regs[a] == regs[b])


ALL: Set[Callable[[Sequence[int], int, int], int]]
ALL = {getattr(opcodes, k) for k in dir(opcodes) if len(k) == 4}


def compute(s: str) -> int:
    inputs, _ = s.split('\n\n\n')

    matching_tests = 0
    for test in inputs.split('\n\n'):
        before, code, after = test.splitlines()
        registers_before = tuple(int(c) for c in before[9::3])
        opc, va, vb, vc = [int(x) for x in code.split()]
        registers_after = tuple(int(c) for c in after[9::3])

        before_w = [v for i, v in enumerate(registers_before) if i != vc]
        after_w = [v for i, v in enumerate(registers_after) if i != vc]
        # modified something other than the target register
        if before_w != after_w:
            continue

        matching_opcodes = 0
        for opcode in ALL:
            retc = opcode(registers_before, va, vb)
            if registers_after[vc] == retc:
                matching_opcodes += 1
                if matching_opcodes == 3:
                    matching_tests += 1
                    break

    return matching_tests


SAMPLE1 = '''\
Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]


14 3 3 2
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (SAMPLE1, 1),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file')
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
