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
        return regs[a] | b

    @staticmethod
    def borr(regs: Sequence[int], a: int, b: int) -> int:
        return regs[a] | regs[b]

    @staticmethod
    def bori(regs: Sequence[int], a: int, b: int) -> int:
        return regs[a] & b

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

    registers = [0] * 6
    registers[0] = 1
    ip = 0

    while ip != 35:
        registers[ip_reg] = ip
        op, va, vb, vc = prog[ip]
        registers[vc] = op(registers, va, vb)
        ip = registers[ip_reg]
        ip += 1

    # determined empirically by analyzing the disassembly
    x = registers[2]
    z = 0
    for i in range(1, x + 1):
        if x % i == 0:
            z += i
    return z


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
