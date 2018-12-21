import re

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

j_tmpl = {
    'eqrr': (
        '    if (reg{va} != reg{vb}) {{\n'
        '        reg{vc} = 0;\n'
        '        goto instr{jump};\n'
        '    }} else {{\n'
        '        reg{vc} = 1;\n'
        '    }}'
    ),
    'eqri': (
        '    if (reg{va} != {vb}) {{\n'
        '        reg{vc} = 0;\n'
        '        goto instr{jump};\n'
        '    }} else {{\n'
        '        reg{vc} = 1;\n'
        '    }}'
    ),
    'gtir': (
        '    if ({va} <= reg{vb}) {{\n'
        '        reg{vc} = 0;\n'
        '        goto instr{jump};\n'
        '    }} else {{\n'
        '        reg{vc} = 1;\n'
        '    }}'
    ),
    'gtrr': (
        '    if (reg{va} <= reg{vb}) {{\n'
        '        reg{vc} = 0;\n'
        '        goto instr{jump};\n'
        '    }} else {{\n'
        '        reg{vc} = 1;\n'
        '    }}'
    ),
}

HALT = (
    '    printf("HALT %lld\\n", reg0);\n'
    '    return 0;\n'
)


def main() -> int:
    code = []

    code.append('#include <assert.h>')
    code.append('#include <stdio.h>')
    code.append('')
    code.append('int main() {')
    code.append('    unsigned long long reg0, reg2, reg3, reg4, reg5;')
    code.append('    reg0 = reg2 = reg3 = reg4 = reg5 = 0;')

    currlabel = 0

    with open('day21/input.txt') as f:
        # discard first line
        next(f)
        lines = list(f)

    line_iter = iter(lines)
    while True:
        try:
            line = next(line_iter)
        except StopIteration:
            break
        code.append(f'instr{currlabel}:')
        instr, *rest = line.split()
        va, vb, vc = [int(p) for p in rest]
        if vc == 1:
            if instr == 'addi':
                code.append(f'    goto instr{currlabel + vb + 1};')
            elif line == 'mulr 1 1 1\n':
                code.append(HALT)
            elif instr == 'addr':
                assert line == 'addr 1 0 1\n', line
                code.append('    goto instr27;\n')
            elif instr == 'seti':
                code.append(f'    goto instr{va + 1};\n')
            else:
                assert False, line
        else:
            if instr in ('eqri', 'eqrr', 'gtir', 'gtrr'):
                addr = next(line_iter).strip()
                jump_instr = next(line_iter).strip()
                assert addr in {f'addr 1 {vc} 1', f'addr {vc} 1 1'}, (addr, vc)
                assert jump_instr.endswith('1'), jump_instr
                if jump_instr.startswith('seti'):
                    _, dest_s, _, _ = jump_instr.split()
                    jump = int(dest_s) + 1
                elif jump_instr.startswith('addi'):
                    assert jump_instr.startswith('addi 1 ')
                    _, _, jump_s, _ = jump_instr.split()
                    jump = currlabel + 2 + int(jump_s) + 1
                else:
                    assert False, jump_instr
                code.append(j_tmpl[instr].format(
                    va=va, vb=vb, vc=vc, jump=jump,
                ))
                currlabel += 2
            else:
                res = tmpl[instr].format(va=va, vb=vb, vc=vc)
                res = res.replace('reg1', str(currlabel))
                code.append(res)
        currlabel += 1

    code.append('}')

    used_gotos = set()
    for line in code:
        match = GOTO_RE.search(line)
        if match:
            used_gotos.add(match.group(1) + ':')

    code = [
        line for line in code
        if not line.endswith(':') or line in used_gotos
    ]

    print('\n'.join(code))

    return 0


if __name__ == '__main__':
    exit(main())
