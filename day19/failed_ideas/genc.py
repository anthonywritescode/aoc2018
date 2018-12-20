tmpl = {
    'addi': '    reg{vc} = reg{va} + {vb};',
    'seti': '    reg{vc} = {va};',
    'mulr': '    reg{vc} = reg{va} * reg{vb};',
    'addr': '    reg{vc} = reg{va} + reg{vb};',
    'muli': '    reg{vc} = reg{va} * {vb};',
    'setr': '    reg{vc} = reg{va};',
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
    print('#include <assert.h>')
    print('#include <stdio.h>')
    print()
    print('int main() {')
    print('    unsigned long long reg0, reg1, reg2, reg3, reg5;')
    print('    reg0 = 1;')
    print('    reg1 = reg2 = reg3 = reg5 = 0;')

    currlabel = 0

    with open('day19/input.txt') as f:
        # discard first line
        next(f)
        lines = list(f)

    line_iter = iter(lines)
    while True:
        try:
            line = next(line_iter)
        except StopIteration:
            break
        print(f'instr{currlabel}:')
        instr, *rest = line.split()
        va, vb, vc = [int(p) for p in rest]
        if vc == 4:
            if instr == 'addi':
                print(f'    goto instr{currlabel + vb + 1};')
            elif line == 'mulr 4 4 4\n':
                print(HALT)
            elif instr == 'addr':
                assert line == 'addr 4 0 4\n', line
                print('    goto instr27;\n')
            elif instr == 'seti':
                print(f'    goto instr{va + 1};\n')
            else:
                assert False, line
        else:
            if instr in ('eqrr', 'gtrr'):
                addr = next(line_iter).strip()
                jump_instr = next(line_iter).strip()
                assert addr in {f'addr 4 {vc} 4', f'addr {vc} 4 4'}, (addr, vc)
                assert jump_instr.endswith('4'), jump_instr
                if jump_instr.startswith('seti'):
                    _, dest_s, _, _ = jump_instr.split()
                    jump = int(dest_s) + 1
                elif jump_instr.startswith('addi'):
                    assert jump_instr.startswith('addi 4 ')
                    _, _, jump_s, _ = jump_instr.split()
                    jump = currlabel + 2 + int(jump_s) + 1
                else:
                    assert False, jump_instr
                print(j_tmpl[instr].format(va=va, vb=vb, vc=vc, jump=jump))
                currlabel += 2
            else:
                res = tmpl[instr].format(va=va, vb=vb, vc=vc)
                res = res.replace('reg4', str(currlabel))
                print(res)
        currlabel += 1

    print('    assert("unreachable!");')
    print('}')
    return 0


if __name__ == '__main__':
    exit(main())
