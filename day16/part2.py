import argparse
from typing import Callable
from typing import List
from typing import Sequence
from typing import Tuple

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


ALL: Tuple[Callable[[Sequence[int], int, int], int], ...]
ALL = tuple({getattr(opcodes, k) for k in dir(opcodes) if len(k) == 4})


def compute(s: str) -> int:
    inputs, program = s.split('\n\n\n\n')

    possible = {i: set(ALL) for i in range(16)}
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

        possible[opc] = {
            fn for fn in possible[opc]
            if fn(registers_before, va, vb) == registers_after[vc]
        }

    # discard any "known" from others
    to_discard: List[Tuple[int, Callable[[Sequence[int], int, int], int]]] = []
    for opc, v in possible.items():
        if len(v) == 1:
            fn, = v
            to_discard.append((opc, fn))

    while to_discard:
        opc, fn = to_discard.pop()
        for other_opc, other_v in possible.items():
            if other_opc != opc and fn in other_v:
                other_v.discard(fn)
                if len(other_v) == 1:
                    other_fn, = other_v
                    to_discard.append((other_opc, other_fn))

    opcodes = {k: next(iter(v)) for k, v in possible.items()}
    registers = [0, 0, 0, 0]

    for line in program.splitlines():
        opc, va, vb, vc = [int(x) for x in line.split()]
        registers[vc] = opcodes[opc](registers, va, vb)

    return registers[0]


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (),
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
