import argparse
import re
from typing import Tuple

GOTO_RE = re.compile(r'goto (instr\d+);')


tmpl = {
    'addi': '    reg{vc} = reg{va} + {vb};',
    'seti': '    reg{vc} = {va};',
    'mulr': '    reg{vc} = reg{va} * reg{vb};',
    'addr': '    reg{vc} = reg{va} + reg{vb};',
    'muli': '    reg{vc} = reg{va} * {vb};',
    'setr': '    reg{vc} = reg{va};',
    'bani': '    reg{vc} = reg{va} & {vb};',
    'bori': '    reg{vc} = reg{va} | {vb};',
}

cond = {
    'eqrr': 'reg{va} != reg{vb}',
    'eqri': 'reg{va} != {vb}',
    'gtir': '{va} <= reg{vb}',
    'gtrr': 'reg{va} <= reg{vb}',
}

HALT = (
    '    printf("HALT %lld\\n", reg0);\n'
    '    return 0;\n'
)


def parse_instr(s: str) -> Tuple[str, int, int, int]:
    instr, *rest = s.split()
    va, vb, vc = [int(c) for c in rest]
    return instr, va, vb, vc


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--reg0-initial', type=int, default=0)
    args = parser.parse_args()

    with open(args.filename) as f:
        regline = next(f)
        assert regline.startswith('#ip ')
        _, reg_s = regline.split()
        reg = int(reg_s)
        lines = list(f)

    code = []
    currlabel = 0

    line_iter = iter(lines)
    while True:
        try:
            line = next(line_iter)
        except StopIteration:
            break
        code.append(f'instr{currlabel}:')
        instr, va, vb, vc = parse_instr(line)
        if vc == reg:
            if instr == 'addi':
                code.append(f'    goto instr{currlabel + vb + 1};')
            elif instr == 'seti':
                code.append(f'    goto instr{va + 1};\n')
            elif (
                    instr == 'mulr' and
                    va == vb == vc and
                    currlabel * currlabel > len(lines)
            ):
                code.append(HALT)
            elif instr == 'addr' and {va, vb} == {reg, 0}:
                if args.reg0_initial == 0:
                    pass  # this is a noop instruction
                elif args.reg0_initial == 1:
                    code.append(f'    goto instr{currlabel + 2};')
                else:
                    assert False, line
            else:
                assert False, line
        else:
            if instr in ('eqri', 'eqrr', 'gtir', 'gtrr'):
                addr = next(line_iter).strip()
                addr_intsr, addr_va, addr_vb, addr_vc = parse_instr(addr)
                jump = next(line_iter).strip()
                jump_instr, jump_va, jump_vb, jump_vc = parse_instr(jump)
                assert addr_vc == reg, (addr, reg)
                assert {addr_va, addr_vb} == {reg, vc}, (addr, line)
                assert jump_vc == reg, (jump, reg)
                if jump_instr == 'seti':
                    dest = jump_va + 1
                elif jump_instr == 'addi':
                    assert jump_va == reg, (jump, reg)
                    dest = currlabel + 2 + jump_vb + 1
                else:
                    assert False, jump
                code.append(
                    f'    if ({cond[instr].format(va=va, vb=vb)}) {{\n'
                    f'        reg{vc} = 0;\n'
                    f'        goto instr{dest};\n'
                    f'    }} else {{\n'
                    f'        reg{vc} = 1;\n'
                    f'    }}'
                )
                currlabel += 2
            else:
                res = tmpl[instr].format(va=va, vb=vb, vc=vc)
                res = res.replace(f'reg{reg}', str(currlabel))
                code.append(res)
        currlabel += 1

    used_gotos = set()
    for line in code:
        match = GOTO_RE.search(line)
        if match:
            used_gotos.add(match.group(1) + ':')

    code = [
        line for line in code
        if not line.endswith(':') or line in used_gotos
    ]

    print('#include <assert.h>')
    print('#include <stdio.h>')
    print('')
    print('int main() {')

    regvars = [f'reg{i}' for i in range(6) if i != reg]
    print(f'    unsigned long long {", ".join(regvars)};')
    print(f'    {" = ".join(regvars)} = 0;')
    if args.reg0_initial:
        print(f'    reg0 = {args.reg0_initial};')

    print('\n'.join(code))

    print(HALT)
    print('}')

    return 0


if __name__ == '__main__':
    exit(main())
