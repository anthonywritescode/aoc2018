#include <assert.h>
#include <stdio.h>

int main() {
    unsigned long long reg0, reg1, reg2, reg3, reg5;
    reg0 = 1;
    reg1 = reg2 = reg3 = reg5 = 0;
instr0:
    goto instr17;
instr1:
    reg5 = 1;
instr2:
    reg3 = 1;
instr3:
    reg1 = reg5 * reg3;
instr4:
    if (reg1 != reg2) {
        reg1 = 0;
        goto instr8;
    } else {
        reg1 = 1;
    }
instr7:
    reg0 = reg5 + reg0;
instr8:
    reg3 = reg3 + 1;
instr9:
    if (reg3 <= reg2) {
        reg1 = 0;
        goto instr3;
    } else {
        reg1 = 1;
    }
instr12:
    reg5 = reg5 + 1;
instr13:
    if (reg5 <= reg2) {
        reg1 = 0;
        goto instr2;
    } else {
        reg1 = 1;
    }
instr16:
    printf("HALT %lld\n", reg0);
    return 0;

instr17:
    reg2 = reg2 + 2;
instr18:
    reg2 = reg2 * reg2;
instr19:
    reg2 = 19 * reg2;
instr20:
    reg2 = reg2 * 11;
instr21:
    reg1 = reg1 + 6;
instr22:
    reg1 = reg1 * 22;
instr23:
    reg1 = reg1 + 18;
instr24:
    reg2 = reg2 + reg1;
instr25:
    goto instr27;

instr26:
    goto instr1;

instr27:
    reg1 = 27;
instr28:
    reg1 = reg1 * 28;
instr29:
    reg1 = 29 + reg1;
instr30:
    reg1 = 30 * reg1;
instr31:
    reg1 = reg1 * 14;
instr32:
    reg1 = reg1 * 32;
instr33:
    reg2 = reg2 + reg1;
instr34:
    reg0 = 0;
instr35:
    goto instr1;

    assert("unreachable!");
}
