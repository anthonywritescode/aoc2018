import argparse
from typing import Callable
from typing import Dict
from typing import Sequence

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


ALL: Dict[str, Callable[[Sequence[int], int, int], int]]
ALL = {k: getattr(opcodes, k) for k in dir(opcodes) if len(k) == 4}


def compute(s: str) -> int:
    ip_reg_line, *rest = s.splitlines()
    ip_reg = int(ip_reg_line.split()[1])
    prog = [
        (ALL[opc], int(va), int(vb), int(vc))
        for opc, va, vb, vc in (line.split() for line in rest)
    ]

    reg = [0] * 6
    ip = 0

    i = 0
    while ip in range(len(prog)):
        i += 1
        reg[ip_reg] = ip
        if ip == 28:
            return reg[3]
        op, va, vb, vc = prog[ip]
        reg[vc] = op(reg, va, vb)
        ip = reg[ip_reg]
        ip += 1

    assert False, 'unreachable!'


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
