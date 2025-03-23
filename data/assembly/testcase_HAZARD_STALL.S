.section .text
.globl _start
_start:
    nop
    addi x1, x0, 4          # x1 = 4
    sw x1, 0(x1)            # store x1 (4) at memory address x1 (4)
    addi x2, x0, 4          # x2 = 4
    beq x2, x1, j_eq        # x2 == x1, so jump to j_eq

end:
    addi x3, x0, 10          # x3 = 10
    nop                     # end of program
    nop                     # end of program
    nop                     # end of program
    nop                     # end of program
    ecall                   # end of program


j_eq:
    addi x3, x0, 1          # x3 = 1
    lw x3, 0(x1)            # load from address x1 (loads 4 into x3)
    beq x3, x1, end         # since x3 == x1 (4 == 4), jump to end
    addi x3, x0, 15          # x3 = 2


