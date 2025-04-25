.section .text
.globl _start
_start:
    nop
    addi x1, x2, 4          # x1 = 4
    sw x1, 0(x1)            # store x1 (4) at memory address x1 (4)
    addi x2, x0, 4          # x2 = 4
    beq x2, x1, j_eq        # x2 == x1, so jump to j_eq

addi x5 , x0, 15          # x5 = 1
addi x6 , x0, 32         # x6 = 32
addi x7 , x0, 64         # x7 = 64
addi x8 , x0, 127        # x8 = 128
addi x9 , x0, 255        # x9 = 255
    
j_eq:
    addi x3, x0, 1          # x3 = 1
    lw x3, 0(x1)            # load from address x1 (loads 4 into x3)
    beq x3, x1, _start         # since x3 == x1 (4 == 4), jump to end


